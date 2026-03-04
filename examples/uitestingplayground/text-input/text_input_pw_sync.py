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
        play_side(page, 'sides/text_input_step_1.side', name='Go to the home of http://uitestingplayground.com', debug=True)
        play_side(page, 'sides/text_input_step_2.side', name='Adjust browser size to 1200x1200', debug=True)
        play_side(page, 'sides/text_input_step_3.side', name='Click Text Input', debug=True)
        play_side(page, 'sides/text_input_step_4.side', name='Enter MyNewButton as the new button name and click the blue button', debug=True)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
