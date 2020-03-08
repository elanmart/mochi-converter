from pathlib import Path
import tempfile
import zipfile

import edn_format

from mochi_converter.cli import _main


def test_main():
    _here = Path(__file__).resolve().parent

    with tempfile.TemporaryDirectory() as d:
        _main(
            _here / '..' / 'template.md', 
            Path(str(d)) / 'converted',
            _here / '..' / 'config.example.yaml'
        )

        mochi = Path(str(d)) / 'converted.mochi'
        with zipfile.ZipFile(mochi) as zf:
            data = zf.open('data.edn').read().decode()
            edn = edn_format.loads(data, )

    K = edn_format.Keyword

    assert edn[K('version')] == 2
    assert len(edn[K('decks')]) == 2
    
    d1 = edn[K('decks')][0]
    assert d1[K('name')] == 'Test'
    assert '2 + 2' in d1[K('cards')][0][K('content')]
