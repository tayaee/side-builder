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
        play_side(page, 'sides/signup_logout_step_1.side', name='Go to the home of demoblaze.com', debug=True)
        play_side(page, 'sides/signup_logout_step_2.side', name='Adjust browser size to 1200x1200', debug=True)
        play_side(page, 'sides/signup_logout_step_3.side', name='Sign up as side-builder-user-20260303 with password-20260303', debug=True)
        browser.close()
        print("Done.")


if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
