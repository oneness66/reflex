import os

base_path = r"C:\Users\rampr\Desktop\Explore\reflex\.venv\Lib\site-packages\replicate"
files_to_patch = [
    "pagination.py",
    "model.py",
    "prediction.py",
    "resource.py",
    "stream.py",
    "training.py",
    "deployment.py",
    "hardware.py"
]

target_block = """try:
    from pydantic import v1 as pydantic  # type: ignore
except ImportError:
    import pydantic  # type: ignore"""

replacement = "import pydantic"

for filename in files_to_patch:
    file_path = os.path.join(base_path, filename)
    if not os.path.exists(file_path):
        print(f"Skipping {filename} (not found)")
        continue
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    if target_block in content:
        new_content = content.replace(target_block, replacement)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Patched {filename}")
    else:
        # Try a more flexible replacement if exact match fails (e.g. whitespace differences)
        # But for now just report
        print(f"Target block not found in {filename}")

print("Patching complete.")
