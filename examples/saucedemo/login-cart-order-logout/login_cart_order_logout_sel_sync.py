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
        play_side(
            driver,
            "sides/login_cart_order_logout_step_1.side",
            name="Go to the home of https://saucedemo.com",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_2.side",
            name="Log in",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_3.side",
            name="Add a backpack to the cart",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_4.side",
            name="Add a jacket to the cart",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_5.side",
            name="Click the cart on the right top corner",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_6.side",
            name="Remove backpack",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_7.side",
            name="Click Checkout",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_8.side",
            name="Enter John as first name, Doe as last name, 11111 as zip code and click Continue",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_9.side",
            name="Click Finish",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_10.side",
            name="Click Back Home",
            debug=True,
        )
        play_side(
            driver,
            "sides/login_cart_order_logout_step_11.side",
            name="Log out",
            debug=True,
        )
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
