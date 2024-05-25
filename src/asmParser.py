from util import INSTRUCTIONS


class Node:
    def __init__(self, type, lexeme = '\0') -> None:
        self.type = type
        self.lexeme = lexeme
        self.children = []

    def __repr__(self) -> str:
        return f'{self.type}({self.lexeme}) -> {self.children}'

    def addChildren(self, child) -> None:
        if type(child) is list:
            self.children.extend(child)
        else:
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

        # if (currentToken := self.getCurrentToken()[0]) == '.data': # todo: create data section

        if (currentToken := self.getCurrentToken()[0]) == '.text':
            node.addChildren(self.textField())
        
        return node
    
    def textField(self) -> Node:
        if self.getCurrentToken()[0] == '.text':
            node = Node('Text Field')
            self.advance()

        else:
            raise Exception('SYNTACTICAL ERROR: unexpected token. Expected ".text". Got "' + self.getCurrentToken()[0] + '"')

        if (instList := self.instList()) is not None:
            node.addChildren(instList)
        
        return node

    def instList(self) -> Node:
        instList = []

        if self.getCurrentToken()[0] in INSTRUCTIONS:
            instList.append(self.inst())
        
        elif self.getCurrentToken()[0] == 'label':
            instList.append(self.labelDec())
            instList.append(self.inst())

        if self.getCurrentToken()[0] in INSTRUCTIONS or self.getCurrentToken()[0] == 'label':
            instList.extend(self.instList())

        return instList
    
    def inst(self) -> Node:
        if (currentToken := self.getCurrentToken()[0]) in INSTRUCTIONS: # todo - add inst types

            node = Node('instruction', self.getCurrentToken()[1])
            self.advance()
            
            return node

        else:
            raise Exception('SYNTACTICAL ERROR: Unexpected token. Expected instruction. Got "' + currentToken + '"')

    def labelDec(self) -> Node:
        if (currentToken := self.getCurrentToken()[0]) == 'label':
            node = Node('labelDec', self.getCurrentToken()[1])
            self.advance()

            if self.getCurrentToken()[0] == 'colon':
                self.advance()
            
            else:
                raise Exception('Syntactical Error - Expected : after label declaration. Got ' + self.getCurrentToken()[0])
       
        else:
            raise Exception('Syntactical Error - Expected label declaration. Got ' + currentToken)
        
        return node
