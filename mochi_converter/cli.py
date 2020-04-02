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

    parser.add_argument(
        '--input',
        help='Input markdown file that should be converted into Mochi file', 
        required=True
    )
    parser.add_argument(
        '--output', 
        default='converted', 
        help='''filename or path where the results should be written. Defaults to "converted"
        Note: the filename should NOT include the extension, as the converted will generate 
        two files: <name>.edn and <name>.mochi 
        The latter is just a zipped version of the former.
        '''
    )
    parser.add_argument(
        '--config', 
        default='config.yaml',
        help='Path to the config file which should specify the names and IDs of your decks'
    )

    args = parser.parse_args()

    _main(args.input, args.output, args.config)


if __name__ == '__main__':
    main()