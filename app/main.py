import sys
import app.Lox as Lox


def main():
    if len(sys.argv) < 2:
        print('Usage: ./your_program.sh <command> [filename]', file=sys.stderr)
        exit(1)
    else:
        command = sys.argv[1]
        match command:
            case 'interactive':
                Lox.runPrompt()
            case 'tokenize':
                filename = sys.argv[2]
                Lox.runFile(filename)
                if Lox.hadError():
                    exit(65)
            case _:
                print(f'Unknown command: {command}', file=sys.stderr)
                exit(1)


if __name__ == '__main__':
    main()
