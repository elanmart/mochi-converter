# Mochi converter

This is a minimal POC implementation of `markdown` to `mochi` converter.

[Mochi](https://mochi.cards/) is a neat, markdown-centric spaced repetition software. 

In my workflows, I often take notes in `Notion` or other tools, and would then like to convert them all at once into flashcards, which is not yet supported by `Mochi`, hence the converter. 

# What's missing

- [ ] Better docs
- [ ] More roboust tests 
- [ ] Submitting the cards via the REST API

# Installation

You'll need to install [poetry](https://github.com/python-poetry/poetry)

You may wonder -- why not just `requirements.txt`? Very good question. It's just because I wanted to test 
out `poetry` which I have never used before :)

Once ready, run

```bash
poetry install
```

# Configuration

You'll need to provide a `config` file representing the structure of your decks. 

Please see the `Mochi` **FAQ** on how to get the deck IDs, and the 
`config.example.yaml` for example on how to set it up. 
Basically you'll need to map the structure of your decks into the `config.yaml` file.

# Markdown File structure

## Decks

The top-level header (`#`) should contain the name of the deck that
the cards below will go to.

```markdown

# Birthdays

## Q
Alice 
---
1-st January

## Q
Bob
---
2-nd February

# Countries

## Q
Capital of Switzerland
---
Zurich
```

For nested decks (e.g. `General-knowledge` `->` `Countries`) 
you should use `::` to split the levels, e.g.:

```markdown
# General::Countries

## Q
Capital of Switzerland
```

## Cards

The level-2 header (`##`) should be either `## Q` or `## QA`.
If you use `QA`, an inverse card will also be generated.

So the following `markdown` file:

```markdown

# Birthdays

## QA

Alice 
---
1-st January
```

will actually generate `2` cards: `Alice` as a question, and `1-st Jan` as the answer, and the reverse:
`1-st Jan` as the question and `Alice` as the answer.

Note that we use standard `Mochi` convetion to split the sides of a card using `---`

Currently we assume there is only a single `---` present.

See `template.md` for an example.

## Overriding decks

You can override the deck by using `!deck: MyDeck` syntax, not sure how useful this will be:

```markdown

# Birthdays

## QA
!deck: Countries

Capital of Switzerland
---
Zurich
```

# Usage

Once you have your `config.yaml` and the markdown file, run:

```bash
poetry run convert --input my-file.md --output converted --config config.yaml
```

the `output` and `config` are optional, run

```bash
poetry run convert -h
```

for details
