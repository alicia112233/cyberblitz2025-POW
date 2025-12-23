#!/usr/bin/python3
import subprocess
import struct

# All the 16-bit values from the disassembly
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

def test_payload(payload):
    try:
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode(),
            capture_output=True,
            timeout=2,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'successfully traversed' in output or 'submit the flag' in output:
            print(f"\n{'='*70}")
            print(f"SUCCESS! Found the flag:")
            print(f"{'='*70}")
            print(payload)
            print('\n' + output)
            return True
        return False
    except Exception as e:
        return False

# The loop runs 16 times (0-15), and each iteration processes 4 bytes
# So we need 64 bytes total. But we have 75 values - maybe some are padding?

# Let me try interpreting the values differently
# In the traverse function, nibbles are extracted and XORed with 0x2, then XORed with array values

# If we reverse this: to get a properly aligned address, we might need specific nibbles
# Let's try to construct input where each nibble XOR 0x2 equals the array value

# For 16 iterations with 4 bytes each = 64 bytes = 128 nibbles
# But we have 75 values. Let's use the first 64 (16*4)

input_bytes = []
for i in range(64):
    if i < len(values):
        # Reverse the XOR: nibble = (value ^ 0x2)
        nibble = values[i] ^ 0x2
        input_bytes.append(nibble)
    else:
        input_bytes.append(0)

# Pack nibbles into bytes
input_str = ''
for i in range(0, len(input_bytes), 2):
    byte = (input_bytes[i] << 4) | input_bytes[i+1]
    # Convert to hex character representation
    input_str += f'{byte:02x}'

print(f"Constructed input (hex): {input_str}")
print(f"Length: {len(input_str)}")

payload = f"CyberBlitz2025{{{input_str}}}\n"
if test_payload(payload):
    exit(0)

# Maybe we need to use the values as-is as hex chars
input_str2 = ''.join([f'{v:x}' for v in values[:64]])
print(f"\nTrying direct hex representation: {input_str2}")
payload2 = f"CyberBlitz2025{{{input_str2}}}\n"
if test_payload(payload2):
    exit(0)

# Or maybe ASCII representation of hex values
input_str3 = ''
for v in values[:64]:
    input_str3 += chr(ord('0') + (v & 0xf)) if (v & 0xf) < 10 else chr(ord('a') + (v & 0xf) - 10)

print(f"\nTrying ASCII representation: {input_str3}")
payload3 = f"CyberBlitz2025{{{input_str3}}}\n"
if test_payload(payload3):
    exit(0)

print("\nStill not finding it...")
