# paradigm-panes

Installable package that produces a paradigm for a given word, given a pointer to paradigm layouts and FST file. Originally
built for [itwêwina](https://itwewina.altlab.app/).

# PyPi Package

Latest version of the package posted to PyPi: [paradigm-panes 0.3.2](https://pypi.org/project/paradigm-panes/)

# Install

```
pip install paradigm-manager
```

# Developing

Developing is done and managed through [Python Poetry](https://python-poetry.org/) package manager.

To start development:

```
# Download the repo
git clone https://github.com/UAlbertaALTLab/paradigm-panes.git

# Set up virutal env
virtualenv venv --python=python3.9
source venv/bin/activate

# Install dependencies
poetry install

# Now cd into main directory and try out the package
cd paradigm_panes
python
    >>> import paradigm_manager
    >>> ...
```

# Package Documentation:
The package is very simple to use and requires two types of linguistic files to operate. First:

## Installing
Install the paradigm manager with:
```shell
pip install paradigm-manager
```

## Usage and Configuration

Import the library:

```
import paradigm_manager
```

Create PaneManager and specify path to FST file and layouts resources:

```
pm = paradigm_manager.ParadigmManager(
            layout_directory="/home/ubuntu/paradigm_panes/resources/layouts", 
            generation_fst="/home/ubuntu/paradigm_panes/resources/fst/crk-strict-generator.hfstol")
```

Paths to the layout directory and generation FST are required arguments.

Pass lemma and paradigm type to generate a paradigm:

```
lemma = "amisk"
p_type = "NA"
pm.set_lemma(lemma)
pm.set_paradigm(p_type)
```

Generate the paradigm:

```python
paradigm = pm.generate()
```

Optionally add recordings to the paradigm with the following steps:
```python
wordforms = pm.get_all_wordforms()
matched_recordings = <fetch recordings for all wordforms>
paradigm = pm.bulk_add_recordings(matched_recordings)
```

# Testing

To run the tests you need to install required dependencies, it is easier by using a virtual environment like this:

```
# Set up virutal env
virtualenv venv --python=python3.9
source venv/bin/activate

# Install dependencies
poetry install
```

Once the dependencies are installed you can run tests by calling pytest.

```
pytest
```

# Release

Package version number is sorted in pyproject.toml. With every release to PyPi the version needs to be updated. \
Build the package from the main directory before publishing it:

```
poetry build
```

To publish to Test PyPi use poetry and enter credentials associated with Test PyPi account

```
poetry publish -r testpypi
```

To publish to real PyPi use poetry and enter credentials associated with PyPi

```
poetry publish
```

All relevant package specifications and dependencies are managed in `pyproject.toml` file.
