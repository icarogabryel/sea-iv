from tokenizer import Tokenizer


def main():
    input = '.text _loop, add $3 &2 _ifTrue:'

    s = Tokenizer(input)

    print(s.getTokenStream())


if __name__ == '__main__': main()
