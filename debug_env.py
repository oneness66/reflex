import sys
import os

print(f"Executable: {sys.executable}")
print("Sys Path:")
for p in sys.path:
    print(p)

try:
    import replicate
    print(f"Replicate file: {replicate.__file__}")
except ImportError:
    print("Replicate not found")
