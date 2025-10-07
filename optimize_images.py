#!/usr/bin/env python3
"""
Image optimization script for portfolio website
Optimizes images for web performance
"""

import os
import sys

try:
    from PIL import Image, ImageOps
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available. Install with: pip install Pillow")

def optimize_image(input_path, output_path, quality=85, max_width=1920):
    """
    Optimize an image for web use
    """
    if not PIL_AVAILABLE:
        print("PIL/Pillow required for image optimization")
        return
        
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Auto-orient based on EXIF data
            img = ImageOps.exif_transpose(img)
            
            # Resize if too large
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            
            # Save optimized image
            img.save(output_path, 'JPEG', quality=quality, optimize=True, progressive=True)
            
            original_size = os.path.getsize(input_path)
            new_size = os.path.getsize(output_path)
            savings = ((original_size - new_size) / original_size) * 100
            
            print(f"Optimized {os.path.basename(input_path)}: {savings:.1f}% reduction")
            
    except Exception as e:
        print(f"Error optimizing {input_path}: {str(e)}")

def create_placeholder_images():
    """
    Create placeholder images for the portfolio
    """
    if not PIL_AVAILABLE:
        print("Creating placeholder images requires PIL/Pillow")
        return
        
    static_dir = os.path.join(os.path.dirname(__file__), 'static', 'images')
    os.makedirs(static_dir, exist_ok=True)
    
    # Create placeholder images for SEO
    placeholder_configs = [
        {'name': 'og-image.jpg', 'size': (1200, 630), 'color': '#007bff'},
        {'name': 'twitter-card.jpg', 'size': (1200, 675), 'color': '#007bff'},
        {'name': 'favicon-32x32.png', 'size': (32, 32), 'color': '#007bff'},
        {'name': 'favicon-16x16.png', 'size': (16, 16), 'color': '#007bff'},
        {'name': 'apple-touch-icon.png', 'size': (180, 180), 'color': '#007bff'},
    ]
    
    for config in placeholder_configs:
        try:
            img = Image.new('RGB', config['size'], config['color'])
            file_path = os.path.join(static_dir, config['name'])
            
            if config['name'].endswith('.png'):
                img.save(file_path, 'PNG', optimize=True)
            else:
                img.save(file_path, 'JPEG', quality=90, optimize=True)
                
            print(f"Created {config['name']}")
            
        except Exception as e:
            print(f"Error creating {config['name']}: {str(e)}")

if __name__ == '__main__':
    print("Creating placeholder images for SEO...")
    create_placeholder_images()
    print("Image optimization complete!")