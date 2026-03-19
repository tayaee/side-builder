import base64
import json
import os
import sys
import time
from pathlib import Path
from typing import Literal, Optional

import click
from dotenv import load_dotenv
from openai import OpenAI
from playwright.sync_api import sync_playwright

from side_player import __version__
from side_player.common import SeleniumCommand, SeleniumIdeSide, SeleniumTest
from side_player.playwright.sync_api import play_side as play_side_playwright
from side_player.selenium.sync_api import play_side as play_side_selenium

OPENAI_MODEL_NAME = "gpt-5-nano"
DEFAULT_BROWSER_SIZE = "1440x900"


def _parse_browser_size(size: str) -> tuple[int, int] | None:
    """Parse browser size string in 'WIDTHxHEIGHT' format."""
    try:
        parts = size.split("x")
        if len(parts) == 2:
            width, height = int(parts[0]), int(parts[1])
            if width > 0 and height > 0:
                return (width, height)
    except (ValueError, IndexError):
        pass
    return None


def _get_prompt_for_step(step: int, prompt_list: list[str]) -> Optional[str]:
    """Get prompt for the current step from batch list or interactive input.

    Args:
        step: Current step number (1-indexed)
        prompt_list: List of prompts for batch mode (empty list for interactive mode)

    Returns:
        The prompt string, or None if no more prompts in batch mode
    """
    if prompt_list:
        # Batch mode: use prompt from list
        if step - 1 < len(prompt_list):
            prompt = prompt_list[step - 1]
            click.echo(f"\n[Step {step}] AI prompt for browser action: {prompt}")
            return prompt
        else:
            # No more prompts in batch mode
            return None
    else:
        # Interactive mode: prompt user for input
        return click.prompt(
            f"\n[Step {step}] AI prompt for browser action", default="exit"
        )


class SeleniumIdeSideBuilder:
    def __init__(
        self,
        base_url: str,
        driver_name: Literal["uc", "playwright", "selenium"] = "uc",
        stealth: bool = True,
        private: bool = False,
        browser_size: str = DEFAULT_BROWSER_SIZE,
    ):
        self.base_url = base_url
        self.driver_name = driver_name
        self.stealth = stealth
        self.private = private
        self.browser_size = browser_size

        if driver_name == "playwright":
            self.pw = sync_playwright().start()
            self.browser = self.pw.chromium.launch(headless=False)
            size = _parse_browser_size(browser_size)
            if size:
                self.page = self.browser.new_page(
                    viewport={"width": size[0], "height": size[1]}
                )
            else:
                self.page = self.browser.new_page()
        elif driver_name == "uc":
            import undetected_chromedriver as uc
            from selenium.webdriver.chrome.options import Options

            opts = uc.ChromeOptions()
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            }
            opts.add_experimental_option("prefs", prefs)
            opts.add_argument("--disable-features=PasswordLeakDetection")
            opts.add_argument("--disable-features=SafeBrowsingPasswordProtection")
            opts.add_argument("--disable-save-password-bubble")
            self.driver_handle = uc.Chrome(options=opts)

            # Set browser window size
            size = _parse_browser_size(browser_size)
            if size:
                self.driver_handle.set_window_size(size[0], size[1])

            # For uc driver, we simulate page interface
            class PageWrapper:
                def __init__(self, driver):
                    self.driver = driver

                @property
                def url(self):
                    return self.driver.current_url

                def screenshot(self):
                    return self.driver.get_screenshot_as_png()

                def evaluate(self, js):
                    return self.driver.execute_script(js)

                def goto(self, url):
                    return self.driver.get(url)

            self.page = PageWrapper(self.driver_handle)
        else:  # selenium
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            opts = Options()
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
            }
            opts.add_experimental_option("prefs", prefs)
            opts.add_argument("--disable-features=PasswordLeakDetection")
            opts.add_argument("--disable-features=SafeBrowsingPasswordProtection")
            opts.add_argument("--disable-save-password-bubble")
            opts.add_experimental_option("excludeSwitches", ["enable-automation"])
            # chrome_options.use_automation_extension = False
            self.driver_handle = webdriver.Chrome(options=opts)

            # Set browser window size
            size = _parse_browser_size(browser_size)
            if size:
                self.driver_handle.set_window_size(size[0], size[1])

            class PageWrapper:
                def __init__(self, driver):
                    self.driver = driver

                @property
                def url(self):
                    return self.driver.current_url

                def screenshot(self):
                    return self.driver.get_screenshot_as_png()

                def evaluate(self, js):
                    return self.driver.execute_script(js)

                def goto(self, url):
                    return self.driver.get(url)

            self.page = PageWrapper(self.driver_handle)

    def _get_chrome_profile_path(self):
        """Get the Chrome user data directory path."""
        import platform

        system = platform.system()
        if system == "Windows":
            return os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data\Default")
        elif system == "Darwin":  # macOS
            return os.path.expanduser("~/Library/Application Support/Google/Chrome")
        else:  # Linux
            return os.path.expanduser("~/.config/google-chrome")

    def save_side(self, filename: os.PathLike, side: SeleniumIdeSide):
        with open(filename, "w", encoding="utf-8") as f:
            f.write(side.model_dump_json(indent=2))

    def close(self):
        if self.driver_name == "playwright":
            self.browser.close()
            self.pw.stop()
        else:
            self.driver_handle.quit()


class AISideBuilder(SeleniumIdeSideBuilder):
    def __init__(
        self,
        base_url: str,
        api_key: str,
        model: str = OPENAI_MODEL_NAME,
        driver_name: Literal["uc", "playwright", "selenium"] = "uc",
        stealth: bool = True,
        private: bool = False,
        browser_size: str = DEFAULT_BROWSER_SIZE,
    ):
        super().__init__(
            base_url,
            driver_name=driver_name,
            stealth=stealth,
            private=private,
            browser_size=browser_size,
        )
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def _smart_evaluate(self, js_code: str):
        is_playwright = "playwright" in str(type(self.page)).lower()

        if is_playwright:
            # playwright
            final_js = f"() => {{ {js_code} }}"
        else:
            # selenium or uc
            final_js = js_code

        # print(f"DEBUG {is_playwright=}, {final_js=}")

        return self.page.evaluate(final_js)

    def _execute_hint_js(self, selector, description):
        js = (
            """
        var sel = "%s";
        var items = Array.from(document.querySelectorAll(sel));
        return items.map(function(i) {
            var style = getComputedStyle(i);
            var text = (i.innerText || i.ariaLabel || "").trim().substring(0, 15).replace(/\\n/g, " ");
            return '<' + i.tagName +
                   (i.id ? ' id="' + i.id + '"' : '') +
                   ' class="' + i.className + '"' +
                   ' text="' + text + '"' +
                   ' mouse="' + style.cursor + '">';
        }).filter(function(x) { return x !== null; }).join('\\n');
        """
            % selector
        )

        try:
            res = self._smart_evaluate(js)
            # Handle both string and list returns (playwright may return list)
            if res:
                if isinstance(res, list):
                    return list(dict.fromkeys(res)) if res else []
                return list(dict.fromkeys(res.split("\n"))) if res else []
            return []
        except Exception as e:
            print(f"!! JS Error in {description}: {str(e)[:50]}")
            return []

    def build_keyboard_hints(self) -> str:
        print("\n[Scanning Keyboard Elements]")
        # 개별적으로 로깅하며 수집
        h1 = self._execute_hint_js("input", "Standard Input")
        h2 = self._execute_hint_js("textarea", "Text Area")
        h3 = self._execute_hint_js("select", "Selection Box")
        # Each hint is a list, join them properly
        all_hints = []
        for h in [h1, h2, h3]:
            if isinstance(h, list):
                all_hints.extend(h)
            elif h:
                all_hints.append(h)
        return "\n".join(all_hints)

    def build_mouse_hints(self) -> str:
        print("\n[Scanning Mouse Elements]")
        h1 = self._execute_hint_js("button, [role='button']", "Buttons")
        h2 = self._execute_hint_js("a, [role='link']", "Links")

        # Custom Clickables (div, span 등)
        js_custom = """
        var tags = Array.from(document.querySelectorAll('div, span, i'));
        return tags.filter(function(el) {
            var s = getComputedStyle(el);
            return s.cursor === 'pointer' || el.onclick || el.getAttribute('onclick');
        }).map(function(i) {
            return '<' + i.tagName + ' id="' + (i.id||'') + '" class="' + (i.className||'') + '" mouse="pointer">';
        }).join('\\n');
        """
        print("Scanning DOM: [Custom Clickables] Scanning div/span...")
        try:
            # Use _smart_evaluate to handle playwright's arrow function requirement
            custom_res = self._smart_evaluate(js_custom)
            # Handle both string and list returns
            if isinstance(custom_res, list):
                c_count = len(custom_res)
            elif custom_res:
                c_count = len(custom_res.split("\n"))
            else:
                c_count = 0
            print(f"Scanning DOM: [Custom Clickables] Found: {c_count} items")

            # Build all hints properly handling lists
            all_hints = []
            for h in [h1, h2]:
                if isinstance(h, list):
                    all_hints.extend(h)
                elif h:
                    all_hints.append(h)
            if isinstance(custom_res, list):
                all_hints.extend(custom_res)
            elif custom_res:
                all_hints.append(custom_res)
            return "\n".join(all_hints)
        except Exception as e:
            print(f"!! Custom Click Error: {str(e)[:50]}")
            # Return only h1 and h2
            all_hints = []
            for h in [h1, h2]:
                if isinstance(h, list):
                    all_hints.extend(h)
                elif h:
                    all_hints.append(h)
            return "\n".join(all_hints)

    def build_dom_hint(self) -> str:
        kb_part = self.build_keyboard_hints()
        ms_part = self.build_mouse_hints()

        return f"=== KEYBOARD ===\n{kb_part}\n\n=== MOUSE ===\n{ms_part}".strip()

    def process_prompts(
        self,
        prompts: list[str],
        output_name: str,
        sides_dir: Path,
        save_confirm: bool = True,
        interactive_confirm: bool = False,
    ) -> list[tuple[Path, str]]:
        """
        Process a list of AI prompts and generate side files.

        Args:
            prompts: List of AI prompts to process
            output_name: Base name for output files
            sides_dir: Directory to save side files
            save_confirm: If True, save all steps (for non-interactive mode)
            interactive_confirm: If True, prompt user for confirmation (for interactive mode)

        Returns:
            List of tuples (file_path, prompt) for saved steps
        """
        saved_steps = []
        for step, prompt in enumerate(prompts, 1):
            if prompt.lower() in ["exit", "done"]:
                break

            file_name = f"{output_name}_step_{step}.side"
            file_path = sides_dir / file_name

            try:
                self.ai_create_side_file(llm_prompt=prompt, side_file=file_path)
                if self.driver_name == "playwright":
                    play_side_playwright(self.page, file_path, debug=True)
                else:
                    play_side_selenium(self.driver_handle, file_path, debug=True)

                should_save = save_confirm
                if interactive_confirm:
                    should_save = click.confirm(f"    Save {file_path}?", default=True)

                if should_save:
                    saved_steps.append((file_path, prompt))
                elif file_path.exists():
                    file_path.unlink()
            except Exception as e:
                click.echo(f"    Error: {e}")

        return saved_steps

    def ai_create_side_file(
        self,
        llm_prompt: str,
        side_file: Optional[os.PathLike] = None,
    ) -> SeleniumIdeSide:
        screenshot_bytes = self.page.screenshot()
        base64_image = base64.b64encode(screenshot_bytes).decode("utf-8")

        dom_hint = self.build_dom_hint()

        prompt = f"""
        You are a Selenium IDE expert. Return a JSON list of Selenium IDE commands.

        [Instruction]: {llm_prompt}
        [Current URL]: {self.page.url}
        [DOM Hint]: {dom_hint}

        [Supported Commands and Target/Value Formats]:
        - setWindowSize: target="width,height" (e.g., "900,900"), value=""
        - open: target="URL" (e.g., "https://example.com"), value=""
        - click: target="selector" (e.g., "css=.btn"), value=""
        - type: target="selector", value="text to type" (e.g., "user123")
        - select: target="selector", value="label=value"
        - waitForElementVisible: target="selector", value=""

        [Selector Rules]:
        - For ID: use "id=element_id"
        - For Class: use "css=.class_name"
        - For Name: use "name=element_name"
        - For XPath: use "xpath=//tag[@attr='val']"
        - NEVER use "class=" as a prefix. Use "css=." instead.

        [Return Format]:
        Return ONLY a JSON object with this exact structure:
        {{
          "commands": [
            {{"command": "command_name", "target": "target_value", "value": "value_value"}}
          ]
        }}

        Example responses:
        - "Resize browser to 900x900": {{"command": "setWindowSize", "target": "900,900", "value": ""}}
        - "Click shopping cart": {{"command": "click", "target": "css=.shopping_cart_link", "value": ""}}
        - "Type hello in input": {{"command": "type", "target": "css=#username", "value": "hello"}}
        """

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            response_format={"type": "json_object"},
        )

        cmds_data = json.loads(response.choices[0].message.content).get("commands", [])
        selenium_cmds = [SeleniumCommand(**c) for c in cmds_data]

        side = SeleniumIdeSide(
            name=llm_prompt,
            url=self.base_url,
            tests=[SeleniumTest(name=llm_prompt, commands=selenium_cmds)],
            urls=[self.base_url],
        )

        if side_file:
            self.save_side(side_file, side=side)
        return side


# --- Templates for Code Generation ---

PLAYWRIGHT_SYNC_TEMPLATE = """# /// pyproject
# [requires]
# python = ">=3.10"
# playwright = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

from playwright.sync_api import sync_playwright

from side_player.playwright.sync_api import play_side


def main():
    print("Starting " + __file__)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
{steps}
        browser.close()
        print("Done.")


if __name__ == "__main__":
    main()
"""

PLAYWRIGHT_ASYNC_TEMPLATE = """# /// pyproject
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
    print("Starting " + __file__)
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
{steps}
        await browser.close()
        print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
"""

SELENIUM_SYNC_TEMPLATE = """# /// pyproject
# [requires]
# python = ">=3.10"
# selenium = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from side_player.selenium.sync_api import play_side


def main():
    print("Starting " + __file__)
    chrome_options = Options()
    prefs = {{
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-features=SafeBrowsingPasswordProtection")
    chrome_options.add_argument("--disable-save-password-bubble")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    # chrome_options.use_automation_extension = False
    driver = webdriver.Chrome(options=chrome_options)
    try:
{steps}
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    main()
"""

UC_SYNC_TEMPLATE = """# /// pyproject
# [requires]
# python = ">=3.10"
# undetected-chromedriver = "*"
# side-player = "*"
# ///
# Run: uv run <script>.py (with PEP 723 support)

import undetected_chromedriver as uc

from side_player.selenium.sync_api import play_side


def main():
    print("Starting " + __file__)
    chrome_options = uc.ChromeOptions()
    prefs = {{
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    }}
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_argument("--disable-features=PasswordLeakDetection")
    chrome_options.add_argument("--disable-features=SafeBrowsingPasswordProtection")
    chrome_options.add_argument("--disable-save-password-bubble")
    driver = uc.Chrome(options=chrome_options)
    try:
{steps}
    finally:
        driver.quit()
        print("Done.")


if __name__ == "__main__":
    main()
"""


class VersionCommand(click.Command):
    def format_help(self, ctx, formatter):
        from side_player import __version__

        formatter.write(f"\nside-builder version {__version__}\n")
        super().format_help(ctx, formatter)


@click.command(cls=VersionCommand)
@click.version_option(version=__version__, prog_name="side-builder")
@click.option(
    "--output",
    default=f"demo_{int(time.time())}",
    help="Project name (e.g.: demo1)",
)
@click.option(
    "--driver-name",
    "driver_name",
    type=click.Choice(["uc", "playwright", "selenium"], case_sensitive=False),
    default="playwright",
    help="Browser driver to use (default: playwright). uc requires Python 3.10.",
)
@click.option(
    "--private",
    type=bool,
    default=True,
    is_flag=True,
    help="Use private mode (default: False, use desktop browser profile)",
)
@click.option(
    "--browser-size",
    "browser_size",
    default=DEFAULT_BROWSER_SIZE,
    help=f"Browser window size in WIDTHxHEIGHT format (default: {DEFAULT_BROWSER_SIZE})",
)
@click.option(
    "--prompts",
    "prompts",
    default=None,
    help="Semicolon-separated list of AI prompts for non-interactive mode (e.g., 'open page;login;logout')",
)
def main(output, driver_name, private, browser_size, prompts):
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        click.echo("Error: OPENAI_API_KEY not found.")
        return

    # Warning for uc driver with Python 3.11+
    if driver_name == "uc" and sys.version_info >= (3, 11):
        click.echo(
            "WARNING: The 'uc' (undetected_chromedriver) driver may not work correctly "
            "with Python 3.11 or higher. If you encounter issues, please downgrade to "
            "Python 3.10 or use --driver=playwright/--driver=selenium instead.",
            err=True,
        )

    # Validate browser size format
    if _parse_browser_size(browser_size) is None:
        click.echo(
            f"WARNING: Invalid browser size format '{browser_size}'. "
            f"Expected format: WIDTHxHEIGHT (e.g., 1440x900). "
            f"Using default: {DEFAULT_BROWSER_SIZE}",
            err=True,
        )
        browser_size = DEFAULT_BROWSER_SIZE

    stealth = driver_name == "uc"  # uc is designed to be stealthy by default
    print(f"Using OPENAI_API_KEY={api_key[:16]}******************************")
    print(f"{driver_name=}, {private=}, {stealth=}, {browser_size=}")

    sides_dir = Path("sides")
    sides_dir.mkdir(parents=True, exist_ok=True)

    builder = AISideBuilder(
        base_url="",
        api_key=api_key,
        driver_name=driver_name,
        private=private,
        browser_size=browser_size,
    )
    saved_steps = []

    try:
        # Prepare prompt list for batch mode or empty list for interactive mode
        prompt_list = [p.strip() for p in prompts.split(";")] if prompts else []

        # Unified main loop for both interactive and batch modes
        step = 1
        while True:
            # Get prompt - from batch list or interactive input
            prompt = _get_prompt_for_step(step, prompt_list)

            # Break if no more prompts in batch mode
            if prompt is None:
                break

            if prompt.lower() in ["exit", "done"]:
                break

            file_name = f"{output}_step_{step}.side"
            file_path = sides_dir / file_name

            try:
                builder.ai_create_side_file(llm_prompt=prompt, side_file=file_path)
                if driver_name == "playwright":
                    play_side_playwright(builder.page, file_path, debug=True)
                else:
                    play_side_selenium(builder.driver_handle, file_path, debug=True)

                # In batch mode, always save; in interactive mode, ask for confirmation
                if prompt_list:
                    # Batch mode: auto-save
                    saved_steps.append((file_path, prompt))
                else:
                    # Interactive mode: ask for confirmation
                    if click.confirm(f"    Save {file_path}?", default=True):
                        saved_steps.append((file_path, prompt))
                        step += 1
                    elif file_path.exists():
                        file_path.unlink()

                # Increment step for batch mode
                if prompt_list:
                    step += 1
            except Exception as e:
                click.echo(f"    Error: {e}")
    finally:
        builder.close()

    if saved_steps:
        # Generate playwright sync code
        sync_code = "\n".join(
            [
                f"        play_side(page, '{f.as_posix()}', name='{p}', debug=True)"
                for f, p in saved_steps
            ]
        )
        sync_filename = f"{output}_pw_sync.py"
        with open(sync_filename, "w", encoding="utf-8") as f:
            f.write(PLAYWRIGHT_SYNC_TEMPLATE.format(steps=sync_code))

        # Generate playwright async code
        async_code = "\n".join(
            [
                f"        await play_side_async(page, '{f.as_posix()}', name='{p}', debug=True)"
                for f, p in saved_steps
            ]
        )
        async_filename = f"{output}_pw_async.py"
        with open(async_filename, "w", encoding="utf-8") as f:
            f.write(PLAYWRIGHT_ASYNC_TEMPLATE.format(steps=async_code))

        # Generate selenium sync code
        sel_sync_code = "\n".join(
            [
                f"        play_side(driver, '{f.as_posix()}', name='{p}', debug=True)"
                for f, p in saved_steps
            ]
        )
        sel_sync_filename = f"{output}_sel_sync.py"
        with open(sel_sync_filename, "w", encoding="utf-8") as f:
            f.write(SELENIUM_SYNC_TEMPLATE.format(steps=sel_sync_code))

        # Generate uc sync code
        uc_sync_code = "\n".join(
            [
                f"        play_side(driver, '{f.as_posix()}', name='{p}', debug=True)"
                for f, p in saved_steps
            ]
        )
        uc_sync_filename = f"{output}_uc_sync.py"
        with open(uc_sync_filename, "w", encoding="utf-8") as f:
            f.write(UC_SYNC_TEMPLATE.format(steps=uc_sync_code))

        click.echo(
            f"\nScripts created: {sync_filename}, {async_filename}, {sel_sync_filename}, {uc_sync_filename}"
        )
        click.echo(f"Side files saved in: {sides_dir.as_posix()}/")
    else:
        click.echo("\nNo steps saved.")


if __name__ == "__main__":
    main()
