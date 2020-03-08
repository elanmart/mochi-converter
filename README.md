# Mochi converter

This is a minimal POC implementation of `markdown` to `mochi` converter

# What's missing

- [ ] Better docs
- [ ] More roboust tests 
- [ ] Submitting the cards via the REST API

# Installation

You'll need to install [poetry](https://github.com/python-poetry/poetry)

Once ready, run

```bash
poetry install
```

# Configuration

You'll need to provide a `config` file representing the structure of your decks. 

Please see the `Mochi` **FAQ** on how to get the deck IDs, and the 
`config.example.yaml` for example on how to set it up. 

# Markdown File structure

The top-level header (`#`) should contain the name of the deck that
the cards below will go to.

For nested decks (e.g. `General-knowledge` `->` `Countries`) 
you should use `::` to split the levels, e.g.:
`# General-knowledge::Countries`

The level-2 header (`##`) should be either `## Q` or `## QA`.
If you use `QA`, an inverse card will also be generated.

Then below that goes the standard `Mochi` content, split by `---`.

Currently we assume there is only a single `---` present.

See `template.md` for an example

# Usage

```bash
poetry run convert --input my-file.md --output converted --config config.yaml
```

the `output` and `config` are optional, run `poetry run convert -h` for details
