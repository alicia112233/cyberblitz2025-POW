#!/bin/bash
cd "/mnt/c/Users/User/Downloads/San Andreas Fault Line chall"

# Use GDB to break at the malloc call and see what address is being requested
cat > gdb_script.txt << 'EOF'
break *0x555555555285
run
print/x $rax
continue
print/x $rax
continue
print/x $rax
continue
print/x $rax
quit
EOF

echo "CyberBlitz2025{0000}" | gdb -batch -x gdb_script.txt ./san-andreas-fault-line 2>&1 | grep -E "(rax|0x)"
