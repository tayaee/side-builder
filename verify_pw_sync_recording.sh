#!/bin/bash
# Regression test for playwright driver

echo "Running Playwright Regression Test..."
echo ""

cd regression_tests
uv run python test_playwright.py
result=$?

cd ..
exit $result
