import os

# Set the directory you want to clean up (current dir in this case)
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Substrings to look for in filenames
substrings_to_remove = ['.vpp.bak', '.vpp.lck']

# Walk through the directory tree
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if any(substr in file for substr in substrings_to_remove):
            file_path = os.path.join(root, file)
            try:
                os.remove(file_path)
                print(f"Deleted: {file_path}")
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")
