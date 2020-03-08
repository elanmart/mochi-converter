import argparse
import yaml
from pathlib import Path
from typing import Union

from mochi_converter.convert import md_to_mochi


def _main(
    input: Union[str, Path], 
    output: Union[str, Path], 
    config: Union[str, Path],
) -> None:
    with open(config) as f:
        cfg = yaml.load(f, Loader=yaml.SafeLoader)

    md_to_mochi(input, output, cfg['decks'])


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument('--input', required=True)
    parser.add_argument('--output', default='converted')
    parser.add_argument('--config', default='config.yaml')

    args = parser.parse_args()

    _main(args.input, args.output, args.config)


if __name__ == '__main__':
    main()