from typing import Any
from asm_parser import Node, R_TYPE_INSTRUCTIONS


OPCODES = {
    'add': '000001',
    'sub': '000010',
}


class Label:
    label = ''

    def __repr__(self) -> str:
        return f'Label Dec: {self.label}'

class Visitor:
    def __init__(self, root: Node) -> None:       
        self.code = self.visit(root)

        labelTable = {}

    def visit(self, node: Node) -> list[str|Label]:
        match node.type:
            case "Program":
                return self.program(node)
            case "Data Field":
                return self.dataField(node)
            case "Word":
                return self.word(node)
            case "Number":
                return self.number(node)
            case "ASCII":
                return self.ascii(node)
            case "String":
                return self.string(node)
            case "Inst Field":
                return self.instField(node)
            case "R Type Inst":
                return self.rTypeInst(node)
            case "AC Reg":
                return self.acReg(node)
            case "RF Reg":
                return self.rfReg(node)
            case "Label Dec":
                return self.labelDec(node)

    def getMachineCode(self) -> list[str|Label]:
        return self.code
    
    def program(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code

    def dataField(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def word(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def number(self, node: Node) -> str:
        if len(lexemeInBinary := bin(int(node.lexeme))[2:]) > 16:
            raise Exception('SEMANTICAL ERROR - Number out of bounds.')
        
        else:
            return [lexemeInBinary.zfill(16)]
        
    def ascii(self, node: Node) -> list[str|Label]:
        return self.visit(node.children[0])
    
    def string(self, node: Node) ->list[str|Label]:
        string = node.lexeme[1:-1]
        code = []
        
        # convert every char in ascii
        for char in string:
            code.append(bin(ord(char))[2:].zfill(16))

        return code

    def instField(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def rTypeInst(self, node: Node) -> str:
        opcode = OPCODES[node.lexeme]

        ac = self.visit(node.children[0])
        rf1 = self.visit(node.children[1])
        rf2 = self.visit(node.children[2])

        return [opcode + ac + rf1 + rf2]
    
    def acReg(self, node: Node) -> str:
        addr = int(node.lexeme[1:])

        if addr == 1:
            raise Exception('SEMANTICAL ERROR - AC register 1 is reserved for the assembler.') #! Probably error here
        
        elif addr not in [0, 2, 3]:
            raise Exception('SEMANTICAL ERROR - AC register address out of bounds.')
        
        else:
            return bin(int(addr))[2:].zfill(2)
        
    def rfReg(self, node: Node) -> str:
        addr = int(node.lexeme[1:])

        if addr == 0:
            raise Exception('SEMANTICAL ERROR - RF register 0 is read-only.') #! Probably error here
        
        elif addr == 1:
            raise Exception('SEMANTICAL ERROR - RF register 0 is reserved for the assembler.')
        
        elif addr == 14:
            raise Exception('SEMANTICAL ERROR - RF register 14 is the stack pointer register.')
        
        elif addr == 15:
            raise Exception('SEMANTICAL ERROR - RF register 15 is the link register.')
        
        elif addr not in range(2, 14):
            raise Exception('SEMANTICAL ERROR - RF register address out of bounds.')
        
        else:
            return bin(int(addr))[2:].zfill(4)

    def labelDec(self, node: Node) -> Label:
        label = Label()
        label.label = node.lexeme

        return [label]
