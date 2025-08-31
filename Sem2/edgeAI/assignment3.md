# Assignment 3: Post Training Quantization

## Implementation Summary

### Model Training
- Used MobileNetV2 with ImageNet weights, fine-tuning the top 10 layers.  
- Dataset: Rock-Paper-Scissors (train: 2520, test: 372 samples).  
- Image size: 128x128x3.  
- Augmentation: Flip, color jitter, rotation, inversion.  
- Optimizer: Adam (lr=0.00005), Early Stopping.  
- Achieved test accuracy: 80.11%, loss: 0.7086.  

### Efficiency Metrics (Original Model)
- Parameters: 2,227,715.  
- Model Size: 8.50 MB (weights: 8 MB).  
- Total FLOPs: ~Calculated per layer.  
- Inference Time: 0.1369s.  
- Memory Change: 0.018 MB.  

## Observations

### Observations from Post-Training Integer Quantization (int8)

1. **Original Model (Float32):**  
   - **Parameters:** 2,227,715 (weights + biases).  
   - **Size:** 8.50 MB.  
   - **Accuracy:** 80.11%, **Loss:** 0.7086.  
   - **Inference Time:** 0.1369s.  
   - **Memory Change:** 0.018 MB.  

2. **Quantized Model (int8):**  
   - **Parameters (with `pseudo_qconst`)**: 4,561,518.  
   - **Size:** 4.40 MB (or 2.24 MB without `pseudo_qconst`).  
   - **Accuracy:** 71.50%, **Loss:** 4.5927.  
   - **Inference Time:** 0.0093s (**14× speedup**).  
   - **Memory Change:** Negligible (89.46 kb).  

3. **Key Observations:**  
   - **Compression:** Model size reduced 8.50MB → 4.40MB (or 2.24MB without `pseudo_qconst`).  
   - **Speed & Efficiency:** 7× faster inference, nearly zero memory overhead.  
   - **Accuracy Drop:** 80.11% → 71.50%, indicating quantization-induced degradation.  
   - **Loss Surge:** 0.7086 → 4.5927, suggesting higher prediction errors.  
   - **Pseudo_qconst:** Added parameters but no accuracy benefit, assist in defining how quantized values map back to float representations.

### Observations from n-bit Clustering-Based Quantization

1. **Quantization Approach:**  
   - Applied n-bit k-means clustering on flattened float32 model weights.  
   - Explored 2-bit, 4-bit, and 8-bit quantization, where clusters = \(2^n\).  

2. **Compression Ratio:**  
   - Original model: 16MB (weights: 8MB).  
   - Quantization reduces the storage requirements by encoding weights using fewer bits. But, Quantized storage remains np.int8, limiting theoretical compression.  
   - Stored weights: 2MB, aligning with theoretical reduction.  
   - **Compression Ratios:**  
     - 2-bit: 7.77× (Theoretical: 16×)  
     - 4-bit: 7.73× (Theoretical: 8×)  
     - 8-bit: 6.96× (Theoretical: 4×)  

3. **Quantization Error (MSE):**  
   - 2-bit: 76.29 (Highest error)  
   - 4-bit: 59.21 (Moderate)  
   - 8-bit: 46.66 (Lowest)

### Observations from Linear Quantization (int8 & int16)

1. **Quantization Approach:**  
   - Applied custom linear quantization on float32 model weights.  
   - int8: Scaled to [-128, 127], int16: Scaled to [-32768, 32767].  

2. **Compression Ratio:**  
   - Original model: 16MB (weights: 8MB).  
   - int8: 7.78× (file size), 4× (weights).  
   - int16: 3.91× (file size), 2× (weights).  

3. **Quantization Error (MSE):**  
   - int8: 0.000998.  
   - int16: 0.000000.  

4. **Model Performance:**  
   - Original: 80.11% acc, 0.7086 loss.  
   - int8: 73.12% acc, 0.6801 loss.  
   - int16: 79.84% acc, 0.7090 loss.  

5. **Trade-offs:**  
   - int8: Higher compression but slightly larger errors and accuracy drop.  
   - int16: Minimal performance loss with lower compression.  
   - Both methods enable efficient deployment based on resource constraints.
