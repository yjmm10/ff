import os
import pytest
from ff.filehandler import FileHandler

@pytest.fixture
def setup_test_directories(tmpdir):
    # Create a temporary directory structure for testing
    dir1 = tmpdir.mkdir("dir1")
    dir2 = dir1.mkdir("dir2")
    dir3 = dir2.mkdir("dir3")
    dir4 = dir3.mkdir("dir4")
    dir1.join("file1.txt").write("content")
    dir2.join("file2.txt").write("content")
    dir3.join("file3.txt").write("content")
    dir4.join("file4.txt").write("content")
    return tmpdir

def test_get_files(setup_test_directories):
    handler = FileHandler()
    files = handler.get_files([str(setup_test_directories.join("dir1"))], full_path=True, level=-1)
    assert len(files) == 4
    assert all(os.path.basename(file).startswith("file") for file in files)

def test_get_dirs(setup_test_directories):
    handler = FileHandler()
    dirs = handler.get_dirs([str(setup_test_directories.join("dir1"))], full_path=True, level=-1)
    assert len(dirs) == 3
    assert all(os.path.basename(dir).startswith("dir") for dir in dirs)

def test_get_file_info(setup_test_directories):
    handler = FileHandler()
    info = handler.get_file_info(str(setup_test_directories.join("dir1", "file1.txt")))
    assert len(info) == 4
    assert info[1] == "file1.txt"
    assert info[2] == "file1"
    assert info[3] == ".txt"

def test_filter_files(setup_test_directories):
    handler = FileHandler()
    files = handler.get_files([str(setup_test_directories.join("dir1"))], full_path=True, level=-1)
    filtered_files = handler.filter_files(files, include_extensions=[".txt"])
    assert len(filtered_files) == 4
    filtered_files = handler.filter_files(files, exclude_extensions=[".txt"])
    assert len(filtered_files) == 0

def test_batch_operation(setup_test_directories, capsys):
    handler = FileHandler()
    files = handler.get_files([str(setup_test_directories.join("dir1"))], full_path=True, level=-1)
    handler.batch_operation(files, print, 'Additional argument')
    captured = capsys.readouterr()
    assert len(captured.out.splitlines()) == 4