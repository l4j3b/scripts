import os
import argparse
from PIL import Image
import shutil


def convert_to_webp(
    input_folder, output_folder, quality, target_width=None, thumbnail_width=None
):
    input_folder = os.path.expanduser(input_folder)  # Expand the input folder path
    output_folder = os.path.expanduser(output_folder)  # Expand the output folder path

    print(f"Converting images in {input_folder} to WebP format...")

    for root, dirs, files in os.walk(input_folder):
        # Calculate the relative path to create the same structure in the output folder
        relative_path = os.path.relpath(root, input_folder)
        output_dir = os.path.join(output_folder, relative_path)
        thumbnail_dir = os.path.join(
            output_folder, "thumbnails", relative_path
        )  # Thumbnail directory
        os.makedirs(output_dir, exist_ok=True)

        # Make directory for thumbnails if thumbnail width is specified
        if thumbnail_width is not None:
            os.makedirs(thumbnail_dir, exist_ok=True)

        for file in files:
            input_file = os.path.join(root, file)
            output_file = os.path.join(output_dir, file)

            try:
                with Image.open(input_file) as img:
                    original_width, original_height = img.width, img.height

                    # Process main image without upscaling
                    if target_width is not None and original_width > target_width:
                        aspect_ratio = original_height / original_width
                        new_height = int(target_width * aspect_ratio)
                        img = img.resize(
                            (target_width, new_height), Image.Resampling.LANCZOS
                        )  # Updated for Pillow 9.0.0 and later

                    filename, _ = os.path.splitext(output_file)
                    output_file_webp = f"{filename}.webp"
                    img.save(output_file_webp, "WEBP", quality=quality)

                    # Process thumbnail without upscaling
                    if thumbnail_width is not None and original_width > thumbnail_width:
                        thumbnail_aspect_ratio = original_height / original_width
                        thumbnail_height = int(thumbnail_width * thumbnail_aspect_ratio)
                        thumbnail_img = img.resize(
                            (thumbnail_width, thumbnail_height),
                            Image.Resampling.LANCZOS,
                        )  # Updated for Pillow 9.0.0 and later
                        thumbnail_file = os.path.join(
                            thumbnail_dir,
                            f"{os.path.basename(filename)}___thumbnail.webp",
                        )
                        thumbnail_img.save(thumbnail_file, "WEBP", quality=quality)

            except IOError:
                # If the file is not an image, copy it without changes
                shutil.copy2(input_file, output_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert images to WebP format without upscaling, with optional resizing and thumbnails."
    )
    parser.add_argument(
        "--input_folder",
        type=str,
        required=True,
        help="Path to the input folder containing images",
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        required=True,
        help="Path to the output folder for WebP images and thumbnails",
    )
    parser.add_argument(
        "--quality", type=int, required=True, help="Quality of the output WebP images"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=None,
        help="Target width for the main WebP images, skip if not specified",
    )
    parser.add_argument(
        "--thumbnail_width",
        type=int,
        default=None,
        help="Width for thumbnail images (optional)",
    )

    args = parser.parse_args()

    convert_to_webp(
        args.input_folder,
        args.output_folder,
        args.quality,
        args.width,
        args.thumbnail_width,
    )
