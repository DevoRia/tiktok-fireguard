import argparse
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pickle
import os
from crontab import CronTab


COOKIES_FILE = "tiktok_cookies.pkl"
TARGET_USER = os.getenv("TARGET_USER", "Bob")
MESSAGE = os.getenv("MESSAGE", "Ping")
RUN_MODE = os.getenv("RUN_MODE", "single")
SCRIPT_PATH = os.path.abspath(__file__)
PROXY = os.getenv("PROXY")


def create_driver(proxy=None):
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    )
    if proxy:
        options.add_argument(f"--proxy-server={proxy}")
    driver = webdriver.Chrome(options=options)
    return driver


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open(COOKIES_FILE, "wb"))

def load_cookies(driver):
    cookies = pickle.load(open(COOKIES_FILE, "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)

def login_manually(driver):
    driver.get("https://www.tiktok.com/login")
    print("Sign in manually. After the signing in click Enter.")
    input()
    save_cookies(driver)

def send_message(driver):
    driver.get("https://www.tiktok.com/messages")
    time.sleep(10)

    chat = driver.find_element("xpath", f"//p[contains(normalize-space(text()),'{TARGET_USER}')]")
    chat.click()
    time.sleep(2)

    input_box = driver.find_element("xpath", "//div[contains(@data-e2e, 'message-input-area')]")
    input_box.click()

    time.sleep(1)

    pyautogui.typewrite(MESSAGE, interval=0.1)

    time.sleep(1)

    pyautogui.press('enter')

    time.sleep(5)

    print("✅ Message sent!")

def setup_cron_job():
    cron = CronTab(user=True)
    job_exists = any(job for job in cron if SCRIPT_PATH in job.command)

    if job_exists:
        print("⏰ Cron job already exists.")
    else:
        job = cron.new(command=f'/usr/bin/python3 {SCRIPT_PATH} >> /path/to/your/logfile.log 2>&1',
                       comment="TikTok Messaging Automation")
        job.setall("0 8 * * *")  # Run daily at 8:00 AM
        cron.write()
        print("✅ Cron job added. The script will now run daily at 8:00 AM.")


def main(proxy=None):
    driver = create_driver(proxy)
    try:
        if not os.path.exists(COOKIES_FILE):
            login_manually(driver)
        else:
            driver.get("https://www.tiktok.com")
            load_cookies(driver)
            driver.refresh()
            time.sleep(5)
        send_message(driver)
    finally:
        driver.quit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--proxy", help="Proxy server address", default=PROXY)
    args = parser.parse_args()
    proxy = args.proxy

    if RUN_MODE == "single":
        print("🚀 Running in single mode...")
        main(proxy)
    elif RUN_MODE == "cron":
        print("⏰ Setting up cron mode...")
        setup_cron_job()
    else:
        print("❌ Invalid RUN_MODE. Please set RUN_MODE to 'single' or 'cron'.")
