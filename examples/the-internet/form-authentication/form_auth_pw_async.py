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
        await play_side_async(page, 'sides/form_auth_step_1.side', name='Go to the home of the-internet.herokuapp.com', debug=True)
        await play_side_async(page, 'sides/form_auth_step_2.side', name='Resize browser to 1200 x 1200', debug=True)
        await play_side_async(page, 'sides/form_auth_step_3.side', name='Click Form Authentication', debug=True)
        await play_side_async(page, 'sides/form_auth_step_4.side', name='Log in', debug=True)
        await play_side_async(page, 'sides/form_auth_step_5.side', name='Log out', debug=True)
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
