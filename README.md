
# image-video-processing

This repository is a generic library containing scripts for **image and video editing**, including object tracking and trajectory visualization.

## Features

- **Object Tracking:** Uses OpenCV to track objects in a video.
- **Trajectory Visualization:** Dynamically overlays a trajectory on the video.
- **Video Processing Utilities:** General scripts for manipulating images and videos.

---

## **Installation**

### **1. Clone the Repository**
First, clone this repository:
```bash
git clone https://github.com/elharirymatteo/image-video-processing.git
cd image-video-processing
```

### **2. Set Up a Virtual Environment (Recommended) and Install Dependencies**
To avoid dependency conflicts, create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

With the virtual environment activated, install all required packages:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

## **Usage**
The repository contains scripts for processing videos. For example, you can track objects in a video and visualize the trajectory.

### **Run Object Tracking**
To run the object tracking script:
```bash
python3 image_processing/process_video.py /path/to/video/folder
```

- The script will **list videos in the specified folder**.
- You will be prompted to **process, skip, or exit** for each video.
- Processed videos will be saved with `_tracked` appended to their filenames in a `/tracked` folder.


## **Contributions**
Feel free to contribute improvements or additional video processing scripts. Open a **pull request** with your changes.

---
