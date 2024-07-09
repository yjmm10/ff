import pytest
from unittest.mock import patch
from io import StringIO
import os,sys
from ff import cmdline

# Helper function to create a temporary directory with files and subdirectories
def create_temp_structure(temp_dir):
    os.makedirs(os.path.join(temp_dir, 'dir1', 'subdir1'), exist_ok=True)
    os.makedirs(os.path.join(temp_dir, 'dir2'), exist_ok=True)
    with open(os.path.join(temp_dir, 'file1.txt'), 'w') as f:
        f.write('content')
    with open(os.path.join(temp_dir, 'dir1', 'file2.txt'), 'w') as f:
        f.write('content')
    with open(os.path.join(temp_dir, 'dir1', 'subdir1', 'file3.txt'), 'w') as f:
        f.write('content')
    with open(os.path.join(temp_dir, 'dir2', 'file4.py'), 'w') as f:
        f.write('content')

@pytest.fixture
def temp_dir(tmpdir):
    create_temp_structure(tmpdir)
    return str(tmpdir)


def test_cli_get_files(temp_dir, capsys):
    with patch.object(sys, 'argv', ['ff', temp_dir, '--get-files', '--full-path']):
        cmdline.main()
        captured = capsys.readouterr()
        assert f"Found 4 files:" in captured.out
        assert os.path.join(temp_dir, 'file1.txt') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'file2.txt') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'subdir1', 'file3.txt') in captured.out
        assert os.path.join(temp_dir, 'dir2', 'file4.py') in captured.out

def test_cli_get_dirs(temp_dir, capsys):
    with patch.object(sys, 'argv', ['cli.py', temp_dir, '--get-dirs', '--full-path']):
        cmdline.main()
        captured = capsys.readouterr()
        assert f"Found 3 directories:" in captured.out
        assert os.path.join(temp_dir, 'dir1') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'subdir1') in captured.out
        assert os.path.join(temp_dir, 'dir2') in captured.out

def test_cli_filter_files(temp_dir, capsys):
    with patch.object(sys, 'argv', ['cli.py', temp_dir, '--get-files', '--full-path', '--include-extensions', '.txt']):
        cmdline.main()
        captured = capsys.readouterr()
        assert f"Found 3 files:" in captured.out
        assert os.path.join(temp_dir, 'file1.txt') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'file2.txt') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'subdir1', 'file3.txt') in captured.out

def test_cli_filter_dirs(temp_dir, capsys):
    with patch.object(sys, 'argv', ['ff', temp_dir, '--get-dirs', '--full-path', '--include-strings', 'dir1']):
        cmdline.main()
        captured = capsys.readouterr()
        assert f"Found 3 directories:" in captured.out
        assert os.path.join(temp_dir, 'dir1') in captured.out
        assert os.path.join(temp_dir, 'dir1', 'subdir1') in captured.out