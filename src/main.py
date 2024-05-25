from asmTokenizer import Tokenizer
from asmParser import Parser


def main():
    input = '.text _loop: add &2, $1, $2'

    tokenizer = Tokenizer(input)
    print(tokenizer.getTokenStream())

    parser = Parser(tokenizer.getTokenStream())
    print(parser.getAst())


if __name__ == '__main__': main()
