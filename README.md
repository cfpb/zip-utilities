# Zip Utilities

A few zip utilities to make some maintenance tasks easier.

## compare_zips.py

This script compares two zip files and determines the difference in what files each contains
or does not contain. It outputs 5 examples at the CLI (just to give a quick visual check).

### Usage
`python compare_zips.py zip1.zip zip2.zip`

## remove_empty_folders.py

This script removes empty folders from a zip file. It overwrites the zip file in the process,
so make sure you have a backup if you need one!

### Usage
`python remove_empty_folders.py QCCA_Q22026.zip`
