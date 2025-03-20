import argparse
import os
import cv2
import numpy as np
import time
import glob

# Function to create a tracker with compatibility check
def create_tracker(tracker_type='CSRT'):
    if tracker_type == 'CSRT' and hasattr(cv2, 'TrackerCSRT_create'):
        return cv2.TrackerCSRT_create()
    elif tracker_type == 'KCF' and hasattr(cv2, 'TrackerKCF_create'):
        return cv2.TrackerKCF_create()
    else:
        print(f"{tracker_type} tracker not available. Falling back to MIL tracker.")
        return cv2.TrackerMIL_create()

# Function to read frames from a video
def read_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return []
    
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Function to track an object in the video
def track_object(frames):
    if not frames:
        print("Error: No frames to process.")
        return []
    
    tracker = create_tracker('CSRT')
    bbox = cv2.selectROI("Select Object", frames[0], False)
    cv2.destroyWindow("Select Object")
    tracker.init(frames[0], bbox)
    
    trajectory = []
    for frame in frames:
        success, box = tracker.update(frame)
        if success:
            x, y, w, h = [int(v) for v in box]
            center = (x + w // 2, y + h // 2)
            trajectory.append(center)
        else:
            trajectory.append(None)
    return trajectory

# Function to draw the trajectory on the video
def draw_trajectory(frames, trajectory, output_path, fps=30):
    if not frames:
        print("Error: No frames to save.")
        return
    
    height, width, _ = frames[0].shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))
    
    for i in range(len(frames)):
        frame = frames[i].copy()  # Copy the current frame to avoid modifying the original
        
        # Draw the trajectory up to the current frame
        for j in range(1, i + 1):
            if trajectory[j-1] is None or trajectory[j] is None:
                continue
            cv2.line(frame, trajectory[j-1], trajectory[j], (0, 255, 0), 2)
        
        out.write(frame)
    
    out.release()
    print(f"Processed video saved as: {output_path}")

# Main function
def main(video_folder):
    # Ensure the folder exists
    if not os.path.exists(video_folder):
        raise FileNotFoundError(f"Error: The folder '{video_folder}' does not exist.")

    # Get all video files in the folder
    video_files = glob.glob(os.path.join(video_folder, "*.mp4")) + \
                  glob.glob(os.path.join(video_folder, "*.avi")) + \
                  glob.glob(os.path.join(video_folder, "*.mov")) + \
                  glob.glob(os.path.join(video_folder, "*.mkv"))

    if not video_files:
        raise FileNotFoundError(f"Error: No video files found in '{video_folder}'.")

    # Iterate through videos one by one
    for video_path in video_files:
        video_name = os.path.basename(video_path)
        print(f"\nFound video: {video_name}")
        
        while True:
            user_choice = input("Do you want to process this video? (y)es / (s)kip / (e)xit: ").strip().lower()
            if user_choice in ['y', 'yes']:
                break
            elif user_choice in ['s', 'skip']:
                print(f"Skipping {video_name}...\n")
                continue
            elif user_choice in ['e', 'exit']:
                print("Exiting script.")
                return
            else:
                print("Invalid input. Please enter 'y', 's', or 'e'.")

        # Process the video
        frames = read_frames(video_path)
        if not frames:
            print(f"Skipping {video_name} due to read error.\n")
            continue

        trajectory = track_object(frames)
        if not trajectory:
            print(f"Skipping {video_name} due to tracking failure.\n")
            continue

        # Save with "_tracked" suffix
        output_name = os.path.splitext(video_name)[0] + "_tracked.mp4"
        output_path = os.path.join(video_folder, output_name)
        
        draw_trajectory(frames, trajectory, output_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trajectory tracking on videos.")
    parser.add_argument("video_folder", type=str, help="Path to the folder containing videos.")
    args = parser.parse_args()

    main(args.video_folder)
