#!/bin/bash
# Regression test for selenium driver

echo "Running Selenium Regression Test..."
echo ""

cd regression_tests
uv run python test_selenium.py
result=$?

cd ..
exit $result
