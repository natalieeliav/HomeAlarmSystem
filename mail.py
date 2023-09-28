import imaplib
import time
from email.header import decode_header
from cameras import capture_last_seconds
# from email.parser import BytesParser
import json
import whatsapp as Whatsapp
import traceback
import ctypes
import os
from win32con import CF_HDROP
from win32clipboard import OpenClipboard, EmptyClipboard, SetClipboardData, CloseClipboard
from combineCameras import combine
def on_new_email(message_number, imap_server, phone_numbers):
    # Mark the email as read
    imap_server.store(message_number, '+FLAGS', '(\Seen)')

    # Fetch the email headers
    status, email_data = imap_server.fetch(message_number, '(BODY[HEADER.FIELDS (SUBJECT)])')
    if status == 'OK':
        subject = decode_header(email_data[0][1].decode("utf-8"))[0][0]
    # Fetch the email body
    status, email_data = imap_server.fetch(message_number, '(BODY[HEADER.FIELDS (SUBJECT FROM)])')
    if '@alerts.control4.com' in str(email_data):
        # Mark the email as read
        imap_server.store(message_number, '+FLAGS', '(\Seen)')

        print(f"New email received: Subject - {subject}")
        # if subject.strip() == "Alarm":
        print("Creating footage")
        with open('config.json', 'r') as file:
            cameras = json.load(file).get('cameras', '')
            capture_last_seconds(cameras)
        for filename in os.listdir("footage"):
            print((f'{os.path.dirname(os.path.realpath(__file__))}\\footage\\{filename}'))
            copy_file_to_clipboard(f'{os.path.dirname(os.path.realpath(__file__))}\\footage\\{filename}')
            Whatsapp.videor(phone_numbers)
        # combine()
        # copy_file_to_clipboard(f'{os.path.dirname(os.path.realpath(__file__))}\\footage\\combined_cameras.mp4')
        # Whatsapp.videor(["+972546399979"])


        [os.remove(os.path.join("footage", file)) for file in os.listdir("footage") if
         os.path.isfile(os.path.join("footage", file))]


def check_for_new_email(username, password, phone_numbers):
    # Initialize the IMAP server outside the try block to make it accessible in the finally block
    imap_server = None
    try:
        # Connect to the IMAP server
        imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
        imap_server.login(username, password)
        mailbox = 'INBOX'

        while True:
            try:  # Nested try block to handle exceptions during the mail checking loop
                # Select the mailbox
                imap_server.select(mailbox)

                # Search for unseen (new) emails
                status, email_ids = imap_server.search(None, 'UNSEEN')

                if status == 'OK':
                    email_id_list = email_ids[0].split()
                    for email_id in email_id_list:
                        on_new_email(email_id, imap_server, phone_numbers)

                # Wait for a while before checking again (e.g., every 5 seconds)
                time.sleep(5)

            except (imaplib.IMAP4.abort, ConnectionResetError):
                # Catch specific exceptions related to connection loss and try to reconnect
                print("Connection lost. Reconnecting...")
                if imap_server is not None:
                    try:
                        imap_server.logout()  # Try to logout before reconnecting
                    except:
                        pass  # If logout fails, ignore and try to reconnect anyway
                imap_server = imaplib.IMAP4_SSL('imap.gmail.com')
                imap_server.login(username, password)

            except Exception as e:
                print(f"An error occurred during the mail checking loop: {e}")
                traceback.print_exc()
                break  # Exit the loop if an unexpected error occurs

    except Exception as e:
        print(f"An error occurred during IMAP server connection: {e}")
        traceback.print_exc()

    finally:
        if imap_server is not None:
            try:
                imap_server.logout()  # Logout from the IMAP server in the finally block to ensure cleanup
            except:
                pass  # If logout fails, ignore


def copy_file_to_clipboard(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")

    # Define the DROPFILES structure
    class DROPFILES(ctypes.Structure):
        _fields_ = [("pFiles", ctypes.c_uint32),  # Offset of file list
                    ("pt", ctypes.c_long * 2),     # Mouse position
                    ("fNC", ctypes.c_uint32),      # Whether mouse is in client area
                    ("fWide", ctypes.c_uint32)]    # Whether file names are Unicode

    # Calculate the total length of the DROPFILES structure
    length = ctypes.sizeof(DROPFILES) + len(file_path) * 2 + 6  # 6 extra bytes for double null terminators

    # Allocate memory
    hGlobal = ctypes.windll.kernel32.GlobalAlloc(0x42, length)
    pGlobal = ctypes.windll.kernel32.GlobalLock(hGlobal)

    # Create and populate the DROPFILES structure in memory
    dropfiles = DROPFILES()
    dropfiles.pFiles = ctypes.sizeof(DROPFILES)
    dropfiles.fWide = True  # Indicate Unicode file names
    ctypes.memmove(pGlobal, ctypes.addressof(dropfiles), ctypes.sizeof(DROPFILES))
    ctypes.memmove(pGlobal + ctypes.sizeof(DROPFILES), file_path.encode('utf-16le'), len(file_path) * 2 + 2)  # +2 for null terminator

    # Unlock the memory
    ctypes.windll.kernel32.GlobalUnlock(hGlobal)

    # Open the clipboard and set the data
    OpenClipboard(None)
    EmptyClipboard()
    SetClipboardData(CF_HDROP, hGlobal)
    CloseClipboard()

