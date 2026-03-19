@echo off
REM Regression test for playwright driver

echo Running Playwright Regression Test...
echo.

cd regression_tests
uv run python test_playwright.py
set result=%errorlevel%

cd ..
exit /b %result%
