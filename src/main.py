from asm_scanner import Scanner
from asm_parser import Parser, Node
from asm_visitor import Visitor
from asm_linker import Linker

def printAST(ast: Node, tab = 0):
    print('\t' * tab + '-' + ast.type)

    for child in ast.children:
        printAST(child, tab + 1)

def main() -> None:
    with open('../test/example.s', 'r') as f:
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

    showMachineCode = True

    if showMachineCode:
        print('OBJ CODE:\n')
        visitor = Visitor(parser.getAst())
        
        for line in visitor.getMachineCode():
            print(line)

        print('\n')

        linker = Linker(visitor.getMachineCode())

        print('LINKED OBJ CODE:\n')

        for line in linker.rawBytesList:
            print(line)


if __name__ == '__main__': main()
