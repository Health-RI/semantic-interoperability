import os
import fnmatch
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

# Base directory: parent of this script's folder
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Patterns to delete everywhere except .bat (which has special rule)
file_patterns_to_remove = [
    '*vpp.bak*',
    '*vpp.lck*',
    '~$*',
    '*.tmp',
    '*.bak',
    '*.wbk',
    '*.asd',
    '*.lnk',
    '*.lock',
    '*.log',
    '*.ds_store',
    '*.sln.docstates',
    'Thumbs.db',
    'diff.path',
    '*.del',
    'catalog-v*.xml'
]

def is_bat_in_scripts_folder(file_path):
    """
    Checks whether a .bat file is located within the 'scripts' subdirectory,
    in which case it should be preserved.

    Args:
        file_path (str): Full path to the file.

    Returns:
        bool: True if the file is a .bat inside 'scripts', False otherwise.
    """
    rel_path = os.path.relpath(file_path, base_dir)
    parts = rel_path.replace("\\", "/").split('/')
    return 'scripts' in parts and rel_path.lower().endswith('.bat')


def should_delete(file_path, filename):
    """
    Determines whether a file should be deleted based on predefined patterns.
    Special case: .bat files are preserved if under the 'scripts' folder.

    Args:
        file_path (str): Full path to the file.
        filename (str): File name only.

    Returns:
        bool: True if the file should be deleted, False otherwise.
    """
    if filename.lower().endswith('.bat'):
        return not is_bat_in_scripts_folder(file_path)
    
    for pattern in file_patterns_to_remove:
        if fnmatch.fnmatch(filename, pattern):
            return True
    return False


# Walk through directory tree and remove matching files
deleted_count = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        file_path = os.path.join(root, file)
        if should_delete(file_path, file):
            try:
                os.remove(file_path)
                deleted_count += 1
                logging.info(f"Deleted: {file_path}")
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {e}")

logging.info(f"\nTotal files deleted: {deleted_count}")
