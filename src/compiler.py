from asm_scanner import Scanner
from asm_parser import Parser
from asm_visitor import Visitor

def compile(input: str) -> str:
    tokenizer = Scanner(input)
    parser = Parser(tokenizer.getTokenStream())
    visitor = Visitor(parser.getAst())

    return visitor.getMachineCode()
