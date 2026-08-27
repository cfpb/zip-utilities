# Zip Utilities

A few zip utilities to make some maintenance tasks easier.

## compare_zips.py

This script compares two zip files and determines the difference in what files each contains
or does not contain. It outputs 5 examples at the CLI (just to give a quick visual check).

Optionally, provide a `-o` or `--output` flag with a `filename` argument to have the script
output a more comprehensive log of changes to that file.

### Usage
`python compare_zips.py example1.zip example2.zip`

`python compare_zips.py example1.zip example2.zip -o log.txt`



## remove_empty_folders.py

This script removes empty folders from a zip file. It overwrites the zip file in the process,
so make sure you have a backup if you need one!

### Usage
`python remove_empty_folders.py example.zip`
