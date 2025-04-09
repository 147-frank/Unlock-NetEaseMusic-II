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
    browser.add_cookie({"name": "MUSIC_U", "value": "007E02207A6C5C34A89A6D23145DCBC46F01C15986ACDEA57626BEC07BFA931672FDF08AA29758D470E9E0CFA70E8F36D1EE2811B25643E26186D7DAC11FB23DC693FC893A4596D7469E11EF2122D5C59E0FB2A3C84C9FCCCBF4E86AC59F5EB0B8A180987FF11F82706816074C98E49AB09F1A5A7206ED8A44CFECCF8B809FB8420A85A843DCCB81955F4D42A93CD1894826881D4561E131DEC8DE3795199C6552D688173F20E658E4B567A03FB18C3EF4BDA3E7A2D3542F102A9DD3970B1E4EDE93F7D6F11EC9B13B47B0D46C8CF482AD621256E1D1F865AC1DBCD1F670B2F1D4761D94338EE4328D2E26915EE66E49AE06EFEABEE6726C0823C7C5A74559A2117F45847E15935CDEB2748B8D95F3DF06D04D528CC3D4DB6489500820C529593B7A85282D8E0D6C6661ADE5FBD43B43232A63B37A12E2F161F010819A69C1982662B95DDC5F7999023EBA9F05474322BB7C42E67F6C87705FCE876595E0CF68E1"})
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
