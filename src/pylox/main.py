import sys

from lox.Lox import Lox

def display_help():
    """
    Display help with command listing.
    :return:
    """
    print(
        '''
        Usage: python ./src/main.py <command> [filename]
        Available commands:
        - interactive or -i: Run the interpreter in interactive mode
        - tokenize or -f: Run the interpreter on the given file
        - help or -h: Display this help message'''
    )


def parse_cmd(args):
    """
    Parse and run given command from user.
    :param args: argv from main
    """
    commands = {
        '--interactive': Lox.run_prompt,
        '-i': Lox.run_prompt,
        '--tokenize': lambda: Lox.run_file(args[2]),
        '-f': lambda: Lox.run_file(args[2]),
        '--help': display_help,
        '-h': display_help,
    }

    cmd = args[1]
    func = commands.get(cmd)

    if not func:
        print(f'Error: Unknown command {cmd}', file=sys.stderr)
        sys.exit(1)

    func()


def main():
    if len(sys.argv) < 2:  # if no command given, run interactive mode
        Lox.run_prompt()
    elif len(sys.argv) > 3:
        print('Usage: python ./src/main.py [command] [filename]')
    else:
        parse_cmd(sys.argv)


if __name__ == '__main__':
    main()
