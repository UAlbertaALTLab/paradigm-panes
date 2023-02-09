from __future__ import annotations

import logging
import csv
from pathlib import Path
from typing import Dict

from hfst_optimized_lookup import TransducerFile

logger = logging.getLogger(__name__)


class ParadigmNotSetError(Exception):
    """
    Raised when a paradigm is requested, but does not exist.
    """


class FstFileNotProvidedError(Exception):
    """
    Raised when the manager is instantiated without an FST path
    """


class FstNotValidError(Exception):
    """
    Raised when the manager is called with an invalid FST path
    """


class LayoutDirectoryNotProvidedError(Exception):
    """
    Raised when the manager is instantiated without a layout directory
    """


class LayoutDirectoryNotValidError(Exception):
    """
    Raised when the layout directory is not a real directory
    """



class ParadigmManager:
    """
    Everything you need to get from layout files and a generator FST to a full on paradigm layout.

    """

    def __init__(self, layout_directory: Path, generation_fst: Path):
        self.perform_checks(layout_directory, generation_fst)
        self.layout_directory = Path(layout_directory)
        self.generation_fst = generation_fst
        self.paradigm = None
        self.lemma = None
        self.all_wordforms = []
        self.generated_paradigm = None

    @staticmethod
    def perform_checks(layout_directory, generation_fst):
        if not layout_directory:
            raise LayoutDirectoryNotProvidedError
        if not generation_fst:
            raise FstFileNotProvidedError
        if not Path(layout_directory).is_dir():
            raise LayoutDirectoryNotValidError
        if not Path(generation_fst).is_file():
            raise FstNotValidError

    def set_lemma(self, lemma: str):
        self.lemma = lemma

    def get_lemma(self) -> str:
        return self.lemma

    def set_paradigm(self, paradigm: str):
        self.paradigm = paradigm

    def get_paradigm(self) -> str:
        return self.paradigm

    def add_wordform(self, wordform: str):
        self.all_wordforms.append(wordform)

    def get_all_wordforms(self) -> list:
        return self.all_wordforms

    def get_generated_paradigm(self):
        return self.generated_paradigm

    def bulk_add_recordings(self, recordings: Dict[str,str]) -> Dict:
        """ Input recordings object has form:
            {"inflection": recording,...}
        """
        for header in self.generated_paradigm:
            entry = self.generated_paradigm[header]
            for i, row in enumerate(entry["rows"]):
                if "inflections" not in row:
                    continue
                inflections = row["inflections"]
                for inflection in inflections:
                    wf = inflection["wordform"]
                    if wf not in recordings:
                        continue
                    recording = recordings[wf]["recording_url"]
                    inflection["recording"] = recording
        return self.generated_paradigm

    def get_layout_file(self) -> Path:
        files = self.layout_directory.glob('*.tsv')
        for file in files:
            if file.name == f"{self.paradigm}.tsv":
                return file
        raise FileNotFoundError

    @staticmethod
    def clean_line(line):
        ret_line = []
        for l in line:
            if l:
                ret_line.append(l)
        return ret_line

    def generate(self) -> dict:
        """Takes in no arguments, assumes all arguments have been set already
        Returns the generated paradigm of the form:
        {
            <header>: {
                rows: [
                    {subheader: optional_subheader, label: label, inflections: [inflections], recording: optional_recording}
                ]
            },
            <header_2>: {
                ...
            }
        }
        """
        generated_paradigm = dict()
        layout_file = self.get_layout_file()
        transducer_file = TransducerFile(self.generation_fst)
        most_recent_header = ""
        header_and_index = dict()

        with open(layout_file) as file:
            layout_file_lines = csv.reader(file, delimiter="\t")

            for line in layout_file_lines:
                line = self.clean_line(line)
                if not line:
                    continue
                for i, el in enumerate(line):
                    if el.startswith("*"):
                        header_and_index[i+1] = el
                        generated_paradigm[el] = {"rows": []}
                        most_recent_header = el
                    elif el.startswith("|"):
                        subheader = el.replace("| ", "")
                        generated_paradigm[most_recent_header]["rows"].append({"subheader": subheader})
                    elif el.startswith("_"):
                        continue
                    else:
                        header = header_and_index[i]
                        person = line[0].replace("_ ", "")
                        fst_input = el.replace("${lemma}", self.lemma)
                        inflections = transducer_file.lookup(fst_input)
                        if not inflections:
                            all_inflections = [{"wordform": "--"}]
                        else:
                            all_inflections = []
                            for wf in inflections:
                                self.add_wordform(wf)
                                inflections_object = dict()
                                inflections_object["wordform"] = wf
                                all_inflections.append(inflections_object)
                        generated_paradigm[header]["rows"].append({"label": person, "inflections": all_inflections})

        self.generated_paradigm = generated_paradigm
        return generated_paradigm
