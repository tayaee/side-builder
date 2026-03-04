# /// pyproject
# [requires]
# python = ">=3.10"
# selenium = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

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
        play_side(driver, 'sides/text_box_step_1.side', name='Go to https://demoqa.com/text-box.', debug=True)
        play_side(driver, 'sides/text_box_step_2.side', name='Enter John Doe as fullname, johndoe@gmail.com as Email, 123 Devil St FL USA as current address and click Submit', debug=True)
        play_side(driver, 'sides/text_box_step_3.side', name='Click Submit', debug=True)
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
