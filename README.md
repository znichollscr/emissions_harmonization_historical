# Processing historical emissions for CMIP7 harmonization routines
<!--- Adding a one-line description of what this repository is for here may be
helpful -->
<!---

We recommend having a status line in your repo to tell anyone who stumbles
on your repository where you're up to. Some suggested options:

- prototype: the project is just starting up and the code is all prototype
- development: the project is actively being worked on
- finished: the project has achieved what it wanted and is no longer being
  worked on, we won't reply to any issues
- dormant: the project is no longer worked on but we might come back to it, if
  you have questions, feel free to raise an issue
- abandoned: this project is no longer worked on and we won't reply to any
  issues

-->

Scripts that combine historical emissions data records from several datasets like CEDS and GFED to create complete historical emissions files that are input to the IAM emissions harmonization algorithms in `IAMconsortium/concordia` (regional harmonization and spatial gridding for ESMs) and `iiasa/climate-assessment` (global climate emulator workflow).


## Status

- prototype: the project is just starting up and the code is all prototype

## Installation

We do all our environment management using
[poetry](https://python-poetry.org/). To get started, you will need to make
sure that poetry is installed
([instructions here](https://python-poetry.org/docs/#installing-with-the-official-installer),
we found that pipx and pip worked better to install on a Mac).

You may need to upgrade `poetry` if errors occur, as was the case e.g., [here](https://github.com/iiasa/emissions_harmonization_historical/issues/2).

To create the virtual environment, run

```sh
# Tell poetry to put virtual environments in the project
poetry config virtualenvs.in-project true
poetry install --all-extras
poetry run pre-commit install
```

These steps are also captured in the `Makefile` so if you want a single
command, you can instead simply run `make virtual-enviroment`.

Having installed your virtual environment, you can now run commands in your
virtual environment using

```sh
poetry run <command>
```

For example, to run Python within the virtual environment, run

```sh
poetry run python
```

As another example, to run a notebook server, run

```sh
poetry run jupyter lab
```

<!--- Other documentation and instructions can then be added here as you go,
perhaps replacing the other instructions above as they may become redundant.
-->

## Development

<!--- In bigger projects, we would recommend having separate docs where this
development information can go. However, for such a simple repository, having
it all in the README is fine. -->

Install and run instructions are the same as the above (this is a simple
repository, without tests etc. so there are no development-only dependencies).



### Repository structure

General functions in `emissions_harmonization_historical`.

Data: big files, locally, in `data`, especially under the `data_raw` subfolders.
  Structured in `national` (e.g., CEDS, GFED) and `global` (e.g., GCB) folders.


Notebooks: these are the main processing scripts.
  `01**`: preparing input data for `IAMconsortium/concordia`.
  `02**`: preparing input data for `iiasa/climate-assessment`.


### Tools

In this repository, we use the following tools:

- git for version-control (for more on version control, see
  [general principles: version control](https://gitlab.com/znicholls/mullet-rse/-/blob/main/book/theory/version-control.md))
    - for these purposes, git is a great version-control system so we don't
      complicate things any further. For an introduction to Git, see
      [this introduction from Software Carpentry](http://swcarpentry.github.io/git-novice/).
- [Poetry](https://python-poetry.org/docs/) for environment management
  (for more on environment management, see
  [general principles: environment management](https://gitlab.com/znicholls/mullet-rse/-/blob/main/book/theory/environment-management.md))
    - there are lots of environment management systems. Poetry works and for
      simple projects like this there is no need to overcomplicate things
    - we track the `poetry.lock` file so that the environment is completely
      reproducible on other machines or by other people (e.g. if you want a
      colleague to take a look at what you've done)
- [pre-commit](https://pre-commit.com/) with some very basic settings to get some
  easy wins in terms of maintenance, specifically:
    - code formatting with [ruff](https://docs.astral.sh/ruff/formatter/)
    - basic file checks (removing unneeded whitespace, not committing large
      files etc.)
    - (for more thoughts on the usefulness of pre-commit, see
      [general principles: automation](https://gitlab.com/znicholls/mullet-rse/-/blob/main/book/general-principles/automation.md)
    - track your notebooks using
    [jupytext](https://jupytext.readthedocs.io/en/latest/index.html)
    (for more thoughts on the usefulness of Jupytext, see
    [tips and tricks: Jupytext](https://gitlab.com/znicholls/mullet-rse/-/blob/main/book/tips-and-tricks/managing-notebooks-jupytext.md))
        - this avoids nasty merge conflicts and incomprehensible diffs
