from scanner import Scanner


def main():
    input = '76 54'

    s = Scanner(input)

    print(s.getTokenStream())


if __name__ == '__main__': main()
