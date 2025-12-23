#!/usr/bin/python3
import subprocess
import string

def test_input(payload):
    try:
        proc = subprocess.run(
            ['./san-andreas-fault-line'],
            input=payload.encode() + b'\n',
            capture_output=True,
            timeout=1,
            cwd='/mnt/c/Users/User/Downloads/San Andreas Fault Line chall'
        )
        output = proc.stdout.decode() + proc.stderr.decode()
        if 'success' in output.lower() or 'flag' in output.lower():
            print(f"SUCCESS: {payload}")
            print(output)
            return True
        elif 'unaligned' not in output and 'Segmentation' not in output:
            print(f"INTERESTING: {payload}")
            print(output[-200:])
        return False
    except Exception as e:
        return False

# Try different lengths
for length in range(1, 20):
    print(f"\nTrying length {length}...")
    # Try all As
    payload = "CyberBlitz2025{" + "A" * length + "}"
    if test_input(payload):
        break
    
    # Try different patterns
    for char in string.printable[:62]:  # alphanumeric
        payload = "CyberBlitz2025{" + char * length + "}"
        if test_input(payload):
            break
