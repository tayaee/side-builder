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
        play_side(page, 'sides/basic_web_page_step_1.side', name='Go to the home of testpages.eviltester.com', debug=True)
        play_side(page, 'sides/basic_web_page_step_2.side', name='Click Pages in the menu tree', debug=True)
        play_side(page, 'sides/basic_web_page_step_3.side', name='Click Basics', debug=True)
        play_side(page, 'sides/basic_web_page_step_4.side', name='Click Basic Web Page', debug=True)
        play_side(page, 'sides/basic_web_page_step_5.side', name='Click "Click Me" button', debug=True)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
