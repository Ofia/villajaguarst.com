#!/usr/bin/env python3
"""
Image optimization script for Villa Jaguar website
Optimizes all JPG images in the Pictures folder for web use
"""

import os
from PIL import Image
from pathlib import Path

# Configuration
PICTURES_DIR = Path("Pictures")
MAX_WIDTH = 1920  # Maximum width for images
MAX_HEIGHT = 1200  # Maximum height for images
QUALITY = 82  # JPEG quality (1-100, 82 is good balance)
TARGET_SIZE_KB = 300  # Target file size in KB

def optimize_image(image_path):
    """Optimize a single image"""
    try:
        # Get original size
        original_size = os.path.getsize(image_path) / 1024  # KB

        # Open image
        img = Image.open(image_path)

        # Convert RGBA to RGB if necessary
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
            img = background

        # Resize if too large (maintain aspect ratio)
        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            img.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)

        # Save optimized image
        img.save(
            image_path,
            'JPEG',
            quality=QUALITY,
            optimize=True,
            progressive=True
        )

        # Get new size
        new_size = os.path.getsize(image_path) / 1024  # KB
        reduction = ((original_size - new_size) / original_size) * 100

        print(f"[OK] {image_path.name}")
        print(f"  {original_size:.1f} KB -> {new_size:.1f} KB ({reduction:.1f}% reduction)")

        return True

    except Exception as e:
        print(f"[ERROR] Error processing {image_path.name}: {e}")
        return False

def main():
    """Main optimization function"""
    print("=" * 60)
    print("Villa Jaguar Image Optimization")
    print("=" * 60)
    print()

    # Get all JPG files
    image_files = list(PICTURES_DIR.glob("*.jpg")) + list(PICTURES_DIR.glob("*.JPG"))

    if not image_files:
        print("No images found in Pictures directory!")
        return

    print(f"Found {len(image_files)} images to optimize")
    print()

    # Process each image
    successful = 0
    total_original = 0
    total_new = 0

    for image_path in sorted(image_files):
        original_size = os.path.getsize(image_path) / 1024
        total_original += original_size

        if optimize_image(image_path):
            successful += 1
            new_size = os.path.getsize(image_path) / 1024
            total_new += new_size

        print()

    # Summary
    print("=" * 60)
    print("Optimization Complete!")
    print("=" * 60)
    print(f"Successfully optimized: {successful}/{len(image_files)} images")
    print(f"Total size reduction: {total_original:.1f} KB -> {total_new:.1f} KB")
    print(f"Space saved: {total_original - total_new:.1f} KB ({((total_original - total_new) / total_original * 100):.1f}%)")
    print()
    print("You can now commit and push these optimized images to GitHub!")

if __name__ == "__main__":
    main()
