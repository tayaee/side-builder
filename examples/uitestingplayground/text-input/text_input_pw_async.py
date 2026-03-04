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
        await play_side_async(page, 'sides/text_input_step_1.side', name='Go to the home of http://uitestingplayground.com', debug=True)
        await play_side_async(page, 'sides/text_input_step_2.side', name='Adjust browser size to 1200x1200', debug=True)
        await play_side_async(page, 'sides/text_input_step_3.side', name='Click Text Input', debug=True)
        await play_side_async(page, 'sides/text_input_step_4.side', name='Enter MyNewButton as the new button name and click the blue button', debug=True)
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
