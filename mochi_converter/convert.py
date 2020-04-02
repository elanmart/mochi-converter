from collections import defaultdict
from pathlib import Path
import re
import tempfile
from typing import Any, Dict, List, NamedTuple, Tuple, Union
import zipfile

import edn_format


Path_T = Union[Path, str]


class Card(NamedTuple):
    """ Represents a single card to be put into Mochi

    Assumes that the card is a simple, two-sided one, even though 
    Mochi can handle more than two sections.
    """

    deck: str
    question: str
    answer: str


def _merge(a: str, b: str) -> str:
    """ Merge two sides of the card into a single
    piece of markdown
    """

    return '\n---\n'.join([a, b])
    

def _maybe_override_deck(
    content: str, deck: str
) -> Tuple[str, str]:
    """ Given a content of the card and a default deck, check if 
    there is a !deck directive in the card body
    that would override the parent deck.
    Removes the directive from the body.
    """

    override_pattern = re.compile(r'!deck: (.+)')
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
    """ Parse a markdown content into a Card tuple.

    Parameters
    ----------
    header:
        header of the card, determines whetver the reversed card will be generated.
    content:
        content of the card.
    deck:
        deck to which this card will be placed. 
        Set as top-level markdown header. 
    """

    content, deck = _maybe_override_deck(content, deck)
    
    assert '!deck' not in deck
    assert '!deck' not in content

    q, a = content.split('---')
    q, a = q.strip(), a.strip()

    ret = [Card(deck, q, a)]

    if header.startswith('## QA'):
        ret += [Card(deck, a, q)]
        
    return ret


def _flatten_decks_info(
    deck_info: List[Dict], parent_id: str = None
) -> Dict:
    """ Given a config specifying deck hierarchy, 
    creates a flat structure, setting proper :name, :id, and :parent
    field values. 
    """

    result = {}

    def _add(name: str, id: str, pid: str = None) -> None:
        if name in result:
            raise ValueError(
                f'Duplicate name: {name}'
            )

        _pid = {'parent-id': pid} if pid else {}

        result[name] = {
            'name': name, 
            'id': id, 
            **_pid
        }

    for d in deck_info:

        name, id = d['name'], d['id']
        children = d.get('children', [])

        _add(name, id)
        for k, v in _flatten_decks_info(children, id).items():
            _add(name + '::' + k, v['id'], parent_id)

    return result


def read_md(input: Path_T) -> List[Card]:
    """ Read a markdown file and parse it into Mochi cards.
    """
    
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


def cards_to_decks(cards: List[Card]) -> list:
    """ Turn mochi cards into a list of decks representation, which mochi files expect. 
    """
    decks = defaultdict(list)

    for card in cards:
        d = card.deck
        c = {'name': '', 'content': _merge(card.question, card.answer)}
        decks[d].append(c)

    decks = [
        {'name': k, 'cards': v} 
        for k, v in decks.items()
    ]

    return decks    


def expand_decks_list(
    decks: List[Dict[str, Any]],
    deck_info: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """ Given a list of decks and their cards,
    fills in the missing information using the detailed decks specification 
    """

    for item in decks:
        name = item['name']
        info = deck_info[name]

        item['id'] = info['id']
        if 'parent-id' in info:
            item['parent-id'] = info['parent-id']
        
    return decks


def _compress(input: Path, output: Path) -> None:
    """ Write edn data to a zip archive expected by mochi
    """

    with zipfile.ZipFile(output, 'w') as fout:
        fout.write(input, 'data.edn')


def _postporcess_edn(decks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """ Tweak the data representation to fit what 
    mochi expects 
    """

    for d in decks:
        d['name'] = d['name'].split('::')[-1]
        d['id'] = edn_format.Keyword(d['id'])
        
        for c in d['cards']:
            c['deck-id'] = d['id']

        d['cards'] = tuple(d['cards'])
    
    decks_entry = {
        'decks': decks,
        'version': 2
    }

    return decks_entry


def decks_to_mochi(
    decks: List[Dict[str, Any]],
    output: Path_T
) -> None:
    """ Write decks to a mochi-compliant zip archive. 
    """
    output = Path(output)

    edn = output.parent / (output.name + '.edn')
    zip = output.parent / (output.name + '.mochi')

    decks_entry = _postporcess_edn(decks)

    with open(edn, 'w') as f:
        print(
            edn_format.dumps(decks_entry, keyword_keys=True), 
            file=f
        )

    _compress(input=edn, output=zip)


def md_to_mochi(
    input: Path_T, 
    output: Path_T, 
    deck_info: Any = None
) -> None:
    """ Convert markdown file to a .mochi file
    """

    cards = read_md(input)
    decks = cards_to_decks(cards)

    if deck_info is not None:
        deck_info = _flatten_decks_info(deck_info)
        decks = expand_decks_list(decks, deck_info)

    decks_to_mochi(decks, output)
