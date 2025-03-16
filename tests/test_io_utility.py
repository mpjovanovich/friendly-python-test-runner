import pytest
from src.test_runner.io_utility import IoUtility, IoOperationError


def test_write_temp_file_success(tmp_path):
    test_file = tmp_path / "test.txt"
    content = "test content"
    IoUtility.write_temp_file(content, test_file)
    assert test_file.read_text() == content


def test_write_temp_file_invalid_path():
    with pytest.raises(IoOperationError):
        IoUtility.write_temp_file("content", "/invalidpath/file.txt")


def test_create_dir_success(tmp_path):
    new_dir = tmp_path / "new_dir"
    IoUtility.create_dir_if_not_exists(new_dir)
    assert new_dir.exists()
    assert new_dir.is_dir()


def test_delete_dir_success(tmp_path):
    test_dir = tmp_path / "test_dir"
    test_dir.mkdir()
    IoUtility.delete_dir_if_exists(test_dir)
    assert not test_dir.exists()


def test_delete_nonexistent_dir(tmp_path):
    nonexistent_dir = tmp_path / "nonexistent"
    ## Should not raise an error
    IoUtility.delete_dir_if_exists(nonexistent_dir)
