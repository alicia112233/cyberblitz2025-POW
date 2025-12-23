#!/usr/bin/env python3
"""
Forensics analysis script for crypto challenge
Analyzes two encrypted PNG files to extract hidden information
"""

from PIL import Image
import numpy as np

def analyze_images():
    """Analyze and extract information from the two encrypted images"""
    
    # Load both images
    print("[+] Loading images...")
    img1 = Image.open('crypted1.png')
    img2 = Image.open('crypted2.png')
    
    print(f"Image 1 size: {img1.size}, mode: {img1.mode}")
    print(f"Image 2 size: {img2.size}, mode: {img2.mode}")
    
    # Convert to numpy arrays for easier manipulation
    arr1 = np.array(img1)
    arr2 = np.array(img2)
    
    print(f"Array 1 shape: {arr1.shape}")
    print(f"Array 2 shape: {arr2.shape}")
    
    # XOR the two images together
    print("\n[+] XORing images together...")
    xor_result = np.bitwise_xor(arr1, arr2)
    
    # Create image from XOR result
    result_img = Image.fromarray(xor_result.astype('uint8'))
    result_img.save('xor_result.png')
    print("[+] Saved XOR result to xor_result.png")
    
    # Try AND operation
    print("\n[+] Trying AND operation...")
    and_result = np.bitwise_and(arr1, arr2)
    and_img = Image.fromarray(and_result.astype('uint8'))
    and_img.save('and_result.png')
    print("[+] Saved AND result to and_result.png")
    
    # Try OR operation
    print("\n[+] Trying OR operation...")
    or_result = np.bitwise_or(arr1, arr2)
    or_img = Image.fromarray(or_result.astype('uint8'))
    or_img.save('or_result.png')
    print("[+] Saved OR result to or_result.png")
    
    # Check for differences
    print("\n[+] Analyzing differences...")
    diff = np.abs(arr1.astype(int) - arr2.astype(int))
    print(f"Number of different pixels: {np.count_nonzero(diff)}")
    print(f"Max difference: {np.max(diff)}")
    
    # Save difference image
    diff_img = Image.fromarray((diff * 255 // np.max(diff)).astype('uint8'))
    diff_img.save('diff_result.png')
    print("[+] Saved difference image to diff_result.png")
    
    print("\n[+] Analysis complete! Check the generated images.")

if __name__ == "__main__":
    analyze_images()
