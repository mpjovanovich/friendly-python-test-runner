#!/usr/bin/env python3
import argparse
import io
import os
import requests
import sys
import time
"""
python run_test.py test test_file.py --api http://localhost:5000/api/run-tests
"""


def submit_test(test_suite_name, test_file_path, api_url):
    """Submit a test file to the API endpoint."""
    # Validate file exists
    if not os.path.exists(test_file_path):
        print(f"🚫 Error: Test file '{test_file_path}' not found.")
        print(f"Please check the file path and try again.")
        sys.exit(1)

    # Validate file is a Python file
    if not test_file_path.endswith('.py'):
        print(f"Error: The file '{test_file_path}' must have a .py extension.")
        print("Submission cancelled.")
        sys.exit(1)

    # Read the file as binary
    try:
        with open(test_file_path, 'rb') as f:
            file_binary = f.read()
    except Exception as e:
        print(f"🚫 Error reading file: {e}")
        print("Please check file permissions and try again.")
        sys.exit(1)

    # Prepare request headers
    headers = {
        'Content-Type': 'application/octet-stream',
        'X-Test-Suite-Name': test_suite_name
    }

    # Send the request
    print(
        f"Submitting test file '{os.path.basename(test_file_path)}' to test suite '{test_suite_name}'..."
    )

    try:
        # Needed to add this to support unicode characters, like the emojis in the test output
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

        response = requests.post(api_url,
                                 data=file_binary,
                                 headers=headers,
                                 timeout=30)

        if response.status_code == 200:
            print(response.text)
        else:
            print(
                f"Submission failed with status code: {response.status_code}")
            print(f"Response: {response.text}")

    except requests.exceptions.Timeout:
        print(
            "Request timed out. The server might be busy or the test is taking too long."
        )
        print("Please try again later or check with your instructor.")

    except requests.exceptions.ConnectionError:
        print("Connection error. Please check your internet connection.")
        print(f"Make sure the API URL '{api_url}' is correct.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("If this problem persists, please contact your instructor.")


def main():
    # Create argument parser with custom error message
    class FriendlyArgumentParser(argparse.ArgumentParser):

        def error(self, message):
            print("\nThe file was not called correctly. Example usage:\n")
            print("python run_test.py lab-fstrings test_file.py\n")
            sys.exit(1)

    # Use our friendly parser
    parser = FriendlyArgumentParser(
        description="Submit a test file to the testing API.")

    # Add arguments with more descriptive help messages
    parser.add_argument(
        "test_suite",
        help="The test suite name from the lab (e.g., 'lab-fstrings')")

    parser.add_argument(
        "test_file",
        help="The path to your Python test file (must end in .py)")

    ## When distributing to students, replace the placeholder with the
    ## actual API URL
    parser.add_argument(
        "--api",
        default="http://[insert-api-url]/api/run-tests",
        help="API URL for test submission (default: %(default)s)")

    args = parser.parse_args()
    submit_test(args.test_suite, args.test_file, args.api)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSubmission cancelled by user.")
        sys.exit(1)
