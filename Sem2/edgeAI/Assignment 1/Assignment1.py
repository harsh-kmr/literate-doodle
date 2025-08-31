10import time
 
import math
 
from lsm9ds1 import LSM9DS1
 
from machine import Pin, I2C

# configs
N = 100 
SLEEP_MS = 10   
i2c = I2C(1, scl=Pin(15), sda=Pin(14))
imu = LSM9DS1(i2c)
 
def update_queue(queue, new_value): 
    removed = queue.pop(0) 
    queue.append(new_value) 
    return removed

def initial_stats(data):
    s = data[0]
    sum_sq = data[0] * data[0]
    zero_crossings = 0
    diff_sq_sum = 0.0
    abs_diff_sum = 0.0
    min_val = data[0]
    max_val = data[0]
    prev = data[0]
    N = 100

    for i in range(1, N):
        x = data[i]
        s += x
        sum_sq += x * x
        min_val = min(min_val, x)
        max_val = max(max_val, x)
        
        diff = x - prev
        diff_sq_sum += diff * diff
        abs_diff_sum += abs(diff)
        if prev * x < 0:
            zero_crossings += 1
        
        prev = x

    return {
        'sum': s,
        'sum_sq': sum_sq,
        'zero_crossings': zero_crossings,
        'diff_sq_sum': diff_sq_sum,
        'abs_diff_sum': abs_diff_sum,
        'min': min_val,
        'max': max_val
    }


def calculate_running_stats_list(data, old_stats, removed, new_val):
    N = 100
    new_sum = old_stats['sum'] - removed + new_val
    new_sum_sq = old_stats['sum_sq'] - (removed * removed) + (new_val * new_val)
    new_mean = new_sum / N if N != 0 else 0.0

    old_pair = 1 if (removed * data[0] < 0) else 0
    new_pair = 1 if (data[-2] * new_val < 0) else 0
    new_zero_crossings = old_stats['zero_crossings'] - old_pair + new_pair

    old_diff = data[0] - removed
    new_diff = new_val - data[-2]
    new_diff_sq_sum = old_stats['diff_sq_sum'] - (old_diff * old_diff) + (new_diff * new_diff)
    new_abs_diff_sum = old_stats['abs_diff_sum'] - abs(old_diff) + abs(new_diff)

    if removed == old_stats['min']:
        new_min = min(data)
    else:
        new_min = min(old_stats['min'], new_val)
    if removed == old_stats['max']:
        new_max = max(data)
    else:
        new_max = max(old_stats['max'], new_val)

    new_stats = {
        'sum': new_sum,
        'sum_sq': new_sum_sq,
        'zero_crossings': new_zero_crossings,
        'diff_sq_sum': new_diff_sq_sum,
        'abs_diff_sum': new_abs_diff_sum,
        'min': new_min,
        'max': new_max
    }

    features = compute_features_from_state(data, new_stats)
    return new_stats, features

def compute_features_from_state(data, state):
    N = 100 
    mean_val = state['sum'] / N 
    variance = (data[0]-mean_val)**2
    rms_val = math.sqrt(state['sum_sq'] / N)
    min_val = state['min']
    max_val = state['max']
    range_val = max_val - min_val
    zero_crossings = state['zero_crossings']
    RMSD_val = math.sqrt(state['diff_sq_sum'] / (N - 1)) if N > 1 else 0.0
    MAD_val = state['abs_diff_sum'] / (N - 1) if N > 1 else 0.0
    mean_crossings = 0
    for i in range(1, N):
        diff1 = (data[i] - mean_val)
        variance += diff1**2
        if (data[i - 1] - mean_val) * diff1 < 0:
            mean_crossings += 1
    variance /= N-1
    std_dev_val = math.sqrt(variance) if variance > 0 else 0.0
    return [mean_val, std_dev_val, min_val, max_val, range_val, rms_val,zero_crossings, RMSD_val, MAD_val, mean_crossings]

ax_queue = [0.0] * N 
ay_queue = [0.0] * N 
az_queue = [0.0] * N
gx_queue = [0.0] * N 
gy_queue = [0.0] * N 
gz_queue = [0.0] * N
mx_queue = [0.0] * N 
my_queue = [0.0] * N 
mz_queue = [0.0] * N

print("Pre-filling sensor data buffers...") 
for _ in range(N):
    ax, ay, az = imu.accel() 
    gx, gy, gz = imu.gyro() 
    mx, my, mz = imu.magnet() 
    update_queue(ax_queue, ax) 
    update_queue(ay_queue, ay) 
    update_queue(az_queue, az) 
    update_queue(gx_queue, gx) 
    update_queue(gy_queue, gy) 
    update_queue(gz_queue, gz) 
    update_queue(mx_queue, mx) 
    update_queue(my_queue, my) 
    update_queue(mz_queue, mz) 
    time.sleep_ms(SLEEP_MS)
 
state_ax = initial_stats(ax_queue) 
state_ay = initial_stats(ay_queue) 
state_az = initial_stats(az_queue)
state_gx = initial_stats(gx_queue) 
state_gy = initial_stats(gy_queue) 
state_gz = initial_stats(gz_queue)
state_mx = initial_stats(mx_queue) 
state_my = initial_stats(my_queue) 
state_mz = initial_stats(mz_queue)

features_ax = compute_features_from_state(ax_queue, state_ax) 
features_ay = compute_features_from_state(ay_queue, state_ay) 
features_az = compute_features_from_state(az_queue, state_az)
features_gx = compute_features_from_state(gx_queue, state_gx) 
features_gy = compute_features_from_state(gy_queue, state_gy)
features_gz = compute_features_from_state(gz_queue, state_gz)
features_mx = compute_features_from_state(mx_queue, state_mx) 
features_my = compute_features_from_state(my_queue, state_my) 
features_mz = compute_features_from_state(mz_queue, state_mz)

seq = 0  
while True:
    ax, ay, az = imu.accel()
    gx, gy, gz = imu.gyro() 
    mx, my, mz = imu.magnet() 
    removed_ax = update_queue(ax_queue, ax)
    state_ax, features_ax = calculate_running_stats_list(ax_queue, state_ax, removed_ax, ax)
    removed_ay = update_queue(ay_queue, ay) 
    state_ay, features_ay = calculate_running_stats_list(ay_queue, state_ay, removed_ay, ay)
    removed_az = update_queue(az_queue, az)
    state_az, features_az = calculate_running_stats_list(az_queue, state_az, removed_az, az)
    removed_gx = update_queue(gx_queue, gx) 
    state_gx, features_gx = calculate_running_stats_list(gx_queue, state_gx, removed_gx, gx)
    removed_gy = update_queue(gy_queue, gy) 
    state_gy, features_gy = calculate_running_stats_list(gy_queue, state_gy, removed_gy, gy)
    removed_gz = update_queue(gz_queue, gz) 
    state_gz, features_gz = calculate_running_stats_list(gz_queue, state_gz, removed_gz, gz)
    removed_mx = update_queue(mx_queue, mx) 
    state_mx, features_mx = calculate_running_stats_list(mx_queue, state_mx, removed_mx, mx)
    removed_my = update_queue(my_queue, my) 
    state_my, features_my = calculate_running_stats_list(my_queue, state_my, removed_my, my)
    removed_mz = update_queue(mz_queue, mz) 
    state_mz, features_mz = calculate_running_stats_list(mz_queue, state_mz, removed_mz, mz)
  
    print(seq,end=",")
    print(N, end=",") 
    for queue in [ax_queue, ay_queue, az_queue, gx_queue, gy_queue, gz_queue, mx_queue, my_queue, mz_queue]:
        for val in queue: 
            print("{:.2f}".format(val), end=",") 
    for feature in (features_ax, features_ay, features_az, features_gx, features_gy, features_gz, features_mx, features_my, features_mz):
        for f in feature:
            print("{:.2f}".format(f), end=",")
    print()
    seq += 1
    time.sleep_ms(SLEEP_MS)
 
 
 
 
 