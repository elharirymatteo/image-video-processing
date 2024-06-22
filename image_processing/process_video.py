from math import exp
import cv2
import numpy as np

# Function to create a tracker with compatibility check
def create_tracker(tracker_type='CSRT'):
    if tracker_type == 'CSRT' and hasattr(cv2, 'TrackerCSRT_create'):
        return cv2.TrackerCSRT_create()
    elif tracker_type == 'KCF' and hasattr(cv2, 'TrackerKCF_create'):
        return cv2.TrackerKCF_create()
    else:
        print(f"{tracker_type} tracker not available. Falling back to MIL tracker.")
        return cv2.TrackerMIL_create()

# Function to read frames from a video or GIF
def read_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return []
    
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Function to track the object
def track_object(frames):
    if not frames:
        print("Error: No frames to process.")
        return []
    
    tracker = create_tracker('CSRT')
    bbox = cv2.selectROI("Frame", frames[0], False)
    cv2.destroyWindow("Frame")
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

# Function to draw the trajectory dynamically
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

# Main function
def main(video_path, output_path):
    frames = read_frames(video_path)
    if not frames:
        print("Error: No frames were read from the video.")
        return
    
    trajectory = track_object(frames)
    if not trajectory:
        print("Error: Object tracking failed.")
        return
    
    draw_trajectory(frames, trajectory, output_path)

if __name__ == "__main__":

    shape_to_track = 'infinite'
    if shape_to_track == 'circle':
        exp_name = 'ZeroGCamera1_circle_speed4x.mp4'
    elif shape_to_track == 'infinite':
        exp_name = 'ZeroGCamera_infinite_4x.mp4'
    else:
        raise ValueError(f"Unknown shape to track: {shape_to_track}")
    
    base_folder = '/home/matteo/Videos/fp_media_videos/'
    video_path = base_folder + exp_name
    output_name = shape_to_track + '_trajectory_drawn.mp4'
    output_path = base_folder + output_name
    main(video_path, output_path)
