Recording:

% side-builder --output text_input
Using OPENAI_API_KEY=sk-proj-OlHCz-hz******************************

[Step 1] AI prompt for browser action [exit]: Go to the home of http://uitestingplayground.com
Playing: sides\text_input_step_1.side ()
    Success: open http://uitestingplayground.com
    Success: waitForElementVisible css=body
    Save sides\text_input_step_1.side? [Y/n]:

[Step 2] AI prompt for browser action [exit]: Adjust browser size to 1200x1200
Playing: sides\text_input_step_2.side ()
    Success: setWindowSize 1200,1200
    Save sides\text_input_step_2.side? [Y/n]:

[Step 3] AI prompt for browser action [exit]: Click Text Input
Playing: sides\text_input_step_3.side ()
    Success: click xpath=//a[text()='Text Input']
    Save sides\text_input_step_3.side? [Y/n]:

[Step 4] AI prompt for browser action [exit]: Enter MyNewButton as the new button name and click the blue button
Playing: sides\text_input_step_4.side ()
    Success: type id=newButtonName
    Success: click id=updatingButton
    Save sides\text_input_step_4.side? [Y/n]:

[Step 5] AI prompt for browser action [exit]:

Scripts created: text_input_pw_sync.py, text_input_pw_async.py, text_input_sel_sync.py
Side files saved in: sides/

Playing:

% uv run text_input_pw_async.py

% uv run text_input_pw_sync.py

% uv run text_input_sel_sync.py
