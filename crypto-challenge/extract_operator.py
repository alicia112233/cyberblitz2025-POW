#!/usr/bin/env python3
"""
Text extraction and operator identification
"""

from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

def extract_operator_info():
    """Extract operator names from the decrypted image"""
    
    print("="*70)
    print("OPERATOR IDENTIFICATION SYSTEM")
    print("="*70)
    
    # Load the XOR result
    xor_img = Image.open('xor_result.png')
    
    # Try different enhancement techniques
    print("\n[+] Applying image enhancement techniques...\n")
    
    # 1. Increase contrast
    enhancer = ImageEnhance.Contrast(xor_img)
    high_contrast = enhancer.enhance(3.0)
    high_contrast.save('enhanced_contrast.png')
    print("  Created: enhanced_contrast.png (3x contrast)")
    
    # 2. Increase brightness
    enhancer = ImageEnhance.Brightness(xor_img)
    bright = enhancer.enhance(2.0)
    bright.save('enhanced_brightness.png')
    print("  Created: enhanced_brightness.png (2x brightness)")
    
    # 3. Sharpen
    sharpened = xor_img.filter(ImageFilter.SHARPEN)
    sharpened.save('enhanced_sharp.png')
    print("  Created: enhanced_sharp.png (sharpened)")
    
    # 4. Edge detection
    edges = xor_img.filter(ImageFilter.FIND_EDGES)
    edges.save('enhanced_edges.png')
    print("  Created: enhanced_edges.png (edge detection)")
    
    # 5. Extreme contrast on grayscale
    gray = xor_img.convert('L')
    gray_arr = np.array(gray)
    
    # Auto-threshold using Otsu's method approximation
    hist, bins = np.histogram(gray_arr.flatten(), 256, [0, 256])
    total_pixels = gray_arr.size
    
    # Find optimal threshold
    sum_total = np.sum(np.arange(256) * hist)
    sum_background = 0
    weight_background = 0
    max_variance = 0
    threshold = 0
    
    for t in range(256):
        weight_background += hist[t]
        if weight_background == 0:
            continue
        weight_foreground = total_pixels - weight_background
        if weight_foreground == 0:
            break
        
        sum_background += t * hist[t]
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        
        variance = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
        
        if variance > max_variance:
            max_variance = variance
            threshold = t
    
    print(f"\n[+] Optimal threshold calculated: {threshold}")
    
    # Apply optimal threshold
    binary_optimal = (gray_arr > threshold) * 255
    binary_img = Image.fromarray(binary_optimal.astype('uint8'))
    binary_img.save('enhanced_optimal_threshold.png')
    print(f"  Created: enhanced_optimal_threshold.png (threshold={threshold})")
    
    # Try multiple thresholds
    for thresh in [50, 100, 150, 200]:
        binary = (gray_arr > thresh) * 255
        img = Image.fromarray(binary.astype('uint8'))
        img.save(f'threshold_{thresh}.png')
        print(f"  Created: threshold_{thresh}.png")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\nGenerated files for operator identification:")
    print("  1. enhanced_contrast.png")
    print("  2. enhanced_brightness.png")
    print("  3. enhanced_sharp.png")
    print("  4. enhanced_edges.png")
    print("  5. enhanced_optimal_threshold.png")
    print("  6. threshold_50.png, threshold_100.png, threshold_150.png, threshold_200.png")
    print("\nOpen these files to identify the operator(s) responsible for the breach.")
    print("="*70)

if __name__ == "__main__":
    extract_operator_info()
