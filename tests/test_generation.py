"""
Integration tests for paradigms in the itwêwina (crkeng) dictionary.
"""

from pathlib import Path

from paradigm_panes import settings
from paradigm_panes import generation
from paradigm_panes.manager import ParadigmManagerWithExplicitSizes

BASE_DIR = Path(__file__).resolve().parent

def test_default_paradigm_fails_with_empty_fst():
    """
    Generation does not run without first setting FST and throws appropriate error message
    """
    try:
        generation.default_paradigm_manager()
        assert False
    except Exception as e:
        if (str(e) == "Transducer not found in \"\""):
            assert True
        else:
            assert False

def test_default_paradigm_fails_with_invalid_fst():
    """
    Generation does not run with invalid FST and throws appropriate error message
    """
    fst_path = BASE_DIR / "test_resources" / "fst" / "tottaly_missing_fst.hfstol"
    try:
        settings.set_fst_filepath(fst_path)
        generation.default_paradigm_manager()
        assert False
    except settings.FileDoesNotMatch as e:
        assert True
        if (str(e) == f'file \'{fst_path}\' does not exist or does not end in \".hfstol\".'):
            assert True
        else:
            assert False
    except Exception as e:
        assert False

def test_default_paradigm_with_fst():
    """
    Generation runs with valid FST and returns Paradigm manager
    """
    fst_path = BASE_DIR / "test_resources" / "fst" / "crk-strict-generator.hfstol"
    try:
        settings.set_fst_filepath(fst_path)
        paradigm_manager = generation.default_paradigm_manager()
        assert isinstance(paradigm_manager, ParadigmManagerWithExplicitSizes)
        assert True
    except Exception as e:
        assert False