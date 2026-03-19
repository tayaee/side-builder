"""
Regression test for playwright driver.
Tests the side-builder with saucedemo.com scenarios.
"""

import glob
import os
import re
import subprocess
import sys

from dotenv import load_dotenv

# Load .env file to get OPENAI_API_KEY
load_dotenv()


def cleanup_test_files():
    """Clean up test files from previous runs."""
    # Remove python files
    for f in glob.glob("tmp_reg_test_1*.py"):
        try:
            os.remove(f)
        except Exception:
            pass
    # Remove side files
    for f in glob.glob("sides/tmp_reg_test_1*.side"):
        try:
            os.remove(f)
        except Exception:
            pass
    # Create sides directory if it doesn't exist
    os.makedirs("sides", exist_ok=True)
    # Clean up tmp directory if it exists (handle permission errors)
    if os.path.exists("tmp"):
        import shutil

        try:
            shutil.rmtree("tmp")
        except Exception as e:
            print(f"Warning: Could not remove tmp directory: {e}")
    print("Cleaned up test files")


def run_side_builder():
    """Run side-builder with automated prompts."""
    # Use non-interactive mode with --prompts option (semicolon-delimited)
    prompts = "Go to the home of saucedemo.com; Log in; Log out"

    cmd = [
        "uv",
        "run",
        "--python",
        "3.10",
        "side-builder",
        "--driver-name",
        "playwright",
        "--output",
        "tmp_reg_test_1",
        "--prompts",
        prompts,
    ]

    # Use environment with OPENAI_API_KEY
    env = os.environ.copy()
    if "OPENAI_API_KEY" not in env or not env["OPENAI_API_KEY"]:
        print("ERROR: OPENAI_API_KEY not set in environment")
        return False

    try:
        print(f"{subprocess.list2cmdline(cmd)=}")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
            timeout=120,
        )

        stdout = result.stdout
        stderr = result.stderr

        print(f"side-builder output:\n{stdout}")
        if stderr:
            print(f"side-builder errors:\n{stderr}")

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("ERROR: side-builder timed out")
        return False
    except Exception as e:
        print(f"ERROR running side-builder: {e}")
        return False


def verify_test_results():
    """Verify the test results against expected criteria."""
    passed = 0
    total = 6

    # Verify 1: 4 Python files created (pw_sync, pw_async, sel_sync, uc_sync)
    py_files = glob.glob("tmp_reg_test_1*.py")
    if len(py_files) == 4:
        print("Verify 1: PASS - 4 Python files created")
        passed += 1
    else:
        print(f"Verify 1: FAIL - Expected 4 Python files, found {len(py_files)}")

    # Verify 2: Each Python file has 3 play_side calls (play_side or play_side_async)
    all_have_3_play_side = True
    for py_file in py_files:
        with open(py_file, "r") as f:
            content = f.read()
            play_side_count = content.count("play_side(")
            play_side_async_count = content.count("play_side_async(")
            total_count = play_side_count + play_side_async_count
            if total_count != 3:
                print(
                    f"Verify 2: FAIL - {py_file} has {total_count} play_side calls, expected 3"
                )
                all_have_3_play_side = False
    if all_have_3_play_side:
        print("Verify 2: PASS - All Python files have 3 play_side calls")
        passed += 1

    # Verify 3: 3 side files created
    side_files = glob.glob("sides/tmp_reg_test_1*.side")
    if len(side_files) == 3:
        print("Verify 3: PASS - 3 side files created")
        passed += 1
    else:
        print(f"Verify 3: FAIL - Expected 3 side files, found {len(side_files)}")

    # Sort side files to verify in order
    side_files.sort()

    # Verify 4: First side file contains target.*https://saucedemo.com
    if side_files:
        with open(side_files[0], "r") as f:
            content = f.read()
            # Match target with https://saucedemo.com (allowing www. prefix)
            if re.search(r"target.*https://(?:www\.)?saucedemo\.com", content):
                print(
                    "Verify 4: PASS - First side file contains target.*https://saucedemo.com"
                )
                passed += 1
            else:
                print(
                    "Verify 4: FAIL - First side file does not contain target.*https://saucedemo.com"
                )
    else:
        print("Verify 4: SKIP - No side files found")

    # Verify 5: Second side file contains target.*id=login-button
    if len(side_files) >= 2:
        with open(side_files[1], "r") as f:
            content = f.read()
            # The JSON format has target value as "id=login-button" (no quotes in the value)
            if re.search(r"target.*id=login-button", content):
                print(
                    "Verify 5: PASS - Second side file contains target.*id=login-button"
                )
                passed += 1
            else:
                print(
                    "Verify 5: FAIL - Second side file does not contain target.*id=login-button"
                )
    else:
        print("Verify 5: SKIP - Not enough side files found")

    # Verify 6: Third side file contains target.*id=logout_sidebar_link
    if len(side_files) >= 3:
        with open(side_files[2], "r") as f:
            content = f.read()
            # The JSON format has target value as "id=logout_sidebar_link" (no quotes in the value)
            if re.search(r"target.*id=logout_sidebar_link", content):
                print(
                    "Verify 6: PASS - Third side file contains target.*id=logout_sidebar_link"
                )
                passed += 1
            else:
                print(
                    "Verify 6: FAIL - Third side file does not contain target.*id=logout_sidebar_link"
                )
    else:
        print("Verify 6: SKIP - Not enough side files found")

    print(f"\nResult: {passed}/{total} verifications passed")
    return passed == total


def main():
    """Main test execution."""
    print("=" * 60)
    print("Playwright Regression Test")
    print("=" * 60)

    # Cleanup old test files
    cleanup_test_files()

    # Run side-builder
    print("\nRunning side-builder...")
    if not run_side_builder():
        print("\nERROR: side-builder failed")
        return 1

    # Verify results
    print("\nVerifying results...")
    if verify_test_results():
        print("\nAll tests PASSED")
        return 0
    else:
        print("\nSome tests FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
