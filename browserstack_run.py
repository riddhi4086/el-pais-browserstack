import os
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

USERNAME = os.getenv("BROWSERSTACK_USERNAME")
ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")

if not USERNAME or not ACCESS_KEY:
    raise Exception("BrowserStack credentials not found. Check .env file.")

BROWSERSTACK_URL = f"https://{USERNAME}:{ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# --------------------------------------------------
# Browser configurations
capabilities = [
    {
        "browser": "Chrome",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "11",
        "name": "Chrome_Windows_Test"
    },
    {
        "browser": "Firefox",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "11",
        "name": "Firefox_Windows_Test"
    },
    {
        "browser": "Edge",
        "browser_version": "latest",
        "os": "Windows",
        "os_version": "11",
        "name": "Edge_Windows_Test"
    },
    {
        "browser": "Safari",
        "browser_version": "latest",
        "os": "OS X",
        "os_version": "Ventura",
        "name": "Safari_macOS_Test"
    },
    {
        "browser": "Chrome",
        "device": "Samsung Galaxy S23",
        "real_mobile": "true",
        "os_version": "13.0",
        "name": "Android_Chrome_Test"
    }
]

# --------------------------------------------------
# Test runner
def run_test(cap):
    options = Options()

    # BrowserStack required capabilities
    bstack_options = {
        "os": cap.get("os"),
        "osVersion": cap.get("os_version"),
        "browserName": cap.get("browser"),
        "browserVersion": cap.get("browser_version"),
        "deviceName": cap.get("device"),
        "realMobile": cap.get("real_mobile"),
        "sessionName": cap.get("name")
    }

    # Remove None values
    bstack_options = {k: v for k, v in bstack_options.items() if v}

    options.set_capability("bstack:options", bstack_options)

    try:
        driver = webdriver.Remote(
            command_executor=BROWSERSTACK_URL,
            options=options
        )

        driver.get("https://elpais.com")
        time.sleep(3)

        print(f"Running on {cap['name']}")

    except Exception as e:
        print(f"Error on {cap['name']}: {e}")

    finally:
        try:
            driver.quit()
        except:
            pass

# --------------------------------------------------
# Parallel execution
threads = []

for cap in capabilities:
    t = threading.Thread(target=run_test, args=(cap,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\nBrowserStack parallel execution completed successfully")
