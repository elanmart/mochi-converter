import argparse


def foo():
    print('Executing foo()')


def main():
    parser = argparse.ArgumentParser('help')
    parser.add_argument('--foo', required=True)
    args = parser.parse_args()


if __name__ == '__main__':
    main()