# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00846FCEB4298C5249E309916E9171EE691928A0A8D95E70376D15C34CEF3FE5D25D24B999E65BD00835356DEAC6F4F4AF9881AE9350C6325854B554E9B4ADCDFE4FC4E9E823EBFFC8832747B9899CCC1A7C2F08E4B6024A4DFEFB087FF47690691E4CA9F99E21D9275B6373DDB200294FAFC111DE0CE1531AD099462C821FF15C810E01C4E61F17E3150C883EE362FD474AF0DD4E2C934E559146AA4C4936AB4E5BA3D600BB7C215BB26F88EA79A55A7F09189949FFC00B8EE37F7078186A4ADFC6EE868FA95107BD936F7D67955C7A08B776888F251E4D71E6824DBCD507E45B1CCE31A22A6CB9F2FE22D1E336F9FB53935A364E1980C5041AD18E6A76178A3B5C2F0201FEC0CD003454B3A4799EDF364E8E82676343A02D6FF659329A4C0E0723507EA96CAD5DBA23D26E6542BA801DE7F4750EC5F7F7B43CBFDF5ADFBE9243E28EFC1955E5479F1560B4F964B7A3EB0B04F5A554EA95A6C3203B3AB3773D8B"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
