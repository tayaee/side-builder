#!/bin/bash
# Regression test for uc driver

echo "Running UC Regression Test..."
echo ""

cd regression_tests
uv run python test_uc.py
result=$?

cd ..
exit $result
