"""
    Planning to make it a central place to run paradigm generation
"""
from typing import (Dict, Optional)

from generation import default_paradigm_manager
from manager import ParadigmManager
from panes import Paradigm

def main():
    print("Hello World!")

    lemma = "amisk"
    paradigm_type = "NA"
    specified_size = "notexistentsizetype"
    # specified_size = "full"

    if paradigm_type is not None:
        paradigm_manager = default_paradigm_manager()
        sizes = list(paradigm_manager.sizes_of(paradigm_type))
        if "basic" in sizes:
            default_size = "basic"
        else:
            default_size = sizes[0]

        if len(sizes) <= 1:
            size = default_size
        else:
            size = specified_size
            if size not in sizes:
                size = default_size

        paradigm = paradigm_for(paradigm_manager, paradigm_type, lemma, size)
        print(paradigm)

def paradigm_for(paradigm_manager: ParadigmManager, paradigm_type: str, fst_lemma: str, paradigm_size: str) -> Optional[Paradigm]:
    """
    Returns a paradigm for the given wordform at the desired size.

    If a paradigm cannot be found, None is returned
    """

    manager = default_paradigm_manager()

    if paradigm_type:
        if paradigm := paradigm_manager.paradigm_for(paradigm_type, fst_lemma, paradigm_size):
            return paradigm

    return None

if __name__ == "__main__":
    main()
