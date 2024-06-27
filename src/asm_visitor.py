from utils import INSTRUCTIONS
from asm_parser import Node


class semanticError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f'SEMANTIC ERROR - {self.message}'


class Byte:
    def __init__(self, byte: str) -> None:
        self.byte = byte
        self.label = ''

    def __repr__(self) -> str:
        return f'{self.label}: {self.byte}' if len(self.label) > 0 else self.byte


class Visitor:
    def __init__(self, root: Node) -> None:       
        self.code = self.visit(root)

        labelTable = {}

    def visit(self, node: Node):
        match node.type:
            case "Program":
                return self.program(node)
            case 'Include':
                return self.include(node)
            case "Data Field":
                return self.dataField(node)
            case "Space":
                return self.space(node)
            case "Word":
                return self.word(node)
            case 'Byte':
                return self.byte(node)
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
            case _:
                raise Exception('SEMANTICAL ERROR - Invalid node type.' + node.type)

    def getMachineCode(self) :
        return self.code
    
    def program(self, node: Node) :
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def include(self, node: Node):
        from compiler import compile

        fileName = node.children[0].lexeme[1:-1]

        with open(fileName, 'r') as f:
            input = f.read()

        return compile(input)

    def dataField(self, node: Node):
        codeBytes = []

        hasLabel = False
        tempLabel = ''

        for child in node.children:
            if child.type == 'Label Dec':
                hasLabel = True
                tempLabel = child.lexeme

            else:
                match child.type:
                    case 'Space':
                        dataBytes = self.space(child)
                    case 'Word':
                        dataBytes = self.word(child)
                    case 'Byte':
                        dataBytes = self.byte(child)
                    case 'ASCII':
                        dataBytes = self.ascii(child)
                    case _:
                        raise Exception('SEMANTICAL ERROR - Invalid node type.' + child.type)

                if hasLabel:
                    dataBytes[0].label = tempLabel
                    hasLabel = False
                    tempLabel = ''

                codeBytes += dataBytes

        return codeBytes
    
    def space(self, node: Node):
        number = node.children[0].lexeme

        codeBytes = []

        for i in range(int(number)):
            codeByte = Byte('00000000')
            codeBytes.append(codeByte)

        return codeBytes
    
    def word(self, node: Node):
        codeBytes = []

        for child in node.children:
            number = self.number(child)
            number = bin(number)[2:]

            if len(number) > 16:
                raise semanticError('Number out of bounds.')
            
            number = number.zfill(16) # 16 bits length for a word

            byte1 = Byte(number[:8])
            byte2 = Byte(number[8:])

            codeBytes += [byte1, byte2]

        return codeBytes
    
    def byte(self, node: Node):
        code = []

        for child in node.children:
            number = self.number(child)
            number = bin(number)[2:]

            if len(number) > 8:
                raise Exception('SEMANTICAL ERROR - Byte out of bounds.')
            
            number = number.zfill(8)

            code += [Byte(number)]

        return code
    
    def number(self, node: Node) -> int:
            return int(node.lexeme)
        
    def ascii(self, node: Node):
        string = self.string(node.children[0])

        code = []

        for char in string:
            asciiChar = bin(ord(char))[2:].zfill(8)

            code.append(Byte(asciiChar))

        return code

    def string(self, node: Node) -> str:
        return node.lexeme[1:-1]

    def instField(self, node: Node):
        codeBytes = []

        hasLabel = False
        tempLabel = ''

        for child in node.children:
            if child.type == 'Label Dec':
                hasLabel = True
                tempLabel = child.lexeme
            
            else:
                match child.type:
                    case 'R Type Inst':
                        instBytes = self.rTypeInst(child)

                if hasLabel:
                    instBytes[0].label = tempLabel
                    hasLabel = False
                    tempLabel = ''

                codeBytes += instBytes

        return codeBytes
    
    def rTypeInst(self, node: Node):
        opcode = INSTRUCTIONS[node.lexeme] # get opcode

        # get registers numbers
        ac = self.visit(node.children[0])

        if ac == 1:
            raise semanticError('AC register 1 is reserved for the assembler.') # AC1 is unavailable for writing
        
        rf1 = self.visit(node.children[1])
        rf2 = self.visit(node.children[2])

        if rf1 < 0 or rf1 > 15:
            raise semanticError('RF register out of bounds.')
        
        # convert to binary
        ac = bin(ac)[2:].zfill(2)
        rf1 = bin(rf1)[2:].zfill(4)
        rf2 = bin(rf2)[2:].zfill(4)

        # concatenate to form instruction
        inst = opcode + ac + rf1 + rf2

        # split into two bytes
        byte1 = Byte(inst[:8])
        byte2 = Byte(inst[8:])

        return [byte1, byte2]
    
    def acReg(self, node: Node) -> int:
        acNumber = int(node.lexeme[1:])

        if acNumber < 0 or acNumber > 3:
            raise semanticError('AC register out of bounds.')   
        
        return acNumber
        
    def rfReg(self, node: Node) -> int:
        rfNumber = int(node.lexeme[1:])

        if rfNumber < 0 or rfNumber > 15:
            raise semanticError('RF register out of bounds.')
        
        return rfNumber
