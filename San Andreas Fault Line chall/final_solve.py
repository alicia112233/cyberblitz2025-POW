#!/usr/bin/python3
# Based on careful analysis of the disassembly, the traverse function:
# 1. Processes input 4 bytes at a time (16 iterations total = 64 bytes input)
# 2. For each 4-byte group, extracts nibbles (half-bytes) and processes them
# 3. Uses array values to calculate heap addresses
# 4. These addresses must be properly aligned for tcache

# The array from disassembly (taking first 64 values for 16 iterations * 4 bytes each)
values = [
    0x12, 0x15, 0x10, 0x17, 0x14, 0x11, 0x13, 0x1e, 0x1d, 0x17,
    0x10, 0x11, 0x1e, 0x10, 0x1c, 0x1b, 0x16, 0x15, 0x1b, 0x11,
    0x15, 0x10, 0x19, 0x1c, 0x10, 0x15, 0x1b, 0x11, 0x12, 0x12,
    0x1a, 0x1d, 0x12, 0x11, 0x14, 0x13, 0x19, 0x13, 0x1c, 0x1f,
    0x1a, 0x14, 0x10, 0x17, 0x12, 0x11, 0x17, 0x1d, 0x12, 0x15,
    0x1c, 0x12, 0x16, 0x15, 0x16, 0x1e, 0x11, 0x11, 0x1b, 0x11,
    0x15, 0x11, 0x19, 0x1b
]

print(f"Total values: {len(values)}")

# Let me try to interpret these as characters
# Looking at the pattern: values are in range 0x10-0x1f
# If we subtract 0x10, we get 0x00-0x0f (nibble range)
# These might be hex digits!

result = ''
for v in values:
    hex_digit = v - 0x10  # Convert to 0-15 range
    if hex_digit < 10:
        result += str(hex_digit)
    else:
        result += chr(ord('a') + hex_digit - 10)

print(f"Decoded as hex digits: {result}")
print(f"Length: {len(result)}")

# Test this
import subprocess
payload = f"CyberBlitz2025{{{result}}}\n"
print(f"\nTesting payload: {payload}")

try:
    proc = subprocess.run(
        ['./san-andreas-fault-line'],
        input=payload.encode(),
        capture_output=True,
        timeout=3,
        cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
    )
    output = proc.stdout.decode() + proc.stderr.decode()
    
    if 'successfully' in output.lower():
        print("\n" + "="*70)
        print("SUCCESS!")
        print("="*70)
        print(output)
    else:
        print("\nLast 300 chars of output:")
        print(output[-300:])
except Exception as e:
    print(f"Error: {e}")
