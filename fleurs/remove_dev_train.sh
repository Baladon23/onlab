#!/bin/bash

# function to delete files and folder
function delete_files_and_folder {
    find "$1" -type f \( -iname "dev.tsv" -o -iname "train.tsv" \) -delete
    find "$1" -name "audio" -type d -exec bash -c 'rm -r "$0/dev" "$0/train"' {} \;
}

# Verify that the input (folder path) is supplied
if [ -z "$1" ]; then
    echo "Please provide the directory as argument!"
    exit 1
fi

# Check if the provided input is actually a directory
if [ ! -d "$1" ]; then
    echo "$1 is not a directory!"
    exit 1
fi

# loop over all the subdirectories
for dir in "$1"/*; do
    if [ -d "$dir" ]; then
        delete_files_and_folder "$dir"
    fi
done

echo "Deletion done!"
exit 0
