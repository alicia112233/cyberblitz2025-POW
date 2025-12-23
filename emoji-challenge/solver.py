import subprocess
import regex

# All printable ASCII characters (space excluded)
CHARS = [chr(i) for i in range(33, 127)]

def run(c):
    try:
        out = subprocess.check_output(
            ["./emoji.elf", c],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return out
    except:
        return None

# Step 1: Build emoji_output -> character mapping
emoji_map = {}

for c in CHARS:
    out = run(c)
    if out:
        emoji_map[out] = c

# Sort keys by length (longest first for greedy match)
emoji_keys = sorted(emoji_map.keys(), key=len, reverse=True)

# Step 2: Decode target greedily
target = "👌😥😀😈😇🍕🍑🐼😇😥🍌😇👋"
decoded = ""
i = 0

while i < len(target):
    match = False
    for k in emoji_keys:
        if target.startswith(k, i):
            decoded += emoji_map[k]
            i += len(k)
            match = True
            break
    if not match:
        decoded += "?"
        i += 1

print("Decoded:", decoded)