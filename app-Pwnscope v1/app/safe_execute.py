import sys
import builtins

blacklist = [
    'Popen', 'system', 'code', 'bash', 'interact', 'breakpoint'
]

def audit(event, args):
    for i in blacklist:
        if i in event:
            raise Exception(f"{i} is disallowed (source: {event})")

string_blacklist = [
    "import", "'", '"', "sh", "eval", "exec", "breakpoint", "open", "read", "next", "quit"
]

def string_audit(code):
    for i in string_blacklist:
        if i in code:
            raise Exception(f"forbidden char {i} used!")

safe_builtins = {
    "print": print,
    "int": int,
    "test_case": sys.argv[2]
}

safe_globals = {
    "__builtins__": safe_builtins,
}

try:
    code = sys.argv[1]
    sys.addaudithook(audit)
    string_audit(code)
    exec(code, safe_globals)
except Exception as e:
    print(e)
