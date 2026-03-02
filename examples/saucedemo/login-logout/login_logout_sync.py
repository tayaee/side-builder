from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        play_side(page, 'sides/login-logout_step_1.side', name='Go to the home of https://saucedemo.com')
        play_side(page, 'sides/login-logout_step_2.side', name='Log in')
        play_side(page, 'sides/login-logout_step_3.side', name='Log out')
        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
