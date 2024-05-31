from asm_parser import Node

OPCODES = {'add': '000001', 'sub': '000010'}
INST_FUNC = [lambda: RTypeInst]

def decToBin(dec):
    return bin(int(dec))

class Line:
    def __init__(self) -> None:
        self.inst = ''
        self.label = ''

    def __repr__(self) -> str:
        return f'{self.label + ' ' * (8 - len(self.label))} | {self.inst}'

def generate(ast) -> None:
    return asmCode(ast) # todo: chance to accept multiple children
    
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
                lines.append(inst(child))
            
            elif child.type == 'labelDec':
                lines.append(label(child))

        return lines
    
    else:
        raise Exception('SEMANTICAL ERROR: Expected "Text Field". Got "' + Node.type + '"')
    
def inst(node: Node) -> Line:
    if (type := node.type) == 'inst':
        line = Line()

        opcode = OPCODES[node.lexeme.lower()]

        ac = acReg(node.children[0])
        rf1 = rfReg(node.children[1])
        rf2 = rfReg(node.children[2])

        line.inst = opcode + ac + rf1 + rf2
        
        return line
    
    else:
        raise Exception('SEMANTICAL ERROR: Expected "inst". Got "' + type + '"')
    
def acReg(node: Node) -> str:
    if (type := node.type) == 'acReg':
        return decToBin(node.lexeme)[2:].zfill(2)
    
    else:
        raise Exception('SEMANTICAL ERROR: Expected "acReg". Got "' + type + '"')
    
def rfReg(node: Node) -> str:
    if (type := node.type) == 'rfReg':
        return decToBin(node.lexeme)[2:].zfill(4)
    
    else:
        raise Exception('SEMANTICAL ERROR: Expected "rfReg". Got "' + type + '"')
    
def label(node: Node) -> str:
    if (type := node.type) == 'labelDec':
        line = inst(node.children[0])
        line.label = node.lexeme

        return line
    
    else:
        raise Exception('SEMANTICAL ERROR: Expected "label". Got "' + type + '"')
