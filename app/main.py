import sys

from Lox import Lox


def run_interactive():
    """
    Run interactive Lox shell.
    """
    Lox.run_prompt()


def run_file(file) -> bool:
    """
    Run Lox source from file.
    :param file: path to source file
    :return: had error?
    """
    Lox.run_file(file)
    return Lox.had_error


def display_help():
    """
    Display help with command listing.
    :return:
    """
    print(
        '''
        Usage: python ./app/main.py <command> [filename]
        Available commands:
        - interactive or -i: Run the interpreter in interactive mode
        - tokenize or -f: Run the interpreter on the given file
        - help or -h: Display this help message''',
        file=sys.stderr
    )


def parse_cmd(args):
    """
    Parse and run given command from user.
    :param args: argv from main
    """
    commands = {
        '--interactive': run_interactive,
        '-i': run_interactive,
        '--tokenize': lambda: run_file(args[2]),
        '-f': lambda: run_file(args[2]),
        '--help': display_help,
        '-h': display_help,
    }

    cmd = args[1]
    func = commands.get(cmd)

    if not func:
        print(f'Error: Unknown command {cmd}', file=sys.stderr)
        sys.exit(1)

    error = func()
    if error: sys.exit(1)


def main():
    if len(sys.argv) < 2:  # if no command given, run interactive mode
        run_interactive()
    elif len(sys.argv) > 3:
        print('Usage: python ./app/main.py [command] [filename]')
    else:
        parse_cmd(sys.argv)


if __name__ == '__main__':
    main()
