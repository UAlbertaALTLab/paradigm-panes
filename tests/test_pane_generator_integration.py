"""
Integration tests for paradigms in the itwêwina (crkeng) dictionary.
"""

from pathlib import Path

import pytest

import paradigm_panes

BASE_DIR = Path(__file__).resolve().parent

def test_paradigm_gen_setup(pardigm_gen: paradigm_panes.PaneGenerator):
    """
    Checks setup is correct and local imports (from paradigm_panes.init) work correctly
    """
    assert isinstance(pardigm_gen, paradigm_panes.PaneGenerator)
    assert paradigm_panes.settings.is_setup_complete()


@pytest.mark.parametrize(
    ("name", "lemma", "examples"),
    [
        ("VTA", "wâpamêw", ["wâpamêw", "niwâpamâw", "kiwâpamitin", "ê-wâpamât"]),
        ("VAI", "nipâw", ["nipâw", "ninipân", "kinipân", "ninipânân"]),
        ("VTI", "mîciw", ["mîciw", "nimîcin", "kimîcin", "kimîcinânaw", "ê-mîcit"]),
        ("VAI", "mîcisow", ["mîcisow", "nimîcison", "kimîcison", "ê-mîcisoyit"]),
        ("VII", "nîpin", ["nîpin", "nîpin", "ê-nîpihk"]),
        ("NDA", "nôhkom", ["nôhkom", "kôhkom", "ohkoma"]),
        ("NDI", "mîpit", ["mîpit", "nîpit", "kîpit", "wîpit"]),
        ("NA", "minôs", ["minôs", "minôsak", "minôsa"]),
        ("NI", "nipiy", ["nipiy", "nipîhk", "ninipiy", "kinipiy"]),
    ],
)
def test_paradigm(pardigm_gen, name, lemma, examples: list[str]):
    """
    Test paradigm panes generates based on default size, lemma and paradirm name and
    matches an extract of data above
    """
    paradigm = pardigm_gen.generate_pane(lemma=lemma, paradigm_type=name)

    for form in examples:
        assert paradigm.contains_wordform(form)


def test_generates_na_paradigm_default_size(pardigm_gen) -> None:
    """
    Generate a paradigm for a lemma+word class; see if it has some expected basic
    inflections.
    """
    lemma = "minôs"
    word_class = "NA"
    inflections = ["minôsa", "minôsak", "niminôs"]
    inflections_full = ["ominôsiyiwa", "kiminôsiwâwak", "minôsinâhk"]

    paradigm = pardigm_gen.generate_pane(lemma, word_class)

    for form in inflections:
        assert paradigm.contains_wordform(form)
    for form in inflections_full:
        assert not paradigm.contains_wordform(form)

def test_generates_na_paradigm_full_size(pardigm_gen) -> None:
    """
    Generate a paradigm for a lemma+word class; see if it has some expected full
    inflections.
    """
    lemma = "minôs"
    word_class = "NA"
    inflections = ["minôsa", "minôsak", "niminôs", "ominôsiyiwa", "kiminôsiwâwak", "minôsinâhk"]

    size = "full"
    paradigm = pardigm_gen.generate_pane(lemma, word_class, size)

    for form in inflections:
        assert paradigm.contains_wordform(form)

def test_generates_na_paradigm_wrong_size(pardigm_gen) -> None:
    """
    Generate a paradigm for a lemma+word class with specified wrong size type.
    Function overrides wrong size with default option
    """
    lemma = "minôs"
    word_class = "NA"
    inflections = ["minôsa", "minôsak", "niminôs"]
    inflections_full = ["ominôsiyiwa", "kiminôsiwâwak", "minôsinâhk"]

    size = "wrongsize"
    paradigm = pardigm_gen.generate_pane(lemma, word_class, size)

    for form in inflections:
        assert paradigm.contains_wordform(form)
    for form in inflections_full:
        assert not paradigm.contains_wordform(form)

@pytest.fixture
def pardigm_gen() -> paradigm_panes.PaneGenerator:
    """
    Setup resources and create PaneGenerator
    """
    paradigm_panes.settings.set_layouts_dir(BASE_DIR / "test_resources" / "layouts")
    paradigm_panes.settings.set_fst_filepath(BASE_DIR / "test_resources" / "fst" / "crk-strict-generator.hfstol")

    pardigm_gen = paradigm_panes.PaneGenerator()
    return pardigm_gen