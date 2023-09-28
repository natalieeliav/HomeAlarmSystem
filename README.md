# Home Alarm System Project

The Alarm System Project is a comprehensive software solution designed to enhance home security.
This system's primary goal is to provide homeowners with real-time security camera footage when an alarm is triggered.
By leveraging a combination of video streaming and automation, it offers an effective means of monitoring and responding to potential security threats.

# How It Works

The algorithm consists of several components and files:

1. camerasdata.json: This JSON file stores the details of the security cameras, including their names, IP addresses, usernames, and passwords.

2. config.json: This JSON file contains configuration data, including email credentials, phone numbers for notification, and camera details.
   
3. cameras.py: This Python script utilizes the ffmpeg library to capture a specified duration of video footage from multiple security cameras. It accesses camera information (IP address, username, and password) stored in a JSON file.

4. combine_cameras.py: This Python script combines the captured video clips from different cameras into a single video grid.
It ensures that all clips have the same duration and creates a grid layout of the videos.

5. mail.py: This script checks an email account for new messages, specifically monitoring for alarm alerts.
When an alarm alert email is detected, it triggers the capture_last_seconds function to capture video clips from the security cameras.
After capturing, it copies the video clips to the clipboard and sends them via WhatsApp to specified phone numbers.
The captured video files are deleted afterward to save storage space.

6. main.py: This is the main script. It loads camera data and account credentials from JSON files and invokes the check_for_new_email function to continuously monitor the email account for alarm alerts and execute the necessary actions.
   
7. whatsapp.py: This script uses WhatsApp Web to send video clips to specified phone numbers.
It opens WhatsApp Web in a Chrome browser and sends the video clips to the designated recipients.

# Usage

Please note that the Home Alarm System Project is designed to work exclusively on Windows operating systems.

To use this project, follow these steps:
1. Ensure you have Python installed on your system.
2. Install the required Python libraries: ffmpeg, moviepy, imaplib, selenium. You can paste these commands to your cmd:
  pip install ffmpeg-python
  pip install moviepy
  pip install selenium
3. Set up a Gmail account for receiving alarm alert emails.
4. Create a config.json file with your email credentials and phone numbers.
5. Populate the cameras data.json file with the details of your security cameras.
6. Run the main.py script to start monitoring your email account for alarm alerts and initiate the video capture and notification process.




