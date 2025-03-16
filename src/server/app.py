from flask import Flask, request, Response
import logging
from src.test_runner.suite_dispatcher import SuiteDispatcher
from src.test_runner.config_utility import ConfigUtility
from logging.handlers import RotatingFileHandler
"""
To test:
curl -X POST http://localhost:5000/api/run-tests \
  -H "Content-Type: application/json" \
  -d '{"suite_name": "the_suite", "program": "print(1)"}'
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


@app.route('/api/run-tests', methods=['POST'])
def run_tests():
    data = request.get_json()

    if not data or 'suite_name' not in data or 'program' not in data:
        logger.warning(
            f"Invalid submission attempt from IP: {request.remote_addr}")
        return Response(
            "Error: Missing required fields: suite_name and program",
            mimetype='text/plain',
            status=400)

    suite_name = data['suite_name']
    program = data['program']
    logger.info(f"Submission from {request.remote_addr}; Suite: {suite_name}")

    results = dispatcher.run_suite(suite_name, program)
    return Response(results, mimetype='text/plain')


if __name__ == '__main__':
    app.run(debug=True)
