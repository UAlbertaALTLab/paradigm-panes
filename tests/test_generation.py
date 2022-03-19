"""
Integration tests for paradigms in the itwêwina (crkeng) dictionary.
"""

from pathlib import Path

import pytest
from more_itertools import first, ilen

from paradigm_panes import settings
from paradigm_panes import generation
from paradigm_panes.manager import (
    ParadigmManager,
    ParadigmManagerWithExplicitSizes,
    Transducer,
)
BASE_DIR = Path(__file__).resolve().parent

def test_default_paradigm_fails_with_empty_fst():
    try:
        generation.default_paradigm_manager()
        assert False
    except Exception as e:
        print(str(e))
        if (str(e) == "Transducer not found in \"\""):
            assert True
        else:
            assert False

def test_default_paradigm_fails_with_invalid_fst():
    fst_path = BASE_DIR / "test_resources" / "fst" / "tottaly_missing_fst.hfstol"
    try:
        settings.set_fst_filepath(fst_path)
        generation.default_paradigm_manager()
        assert False
    except settings.FileDoesNotMatch as e:
        assert True
        print("file '{fst_path}' does not exist or does not end in \".hfstol\".")
        if (str(e) == f'file \'{fst_path}\' does not exist or does not end in \".hfstol\".'):
            assert True
        else:
            assert False
    except Exception as e:
        assert False

def test_default_paradigm_with_fst():
    fst_path = BASE_DIR / "test_resources" / "fst" / "crk-strict-generator.hfstol"
    try:
        settings.set_fst_filepath(fst_path)
        pm = generation.default_paradigm_manager()
        assert type(pm) == ParadigmManagerWithExplicitSizes
        assert True
    except Exception as e:
        assert False



# @pytest.fixture
# def paradigm_manager() -> ParadigmManager:
#     settings.set_layouts_dir(BASE_DIR / "test_resources" / "layouts")

#     return default_paradigm_manager()