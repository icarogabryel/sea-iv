from asm_lexer import Lexer
from asm_parser import Parser
from code_generation import generate

def printAST(ast, tab = 0):
    print('\t' * tab + '-' + ast.type)

    for child in ast.children:
        printAST(child, tab + 1)

def main():
    with open('./doc/example.asm', 'r') as f:
        input = f.read()

    tokenizer = Lexer(input)
    
    print('TOKEN STREAM:\n')
    for token in tokenizer.getTokenStream():
        print(token)
    print('\n')

    parser = Parser(tokenizer.getTokenStream())
    
    print('AST:\n')
    printAST(parser.getAst())
    print('\n')

    print('OBJ CODE:\n')
    generator = generate(parser.getAst())
    for line in generator:
        print(line)

if __name__ == '__main__': main()
