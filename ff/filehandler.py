import os
from typing import Callable, Iterable, List, Optional, Tuple, Union
   

class FileHandler:
    """
    A class to handle file operations across multiple directories.
    """

    def __init__(self):
        self.files = []
        self.dirs = []

    def get_files(self, directories: List[str], full_path: bool = True, level: Union[int, List[int]] = -1) -> List[str]:
        """
        Retrieve files from multiple directories with specified depth.

        :param directories: List of directory paths to retrieve files from.
        :param full_path: If True, returns the full path of the files. If False, 
                            returns only the file names.
        :param level: The depth level(s) of subdirectories to traverse. -1 for all levels, 
                        [1, 2] for specific levels, etc.
        :return: List of file paths or file names.
        """
        self.files = []
        for directory in directories:
            self._walk_directory(directory, full_path, level)
        return self.files

    def get_dirs(self, directories: List[str], full_path: bool = True, level: Union[int, List[int]] = -1) -> List[str]:
        """
        Retrieve directories from multiple directories with specified depth.

        :param directories: List of directory paths to retrieve directories from.
        :param full_path: If True, returns the full path of the directories. If False, returns only the directory names.
        :param level: The depth level(s) of subdirectories to traverse. -1 for all levels, [1, 2] for specific levels, etc.
        :return: List of directory paths or directory names.
        """
        self.dirs = []
        for directory in directories:
            self._walk_directories(directory, full_path, level)
        return self.dirs

    def _walk_directory(self, directory: str, full_path: bool, level: Union[int, List[int]], current_level: int = 1):
        """
        Helper method to walk through directories recursively based on the specified level and collect files.

        :param directory: The directory path to walk through.
        :param full_path: If True, returns the full path of the files. If False, returns only the file names.
        :param level: The depth level(s) of subdirectories to traverse.
        :param current_level: The current depth level in the recursion.
        """
        for root, _, files in os.walk(directory):
            if self._should_include_level(level, current_level):
                for file in files:
                    if full_path:
                        self.files.append(os.path.join(root, file))
                    else:
                        self.files.append(file)
            if not self._should_continue_walking(level, current_level):
                break
            current_level += 1

    def _walk_directories(self, directory: str, full_path: bool, level: Union[int, List[int]], current_level: int = 1):
        """
        Helper method to walk through directories recursively based on the specified level and collect directories.

        :param directory: The directory path to walk through.
        :param full_path: If True, returns the full path of the directories. If False, returns only the directory names.
        :param level: The depth level(s) of subdirectories to traverse.
        :param current_level: The current depth level in the recursion.
        """
        for root, dirs, _ in os.walk(directory):
            if self._should_include_level(level, current_level):
                for dir in dirs:
                    if full_path:
                        self.dirs.append(os.path.join(root, dir))
                    else:
                        self.dirs.append(dir)
            if not self._should_continue_walking(level, current_level):
                break
            current_level += 1

    def _should_include_level(self, level: Union[int, List[int]], current_level: int) -> bool:
        """
        Determine if the current level should be included based on the specified level(s).

        :param level: The depth level(s) of subdirectories to traverse.
        :param current_level: The current depth level in the recursion.
        :return: True if the current level should be included, False otherwise.
        """
        if isinstance(level, int):
            return level == -1 or level == current_level
        elif isinstance(level, list):
            return current_level in level
        return False

    def _should_continue_walking(self, level: Union[int, List[int]], current_level: int) -> bool:
        """
        Determine if the directory walking should continue based on the specified level(s).

        :param level: The depth level(s) of subdirectories to traverse.
        :param current_level: The current depth level in the recursion.
        :return: True if the walking should continue, False otherwise.
        """
        if isinstance(level, int):
            return level == -1 or current_level < level
        elif isinstance(level, list):
            return current_level < max(level)
        return False

    def get_file_info(self, path: str) -> Tuple[str, str, str]:
        """
        Get information about a path.

        :param path: The path to a file or directory.
        :return: A tuple containing the directory of the path, the file name, and the file extension.
        """
        directory = os.path.dirname(path)
        filename = os.path.basename(path)
        name, ext = os.path.splitext(filename)
        return directory, name+ext, name, ext

    def filter_files(self, files: List[str], include_extensions: Optional[List[str]] = None, exclude_extensions: Optional[List[str]] = None,
                     include_directories: Optional[List[str]] = None, exclude_directories: Optional[List[str]] = None,
                     include_strings: Optional[List[str]] = None, exclude_strings: Optional[List[str]] = None) -> List[str]:
        """
        Filter files based on extension, directory, or path content.

        :param files: List of file paths to filter.
        :param include_extensions: List of file extensions to include.
        :param exclude_extensions: List of file extensions to exclude.
        :param include_directories: List of directories to include.
        :param exclude_directories: List of directories to exclude.
        :param include_strings: List of strings that the file paths must contain.
        :param exclude_strings: List of strings that the file paths must not contain.
        :return: List of filtered file paths.
        """
        filtered_files = []
        for file in files:
            if include_extensions and os.path.splitext(file)[1] not in include_extensions:
                continue
            if exclude_extensions and os.path.splitext(file)[1] in exclude_extensions:
                continue
            if include_directories and os.path.basename(os.path.dirname(file)) not in include_directories:
                continue
            if exclude_directories and os.path.basename(os.path.dirname(file)) in exclude_directories:
                continue
            if include_strings and not all(string in file for string in include_strings):
                continue
            if exclude_strings and any(string in file for string in exclude_strings):
                continue
            filtered_files.append(file)
        return filtered_files

    def batch_operation(self, files: List[str], operation: Callable[[str, ...], None], *args) -> None:
        """
        Perform a batch operation on a list of files.

        :param files: List of file paths to operate on.
        :param operation: A callable that accepts a file path and any number of additional arguments.
        :param args: Additional arguments to pass to the operation.
        """
        for file in files:
            operation(file, *args)


if __name__ == "__main__":

    from pprint import pprint

    # Example usage:
    handler = FileHandler()
    files = handler.get_files(['/nas/projects/Github/ff/ff_test/dir2'], full_path=True,level=-1)
    files = handler.get_dirs(['/nas/projects/Github/ff/ff_test/dir2'], full_path=True,level=-1)
    # filtered_files = handler.filter_files(files, include_directories=['layoutreader'])
    # print(len(files),len(filtered_files))
    # pprint(filtered_files)
    print(len(files),files)


    print(handler.get_file_info("/nas/projects/Github/ff/ff_test/dir2"))

    # handler.batch_operation(filtered_files, print, 'Additional argument')