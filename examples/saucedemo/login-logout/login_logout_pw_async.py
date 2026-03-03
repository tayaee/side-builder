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
            "sides/login-logout_step_1.side",
            name="Go to the home of https://saucedemo.com",
            debug=True,
        )
        await play_side_async(
            page, "sides/login-logout_step_2.side", name="Log in", debug=True
        )
        await play_side_async(
            page, "sides/login-logout_step_3.side", name="Log out", debug=True
        )
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
