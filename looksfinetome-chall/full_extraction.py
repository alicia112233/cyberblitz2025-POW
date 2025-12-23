from PIL import Image
import numpy as np
import re

# Load the image
img = Image.open('NEW_CYBERH4TS.png')
img_array = np.array(img)

print(f"Image shape: {img_array.shape}")
pixels = img_array.flatten()

# Reverse bit order of each pixel
print("=== Reversing bit order of each pixel ===")
reversed_pixels = []
for pixel in pixels:
    # Reverse the 8 bits of each pixel
    reversed_pixel = 0
    for bit in range(8):
        if pixel & (1 << bit):
            reversed_pixel |= (1 << (7 - bit))
    reversed_pixels.append(reversed_pixel)

reversed_pixels = np.array(reversed_pixels, dtype=np.uint8)

# Extract LSB from reversed pixels and get ALL the text
bits = reversed_pixels & 1
packed = np.packbits(bits)
data = bytes(packed)

try:
    text = data.decode('utf-8', errors='ignore')
    print(f"Total extracted text length: {len(text)} characters")
    
    # Find all unique flags
    flags = re.findall(r'CyberBlitz2025\{[^}]+\}', text)
    unique_flags = list(dict.fromkeys(flags))
    
    print(f"\nFound {len(unique_flags)} unique flags:")
    for i, flag in enumerate(unique_flags):
        if 'not_the_flag' in flag:
            print(f"  {i+1}. (DECOY) {flag}")
        else:
            print(f"  {i+1}. *** REAL FLAG: {flag}")
    
    # Show first 1000 characters
    print(f"\nFirst 1000 characters of extracted text:")
    print(text[:1000])
    
    # Show last 1000 characters
    print(f"\nLast 1000 characters of extracted text:")
    print(text[-1000:])
    
    # Search for any text between { and } that looks interesting
    all_braces = re.findall(r'\{[^\}]+\}', text)
    interesting = [b for b in all_braces if len(b) > 20 and 'CyberBlitz' not in b]
    if interesting:
        print(f"\nOther interesting brace content:")
        for item in interesting[:5]:
            print(f"  {item}")
            
except Exception as e:
    print(f"Error: {e}")

# Also try other bit positions on reversed pixels more thoroughly
print("\n\n=== Checking all bit positions on reversed pixels ===")
for bit_pos in range(8):
    bits = (reversed_pixels >> bit_pos) & 1
    packed = np.packbits(bits)
    data = bytes(packed)
    
    try:
        text = data.decode('utf-8', errors='ignore')
        flags = re.findall(r'CyberBlitz2025\{[^}]+\}', text)
        unique = list(dict.fromkeys(flags))
        
        if unique:
            print(f"\nBit position {bit_pos}: Found {len(unique)} unique flags")
            for flag in unique:
                if 'not_the_flag' not in flag:
                    print(f"  *** {flag}")
                else:
                    print(f"  (decoy: {flag[:50]}...)")
    except:
        pass