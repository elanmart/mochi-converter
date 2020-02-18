import tempfile
from pathlib import Path
import requests
import edn_format
import re

from typing import Union, Any, List, Dict, Tuple, NamedTuple


class Card(NamedTuple):
    deck: str
    question: str
    answer: str


Path_T = Union[Path, str]


def _maybe_override_deck(
    content: str, deck: str
) -> Tuple[str, str]:
    override_pattern = re.compile(r'\n!deck: (\w+)')
    override = re.search(override_pattern, content)

    if override is not None:
        deck = override.group(1)
        content = re.sub(override_pattern, '', content)

    return content, deck


def _parse_card(
    header: str,
    content: str,
    deck: str,
) -> List[Card]:

    content, deck = _maybe_override_deck(content, deck)
    
    q, a = content.split('---')
    q, a = q.strip(), a.strip()

    ret = [Card(deck, q, a)]

    if header.startswith('## QA'):
        ret += [Card(deck, a, q)]
        
    return ret


def read_md(input: Path_T) -> List[Card]:
    
    if not Path(input).exists():
        raise ValueError(
            f'Cannot read markdown file at '
            f'{input} -- file does not exist'
        )
    
    with open(input) as f:
        content = f.readlines()

    data = []

    _deck = None
    _header = None
    _card = []

    def _extend_data():
        if (_header is not None) and (_deck is not None):
                data.extend(_parse_card(
                    header=_header,
                    content='\n'.join(_card),
                    deck=_deck,
                ))

    for line in content:

        if line.startswith('# '):
            _deck = line[1:].strip()

        elif line.startswith('## '):
            _extend_data()
            _header = line.strip()
            _card = []

        else:
            _card.append(line)

    _extend_data()
    return data


def mochi_to_md():
    pass


def md_to_mochi(input: Path_T, output: Path_T):
    pass


def submit_mochi(path: Path_T, user: str, token: str):
    raise NotImplementedError()


def submit_md(input: str, user: str, token: str):
    with tempfile.TemporaryDirectory() as d:
        mochi_path = Path(str(d)) / 'out.mochi'
        md_to_mochi(input=input, output=mochi_path)
        submit_mochi(mochi_path, user=user, token=token)


def submit_card(path, user: str, token: str):
    pass


if __name__ == '__main__':
    ret = read_md('./template.md')

    for i, item in enumerate(ret):
        print(i, item['question'])
