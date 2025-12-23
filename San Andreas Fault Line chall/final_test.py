#!/usr/bin/python3
import subprocess
import sys

def test(payload_content):
    try:
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=f"CyberBlitz2025{{{payload_content}}}\n".encode(),
            capture_output=True,
            timeout=1,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'successfully' in output.lower():
            print(f"\n{'='*70}")
            print(f"FOUND IT!")
            print(f"CyberBlitz2025{{{payload_content}}}")
            print(f"{'='*70}\n")
            print(output)
            return True
    except:
        pass
    return False

# The base pattern from decoding
base = "2507413ed701e0cb65b1509c05b122ad214393cfa407217d25c2656e11b1519b"

# Try the base first
if test(base):
    sys.exit(0)

# Try with lowercase hex
if test(base.lower()):
    sys.exit(0)

# Try uppercase
if test(base.upper()):
    sys.exit(0)

# Maybe we need exactly the array values without transformation
values = [
    0x12, 0x15, 0x10, 0x17, 0x14, 0x11, 0x13, 0x1e, 0x1d, 0x17,
    0x10, 0x11, 0x1e, 0x10, 0x1c, 0x1b, 0x16, 0x15, 0x1b, 0x11,
    0x15, 0x10, 0x19, 0x1c, 0x10, 0x15, 0x1b, 0x11, 0x12, 0x12,
    0x1a, 0x1d, 0x12, 0x11, 0x14, 0x13, 0x19, 0x13, 0x1c, 0x1f,
    0x1a, 0x14, 0x10, 0x17, 0x12, 0x11, 0x17, 0x1d, 0x12, 0x15,
    0x1c, 0x12, 0x16, 0x15, 0x16, 0x1e, 0x11, 0x11, 0x1b, 0x11,
    0x15, 0x11, 0x19, 0x1b
]

# Try as direct hex bytes
hex_bytes = ''.join([f'{v:02x}' for v in values])
if test(hex_bytes):
    sys.exit(0)

print("None worked - this may require more sophisticated analysis or a debugger approach")
