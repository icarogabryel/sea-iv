from asm_scanner import Scanner
from asm_parser import Parser, Node
from code_visitor import generateMachineCode


def printAST(ast: Node, tab = 0):
    print('\t' * tab + '-' + ast.type)

    for child in ast.children:
        printAST(child, tab + 1)

def main():
    with open('./doc/example.asm', 'r') as f:
        input = f.read()

    tokenizer = Scanner(input)
    
    print('\nTOKEN STREAM:\n')
    for token in tokenizer.getTokenStream():
        print(token)
    print('\n')

    parser = Parser(tokenizer.getTokenStream())
    
    print('AST:\n')
    printAST(parser.getAst())
    print('\n')

    # print('OBJ CODE:\n')
    # generator = generateMachineCode(parser.getAst())
    # for line in generator:
    #     print(line)

    # print('\n')


if __name__ == '__main__': main()
