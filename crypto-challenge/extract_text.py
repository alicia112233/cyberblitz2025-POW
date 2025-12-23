#!/usr/bin/env python3
"""
Further analysis to extract any text or metadata from the images
"""

from PIL import Image
import pytesseract
import os

def extract_text_from_images():
    """Extract any visible text from the generated images"""
    
    image_files = ['xor_result.png', 'and_result.png', 'or_result.png', 'diff_result.png']
    
    for img_file in image_files:
        if os.path.exists(img_file):
            print(f"\n{'='*60}")
            print(f"Analyzing: {img_file}")
            print('='*60)
            
            img = Image.open(img_file)
            
            # Try to extract text using OCR
            try:
                text = pytesseract.image_to_string(img)
                if text.strip():
                    print(f"\n[+] Text found in {img_file}:")
                    print(text)
                else:
                    print(f"[*] No text detected in {img_file}")
            except Exception as e:
                print(f"[-] OCR failed for {img_file}: {e}")
            
            # Show basic image info
            print(f"\nImage info:")
            print(f"  Size: {img.size}")
            print(f"  Mode: {img.mode}")
            print(f"  Format: {img.format}")

if __name__ == "__main__":
    extract_text_from_images()
