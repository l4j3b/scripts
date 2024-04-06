#!/bin/bash
# Bash script to index all files in all folders in the current folder

for folder in */; do
    cd "$folder"
    i=1
    for file in *.{jpg,jpeg,png,JPG,webp}; do
        mv -- "$file" "${i}.jpg"
        ((i++))
    done
    cd ..
done
