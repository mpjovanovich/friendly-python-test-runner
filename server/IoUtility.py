from pathlib import Path


class IoUtility:

    @staticmethod
    def write_temp_file(content: str, file_path: Path) -> None:
        with open(file_path, "w") as file:
            file.write(content)
