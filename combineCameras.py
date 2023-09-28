import os
import math
from moviepy.editor import VideoFileClip, clips_array


def combine():
    # Folder containing the video files
    folder_path = 'footage'

    # Get all video files in the specified folder
    video_paths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.mp4')]

    # Ensure there is at least one video in the folder
    if not video_paths:
        raise ValueError("The folder must contain at least one .mp4 file")

    # Load video clips
    clips = [VideoFileClip(video) for video in video_paths]

    # Ensure that all clips have the same duration as the shortest clip
    min_duration = min(clip.duration for clip in clips)
    clips = [clip.subclip(0, min_duration) for clip in clips]

    # Calculate the number of rows and columns needed for the grid
    num_videos = len(clips)
    num_cols = math.ceil(math.sqrt(num_videos))
    num_rows = math.ceil(num_videos / num_cols)

    # If the grid has empty spaces, fill them with a black image
    while len(clips) < num_rows * num_cols:
        clips.append(VideoFileClip("black.jpg", duration=min_duration))

    # Arrange clips in a grid
    final_clip = clips_array([[clips[row * num_cols + col] for col in range(num_cols)] for row in range(num_rows)])

    # Set the final clip's frame rate to that of the input clips
    final_clip.fps = clips[0].fps

    # Write the result to a file
    final_clip.write_videofile('footage/combined_cameras.mp4', codec='libx264')
