# Assignment 1: Sensor Data Collection with On-Board Feature Extraction

## Problem Statement
Develop an end-to-end sensor data collection application with on-board feature extraction for activity detection using Arduino Nano BLE Sense IMU sensors, addressing challenges in real-world data collection.

## Solution
- **Sampling Rate:** Achieved 1-2 samples/sec (limited by calculations and communication; 4-5 Hz in IDE, 1.32 Hz with comm).
- **Improvements for Higher Rate:** Use circular buffer/deque instead of list queue; increase UART baud rate; reduce data per iteration.
- **Challenges:** Noisy raw IMU data with drift; intensive real-time feature extraction; delays from large fields and low baud rate; communication errors causing data loss.
- **Insights:** Balance feature detail vs. sample rate; proper organization for large files; minimal data loss from errors.
