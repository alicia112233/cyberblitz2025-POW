#!/usr/bin/python3
import subprocess

# All 75 values from the disassembly
all_values = [
    0x12, 0x15, 0x10, 0x17, 0x14, 0x11, 0x13, 0x1e, 0x1d, 0x17,
    0x10, 0x11, 0x1e, 0x10, 0x1c, 0x1b, 0x16, 0x15, 0x1b, 0x11,
    0x15, 0x10, 0x19, 0x1c, 0x10, 0x15, 0x1b, 0x11, 0x12, 0x12,
    0x1a, 0x1d, 0x12, 0x11, 0x14, 0x13, 0x19, 0x13, 0x1c, 0x1f,
    0x1a, 0x14, 0x10, 0x17, 0x12, 0x11, 0x17, 0x1d, 0x12, 0x15,
    0x1c, 0x12, 0x16, 0x15, 0x16, 0x1e, 0x11, 0x11, 0x1b, 0x11,
    0x15, 0x11, 0x19, 0x1b, 0x11, 0x11, 0x17, 0x17, 0x15, 0x15,
    0x18, 0x1f, 0x1d, 0x17, 0x14
]

# Maybe we need to pair them as bytes?
# Each pair of values forms a byte
result_bytes = ''
for i in range(0, len(all_values) - 1, 2):
    high = (all_values[i] - 0x10) & 0xf
    low = (all_values[i+1] - 0x10) & 0xf
    byte_val = (high << 4) | low
    result_bytes += chr(byte_val) if 32 <= byte_val <= 126 else f'\\x{byte_val:02x}'

print(f"As byte pairs (ASCII where possible): {result_bytes}")

# Or maybe as simple hex string from pairs
hex_result = ''
for i in range(0, len(all_values) - 1, 2):
    high = (all_values[i] - 0x10) & 0xf
    low = (all_values[i+1] - 0x10) & 0xf
    byte_val = (high << 4) | low
    hex_result += f'{byte_val:02x}'

print(f"As hex string from byte pairs: {hex_result}")
print(f"Length: {len(hex_result)}")

# Test it
def test(s):
    try:
        payload = f"CyberBlitz2025{{{s}}}\n"
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode(),
            capture_output=True,
            timeout=2,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'successfully' in output.lower():
            print(f"\n{'='*70}\nSUCCESS with: {payload}\n{'='*70}")
            print(output)
            return True
        else:
            print(f"Failed for {s[:20]}...")
    except:
        pass
    return False

test(hex_result)

# Try just the direct values as hex chars
direct_hex = ''.join([f'{(v-0x10):x}' for v in all_values])
print(f"\nDirect conversion: {direct_hex}")
test(direct_hex)

# Maybe take only specific values
# Looking at the 75 values, maybe the last 11 are padding?
# 64 values = 16 iterations * 4 bytes
hex64 = ''.join([f'{(v-0x10):x}' for v in all_values[:64]])
print(f"\nFirst 64 values: {hex64}")
test(hex64)
