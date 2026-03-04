Recording:

```
% side-builder --output login_logout
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of demoblaze.com
Playing: sides\login_logout_step_1.side ()
    Success: open https://demoblaze.com/
    Save sides\login_logout_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Resize the browser to 1200x1200
Playing: sides\login_logout_step_2.side ()
    Success: setWindowSize 1200,1200
    Save sides\login_logout_step_2.side? [Y/n]: n

[Step 2] AI prompt for browser action [exit]: Log in as side-builder-user-20260303 with password-20260303
Playing: sides\login_logout_step_2.side ()
    Success: setWindowSize 1024,768
    Success: open https://demoblaze.com/
    Success: click id=login2
    Success: waitForElementVisible id=loginusername
    Success: type id=loginusername
    Success: type id=loginpassword
    Success: click xpath=//div[@id='logInModal']//button[contains(@class,'btn-primary') and contains(.,'Log in')]
    Save sides\login_logout_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Log out
Playing: sides\login_logout_step_3.side ()
    Success: waitForElementVisible id=logout2
    Success: click id=logout2
    Save sides\login_logout_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]:

Scripts created: login_logout_pw_sync.py, login_logout_pw_async.py, login_logout_sel_sync.py
Side files saved in: sides/
```

Replaying:
```
% uv run login_logout_pw_sync.py

% uv run login_logout_pw_async.py

% uv run login_logout_sel_sync.py
```