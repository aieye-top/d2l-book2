import argparse
import sys
from d2lbook2.build import build
from d2lbook2.deploy import deploy
from d2lbook2.clear import clear
from d2lbook2.activate import activate
from d2lbook2.translate import translate
import logging

logging.basicConfig(format='[d2lbook2:%(filename)s:L%(lineno)d] %(levelname)-6s %(message)s')
logging.getLogger().setLevel(logging.INFO)


def main():
    commands = {'build': build, 'deploy':deploy, 'clear':clear,
                'activate':activate, 'translate':translate}
    parser = argparse.ArgumentParser(description='''
D2L Book: Publish a book based on Jupyter notebooks.

Run d2lbook2 command -h to get the help message for each command.
''')
    parser.add_argument('command', nargs=1, choices=commands.keys())
    args = parser.parse_args(sys.argv[1:2])
    commands[args.command[0]]()

if __name__ == "__main__":
    main()
