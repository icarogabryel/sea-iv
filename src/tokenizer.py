IGNORED_CHARS = [' ', '\n', '\t']
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
SYMBOLS = '_.:'
ALPHABET = NUMBERS + LETTERS + SYMBOLS
DIRECTIVES = ['.text']

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
  
        while True:
            if self.isEOF() or self.getCurrentChar() in IGNORED_CHARS: # Read characters until a whitespace, end token or EOF is found # todo: add token ends
                break
            
            if self.getCurrentChar() not in ALPHABET: # Check if the character is valid
                raise Exception('Invalid character: ' + self.getCurrentChar())
            
            lexeme += self.getCurrentChar()
            self.advance()
        
        return lexeme
    
    def getTokenLabel(self, lexeme: str) -> str:
        # if lexeme.isnumeric(): # todo
        #     return 'NUM'
        
        if lexeme[0] == '.': # Check if the lexeme is a directive
            lowerLexeme = lexeme.lower()

            if lowerLexeme in DIRECTIVES:
                return lowerLexeme
            else:
                raise Exception('Invalid directive: ' + lexeme)

        if lexeme[0] == '_': # Check if the lexeme is a label

            if all(char in LETTERS for char in lexeme[1:-1]) and lexeme[-1] == ':':
                return 'label'
            else:
                raise Exception('Invalid label: ' + lexeme)

    def getTokenStream(self) -> list:
        return self.tokenStream
