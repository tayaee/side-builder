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
        await play_side_async(page, 'sides/basic_web_page_step_1.side', name='Go to the home of testpages.eviltester.com', debug=True)
        await play_side_async(page, 'sides/basic_web_page_step_2.side', name='Click Pages in the menu tree', debug=True)
        await play_side_async(page, 'sides/basic_web_page_step_3.side', name='Click Basics', debug=True)
        await play_side_async(page, 'sides/basic_web_page_step_4.side', name='Click Basic Web Page', debug=True)
        await play_side_async(page, 'sides/basic_web_page_step_5.side', name='Click "Click Me" button', debug=True)
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
