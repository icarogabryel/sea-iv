import regex as re


IGNORED_CHARS = ' \n\t'
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS = ',:'
ALPHABET = NUMBERS + LETTERS + SYMBOLS + '._&$'
TOKEN_ENDS = IGNORED_CHARS + SYMBOLS
DIRECTIVES = ['.text']


class Lexer:
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
        
        if self.getCurrentChar() == '#': # Ignore comments
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
                raise Exception('LEXICAL ERROR - Invalid character: ' + self.getCurrentChar())
            
            lexeme += self.getCurrentChar()
            self.advance()
        
        return lexeme
    
    def getTokenLabel(self, lexeme: str) -> str:
        if lexeme in SYMBOLS: # Check if the lexeme is a symbol
            match lexeme:
                case ',':
                    return 'comma'
                
                case ':':
                    return 'colon'
                
                case _:
                    raise Exception('LEXICAL ERROR - How did you get here? :O - Please report this issue on GitHub.')

        elif lexeme in DIRECTIVES:
            match lexeme:
                case '.data':
                    return 'data_dir'
                case '.text':
                    return 'text_dir'
                case _:
                    raise Exception('LEXICAL ERROR - How did you get here? :O - Please report this issue on GitHub.')
        
        elif bool(re.match(r'^_[a-z0-9_]+$', lexeme)): # Check if the lexeme is a label
            return 'label'
        
        elif bool(re.match(r'^[a-z]+$', lexeme)): # Check if the lexeme is a mnemonic
            return 'mnemonic'
        
        elif bool(re.match(r'^&(0|[1-9][0-9]*)$', lexeme)): # Check if the lexeme is an AC register
            return 'acReg'
        
        elif bool(re.match(r'^\$(0|[1-9][0-9]*)$', lexeme)): # Check if the lexeme is a RF register
            return 'rfReg'
        
        else:
            raise Exception('LEXICAL ERROR - Invalid lexeme: ' + lexeme)
        
    def getTokenStream(self) -> list:
        return self.tokenStream
