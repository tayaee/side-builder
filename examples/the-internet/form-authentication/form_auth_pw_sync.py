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
        play_side(page, 'sides/form_auth_step_1.side', name='Go to the home of the-internet.herokuapp.com', debug=True)
        play_side(page, 'sides/form_auth_step_2.side', name='Resize browser to 1200 x 1200', debug=True)
        play_side(page, 'sides/form_auth_step_3.side', name='Click Form Authentication', debug=True)
        play_side(page, 'sides/form_auth_step_4.side', name='Log in', debug=True)
        play_side(page, 'sides/form_auth_step_5.side', name='Log out', debug=True)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
