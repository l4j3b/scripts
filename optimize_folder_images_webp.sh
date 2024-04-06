# Desc: Optimize images in the current directory using cwebp
# Usage: ./optimize_folder_images_webp.sh <resize_width>

# Note: width 330 for art0

#!/bin/bash

# Check if an argument is provided
if [ $# -eq 0 ]; then
  echo "Usage: $0 <resize_width>"
  exit 1
fi

# Assign the first argument to a variable
resize_width=$1

# Desc: Optimize images in a directory using cwebp
for dir in */; do
  cd "$dir"

  # Process JPG and PNG files
  for file in *.jpg *.png *.webp; do
    extension="${file##*.}"
    cwebp -resize "$resize_width" 0 "$file" -o "${file%.$extension}.webp"
  done

  cd ..
done
