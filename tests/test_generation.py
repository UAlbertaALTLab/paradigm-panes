"""
Integration tests for paradigms in the itwêwina (crkeng) dictionary.
"""

from pathlib import Path

from paradigm_manager.manager import ParadigmManager, LayoutDirectoryNotValidError, LayoutDirectoryNotProvidedError, FstNotValidError, FstFileNotProvidedError
from tests.test_resources.serialized_response import amisk_serialized

BASE_DIR = Path(__file__).resolve().parent

FST = BASE_DIR / "test_resources/fst/generator-gt-dict-norm-no-bound.hfstol"
LAYOUTS = BASE_DIR / "test_resources/layouts"

def test_default_paradigm_fails_with_empty_layout_dir():
    """
    Generation does not run without first setting FST and throws appropriate error message
    """
    try:
        pm = ParadigmManager(layout_directory="", generation_fst=FST)
    except Exception as e:
        assert (e.__class__ == LayoutDirectoryNotProvidedError)


def test_default_paradigm_fails_with_empty_fst_path():
    """
    Generation does not run without first setting FST and throws appropriate error message
    """
    try:
        pm = ParadigmManager(layout_directory=LAYOUTS, generation_fst="")
    except Exception as e:
        assert (e.__class__ == FstFileNotProvidedError)


def test_default_paradigm_fails_with_invalid_layout_dir():
    """
    Generation does not run without first setting FST and throws appropriate error message
    """
    try:
        pm = ParadigmManager(layout_directory="/", generation_fst=FST)
    except Exception as e:
        assert (e.__class__ == LayoutDirectoryNotValidError)


def test_default_paradigm_fails_with_invalid_fst():
    """
    Generation does not run without first setting FST and throws appropriate error message
    """
    try:
        pm = ParadigmManager(layout_directory=LAYOUTS, generation_fst="/")
    except Exception as e:
        assert (e.__class__ == FstNotValidError)


def test_paradigm_generation_succeeds():
    pm = ParadigmManager(layout_directory=Path(LAYOUTS), generation_fst=FST)
    pm.set_lemma("amisk")
    pm.set_paradigm("NA")

    paradigm = pm.generate()
    assert (paradigm == amisk_serialized())
