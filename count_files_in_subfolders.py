import os
import sys


def count_files_in_subfolders(parent_folder):
    print(f"Analyzing folder: {parent_folder}")
    # Check if the parent folder exists
    if not os.path.exists(parent_folder):
        print(f"The folder {parent_folder} does not exist.")
        return

    # Initialize a list to hold file counts for each subfolder
    file_counts = []

    # Get all entries in the parent folder sorted by name to ensure order
    entries = sorted(os.listdir(parent_folder))

    # Iterate over all sorted entities in the given parent folder
    for entry in entries:
        # Create the full path to the item
        full_path = os.path.join(parent_folder, entry)
        # Check if the item is a directory
        if os.path.isdir(full_path):
            # Count the files in this directory
            num_files = len(
                [
                    f
                    for f in os.listdir(full_path)
                    if os.path.isfile(os.path.join(full_path, f))
                ]
            )
            file_counts.append(num_files)

    print(file_counts)
    print()  # Print a newline for better readability between folder results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <folder_path1> <folder_path2> ...")
        sys.exit(1)

    # Loop over all folder paths provided as arguments
    for folder_path in sys.argv[1:]:
        count_files_in_subfolders(folder_path)
