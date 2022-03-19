from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# The order in which paradigm sizes will be presented to the user.
# The first size in this list is the "default".
# Make sure to exhaustively specify all size options available!
MORPHODICT_PARADIGM_SIZES = [
    # The most user-friendly size should be first:
    "basic",
    # Then, a more complete paradigm layout:
    "full",
    # Variants for linguists go here:
]

# TODO remove default and error check if empty
STRICT_GENERATOR_FST_FILEPATH = BASE_DIR / "resources" / "fst" / "generator-gt-norm.hfstol"
LAYOUTS_DIR = BASE_DIR / "resources" / "layouts"

class FileDoesNotMatch(Exception):
    """
    Raised when file cannot be found or does not match .hfstol extension
    """

def set_fst_filepath(filepath):
    if (Path(filepath).is_file() and Path(filepath).match("*.hfstol")):
        global STRICT_GENERATOR_FST_FILEPATH
        STRICT_GENERATOR_FST_FILEPATH = filepath
    else:
        raise FileDoesNotMatch(f"file {filepath!r} does not exist or does not end in \".hfstol\".")

def get_fst_filepath():
    return STRICT_GENERATOR_FST_FILEPATH

class DirectoryDoesNotExist(Exception):
    """
    Raised when directory with paradigm layouts is missing
    """

def set_layouts_dir(dir_path):
    if (Path(dir_path).is_dir()):
        global LAYOUTS_DIR
        LAYOUTS_DIR = dir_path
    else:
        raise DirectoryDoesNotExist(f"Directory {dir_path!r} does not exist.")

def get_layouts_dir():
    return LAYOUTS_DIR