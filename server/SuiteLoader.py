import yaml
from pathlib import Path
from Case import Case


class SuiteLoader:

    REGISTRY_FILE_NAME = 'registry.yaml'

    def __init__(self, test_cases_dir: str):
        try:
            self._base_path = Path(test_cases_dir)
            self._registry_path = self._base_path / self.REGISTRY_FILE_NAME
            self._registry = self._load_registry()
        except FileNotFoundError:
            raise FileNotFoundError("Registry file not found")

    def _load_registry(self):
        with open(self._registry_path, 'r') as f:
            return yaml.safe_load(f)

    def load_suite(self, suite_name) -> list[Case]:
        try:
            suite_path = self._registry[suite_name]
            file_path = self._base_path / suite_path
            with open(file_path, 'r') as f:
                test_data = yaml.safe_load(f)
                ## Because I'll probably forget what this is doing:
                ## **case is Python's dictionary unpacking syntax.
                ## It will unpack the dictionary into keyword arguments for
                ## the Case constructor.
                return [Case(**case) for case in test_data]
        except KeyError:
            raise KeyError(f"Suite '{suite_name}' not found in registry")
        except FileNotFoundError:
            raise FileNotFoundError(f"Test suite file not found: {suite_name}")
