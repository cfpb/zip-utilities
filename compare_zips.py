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

def write_diff_output( output_path, zip1_path, zip2_path, files1, files2,
        only_in_zip1, only_in_zip2, common_files):
    """Writes the full diff output to a text file."""
    with open( output_path, "w" ) as f:
        f.write("=" * 30 + "\n")
        f.write("Comparison Report\n")
        f.write(f"Zip1: {zip1_path} - {len(files1)} files\n")
        f.write(f"    {len(only_in_zip1)} files ONLY found in Zip1\n")
        f.write(f"Zip2: {zip2_path} - {len(files2)} files\n")
        f.write(f"    {len(only_in_zip2)} files ONLY found in Zip2\n")
        f.write(f"{len(common_files)} files in common\n")
        f.write("=" * 30 + "\n")

        f.write("Files ONLY in zip1:\n")
        if only_in_zip1:
            for file in only_in_zip1:
                f.write(f"   {file}\n")
        else:
            f.write("   None\n")

        f.write("Files ONLY in zip2:\n")
        if only_in_zip2:
            for file in only_in_zip2:
                f.write(f"   {file}\n")
        else:
            f.write("   None\n")        



def compare_zips(zip1_path, zip2_path, output_path=None):
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

    # Write output, when arg is present
    if (output_path):
        write_diff_output(
            output_path, zip1_path, zip2_path, files1, files2,
            only_in_zip1, only_in_zip2, common_files)
        print(f"\nFull diff output written to {output_path}")


if __name__ == "__main__":
    # Handle command line inputs using argparse
    parser = argparse.ArgumentParser(
        description="Compare unique filenames between two ZIP files, ignoring directory structures."
    )
    parser.add_argument("zip1", help="Path to the first ZIP file")
    parser.add_argument("zip2", help="Path to the second ZIP file")
    parser.add_argument("-o", "--output",
        help="Name of a text file to write a full comparison diff output file",
        default=None,
    )

    args = parser.parse_args()

    compare_zips(args.zip1, args.zip2, args.output)
