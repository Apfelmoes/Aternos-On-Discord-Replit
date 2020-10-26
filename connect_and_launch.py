from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from helper import can_fire, can_fire_async
import asyncio
import time
from dotenv import load_dotenv
import os
from chromedriver_py import binary_path

if os.path.exists(os.path.relpath(".env")):
    load_dotenv()
    USER = os.getenv('USERNAME_C')
    PASSWORD = os.getenv('PASSWORD_C')
    URL = "https://aternos.org/server/"
    SERVER_STATUS_URI = URL
   
connected = False

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
options.add_argument('--ignore-certificate-errors')
options.add_argument("--allow-insecure-localhost")
#options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125")

driver = webdriver.Chrome(options=options, executable_path=binary_path)

async def start_server():
    """ Starts the server by clicking on the start button.
        The try except part tries to find the confirmation button, and if it 
        doesn't, it continues to loop until the confirm button is clicked."""
#    if not connected:
#        connect_account()  
    await asyncio.sleep(5)
    element = driver.find_element_by_xpath("/html/body/div[20]/div/div/div/div[3]/div[2]/div[2]")
    element.click()
    await asyncio.sleep(3)
    element = driver.find_element_by_xpath('/html/body/div[2]/main/section/div[3]/div[4]/div[1]')
    element.click()
    await asyncio.sleep(10)
    element = driver.find_element_by_xpath('/html/body/div[2]/main/div/div/div/main/div/a[2]')
    element.click()
    state = driver.find_element_by_xpath('/html/body/div[2]/main/section/div[3]/div[3]/div[1]/div/span[2]/span')
    while state.text == "Wachten in de wachtrij":
        state = driver.find_element_by_xpath('/html/body/div[2]/main/section/div[3]/div[3]/div[1]/div/span[2]/span')
        try:
            element = driver.find_element_by_xpath('/html/body/div[2]/main/section/div[3]/div[4]/div[6]')
            element.click()
        except ElementNotInteractableException as e:
            pass
    driver.close()

@can_fire
def connect_account():
    """ Connects to the accounts through a headless chrome tab so we don't
        have to do it every time we want to start or stop the server."""

    driver.get(URL)
    element = driver.find_element_by_xpath('//*[@id="user"]')
    element.send_keys(USER)
    element = driver.find_element_by_xpath('//*[@id="password"]')
    element.send_keys(PASSWORD)
    element = driver.find_element_by_xpath('//*[@id="login"]')
    element.click()
    connected = True
    time.sleep(10)

@can_fire
def get_status():
    # Returns the status of the server as a string
    driver.get(SERVER_STATUS_URI)
    time.sleep(2)
    if not connected:
        connect_account()
        time.sleep(2)
        element = driver.find_element_by_xpath('/html/body/div/main/section/div/div[2]/div/div[1]')
        element.click()
        time.sleep(1)
    element = driver.find_element_by_class_name('statuslabel-label')
    print(element.text)
    return element.text

@can_fire
def get_number_of_players():
    # Returns the number of players as a string
    driver.get(SERVER_STATUS_URI)
    if not connected:
        connect_account()
        time.sleep(5)
        element = driver.find_element_by_xpath('/html/body/div/main/section/div/div[2]/div/div[1]')
        element.click()
        time.sleep(1)
    number_of_players = WebDriverWait(driver, 360).until(ec.presence_of_element_located((By.XPATH, '/html/body/div[2]/main/section/div[3]/div[5]/div[2]/div[1]/div/div[2]/div/span')))
    return number_of_players.text

async def stop_server():
    if not connected:
        connect_account()
    driver.get(URL)
    element = driver.find_element_by_xpath("/html/body/div/main/section/div/div[2]/div[1]/div[1]")
    element.click()
    await asyncio.sleep(3)
    element = driver.find_element_by_xpath('//*[@id="stop"]')
    element.click()

