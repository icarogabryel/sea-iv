from asmParser import Node


class Line:
    def __init__(self) -> None:
        self.inst = ''
        self.label = ''

    def __repr__(self) -> str:
        return self.label + ' - ' + self.inst + '\n'


class Generator:
    def __init__(self, ast: Node) -> None:
        self.objCode = self.generate(ast)

    def getObjCode(self) -> str:
        return self.objCode
    
    def generate(self, ast) -> None:
        return self.asmCode(ast) # todo: chance to accept multiple children
        
    def asmCode(self, ast) -> str:
        lines = []

        for child in ast.children: # todo: add others fields
            if child.type == 'Text Field':
                lines += self.textField(child)

        return lines
        
    def textField(self, Node) -> str:
        if Node.type == 'Text Field':
            lines = []

            for child in Node.children:
                if child.type == 'inst':
                    lines.append(self.inst(child))
                
                elif child.type == 'labelDec':
                    lines.append(self.label(child))

            return lines
        
        else:
            raise Exception('SEMANTICAL ERROR: Expected "Text Field". Got "' + Node.type + '"')
        
    def inst(self, Node) -> Line:
        if (type := Node.type) == 'inst':
            line = Line()

            opcode = Node.lexeme

            ac = self.acReg(Node.children[0])
            rf1 = self.rfReg(Node.children[1])
            rf2 = self.rfReg(Node.children[2])

            line.inst = opcode.lower() + ' ' + ac + ', ' + rf1 + ', ' + rf2
            
            return line
        
        else:
            raise Exception('SEMANTICAL ERROR: Expected "inst". Got "' + type + '"')
        
    def acReg(self, Node) -> str:
        if (type := Node.type) == 'acReg':
            return Node.lexeme
        
        else:
            raise Exception('SEMANTICAL ERROR: Expected "acReg". Got "' + type + '"')
        
    def rfReg(self, Node) -> str:
        if (type := Node.type) == 'rfReg':
            return Node.lexeme
        
        else:
            raise Exception('SEMANTICAL ERROR: Expected "rfReg". Got "' + type + '"')
        
    def label(self, Node) -> str:
        if (type := Node.type) == 'labelDec':
            line = self.inst(Node.children[0])
            line.label = Node.lexeme

            return line
        
        else:
            raise Exception('SEMANTICAL ERROR: Expected "label". Got "' + type + '"')
