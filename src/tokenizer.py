IGNORED_CHARS = ' \n\t'
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYMBOLS = ',:'
MARKS = '._&$' # Marks are used to indicate labels and directives to the assembler
ALPHABET = NUMBERS + LETTERS + SYMBOLS + MARKS
TOKEN_ENDS = IGNORED_CHARS + SYMBOLS
DIRECTIVES = ['.text']
INSTRUCTIONS = ['add', 'sub']


class Tokenizer:
    def __init__(self, asmCode: str) -> None:
        self.asmCode = asmCode
        self.tokenStream = []
        self.index = 0

        self.makeTokenStream()

    def makeTokenStream(self) -> None: # Generate token stream
        while True:
            token = self.getNextToken()
            
            if token[0] == 'EOF':
                self.tokenStream.append(token)
                break

            self.tokenStream.append(token)
    
    def getNextToken(self) -> tuple: # Get next token
        while self.getCurrentChar() in IGNORED_CHARS: # Ignore whitespaces
            self.advance()
        
            if self.isEOF():
                return ('EOF', self.getCurrentChar())
        
        if self.getCurrentChar() == ';': # Ignore comments
            while self.getCurrentChar() != '\n':
                self.advance()

                if self.isEOF():
                    return ('EOF', self.getCurrentChar())

            return self.getNextToken()
        
        if self.isEOF(): # Return EOF token if end of file
            return ('EOF', self.getCurrentChar())
        
        lexeme = self.getLexeme()

        return (self.getTokenLabel(lexeme), lexeme)

    def advance(self) -> None: # Increment index by 1
        self.index += 1

    def getCurrentChar(self) -> str: # Return current character pointed by index or null character if index is out of bounds
        return self.asmCode[self.index] if self.index < len(self.asmCode) else '\0'
    
    def isEOF(self) -> bool:
        return True if self.getCurrentChar() == '\0' else False
    
    def getLexeme(self) -> str: # Get lexeme
        lexeme = ''
  
        if self.getCurrentChar() in SYMBOLS: # Check if the character is a symbol
            lexeme += self.getCurrentChar()
            self.advance()
            
            return lexeme
        
        while True: # Start reading characters to form a lexeme
            if self.isEOF() or self.getCurrentChar() in TOKEN_ENDS: # Read characters until a token ends symbol or EOF is found
                break
            
            if self.getCurrentChar() not in ALPHABET: # Check if the character is valid
                raise Exception('Invalid character: ' + self.getCurrentChar())
            
            lexeme += self.getCurrentChar()
            self.advance()
        
        return lexeme
    
    def getTokenLabel(self, lexeme: str) -> str:
        # if lexeme.isnumeric(): # todo
        #     return 'NUM'
        if lexeme in SYMBOLS:
            match lexeme:
                case ',':
                    return 'comma'
                case ':':
                    return 'colon'
                case _:
                    raise Exception('How did you get here? :O - Please report this issue on GitHub.')

        if lexeme[0] == '.': # Check if the lexeme is a directive
            if (lowerLexeme := lexeme.lower()) in DIRECTIVES:
                return lowerLexeme
            else:
                raise Exception('Invalid directive: ' + lexeme)

        elif lexeme[0] == '_': # Check if the lexeme is a label
            if all(char in LETTERS for char in lexeme[1:]):
                return 'label'
            else:
                raise Exception('Invalid label: ' + lexeme)

        elif lexeme[0] == '&':
            if (registerNumber := int(lexeme[1:])) == 0:
                raise Exception('Register &0 is reserved for the assembler.')
            elif registerNumber in range(1, 16):
                return 'acRegister'
            else:
                raise Exception('Invalid AC register: ' + lexeme)

        if (lowerLexeme := lexeme.lower()) in INSTRUCTIONS:
            return lowerLexeme
        
    def getTokenStream(self) -> list:
        return self.tokenStream
