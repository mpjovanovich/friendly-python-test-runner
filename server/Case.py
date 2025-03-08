class Case:

    def __init__(self,
                 title: str,
                 inputs: list[str],
                 expected_output: str,
                 comparison_type: str,
                 is_bonus: bool = False):
        self.title = title
        self.inputs = inputs
        self.expected_output = expected_output
        self.comparison_type = comparison_type
        self.is_bonus = is_bonus
        self.passed = None
        self.error = None

    def set_result(self, passed: bool, error: str = None):
        self.passed = passed
        self.error = error
