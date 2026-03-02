# Side Player (side-builder)

side-player is a next-generation automation tool that bridges the gap between AI-driven intent and rock-solid execution. It allows you to create Selenium IDE (.side) scripts interactively using natural language and execute them anywhere using Playwright or Selenium.

---

## Quick Start

### To create and play *.side files with Playwright
Install the package via pip or uv:

```bash
pip install side-player   # with pip
uv add side-player        # with uv
```

Install Playwright
```
playwright install
```

### To create and play *.side files with Selenium
Install the package via pip or uv:

```bash
pip install side-player   # with pip
uv add side-player        # with uv
```

### Configuration
Set the environment variable OPENAI_API_KEY with your ownkey to run side-builder. No API key is required the run the *.side files.

## Demo

### Demo 1. Generate *.side files and demo1_{sync,async,sel_sync}.py

```bash
% side-builder --output demo1
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of https://saucedemo.com
Playing: sides\demo1_step_1.side ()
    Success: open https://saucedemo.com
    Save sides\demo1_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Log in
Playing: sides\demo1_step_2.side ()
    Success: open https://www.saucedemo.com/
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
    Save sides\demo1_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Log out
Playing: sides\demo1_step_3.side ()
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
    Save sides\demo1_step_3.side? [Y/n]:

[Step 10] AI prompt for browser action [exit]:

Scripts created: demo1_sync.py, demo1_async.py, demo1_sel_sync.py
Side files saved in: sides/
```

### Demo 2. Playing *.side files using Playwright Sync API
```
% uv run demo1_sync.py
Playing: sides/demo1_step_1.side (Go to the home of https://saucedemo.com)
    Success: open https://saucedemo.com
Playing: sides/demo1_step_2.side (Log in)
    Success: open https://www.saucedemo.com/
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
Playing: sides/demo1_step_3.side (Log out)
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
Done.
```

### Demo 3. Playing *.side files using Playwright Async API
```
% uv run demo1_async.py
Playing (Async): sides/demo1_step_1.side (Go to the home of https://saucedemo.com)
    Success: open https://saucedemo.com
Playing (Async): sides/demo1_step_2.side (Log in)
    Success: open https://www.saucedemo.com/
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
Playing (Async): sides/demo1_step_3.side (Log out)
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
Done.
```

### Demo 4. Play *.side files using Selenium
```
>uv run demo1_sel_sync.py
Playing: sides/demo1_step_1.side (Go to the home of https://saucedemo.com)
    Success: open https://saucedemo.com
Playing: sides/demo1_step_2.side (Log in)
    Success: open https://www.saucedemo.com/
    Success: type id=user-name
    Success: type id=password
    Success: click id=login-button
Playing: sides/demo1_step_3.side (Log out)
    Success: click id=react-burger-menu-btn
    Success: click id=logout_sidebar_link
Done.
```

## Key Features

* Zero-config Selectors: AI finds the best ID, CSS, or XPath for you automatically.
* Cost Efficient: Use AI only for recording. Execution is 100% local and free.
* Standard Format: Generates standard .side files compatible with the Selenium IDE.
* Developer Friendly: Provides both Sync and Async Playwright APIs.
* Extensible: Built with a modular structure to support Playwright and Selenium.

---

## Prerequisites

- Python 3.12+
- OpenAI API Key (required only for the side-builder recording phase)

## License

This project is licensed under the MIT License.
