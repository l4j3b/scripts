#!/bin/bash
# Bash Scripting: index all files in the current folder with extensions jpg, jpeg, or png

i=1
for file in *.{jpg,jpeg,png,JPG}; do
  mv -- "$file" "${i}.jpg"
  ((i++))
done
