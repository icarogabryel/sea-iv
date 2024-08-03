import csv


class Node: # AST Node
    def __init__(self, type, lexeme: str = '\0') -> None:
        self.type = type
        self.lexeme: str = lexeme
        self.children: list[Node] = []

    def __repr__(self) -> str:
        return f'{self.type}({self.lexeme}) -> {self.children}'

    def addChild(self, child) -> None:
        self.children.append(child)


class Byte: # Object code byte
    def __init__(self, byte: str) -> None:
        self.byte = byte
        self.label = ''

    def __repr__(self) -> str:
        return f'{self.label}: {self.byte}' if len(self.label) > 0 else self.byte


# Exceptions
class LexicalError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return 'Lexical Error: ' + self.message
    

class SyntacticError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return 'Syntactic Error: ' + self.message


class SemanticError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return 'Semantic Error: ' + self.message


def getInsts():
    instructionsDict = {}

    with open('../data/insts.csv', 'r') as file:
        reader = csv.reader(file)
        
        for row in reader:
            instructionsDict.update({row[0]: (row[1], row[2])})

    return instructionsDict


# Constants
INSTRUCTIONS = getInsts()
IGNORED_CHARS = ' \n\t'
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS = ',:()'
ALPHABET = NUMBERS + LETTERS + SYMBOLS + '._&$\"/'
TOKEN_ENDS = IGNORED_CHARS + SYMBOLS
DIRECTIVES = {
    '.include': 'includeDir',
    '.data': 'dataDir',
    '.space': 'spaceDir',
    '.word': 'wordDir',
    '.ascii': 'asciiDir',
    '.byte': 'byteDir',
    '.inst': 'instDir'
}
DATA_TYPES = ['spaceDir', 'wordDir', 'asciiDir', 'byteDir']
