#!/usr/bin/env python3
import argparse
import os
import tempfile
import zipfile

def remove_empty_folders(zip_path):
    if not os.path.exists(zip_path):
        print(f"Error: File '{zip_path}' does not exist.")
        return

    # Temporary file to write the cleaned zip contents
    temp_fd, temp_path = tempfile.mkstemp()
    
    try:
        with zipfile.ZipFile(zip_path, 'r') as src, zipfile.ZipFile(temp_path, 'w', src.compression) as dst:
            # Track which folders contain actual files
            non_empty_folders = set()
            all_items = src.namelist()

            # Pass 1: Identify folders that contain files or sub-items
            for item in all_items:
                if not item.endswith('/'):  # It's a file
                    # Add all parent directory paths to the non-empty set
                    parts = item.split('/')
                    for i in range(1, len(parts)):
                        parent = '/'.join(parts[:i]) + '/'
                        non_empty_folders.add(parent)

            # Pass 2: Rebuild the ZIP, skipping empty folders
            removed_count = 0
            for item in all_items:
                if item.endswith('/'):
                    # Skip if the folder is completely empty
                    if item not in non_empty_folders:
                        removed_count += 1
                        continue
                
                # Copy the file or valid non-empty folder structure
                dst.writestr(item, src.read(item))
                
        # Replace the original archive safely
        os.close(temp_fd)
        os.replace(temp_path, zip_path)
        print(f"Success! Removed {removed_count} empty folder(s) from '{zip_path}'.")

    except Exception as e:
        print(f"An error occurred: {e}")
        if os.path.exists(temp_path):
            os.unlink(temp_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove empty directories from a ZIP archive.")
    parser.add_argument("zip_file", help="Path to the target ZIP file.")
    args = parser.parse_args()
    
    remove_empty_folders(args.zip_file)