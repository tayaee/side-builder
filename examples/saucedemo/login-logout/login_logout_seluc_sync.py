# /// pyproject
# [requires]
# python = ">=3.10"
# selenium = "*"
# uc = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)
#
# This sample uses undetected_chromedriver to avoid bot detection.
# Install with: uv add side-builder[uc]
# Or for all extras: uv add side-builder[all]

from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

from side_player.selenium.sync_api import play_side


def main():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # undetected_chromedriver automatically handles many anti-bot measures
    driver = uc.Chrome(options=chrome_options)

    try:
        play_side(
            driver,
            "sides/login-logout_step_1.side",
            name="Go to the home of https://saucedemo.com",
            debug=True,
        )
        play_side(driver, "sides/login-logout_step_2.side", name="Log in", debug=True)
        play_side(driver, "sides/login-logout_step_3.side", name="Log out", debug=True)
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
