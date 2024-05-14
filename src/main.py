from asmTokenizer import Tokenizer
from asmParser import Parser


def main():
    input = '.text _loop: add  sub _ifTrue:'

    tokenizer = Tokenizer(input)
    parser = Parser(tokenizer.getTokenStream())

    print(parser.getAst())


if __name__ == '__main__': main()
