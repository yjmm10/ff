import argparse
from filehandler import FileHandler

def main():
    parser = argparse.ArgumentParser(description="FileHandler CLI")
    parser.add_argument("directories", nargs="+", help="List of directory paths to retrieve files or directories from.")
    parser.add_argument("--full-path", action="store_true", help="Return the full path of the files or directories.")
    parser.add_argument("--level", type=int, default=-1, help="The depth level(s) of subdirectories to traverse. -1 for all levels.")
    parser.add_argument("--get-files", action="store_true", help="Retrieve files from the specified directories.")
    parser.add_argument("--get-dirs", action="store_true", help="Retrieve directories from the specified directories.")
    parser.add_argument("--include-extensions", nargs="+", help="List of file extensions to include.")
    parser.add_argument("--exclude-extensions", nargs="+", help="List of file extensions to exclude.")
    parser.add_argument("--include-directories", nargs="+", help="List of directories to include.")
    parser.add_argument("--exclude-directories", nargs="+", help="List of directories to exclude.")
    parser.add_argument("--include-strings", nargs="+", help="List of strings that the file paths must contain.")
    parser.add_argument("--exclude-strings", nargs="+", help="List of strings that the file paths must not contain.")

    args = parser.parse_args()

    handler = FileHandler()

    if args.get_files:
        files = handler.get_files(args.directories, args.full_path, args.level)
        if any([args.include_extensions, args.exclude_extensions, args.include_directories, args.exclude_directories, args.include_strings, args.exclude_strings]):
            files = handler.filter_files(files, args.include_extensions, args.exclude_extensions, args.include_directories, args.exclude_directories, args.include_strings, args.exclude_strings)
        print(f"Found {len(files)} files:")
        for file in files:
            print(file)

    if args.get_dirs:
        dirs = handler.get_dirs(args.directories, args.full_path, args.level)
        print(f"Found {len(dirs)} directories:")
        for dir in dirs:
            print(dir)


if __name__ == "__main__":
    main()