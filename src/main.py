from tokenizer import Tokenizer


def main():
    input = '.text _Gerg  _ergrg'

    s = Tokenizer(input)

    print(s.getTokenStream())


if __name__ == '__main__': main()
