#!/bin/bash
cd "/mnt/c/Users/User/Downloads/San Andreas Fault Line chall"

# Test single characters
for char in 0 1 2 3 4 5 6 7 8 9 A B C D E F; do
    echo "Testing: $char"
    echo "CyberBlitz2025{$char}" | timeout 1 ./san-andreas-fault-line 2>&1 | tail -3
    echo "---"
done
