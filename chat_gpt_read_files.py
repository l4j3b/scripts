import sys
import os
import pyperclip

EXCLUDE_DIRS = {
    "__pycache__",
    "node_modules",
    ".vercel",
    "public",
    "build",
    ".cache",
    ".env",
}  # Set of default excluded directories

CODE_EXTENSIONS = {
    ".py",
    ".js",
    ".html",
    ".css",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".sh",
    ".php",
    ".rb",
    ".go",
    ".tsx",
    ".jsx",
    ".ts",
    ".yml",
    ".yaml",
    ".xml",
    ".md",
    ".txt",
    ".gitignore",
    ".editorconfig",
    ".babelrc",
    ".eslintrc",
    ".prettierignore",
    ".cjs",
    ".scss",
    ".sass",
    ".less",
    ".prettierrc",
}  # Expand this set as needed


def add_files_from_folder(folder_path, file_set, excluded_dirs):
    for root, dirs, files in os.walk(folder_path, topdown=True):
        dirs[:] = [
            d for d in dirs if d not in excluded_dirs
        ]  # Modify dirs in-place to exclude unwanted dirs
        for file in files:
            if (
                os.path.splitext(file)[1] in CODE_EXTENSIONS
            ):  # Check if the file extension is in the list of code extensions
                file_path = os.path.join(root, file)
                file_set.add(file_path)


def read_gitignore():
    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    excluded_dirs = EXCLUDE_DIRS.copy()
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as gitignore_file:
            for line in gitignore_file:
                cleaned_line = line.strip()
                if cleaned_line and not cleaned_line.startswith("#"):
                    excluded_dirs.add(cleaned_line)
    return excluded_dirs


def read_and_write_files(file_list):
    output_content = "\n\n"
    file_set = set()
    excluded_dirs = read_gitignore()

    for item in file_list:
        if os.path.isdir(item):
            add_files_from_folder(item, file_set, excluded_dirs)
        elif os.path.isfile(item) and os.path.splitext(item)[1] in CODE_EXTENSIONS:
            file_set.add(item)
        else:
            print(f"Invalid path or non-code file: {item}")

    for file_name in file_set:
        try:
            with open(file_name, "r") as infile:
                content = infile.read()
                output_content += f"<{file_name}>\n\n{content}\n\n"
        except FileNotFoundError:
            print(f"File not found: {file_name}")
        except Exception as e:
            print(f"Error reading file {file_name}: {e}")

    # Copy content to clipboard
    pyperclip.copy(output_content)
    print("Content copied to clipboard.")


def main():
    # Command line arguments, excluding the script name
    files_to_process = sys.argv[1:]

    # Process the files
    read_and_write_files(files_to_process)


if __name__ == "__main__":
    main()
