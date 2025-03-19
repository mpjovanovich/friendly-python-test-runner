from flask import Flask, request, Response
import logging
from src.test_runner.suite_dispatcher import SuiteDispatcher
from src.test_runner.config_utility import ConfigUtility
from logging.handlers import RotatingFileHandler
"""
## Raw string
curl -X POST http://localhost:5000/api/run-tests \
  -H "Content-Type: application/octet-stream" \
  -H "X-Test-Suite-Name: test" \
  --data-raw "print(1)" \
  http://localhost:5000/api/run-tests

## File upload
curl -X POST \
  -H "Content-Type: application/octet-stream" \
  -H "X-Test-Suite-Name: test" \
  --data-binary @path/to/script.py \
  http://localhost:5000/api/run-tests
"""

TMP_DIR = ConfigUtility.get_setting("TEST_RUNNER_TMP_DIR")
TEST_CASES_DIR = ConfigUtility.get_setting("TEST_RUNNER_TEST_CASES_DIR")

app = Flask(__name__)

## Disable logging from Flask. We're using our own logging.
app.logger.disabled = True
log = logging.getLogger('werkzeug')
log.disabled = True

dispatcher = SuiteDispatcher(TMP_DIR, TEST_CASES_DIR)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        # 5MB per file, keep 5 backup files
        RotatingFileHandler('student_submissions.log',
                            maxBytes=5 * 1024 * 1024,
                            backupCount=5),
        logging.StreamHandler()
    ])
logger = logging.getLogger(__name__)


def validate_and_extract_data(request):
    """Returns program text, suite_name, and error message."""
    program_text = None
    suite_name = None
    error = None
    content_type = request.headers.get('Content-Type')

    if content_type != 'application/octet-stream':
        error = "Content-Type must be application/octet-stream"
    elif not request.data or 'X-Test-Suite-Name' not in request.headers:
        error = "Missing required fields: X-Test-Suite-Name and program"
    else:
        try:
            program_text = request.get_data().decode('utf-8')
            suite_name = request.headers.get('X-Test-Suite-Name')
        except UnicodeDecodeError:
            error = "Program data must be a valid text file"

    return program_text, suite_name, error


@app.route('/api/run-tests', methods=['POST'])
def run_tests():
    program, suite_name, error = validate_and_extract_data(request)

    if error:
        logger.warning(
            f"Invalid submission attempt from IP: {request.remote_addr} - {error}"
        )
        return Response(f"Error: {error}", mimetype='text/plain', status=400)

    logger.info(f"Submission from {request.remote_addr}; Suite: {suite_name}")
    results = dispatcher.run_suite(suite_name, program)
    return Response(results, mimetype='text/plain')


if __name__ == '__main__':
    debug_mode = ConfigUtility.get_setting("TEST_RUNNER_DEBUG", False)
    app.run(debug=debug_mode, host='0.0.0.0')
