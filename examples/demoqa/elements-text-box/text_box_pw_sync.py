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
        play_side(page, 'sides/text_box_step_1.side', name='Go to https://demoqa.com/text-box.', debug=True)
        play_side(page, 'sides/text_box_step_2.side', name='Enter John Doe as fullname, johndoe@gmail.com as Email, 123 Devil St FL USA as current address and click Submit', debug=True)
        play_side(page, 'sides/text_box_step_3.side', name='Click Submit', debug=True)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
