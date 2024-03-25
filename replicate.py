import argparse
import os
import shutil

def copy_files(src_folder, dest_folder):
    for file in os.listdir(src_folder):
        src_file = os.path.join(src_folder, file)
        dest_file = os.path.join(dest_folder, file)

        # Copy if source doesn't exist in the destination
        if os.path.exists(dest_file): continue

        shutil.copy2(src_file, dest_folder)
        print(f"Copied {src_file} to {dest_folder}")

def remove_files(src_folder, dest_folder):
    for file in os.listdir(dest_folder):
        file_path = os.path.join(dest_folder, file)

        if os.path.exists(os.path.join(src_folder, file)): continue
        if not os.path.isfile(file_path): continue

        os.remove(file_path)
        print(f"Deleted {file_path}")


def replicate(src_folder, dest_folder, remove_only=False, copy_only=False):
    # Ensure destination folder exists, create if it doesn't
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # Copy new and updated files
    if not remove_only:
        copy_files(src_folder, dest_folder)

    # Delete extra files in the destination folder
    if not copy_only:
        remove_files(src_folder, dest_folder)

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("src", help="Source folder")
    parser.add_argument("dest", help="Destination folder")

    parser.add_argument("-r", "--remove-only", action="store_true", help="Remove files only")
    parser.add_argument("-c", "--copy-only", action="store_true", help="Copy files only")

    args = parser.parse_args()

    replicate(args.src, args.dest, args.remove_only, args.copy_only)
