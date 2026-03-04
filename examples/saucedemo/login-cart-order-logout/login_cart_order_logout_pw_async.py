# /// pyproject
# [requires]
# python = ">=3.10"
# playwright = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

import asyncio

from playwright.async_api import async_playwright

from side_player.playwright.async_api import play_side_async


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_1.side",
            name="Go to the home of https://saucedemo.com",
            debug=True,
        )
        await play_side_async(
            page, "sides/login_cart_order_logout_step_2.side", name="Log in", debug=True
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_3.side",
            name="Add a backpack to the cart",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_4.side",
            name="Add a jacket to the cart",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_5.side",
            name="Click the cart on the right top corner",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_6.side",
            name="Remove backpack",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_7.side",
            name="Click Checkout",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_8.side",
            name="Enter John as first name, Doe as last name, 11111 as zip code and click Continue",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_9.side",
            name="Click Finish",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_10.side",
            name="Click Back Home",
            debug=True,
        )
        await play_side_async(
            page,
            "sides/login_cart_order_logout_step_11.side",
            name="Log out",
            debug=True,
        )
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
