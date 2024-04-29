IGNORED_CHARS = [' ', '\n', '\t']


class Scanner:
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
    
    def getNextToken(self) -> tuple:
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
        
        if self.getCurrentChar().isdecimal(): # Return NUMBER token
            return ('NUMBER', self.getNumber())

    def advance(self) -> None:
        self.index += 1

    def getCurrentChar(self) -> str:
        return self.asmCode[self.index] if self.index < len(self.asmCode) else None
    
    def isEOF(self) -> bool:
        return True if self.getCurrentChar() == None else False
    
    def getNumber(self) -> tuple:
        number = ''
        
        while True:
            number += self.getCurrentChar()
            self.advance()

            if self.isEOF() or self.getCurrentChar() in IGNORED_CHARS:
                break
        
        return int(number)

    def getTokenStream(self) -> list:
        return self.tokenStream
