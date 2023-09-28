import json
from mail import check_for_new_email

# Load cameras data from camerasData.json
with open('camerasData.json', 'r') as file:
    cameras = json.load(file)

# Load account data from account.json
with open('config.json', 'r') as file:
    account = json.load(file)

# Capture the last 5 seconds from each camera
if __name__ == "__main__":
    email = account.get('email', '')  # Get email from account.json
    password = account.get('password', '')  # Get password from account.json
    phone_numbers = account.get('phone_numbers', '')  # Get phone numbers from account.json
    if not email or not password or not phone_numbers:
        raise ValueError("Config data must be set up in config.json")

    check_for_new_email(email, password, phone_numbers)
