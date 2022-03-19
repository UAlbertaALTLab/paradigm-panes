# paradigm-panes

Installable package that produces a paradigm for a given word, given a pointer to paradigm layouts and FST file. Originally
built for [itwêwina](https://itwewina.altlab.app/).

# Example Usage:

```
    import paradigm_panes
    pg = paradigm_panes.PaneGenerator()

    lemma = "amisk"
    p_type = "NA"

    pg.set_layouts_dir("/home/ubuntu/cmput401/paradigm-panes/paradigm_panes/resources/layouts")
    pg.set_fst_filepath("/home/ubuntu/cmput401/paradigm-panes/paradigm_panes/resources/fst/generator-gt-norm.hfstol")

    pg.generate_pane(lemma, p_type)
```

- `set_layouts_dir(path)` specifies a location of a directory with paradigm layouts that are relevant for current paradigm generation.

- `set_fst_filepath(path)` specifies FST file location with layout translation that are relevant for current paradigm generation.

- `set_tag_style(path)` specifies template rendering type.

> Available tag styles:

> 1.  "Plus"
> 2.  "Bracket"

The generator must specify both location before generating a paradigm.

Size is optional to paradigm generation; by default a base size (or first available) will be used.
