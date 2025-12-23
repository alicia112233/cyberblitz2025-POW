#!/usr/bin/python3
import subprocess

values = [
    0x12, 0x15, 0x10, 0x17, 0x14, 0x11, 0x13, 0x1e, 0x1d, 0x17,
    0x10, 0x11, 0x1e, 0x10, 0x1c, 0x1b, 0x16, 0x15, 0x1b, 0x11,
    0x15, 0x10, 0x19, 0x1c, 0x10, 0x15, 0x1b, 0x11, 0x12, 0x12,
    0x1a, 0x1d, 0x12, 0x11, 0x14, 0x13, 0x19, 0x13, 0x1c, 0x1f,
    0x1a, 0x14, 0x10, 0x17, 0x12, 0x11, 0x17, 0x1d, 0x12, 0x15,
    0x1c, 0x12, 0x16, 0x15, 0x16, 0x1e, 0x11, 0x11, 0x1b, 0x11,
    0x15, 0x11, 0x19, 0x1b
]

# From disassembly: nibble is extracted, then:
# edx = (nibble >> (i*4)) & 0xf  (extract nibble based on position)
# eax = edx ^ 0x2                (XOR with 2)
# ecx = eax                      
# then XOR'd with array value

# To reverse: input_nibble = (desired_result ^ array_value) ^ 0x2

# For proper alignment, try making all results = 0
input_hex = ''
for v in values:
    # To get result 0: nibble = (0 ^ v) ^ 0x2 = v ^ 0x2
    nibble = v ^ 0x2
    input_hex += f'{nibble&0xf:x}'

print(f"Input for all-zero results: {input_hex}")

def test(s):
    try:
        payload = f"CyberBlitz2025{{{s}}}\n"
        print(f"Testing: {payload[:50]}...")
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode(),
            capture_output=True,
            timeout=3,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'successfully' in output.lower():
            print(f"\n{'='*70}\nSUCCESS!\n{'='*70}")
            print(payload)
            print(output)
            return True
        else:
            last_lines = output.split('\n')[-10:]
            print("Last lines:", '\n'.join(last_lines))
    except Exception as e:
        print(f"Exception: {e}")
    return False

if not test(input_hex):
    # Try other target values
    # Maybe all 0xf?
    input_hex2 = ''
    for v in values:
        nibble = (0xf ^ v) ^ 0x2
        input_hex2 += f'{nibble&0xf:x}'
    print(f"\nTrying for all-0xf results: {input_hex2}")
    test(input_hex2)
