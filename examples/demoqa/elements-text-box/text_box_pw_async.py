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
        await play_side_async(page, 'sides/text_box_step_1.side', name='Go to https://demoqa.com/text-box.', debug=True)
        await play_side_async(page, 'sides/text_box_step_2.side', name='Enter John Doe as fullname, johndoe@gmail.com as Email, 123 Devil St FL USA as current address and click Submit', debug=True)
        await play_side_async(page, 'sides/text_box_step_3.side', name='Click Submit', debug=True)
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    asyncio.run(main())
