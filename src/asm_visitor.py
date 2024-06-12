from typing import Any
from asm_parser import Node, R_TYPE_INSTRUCTIONS


OPCODES = {
    'add': '000001',
    'sub': '000010',
}


class Line:
    def __init__(self) -> None:
        self.word = ''
        self.label = ''

    def __repr__(self) -> str:
        return f'{self.label + ' ' * (8 - len(self.label))} | {self.word}'


class Visitor:
    def __init__(self, root: Node) -> None:
        self.NODE_TYPES = {
            "asmCode": self.asmCode,
            "Data Field": self.dataField,
            "Word": self.word,
            "Number": self.number,
            "Text Field": self.textField,
            "inst": self.inst,
            "rTypeInst": self.rTypeInst,
            "acReg": self.acReg,
            "rfReg": self.rfReg,
            "labelDec": self.label
        }
        
        self.code = self.visit(root)

    def visit(self, node: Node) -> list[Line]:
        return self.NODE_TYPES[node.type](node)

    def getMachineCode(self) -> list[Line]:
        return self.code
    
    def asmCode(self, node: Node) -> list[Line]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code

    def dataField(self, node: Node) -> list[Line]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def word(self, node: Node) -> list[Line]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def number(self, node: Node) -> Line:
        if len(lexemeInBinary := bin(int(node.lexeme))[2:]) > 16:
            raise Exception('SEMANTICAL ERROR - Number out of bounds.')
        
        else:
            line = Line()
            line.word = lexemeInBinary.zfill(16)
            
            return [line]

    def textField(self, node: Node) -> list[Line]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def inst(self, node: Node) -> list[Line]: # todo: take off to put directly the instruction type
        return self.visit(node.children[0])
    
    def rTypeInst(self, node: Node) -> list[Line]:
        line = Line()

        opcode = OPCODES[node.lexeme]

        ac = self.visit(node.children[0])
        rf1 = self.visit(node.children[1])
        rf2 = self.visit(node.children[2])

        line.word = opcode + ac + rf1 + rf2

        return [line]
    
    def acReg(self, node: Node) -> str:
        addr = int(node.lexeme[1:])

        if addr == 1:
            raise Exception('SEMANTICAL ERROR - AC register 1 is reserved for the assembler.')
        
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

    def label(self, node: Node) -> list[Line]:
        code = self.visit(node.children[0])

        code[0].label = node.lexeme

        return code

# class Visitor:
#     def __init__(self, ast) -> None:
#         self.machineCode = self.asmCode(ast)

#     def decToBin(self, dec):
#         return bin(dec)[2:]

#     def getMachineCode(self) -> list[Line]:
#         return self.machineCode
        
#     def asmCode(self, node: Node) -> list[Line]:
#         code = []

#         for child in node.children:
#             if child.type == 'Data Field':
#                 code += self.dataField(child)
#             elif child.type == 'Text Field':
#                 code += self.textField(child)

#         return code
    
#     def dataField(self, node: Node) -> str:
#         if node.type == 'Data Field':
#             code = []

#             for child in node.children:
#                 if child.type == '.word':
#                     code += self.word(child)
                
#                 elif child.type == 'labelDec':
#                     code += self.label(child)

#             return code
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "Data Field". Got "' + Node.type + '".')

#     def textField(self, node: Node) -> str:
#         if node.type == 'Text Field':
#             code = []

#             for child in node.children:
#                 if child.type == 'inst':
#                     code += self.inst(child)
                
#                 elif child.type == 'labelDec':
#                     code += self.label(child)

#             return code
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "Text Field". Got "' + Node.type + '".')
        
#     def inst(self, node: Node) -> list[Line]:
#         if (type := node.type) == 'inst':
#             if (mnemonic := node.children[0].lexeme) in R_TYPE_INSTRUCTIONS:
#                 return self.rTypeInst(node.children[0])
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "inst". Got "' + type + '".')

#     def rTypeInst(self,node: Node) -> list[Line]:
#         if (type := node.type) == 'rTypeInst':
#             line = Line()

#             opcode = OPCODES[node.lexeme]

#             ac = self.acReg(node.children[0])
#             rf1 = self.rfReg(node.children[1])
#             rf2 = self.rfReg(node.children[2])

#             line.inst = opcode + ac + rf1 + rf2
            
#             return [line]
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "rTypeInst". Got "' + type + '".')

#     def acReg(self, node: Node) -> str:
#         if (type := node.type) == 'acReg':
#             addr = int(node.lexeme[1:])

#             if addr == 1:
#                 raise Exception('SEMANTICAL ERROR - AC register 1 is reserved for the assembler.')
            
#             elif addr not in [0, 2, 3]:
#                 raise Exception('SEMANTICAL ERROR - AC register address out of bounds.')
#             else:
#                 return self.decToBin(addr).zfill(2)
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "acReg". Got "' + type + '".')
        
#     def rfReg(self, node: Node) -> str:
#         if (type := node.type) == 'rfReg':
#             addr = int(node.lexeme[1:])

#             if addr == 0:
#                 raise Exception('SEMANTICAL ERROR - RF register 0 is read-only.')
            
#             elif addr == 1:
#                 raise Exception('SEMANTICAL ERROR - RF register 0 is reserved for the assembler.')
            
#             elif addr == 14:
#                 raise Exception('SEMANTICAL ERROR - RF register 14 is the stack pointer register.')
            
#             elif addr == 15:
#                 raise Exception('SEMANTICAL ERROR - RF register 15 is the link register.')
            
#             elif addr not in range(2, 14):
#                 raise Exception('SEMANTICAL ERROR - RF register address out of bounds.')
            
#             else:
#                 return self.decToBin(addr).zfill(4)
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "rfReg". Got "' + type + '".')
        
#     def label(self, node: Node) -> str:
#         if (type := node.type) == 'labelDec':
#             line = self.inst(node.children[0])[0]
#             line.label = node.lexeme

#             return [line]
        
#         else:
#             raise Exception('SEMANTICAL ERROR - Expected "label". Got "' + type + '".')
