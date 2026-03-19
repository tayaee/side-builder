@echo off
REM Regression test for selenium driver

echo Running Selenium Regression Test...
echo.

cd regression_tests
uv run python test_selenium.py
set result=%errorlevel%

cd ..
exit /b %result%
