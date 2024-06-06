from asm_parser import Node, R_TYPE_INSTRUCTIONS


OPCODES = {'add': '000001', 'sub': '000010'}


class Line:
    def __init__(self) -> None:
        self.inst = ''
        self.label = ''

    def __repr__(self) -> str:
        return f'{self.label + ' ' * (8 - len(self.label))} | {self.inst}'


def decToBin(dec):
    return bin(dec)[2:]

def generateMachineCode(ast) -> None:
    return asmCode(ast)
    
def asmCode(node: Node) -> list[Line]:
    lines = []

    for child in node.children: # todo: add others fields
        if child.type == 'Text Field':
            lines += textField(child)

    return lines

def textField(node: Node) -> str:
    if node.type == 'Text Field':
        lines = []

        for child in node.children:
            if child.type == 'inst':
                lines += inst(child)
            
            elif child.type == 'labelDec':
                lines += label(child)

        return lines
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "Text Field". Got "' + Node.type + '".')
    
def inst(node: Node) -> list[Line]:
    if (type := node.type) == 'inst':
        if (mnemonic := node.children[0].lexeme) in R_TYPE_INSTRUCTIONS:
            return rTypeInst(node.children[0])
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "inst". Got "' + type + '".')

def rTypeInst(node: Node) -> list[Line]:
    if (type := node.type) == 'rTypeInst':
        line = Line()

        opcode = OPCODES[node.lexeme]

        ac = acReg(node.children[0])
        rf1 = rfReg(node.children[1])
        rf2 = rfReg(node.children[2])

        line.inst = opcode + ac + rf1 + rf2
        
        return [line]
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "rTypeInst". Got "' + type + '".')

def acReg(node: Node) -> str:
    if (type := node.type) == 'acReg':
        addr = int(node.lexeme[1:])

        if addr == 1:
            raise Exception('SEMANTICAL ERROR - AC register 1 is reserved for the assembler.')
        
        elif addr not in [0, 2, 3]:
            raise Exception('SEMANTICAL ERROR - AC register address out of bounds.')
        else:
            return decToBin(addr).zfill(2)
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "acReg". Got "' + type + '".')
    
def rfReg(node: Node) -> str:
    if (type := node.type) == 'rfReg':
        addr = int(node.lexeme[1:])

        if addr == 0:
            raise Exception('SEMANTICAL ERROR - RF register 0 is read-only.')
        
        elif addr == 1:
            raise Exception('SEMANTICAL ERROR - RF register 0 is reserved for the assembler.')
        
        elif addr == 14:
            raise Exception('SEMANTICAL ERROR - RF register 14 is the stack pointer register.')
        
        elif addr == 15:
            raise Exception('SEMANTICAL ERROR - RF register 15 is the link register.')
        
        elif addr not in range(2, 14):
            raise Exception('SEMANTICAL ERROR - RF register address out of bounds.')
        
        else:
            return decToBin(addr).zfill(4)
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "rfReg". Got "' + type + '".')
    
def label(node: Node) -> str:
    if (type := node.type) == 'labelDec':
        line = inst(node.children[0])[0]
        line.label = node.lexeme

        return [line]
    
    else:
        raise Exception('SEMANTICAL ERROR - Expected "label". Got "' + type + '".')
