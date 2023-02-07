from paradigm_panes.manager import ParadigmManager
import json
import requests
import urllib

def divide_chunks(terms, size):
    # looping till length l
    for i in range(0, len(terms), size):
        yield terms[i : i + size]


def get_recordings_from_url(search_terms, url):
    matched_recordings = {}
    query_params = [("q", term) for term in search_terms]
    response = requests.get(url + "?" + urllib.parse.urlencode(query_params))
    if response.status_code == 200:
        recordings = response.json()

        for recording in recordings["matched_recordings"]:
            entry = recording["wordform"]
            matched_recordings[entry] = {}
            matched_recordings[entry]["recording_url"] = recording["recording_url"]
            matched_recordings[entry]["speaker"] = recording["speaker"]

    return matched_recordings


layout_directory = "/Users/jolenepoulin/Documents/morphodict/src/CreeDictionary/res/layouts/VAI/revised"
generation_fst = "/Users/jolenepoulin/Documents/giellatekno/lang-crk/generator-gt-dict-norm-no-bound.hfstol"
pm = ParadigmManager(layout_directory=layout_directory, generation_fst=generation_fst)
pm.set_lemma("atim")
pm.set_paradigm("NA")

paradigm = pm.generate()

wordforms = pm.get_all_wordforms()
matched_recordings = {}
for search_terms in divide_chunks(wordforms, 30):
    url = "https://speech-db.altlab.app/maskwacis/api/bulk_search"
    matched_recordings.update(get_recordings_from_url(search_terms, url))

paradigm = pm.bulk_add_recordings(matched_recordings)

print(paradigm)

