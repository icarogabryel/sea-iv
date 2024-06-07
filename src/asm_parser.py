DATA_TYPES = {'.word': lambda self: Parser.word(self)}
R_TYPE_INSTRUCTIONS = ['add', 'sub']
INSTRUCTIONS = R_TYPE_INSTRUCTIONS

class Node:
    def __init__(self, type, lexeme: str = '\0') -> None:
        self.type = type
        self.lexeme: str = lexeme
        self.children: list[Node] = []

    def __repr__(self) -> str:
        return f'{self.type}({self.lexeme}) -> {self.children}'

    def addChild(self, child) -> None:
        self.children.append(child)


class Parser:
    def __init__(self, tokenStream: list) -> None:
        self.tokenStream = tokenStream
        self.index = 0

        self.ast = None

        self.parse()

    def getAst(self) -> Node:
        return self.ast
    
    def getCurrentToken(self) -> str:
        return self.tokenStream[self.index]
    
    def peekNextToken(self) -> str:
        return self.tokenStream[self.index + 1]
    
    def advance(self) -> None:
        self.index += 1

    def parse(self) -> None:
        self.ast = self.asmCode()

    def asmCode(self) -> Node:
        node = Node('asmCode')

        if self.getCurrentToken()[0] == '.data':
            node.addChild(self.dataField())

        if self.getCurrentToken()[0] == '.text':
            node.addChild(self.textField())
        
        return node
    
    def dataField(self) -> Node:
        if self.getCurrentToken()[0] == '.data':
            node = Node('Data Field')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".data". Got "' + self.getCurrentToken()[0] + '"')

        if (dataList := self.dataList()) != []:
            for data in dataList:
                node.addChild(data)
        
        return node
    
    def dataList(self) -> list[Node]:
        dataList = []

        if (tokenLabel := self.getCurrentToken()[0]) in DATA_TYPES:
            dataList.append(DATA_TYPES[tokenLabel](self))
        
        elif tokenLabel == 'label':
            node = self.labelDec()
            node.addChild(self.word())
            dataList.append(node)

        if (self.getCurrentToken()[0] in DATA_TYPES ) or (self.getCurrentToken()[0] == 'label'):
            for data in self.dataList():
                dataList.append(data)

        return dataList
    
    def word(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == '.word':
            node = Node('Word')
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".word". Got "' + tokenLabel + '"')
        
        node.addChild(self.number())

        currentToken = self.getCurrentToken()

        while currentToken[0] == 'comma':
            self.advance()

            node.addChild(self.number())

            currentToken = self.getCurrentToken()

        return node
    
    def number(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'number':
            node = Node('Number', self.getCurrentToken()[1])
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected number. Got "' + tokenLabel + '"')
        
        return node

    def textField(self) -> Node:
        if self.getCurrentToken()[0] == '.text':
            node = Node('Text Field')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".text". Got "' + self.getCurrentToken()[0] + '"')

        if (instList := self.instList()) != []:
            for inst in instList:
                node.addChild(inst)
        
        return node

    def instList(self) -> list[Node]:
        instList = []

        if self.getCurrentToken()[0] == 'mnemonic':
            instList.append(self.inst())
        
        elif self.getCurrentToken()[0] == 'label':
            node = self.labelDec()
            node.addChild(self.inst())
            instList.append(node)

        if (self.getCurrentToken()[1] == 'mnemonic') or (self.getCurrentToken()[0] == 'label'):
            for inst in self.instList():
                instList.append(inst)

        return instList
    
    def inst(self) -> Node:
        node = Node('inst')

        if (tokenLabel := self.getCurrentToken()[0])  == 'mnemonic':
            if (tokenLexeme := self.getCurrentToken()[1]) in R_TYPE_INSTRUCTIONS:
                node.addChild(self.rTypeInst())

            # todo: add more instruction types here
            else:
                raise Exception('SYNTACTICAL ERROR - Invalid mnemonic. Got "' + tokenLexeme + '"')

        else:
            raise Exception('SYNTACTICAL ERROR - Expected mnemonic. Got "' + tokenLabel + '"')
        
        return node

    def rTypeInst(self) -> Node:
        if (tokenlexeme := self.getCurrentToken()[1]) in R_TYPE_INSTRUCTIONS:
            node = Node('rTypeInst', tokenlexeme)
            self.advance()

            node.addChild(self.acReg())

            if self.getCurrentToken()[0] == 'comma':
                self.advance()
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected , after AC register. Got ' + self.getCurrentToken()[0] + '"')
            
            node.addChild(self.rfReg())

            if self.getCurrentToken()[0] == 'comma':
                self.advance()
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token.Expected , after AC register. Got ' + self.getCurrentToken()[0] + '"')
            
            node.addChild(self.rfReg())

            return node

        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected R-Type instruction. Got ' + tokenlexeme + '"')

    def labelDec(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'label':
            node = Node('labelDec', self.getCurrentToken()[1])
            self.advance()

            if self.getCurrentToken()[0] == 'colon':
                self.advance()
            
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected ":" after label declaration. Got "' + self.getCurrentToken()[0] + '"')
       
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected label declaration. Got "' + tokenLabel + '"')
        
        return node
        
    def acReg(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'acReg':
            node = Node('acReg', self.getCurrentToken()[1])
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected AC register. Got ' + tokenLabel + '"')
        
        return node
        
    def rfReg(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'rfReg':
            node = Node('rfReg', self.getCurrentToken()[1])
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected RF register. Got ' + tokenLabel + '"')
        
        return node
