# InstaDrawBot
**Automated Instagram drawing bot using Python, OpenCV, and ADB.**

This project reproduces black-and-white images directly on an Android phone using Instagram’s drawing feature.  
It uses computer vision techniques to extract the skeleton of an image and sends real-time touch gestures through the Android Debug Bridge (ADB) to draw it automatically.

---

## Overview

InstaDrawBot connects a Windows PC to an Android phone and automates the process of drawing on Instagram.  
Using OpenCV, the system processes an input image into single-pixel-wide contour paths, which are then translated into swipe gestures.  
Each gesture is executed sequentially on the phone, allowing precise, smooth reproduction of the original drawing.

For live visual feedback, **scrcpy** is used to mirror the phone’s screen on the computer.

---

## Features
- Grayscale conversion and adaptive thresholding for robust edge detection  
- Morphological cleanup and skeletonization for thin, connected lines  
- Contour extraction and coordinate mapping to the phone’s screen resolution  
- Real-time gesture execution using `adb shell input swipe`  
- Compatible with any Android device that supports ADB and Instagram’s drawing tool  

---

## Requirements
- **Python 3.9+**
- **Android Debug Bridge (ADB)** (included with `scrcpy` or Android SDK)
- **Packages**:
  ```bash
  pip install numpy opencv-python scikit-image

