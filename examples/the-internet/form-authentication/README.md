Recording:

% side-builder --output form_auth
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of the-internet.herokuapp.com
Playing: sides\form_auth_step_1.side ()
    Success: open https://the-internet.herokuapp.com/
    Save sides\form_auth_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Resize browser to 1200 x 1200
Playing: sides\form_auth_step_2.side ()
    Success: setWindowSize 1200,1200
    Save sides\form_auth_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Click Form Authentication
Playing: sides\form_auth_step_3.side ()
    Success: open https://the-internet.herokuapp.com/
    Success: waitForElementVisible xpath=//a[normalize-space()='Form Authentication']
    Success: click xpath=//a[normalize-space()='Form Authentication']
    Save sides\form_auth_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]: Log in
Playing: sides\form_auth_step_4.side ()
    Success: open https://the-internet.herokuapp.com/login
    Success: type id=username
    Success: type id=password
    Success: click css=.radius
    Save sides\form_auth_step_4.side? [Y/n]:

[Step 5] AI prompt for browser action [exit]: Log out
Playing: sides\form_auth_step_5.side ()
    Success: waitForElementVisible css=a.button.secondary.radius
    Success: click css=a.button.secondary.radius
    Save sides\form_auth_step_5.side? [Y/n]:

[Step 6] AI prompt for browser action [exit]:

Scripts created: form_auth_pw_sync.py, form_auth_pw_async.py, form_auth_sel_sync.py
Side files saved in: sides/

Replay:

# Replay them with Playwright Async API
% uv run form_auth_pw_async.py

# Replay them with Playwright Sync API
% uv run form_auth_pw_sync.py

# Replay them with Selenium Sync API
% uv run form_auth_sel_sync.py
