# /// pyproject
# [requires]
# python = ">=3.10"
# selenium = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from side_player.selenium.sync_api import play_side


def main():
    chrome_options = Options()
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-features=SafeBrowsingPasswordProtection")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.use_automation_extension = False
    driver = webdriver.Chrome(options=chrome_options)
    try:
        play_side(
            driver,
            "sides/resize_screen_step_1.side",
            name="Adjust browser size to 500x500",
            debug=True,
        )
        time.sleep(2)
        play_side(
            driver,
            "sides/resize_screen_step_2.side",
            name="Adjust browser size to 1000x1000",
            debug=True,
        )
        time.sleep(2)
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    main()
