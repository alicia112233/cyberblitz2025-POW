#!/usr/bin/python3
import subprocess
import itertools

def test_input(payload):
    try:
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode(),
            capture_output=True,
            timeout=1,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        
        # Check for success
        if 'successfully traversed' in output:
            print(f"\n{'='*60}")
            print(f"FOUND IT: {payload}")
            print(f"{'='*60}")
            print(output)
            return True
        elif 'unaligned' not in output and 'Segmentation' not in output and 'Aborted' not in output:
            print(f"No crash (but no success): {payload}")
            print(output[-300:])
        return False
    except subprocess.TimeoutExpired:
        print(f"Timeout: {payload}")
        return False
    except Exception as e:
        return False

# The challenge mentions "aligned" - maybe we need specific byte values
# that create aligned addresses when processed

# Try hex values that might result in aligned pointers
print("Testing with hex-like strings...")
for val in range(0x00, 0x100, 0x10):  # Try 16-byte aligned values
    payload = f"CyberBlitz2025{{{val:02x}}}\n"
    if test_input(payload):
        exit(0)
    payload = f"CyberBlitz2025{{{val:04x}}}\n"
    if test_input(payload):
        exit(0)

print("\nTesting printable character combinations...")
chars = "0123456789abcdefABCDEF"
for length in range(1, 10):
    print(f"Length {length}...")
    for combo in itertools.product(chars, repeat=length):
        payload = "CyberBlitz2025{" + "".join(combo) + "}\n"
        if test_input(payload):
            exit(0)
