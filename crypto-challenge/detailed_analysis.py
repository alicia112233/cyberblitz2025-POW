#!/usr/bin/env python3
"""
Comprehensive forensics analysis - Extract operator information
"""

from PIL import Image
import numpy as np

def detailed_analysis():
    """Perform detailed analysis of all generated images"""
    
    print("="*70)
    print("FORENSICS ANALYSIS REPORT - Team Rainbow Breach Investigation")
    print("="*70)
    
    # Analyze XOR result (most likely to contain the message)
    print("\n[+] PRIMARY ANALYSIS: XOR Result")
    print("-"*70)
    
    xor_img = Image.open('xor_result.png')
    xor_arr = np.array(xor_img)
    
    # Check if image is mostly black (which would indicate clear text on black background)
    unique_colors = np.unique(xor_arr.reshape(-1, xor_arr.shape[2]), axis=0)
    print(f"Number of unique colors in XOR result: {len(unique_colors)}")
    
    # Calculate brightness
    brightness = np.mean(xor_arr)
    print(f"Average brightness: {brightness:.2f}/255")
    
    # Check different color channels
    print(f"\nColor channel analysis:")
    print(f"  Red channel average: {np.mean(xor_arr[:,:,0]):.2f}")
    print(f"  Green channel average: {np.mean(xor_arr[:,:,1]):.2f}")
    print(f"  Blue channel average: {np.mean(xor_arr[:,:,2]):.2f}")
    
    # Look for patterns - check if there are distinct regions
    print(f"\n[+] Image statistics:")
    print(f"  Min pixel value: {np.min(xor_arr)}")
    print(f"  Max pixel value: {np.max(xor_arr)}")
    print(f"  Standard deviation: {np.std(xor_arr):.2f}")
    
    # Convert to grayscale and enhance contrast
    print(f"\n[+] Creating enhanced versions...")
    gray = xor_img.convert('L')
    gray.save('xor_grayscale.png')
    print("  Saved: xor_grayscale.png")
    
    # Create high contrast version
    gray_arr = np.array(gray)
    threshold = 128
    binary = (gray_arr > threshold) * 255
    binary_img = Image.fromarray(binary.astype('uint8'))
    binary_img.save('xor_binary.png')
    print("  Saved: xor_binary.png")
    
    # Try inverted version
    inverted = 255 - gray_arr
    inverted_img = Image.fromarray(inverted.astype('uint8'))
    inverted_img.save('xor_inverted.png')
    print("  Saved: xor_inverted.png")
    
    print("\n[+] Analysis complete!")
    print("[*] Check the generated images for operator identification")
    print("    - xor_result.png (original XOR)")
    print("    - xor_grayscale.png (grayscale version)")
    print("    - xor_binary.png (high contrast)")
    print("    - xor_inverted.png (inverted colors)")
    print("\n" + "="*70)

if __name__ == "__main__":
    detailed_analysis()
