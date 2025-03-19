import pexpect


class OutputUtility:

    @staticmethod
    def get_error_info(error_output: str) -> str:
        """Gets friendly error info from the program after it has finished running"""
        lines = [line.strip() for line in error_output.split("\n")]
        error_lines = []

        for line in lines:
            if not line.startswith("File ") and not line.startswith(
                    "Traceback"):
                error_lines.append(line)

        return "\n".join(error_lines)
