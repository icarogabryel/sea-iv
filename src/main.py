from asmTokenizer import Tokenizer
from asmParser import Parser


def main():
    input = '.text add _loop: sub'

    tokenizer = Tokenizer(input)
    print(tokenizer.getTokenStream())

    parser = Parser(tokenizer.getTokenStream())
    print(parser.getAst())


if __name__ == '__main__': main()
