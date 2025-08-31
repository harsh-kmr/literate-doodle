# Assignment 4: Custom Keyword Spotting (KWS)

## Overview

This document outlines the work completed for Edge AI Assignment 4, focusing on developing a custom Keyword Spotting (KWS) system to recognize the name "Harsh". The assignment involved data collection, model development, and deployment on an edge device.

## Step 1: Data Collection

### Dataset Creation for "Harsh"
- Recorded over 200 samples of the keyword "Harsh" (Hindi pronunciation).
- 90% of the samples were collected using a laptop microphone in various environments with different background noises.
- The remaining 10% were collected on edge devices (e.g., Nano 33 BLE Sense) to simulate real-world deployment conditions.
- Each audio sample is 1 second in duration.
- Used the Open Speech Recording tool (https://tinyml.seas.harvard.edu/open_speech_recording/) for collection.
- Ensured good quality and proper labeling.

### Additional Data for Noise and Unknown Labels
- Incorporated "yes" and "no" utterances from open source datasets to serve as noise and unknown labels.
- This helps in training the model to distinguish the keyword from common speech and background noise.

## Step 2: Model Development and Compression

- Processed the collected audio data (feature extraction, normalization).
- Trained a machine learning model (using Edge Impulse) to classify the keyword "Harsh" against noise and unknown labels.
- Optimized the model for edge deployment by applying compression techniques (e.g., quantization, pruning) to reduce size and improve inference speed.

## Step 3: Model Deployment and Demonstration

- Deployed the compressed model onto the Arduino Nano 33 BLE Sense board.
- Updated the default KWS application to integrate the custom model.
- Demonstrated the working application during the lab session, showing real-time keyword detection.

## Submission

- All datasets (audio samples).
- Jupyter notebook for model development and compression (or Edge Impulse project screenshots).
- Modified KWS app code for Nano 33 BLE Sense.

## Notes

- This is a lab-based assignment.
- Software setup, data collection, and model development were completed prior to the lab session.
- The final demo was conducted during the lab session.
