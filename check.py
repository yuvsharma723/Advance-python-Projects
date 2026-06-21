import sys

print("stdout =", sys.stdout.encoding)
print("stdin  =", sys.stdin.encoding)

s = "क्षेत्रफल"
print(s)
print(repr(s))

print([hex(ord(c)) for c in s])














