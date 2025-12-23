#!/usr/bin/python3
# Extract the array values from the disassembly
values = [
    0x12, 0x15, 0x10, 0x17, 0x14, 0x11, 0x13, 0x1e, 0x1d, 0x17,
    0x10, 0x11, 0x1e, 0x10, 0x1c, 0x1b, 0x16, 0x15, 0x1b, 0x11,
    0x15, 0x10, 0x19, 0x1c, 0x10, 0x15, 0x1b, 0x11, 0x12, 0x12,
    0x1a, 0x1d, 0x12, 0x11, 0x14, 0x13, 0x19, 0x13, 0x1c, 0x1f,
    0x1a, 0x14, 0x10, 0x17, 0x12, 0x11, 0x17, 0x1d, 0x12, 0x15,
    0x1c, 0x12, 0x16, 0x15, 0x16, 0x1e, 0x11, 0x11, 0x1b, 0x11,
    0x15, 0x11, 0x19, 0x1b, 0x11, 0x11, 0x17, 0x17, 0x15, 0x15,
    0x18, 0x1f, 0x1d, 0x17, 0x14
]

print(f"Total values: {len(values)}")
print("Values:", [hex(v) for v in values])

# Based on the disassembly, traverse is called 16 times (loop compares with 0xf)
# Each iteration uses 4 characters of input

# The address calculation appears to be:
# - Take input byte
# - Shift right by (i*4) bits where i is position in 4-byte group 
# - AND with 0xf (get nibble)
# - XOR with 0x2
# - XOR with the array value at current index
# - Use in address calculation

# For alignment, the resulting address after adding 0x100 must be 16-byte aligned
# This means the calculated value before adding 0x100 must end in 0x...f0 or similar

# Let's try to find input that results in aligned addresses
import subprocess

def test_payload(payload):
    try:
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode(),
            capture_output=True,
            timeout=1,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'successfully traversed' in output:
            print(f"\n{'='*70}")
            print(f"SUCCESS! Found the flag:")
            print(f"{'='*70}")
            print(payload)
            print(output)
            return True
        return 'unaligned' not in output and 'Segmentation' not in output and 'Aborted' not in output
    except Exception as e:
        return False

# The challenge hint says "aligned" and we need 64 hex chars (16 * 4)
# Try different hex values that might create aligned pointers

# Looking at the values, they seem to be encoding something
# Let's try to decode them as characters
decoded = ''.join([chr(v + ord('0')) for v in values])
print(f"\nDecoded as chars (offset by '0'): {decoded}")

decoded2 = ''.join([chr(v + ord('A') - 0x10) for v in values])
print(f"Decoded as chars (offset by 'A' - 0x10): {decoded2}")

# Let's try these as input
payload1 = f"CyberBlitz2025{{{decoded}}}\n"
if test_payload(payload1):
    exit(0)

payload2 = f"CyberBlitz2025{{{decoded2}}}\n"
if test_payload(payload2):
    exit(0)

# Try hex representation
hex_str = ''.join([f'{v:x}' for v in values])
payload3 = f"CyberBlitz2025{{{hex_str}}}\n"
if test_payload(payload3):
    exit(0)

print(f"\nNone of the simple decoding worked. The values might need specific processing...")
