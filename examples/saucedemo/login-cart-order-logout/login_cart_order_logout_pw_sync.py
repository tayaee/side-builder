# /// pyproject
# [requires]
# python = ">=3.10"
# playwright = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        play_side(
            page,
            "sides/login_cart_order_logout_step_1.side",
            name="Go to the home of https://saucedemo.com",
            debug=True,
        )
        play_side(
            page, "sides/login_cart_order_logout_step_2.side", name="Log in", debug=True
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_3.side",
            name="Add a backpack to the cart",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_4.side",
            name="Add a jacket to the cart",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_5.side",
            name="Click the cart on the right top corner",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_6.side",
            name="Remove backpack",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_7.side",
            name="Click Checkout",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_8.side",
            name="Enter John as first name, Doe as last name, 11111 as zip code and click Continue",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_9.side",
            name="Click Finish",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_10.side",
            name="Click Back Home",
            debug=True,
        )
        play_side(
            page,
            "sides/login_cart_order_logout_step_11.side",
            name="Log out",
            debug=True,
        )
        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
