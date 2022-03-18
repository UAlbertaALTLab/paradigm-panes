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

STRICT_GENERATOR_FST_FILENAME = "generator-gt-norm.hfstol"