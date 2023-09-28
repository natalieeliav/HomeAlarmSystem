import subprocess
import json
from concurrent.futures import ThreadPoolExecutor


def capture_seconds_for_camera(name, camera, ffmpeg_path, channel, duration):
    ip = camera['ip']
    username = camera['username']
    password = camera['password']

    # Formulate the RTSP URL
    url = f'rtsp://{username}:{password}@{ip}/Streaming/Channels/{channel}'

    # Define the output file name based on camera's name
    output_file = f'footage/{name}_last_{duration}_seconds.mp4'

    # Run ffmpeg command to capture the last seconds
    process = subprocess.Popen([
        ffmpeg_path,
        '-y',  # Overwrite output file if it exists
        '-t', str(duration),  # Duration to capture in seconds
        '-i', url,  # Input RTSP URL
        output_file  # Output file name
    ], stderr=subprocess.PIPE)

    # Wait for the subprocess to complete and catch any errors
    _, err = process.communicate()
    if process.returncode != 0:
        print(f"Error capturing from {name} ({ip})")
        # print(err.decode())


def capture_last_seconds(cameras, ffmpeg_path='ffmpeg/bin/ffmpeg.exe', channel=1, duration=5):
    with ThreadPoolExecutor() as executor:
        # Start capturing for all cameras concurrently
        futures = []
        for name, camera in cameras[0].items():
            future = executor.submit(capture_seconds_for_camera, name, camera, ffmpeg_path, channel, duration)
            futures.append(future)

        # Wait for all captures to complete
        for future in futures:
            future.result()


