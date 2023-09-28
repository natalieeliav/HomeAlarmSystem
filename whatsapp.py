import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from plyer import notification
from creds import *
import traceback

try:

    chrome_options = Options()
    chrome_options.add_argument("user-data-dir=C:\\Users\\ADIL\\AppData\\Local\\Google\\Chrome\\UserData")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://web.whatsapp.com/')
    driver.minimize_window()

    base_url = "https://web.whatsapp.com"

    # Where chromedriver is located on your computer
    path = r"chromedriver.exe"


    # Open Whatsapp

    driver.get(base_url)
except Exception as e:
    traceback.print_exc()
    print(e)


def messenger(msg, member_list):

    """ This function receives a message and a list of tuples- each tuple includes a name and a phone number as \
    strings. The function sends the message to everyone on the list with the intro Hello, -name-. """

    try:
        # Send message to every person in member_list
        for member_phone in member_list:
            new_chat = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]'))
            new_chat.click()

            input_box_search = WebDriverWait(driver, 50).until(
                 lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div/div[2]/div/div[1]/p'))
            input_box_search.send_keys(member_phone)
            send_to = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]'))
            send_to.click()
            type_it = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))

            type_it.send_keys(msg + Keys.ENTER)
            time.sleep(1)
        time.sleep(5)
        # driver.quit()
    except Exception as e:
        traceback.print_exc()
        print(e)

def videor(member_list):



    try:
        # Send message to every person in member_list
        for member_phone in member_list:
            new_chat = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[4]/header/div[2]/div/span/div[4]'))
            new_chat.click()

            input_box_search = WebDriverWait(driver, 50).until(
                 lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[1]/div/div[2]/div/div[1]/p'))
            input_box_search.send_keys(member_phone)
            send_to = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/span/div/span/div/div[2]/div/div/div/div[2]/div/div/div[2]'))
            send_to.click()

            type_it = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'))
            type_it.send_keys(Keys.CONTROL, 'v')
            type_it = WebDriverWait(driver, 50).until(
                lambda driver: driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[1]/div[3]/div/div/div[1]/div[1]/p'))
            type_it.send_keys(Keys.ENTER)
            time.sleep(1)
        time.sleep(5)
        # driver.quit()
    except Exception as e:
        traceback.print_exc()
        print(e)
