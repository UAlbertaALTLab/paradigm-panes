"""
    Planning to make it a central place to run paradigm generation
"""
import settings

from pathlib import Path
from typing import (Dict, Optional)

from generation import default_paradigm_manager
from manager import ParadigmManager
from panes import Paradigm

BASE_DIR = Path(__file__).resolve().parent

def main():
    set_layouts_dir(BASE_DIR / "resources" / "layouts")
    # set_fst_filepath(BASE_DIR / "resources" / "fst" / "crk-strict-generator.hfstol")

    lemma = "amisk"
    paradigm_type = "NA"
    specified_size = "notexistentsizetype"
    # specified_size = "full"

    generate_pane(lemma, paradigm_type, specified_size)

def generate_pane(lemma: str, paradigm_type: str, specified_size: Optional[str] = None):
    if (settings.is_setup_complete()):
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
            serialized_paradigm = serialize_paradigm(paradigm)
            print(serialized_paradigm)

            return serialized_paradigm
        else:
            raise Exception("Paradigm layout specification is missing.")
    else:
        raise Exception("FST and Layouts resources are not configured correctly.")

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

# TODO cleanup for package use
def serialize_paradigm(paradigm: Paradigm) -> Dict[str, any]:
    """
    Serializes a Paradigm object as a dictionary

    :param paradigm: the paradigm to be serialized
    :return: dictionary representation
    """
    panes = []

    for pane in (paradigm.panes or []):

        tr_rows = []
        for row in (pane.rows or []):   # potential problem: we don't distinguish between compound rows and non-compound rows. this might be a problem for the frontend.
            if row.is_header:
                tr_rows.append({
                    "is_header": True,
                    "label": row.fst_tags,
                    "cells": []
                })
            else:
                cells = []
                for cell in (row.cells or []):
                    cell_data = {
                        "should_suppress_output": cell.should_suppress_output,
                        "is_label": cell.is_label,
                        "is_inflection": cell.is_inflection,
                        "is_missing": cell.is_missing,
                        "is_empty": cell.is_empty
                    }

                    if cell_data["is_label"]:
                        cell_data["label_for"] = cell.label_for
                        cell_data["label"] = cell.fst_tags

                        if type(cell_data["label_for"]) != str:  # if cell.label_for was never instantiated
                            cell_data["label_for"] = ""
                        if cell_data["label_for"] == "row":
                            cell_data["row_span"] = cell.row_span

                    elif cell_data["is_inflection"] and not cell_data["is_missing"]:
                        # TODO add orth
                        # cell_data["inflection"] = orth(cell.inflection)
                        cell_data["inflection"] = cell.inflection
                        cell_data["recording"] = cell.recording

                        # TODO check wordforms?
                        # if cell.inflection in observed_wordforms():
                        #     cell_data["observed"] = True
                        # else:
                        #     cell_data["observed"] = False
                        cell_data["observed"] = False

                    cells.append(cell_data)

                tr_rows.append({
                    "is_header": False,
                    "label": None,  # shouldn't be used.
                    "cells": cells
                })

        panes.append({"tr_rows": tr_rows})

    return {"panes": panes}

def set_fst_filepath(path) -> None:
    settings.set_fst_filepath(path)

def set_layouts_dir(path) -> None:
    settings.set_layouts_dir(path)

if __name__ == "__main__":
    main()
