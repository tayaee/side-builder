Recording:

```
% side-builder --output signup_logout
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of demoblaze.com
Playing: sides\signup_logout_step_1.side ()
    Success: open https://www.demoblaze.com
    Success: waitForElementVisible xpath=//body
    Save sides\signup_logout_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Adjust browser size to 1200x1200
Playing: sides\signup_logout_step_2.side ()
    Success: setWindowSize 1200,1200
    Save sides\signup_logout_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Sign up as side-builder-user-20260303 with password-20260303
Playing: sides\signup_logout_step_3.side ()
    Success: setWindowSize 1024,768
    Success: open https://www.demoblaze.com/
    Success: click id=signin2
    Success: type id=sign-username
    Success: type id=sign-password
    Success: click xpath=//div[@id='signInModal']//button[@class='btn btn-primary']
    Success: waitForElementVisible id=nameofuser
    Save sides\signup_logout_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]:

Scripts created: signup_logout_pw_sync.py, signup_logout_pw_async.py, signup_logout_sel_sync.py
Side files saved in: sides/
```

Replaying:
```
% uv run signup_logout_pw_async.py

% uv run signup_logout_pw_sync.py

% uv run signup_logout_sel_sync.py
```