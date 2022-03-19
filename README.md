# paradigm-panes

Installable package that produces a paradigm for a given word, given a pointer to paradigm layouts and FST file. Originally
built for [itwêwina](https://itwewina.altlab.app/).

# Example Usage:

```
    pane_generator = PaneGenerator()
    pane_generator.set_layouts_dir(BASE_DIR / "resources" / "layouts")
    pane_generator.set_fst_filepath(BASE_DIR / "resources" / "fst" / "crk-strict-generator.hfstol")

    lemma = "amisk"
    paradigm_type = "NA"
    specified_size = "full"

    pane_generator.generate_pane(lemma, paradigm_type, specified_size)
```

- `set_layouts_dir(path)` specifies a location of a directory with paradigm layouts that are relevant for current paradigm generation.

- `set_fst_filepath(path)` specifies FST file location with layout translation that are relevant for current paradigm generation.

The generator must specify both location before generating a paradigm.

Size is optional to paradigm generation; by default a base size (or first available) will be used.
