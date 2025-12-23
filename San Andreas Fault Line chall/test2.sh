#!/bin/bash
cd "/mnt/c/Users/User/Downloads/San Andreas Fault Line chall"

# Test with gdb to see what's happening
echo "CyberBlitz2025{A}" | gdb -batch -ex "run" -ex "bt" ./san-andreas-fault-line 2>&1 | tail -30
