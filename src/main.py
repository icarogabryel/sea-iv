from asmTokenizer import Tokenizer
from asmParser import Parser
from asmGenerator import Generator

def printAST(ast, tab = 0):
    print('\t' * tab + '-' + ast.type)

    for child in ast.children:
        printAST(child, tab + 1)


def main():
    with open('./doc/example.asm', 'r') as f:
        input = f.read()

    tokenizer = Tokenizer(input)
    print(tokenizer.getTokenStream())
    print('\n')

    parser = Parser(tokenizer.getTokenStream())
    printAST(parser.getAst())

    generator = Generator(parser.getAst())
    print(generator.getObjCode())


if __name__ == '__main__': main()
