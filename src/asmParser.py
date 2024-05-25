from util import INSTRUCTIONS


class Node:
    def __init__(self, nodeType) -> None:
        self.nodeType = nodeType
        self.children = []

    def __repr__(self) -> str:
        return self.nodeType + ' -> ' + str(self.children)

    def addChild(self, child) -> None:
        self.children.append(child)

    def addChildren(self, children) -> None:
        self.children.extend(children)


class Parser:
    def __init__(self, tokenStream: list) -> None:
        self.tokenStream = tokenStream
        self.index = 0

        self.ast = Node

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

        if self.getCurrentToken()[0] == '.text': # todo - add more sections
            node.addChild(self.textField())
        
        return node
    
    def textField(self) -> Node:
        if self.getCurrentToken()[0] == '.text':
            node = Node('Text Field')
            self.advance()
        else:
            raise Exception('Syntactical error - unexpected token. Expected .text. Got ' + self.getCurrentToken()[0])

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
        if self.getCurrentToken()[0] in INSTRUCTIONS:
            node = Node('instruction')
            self.advance()
            
            return node

        else:
            raise Exception('Syntactical Error - Unexpected token. Expected instruction or label declaration. Got ' + self.getCurrentToken()[0])

    def labelDec(self) -> Node:
        node = Node('labelDec')
        self.advance()

        if self.getCurrentToken()[0] == 'colon':
            self.advance()
        else:
            raise Exception('Syntactical Error - Expected : after label declaration. Got ' + self.getCurrentToken()[0])
        
        return node
