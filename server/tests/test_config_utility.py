import os
import pytest
import sys
from pathlib import Path

# Add parent directory to Python path
sys.path.append(str(Path(__file__).parent.parent))

from ConfigUtility import ConfigUtility


def test_fetch_environment_variable_found():
    os.environ['TEST_ENV_VAR_FOUND'] = 'test-cases-repo'
    assert ConfigUtility.get_setting('TEST_ENV_VAR_FOUND') == 'test-cases-repo'
    del os.environ['TEST_ENV_VAR_FOUND']


def test_fetch_environment_variable_not_found():
    with pytest.raises(ValueError):
        ConfigUtility.get_setting('TEST_ENV_VAR_NOT_FOUND')
