from utils import INSTRUCTIONS, PSEUDO_INSTRUCTIONS, DATA_TYPES, Node, SyntacticError


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

    def matchLabel(self, expectedLabel) -> None:
        if (currentTokenLabel := self.getCurrentToken()[0]) == expectedLabel:
            self.advance()

        else:
            raise SyntacticError('Expected ' + expectedLabel + '. Got "' + currentTokenLabel + '"')

    def parse(self) -> None:
        self.ast = self.program()

    def program(self) -> Node:
        node = Node('Program')

        while (currentToken := self.getCurrentToken()[0]) != 'EOF':
            if currentToken == 'dataDir':
                node.addChild(self.dataField())

            elif currentToken == 'instDir':
                node.addChild(self.instField())
            
            elif currentToken == 'includeDir':
                node.addChild(self.includeDir())

            else:
                raise Exception('SYNTACTICAL ERROR: unexpected token. Expected data, instruction or include directive. Got "' + currentToken + '"')
            
        return node
    
    def includeDir(self) -> Node:
        if self.getCurrentToken()[0] == 'includeDir':
            node = Node('Include')
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".include". Got "' + self.getCurrentToken()[0] + '"')
        
        if (tokenLabel := self.getCurrentToken()[0]) == 'string':
            node.addChild(Node('String', self.getCurrentToken()[1]))
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected string. Got "' + tokenLabel + '"')
        
        return node
    
    def dataField(self) -> Node:
        if self.getCurrentToken()[0] == 'dataDir':
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
            dataList.append(self.data())
        
        elif tokenLabel == 'label':
            dataList.append(self.labelDec())
            dataList.append(self.data())

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected data or label declaration. Got "' + tokenLabel + '"')

        if (self.getCurrentToken()[0] in DATA_TYPES) or (self.getCurrentToken()[0] == 'label'):
            for data in self.dataList():
                dataList.append(data)

        return dataList
    
    def data(self) -> Node:
        match self.getCurrentToken()[0]:
            case 'spaceDir':
                return self.space()
            case 'wordDir':
                return self.word()
            case 'byteDir':
                return self.byte()
            case 'asciiDir':
                return self.ascii()
            case _:
                raise Exception('SYNTACTICAL ERROR: unexpected token. Expected data directive. Got "' + self.getCurrentToken()[0] + '"')
            
    def space(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'spaceDir':
            node = Node('Space')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".space". Got "' + tokenLabel + '"')
        
        node.addChild(self.number())

        return node
    
    def word(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'wordDir':
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
    
    def byte(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'byteDir':
            node = Node('Byte')
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".byte". Got "' + tokenLabel + '"')
        
        node.addChild(self.number())

        currentToken = self.getCurrentToken()

        while currentToken[0] == 'comma':
            self.advance()

            node.addChild(self.number())

            currentToken = self.getCurrentToken()

        return node
    
    def ascii(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'asciiDir':
            node = Node('ASCII')
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".ascii". Got "' + tokenLabel + '"')
        
        node.addChild(self.string())

        return node
    
    def string(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'string':
            node = Node('String', self.getCurrentToken()[1])
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected string. Got "' + tokenLabel + '"')
        
        return node
    
    def number(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'number':
            node = Node('Number', self.getCurrentToken()[1])
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected number. Got "' + tokenLabel + '"')
        
        return node

    def instField(self) -> Node:
        if self.getCurrentToken()[0] == 'instDir':
            node = Node('Inst Field')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".inst". Got "' + self.getCurrentToken()[0] + '"')

        if (instList := self.instList()) != []:
            for inst in instList:
                node.addChild(inst)
        
        return node

    def instList(self) -> list[Node]:
        instList = []

        tokenLabel, tokenLexeme = self.getCurrentToken()

        if tokenLabel == 'mnemonic':
            instList.append(self.inst())
        
        elif tokenLabel == 'label':
            instList.append(self.labelDec())
            instList.append(self.inst())

        if (self.getCurrentToken()[0] == 'mnemonic') or (self.getCurrentToken()[0] == 'label'):
            for inst in self.instList():
                instList.append(inst)

        return instList
    
    def inst(self) -> Node:
        tokenLabel, tokenLexeme = self.getCurrentToken()

        if tokenLabel != 'mnemonic':
            raise SyntacticError('Expected mnemonic. Got "' + tokenLabel + '"')
        
        if tokenLexeme in PSEUDO_INSTRUCTIONS:
            return self.pseudoInst()

        if tokenLexeme not in INSTRUCTIONS:
            raise SyntacticError('Invalid mnemonic: ' + tokenLexeme)
        
        instType = INSTRUCTIONS[tokenLexeme][0]
        
        match instType:
            case 'n':
                return self.nTypeInst(tokenLexeme)
            case'r':
                return self.rTypeInst(tokenLexeme)
            case 'i':
                return self.iTypeInst(tokenLexeme)
            case 's':
                return self.sTypeInst(tokenLexeme)
            case 'j':
                return self.jTypeInst(tokenLexeme)
            case 'e1':
                return self.e1TypeInst(tokenLexeme)
            case 'e2':
                return self.e2TypeInst(tokenLexeme)
            case 'e3':
                return self.e3TypeInst(tokenLexeme)
            case 'e4':
                return self.e4TypeInst(tokenLexeme)
            case _:
                raise SyntacticError('Dude, how did you get here? :O - Please report this issue on GitHub.')

    def nTypeInst(self, mnemonic) -> Node:
        node = Node('N Type Inst', mnemonic)
        self.advance()

        return node

    def rTypeInst(self, mnemonic) -> Node:
        node = Node('R Type Inst', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())

        return node
    
    def iTypeInst(self, mnemonic) -> Node:
        node = Node('I Type Inst', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.number())

        return node
    
    def sTypeInst(self, mnemonic) -> Node:
        node = Node('S Type Inst', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())
        self.matchLabel('comma')
        node.addChild(self.number())

        return node
    
    def jTypeInst(self, mnemonic) -> Node:
        node = Node('J Type Inst', mnemonic)
        self.advance()
        node.addChild(self.number())

        return node
    
    def e1TypeInst(self, mnemonic) -> Node:
        node = Node('E1 Type Inst', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())

        return node
    
    def e2TypeInst(self, mnemonic) -> Node:
        node = Node('E2 Type Inst', mnemonic)
        self.advance()
        node.addChild(self.rfReg())

        return node
    
    def e3TypeInst(self, mnemonic) -> Node:
        node = Node('E3 Type Inst', mnemonic)
        self.advance()
        node.addChild(self.acReg())

        return node
    
    def e4TypeInst(self, mnemonic) -> Node:
        node = Node('E4 Type Inst', mnemonic)
        self.advance()
        node.addChild(self.rfReg())

        return node
    
    def pseudoInst(self) -> Node:
        match (tokenLexeme := self.getCurrentToken()[1]):
            case 'jump':
                return self.jump(tokenLexeme)
            case 'mul':
                return self.mul(tokenLexeme)
            case 'div':
                return self.div(tokenLexeme)
            case 'lw':
                return self.lw(tokenLexeme)
            case 'sw':
                return self.sw(tokenLexeme)
            case 'swap':
                return self.swap(tokenLexeme)
            case _:
                raise SyntacticError('How did you get here? :O - Please report this issue on GitHub.')
            
    def jump(self, lexeme) -> Node:
        node = Node('Pseudo Jump', lexeme)
        self.advance()

        if self.getCurrentToken()[0] == 'number':
            node.addChild(self.number())
        elif self.getCurrentToken()[0] == 'label':
            node.addChild(self.label())
        else:
            raise SyntacticError('Expected number or label. Got "' + self.getCurrentToken()[0] + '"')

        return node
    
    def mul(self, lexeme) -> Node:
        node = Node('Pseudo Mul', lexeme)
        self.advance()
        node.addChild(self.rfReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())

        return node
    
    def div(self, lexeme) -> Node:
        node = Node('Pseudo Div', lexeme)
        self.advance()
        node.addChild(self.rfReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())

        return node
    
    def lw(self, mnemonic) -> Node:
        node = Node('Pseudo Load', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.label())
        self.matchLabel('lBracket')
        node.addChild(self.number())
        self.matchLabel('rBracket')

        return node
    
    def sw(self, mnemonic) -> Node:
        node = Node('Pseudo Store', mnemonic)
        self.advance()
        node.addChild(self.acReg())
        self.matchLabel('comma')
        node.addChild(self.label())
        self.matchLabel('lBracket')
        node.addChild(self.number())
        self.matchLabel('rBracket')

        return node
    
    def swap(self, mnemonic) -> Node:
        node = Node('Pseudo Swap', mnemonic)
        self.advance()
        node.addChild(self.rfReg())
        self.matchLabel('comma')
        node.addChild(self.rfReg())

        return node

    def labelDec(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'label':
            node = Node('Label Dec', self.getCurrentToken()[1])
            self.advance()

            if self.getCurrentToken()[0] == 'colon':
                self.advance()
            
            else:
                raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected ":" after label declaration. Got "' + self.getCurrentToken()[0] + '"')
       
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected label declaration. Got "' + tokenLabel + '"')
        
        return node
    
    def label(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'label':
            node = Node('Label', self.getCurrentToken()[1])
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected label. Got "' + tokenLabel + '"')
        
        return node
        
    def acReg(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'acReg':
            node = Node('AC Reg', self.getCurrentToken()[1])
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected AC register. Got ' + tokenLabel + '"')
        
        return node
        
    def rfReg(self) -> Node:
        if (tokenLabel := self.getCurrentToken()[0]) == 'rfReg':
            node = Node('RF Reg', self.getCurrentToken()[1])
            self.advance()
        
        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected RF register. Got ' + tokenLabel + '"')
        
        return node
