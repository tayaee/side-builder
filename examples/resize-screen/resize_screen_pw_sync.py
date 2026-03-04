# /// pyproject
# [requires]
# python = ">=3.10"
# playwright = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

import time

from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        play_side(
            page,
            "sides/resize_screen_step_1.side",
            name="Adjust browser size to 500x500",
            debug=True,
        )
        time.sleep(2)
        play_side(
            page,
            "sides/resize_screen_step_2.side",
            name="Adjust browser size to 1000x1000",
            debug=True,
        )
        time.sleep(2)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
