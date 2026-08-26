# import zipfile
# import os

# def get_filenames(zip_path):
#     with zipfile.ZipFile(zip_path, 'r') as zf:
#         # Get list of all items and strip folder paths
#         return {os.path.basename(name) for name in zf.namelist() if not name.endswith('/')}

# def compare_zips(zip1, zip2):
#     files1 = get_filenames(zip1)
#     files2 = get_filenames(zip2)
    
#     unique_to_1 = files1 - files2
#     unique_to_2 = files2 - files1
#     common = files1 & files2

#     print(f"Files only in {zip1}: {unique_to_1}")
#     print(f"Files only in {zip2}: {unique_to_2}")
#     print(f"Files in both: {common}")

# Replace with your actual file paths
#compare_zips('2025_Q4.zip', '2026_Q1.zip')

import argparse
import os
from zipfile import ZipFile
from pathlib import Path


def get_files(zip_path):
    filenames = set()
    with ZipFile(zip_path, "r") as archive:
        for info in archive.infolist():
            # Skip entries that are directories
            if not info.is_dir():
                # get containing directory plus filename for comparison
                # (sometimes there are extra root folders, and we ignore them)
                path_obj = Path(info.filename)
                name = path_obj.name
                parent_folder = path_obj.parent.name
                fullname = parent_folder + "/" + name

                # Don't add empty strings
                if fullname:
                    filenames.add(fullname)
    return filenames


def compare_zips(zip1_path, zip2_path):
    """Compares unique filenames between two zip archives."""
    # Check if files exist
    if not os.path.exists(zip1_path):
        print(f"Error: File not found -> {zip1_path}")
        return
    if not os.path.exists(zip2_path):
        print(f"Error: File not found -> {zip2_path}")
        return

    # Extract clean sets of filenames
    files1 = get_files(zip1_path)
    files2 = get_files(zip2_path)

    # Perform set operations to find differences and matches
    only_in_zip1 = sorted(files1 - files2)
    only_in_zip2 = sorted(files2 - files1)
    common_files = sorted(files1 & files2)

    # Print Report Results
    print("=" * 60)
    print(f"Comparison Report")
    print(f"ZIP 1: {zip1_path} ({len(files1)} unique files)")
    print(f"ZIP 2: {zip2_path} ({len(files2)} unique files)")
    print("=" * 60)

    print(f"\n>> Common files in both archives = {len(common_files)}")

    print(f"\n>> Files ONLY in ZIP 1 = {len(only_in_zip1)} (Showing up to 5):")
    if only_in_zip1:
        for f in only_in_zip1[:5]:
            print(f"  {f}")
    else:
        print("  None")

    print(f"\n>> Files ONLY in ZIP 2 = {len(only_in_zip2)} (Showing up to 5):")
    if only_in_zip2:
        for f in only_in_zip2[:5]:
            print(f"  {f}")
    else:
        print("  None")


if __name__ == "__main__":
    # Handle command line inputs using argparse
    parser = argparse.ArgumentParser(
        description="Compare unique filenames between two ZIP files, ignoring directory structures."
    )
    parser.add_argument("zip1", help="Path to the first ZIP file")
    parser.add_argument("zip2", help="Path to the second ZIP file")

    args = parser.parse_args()

    compare_zips(args.zip1, args.zip2)
