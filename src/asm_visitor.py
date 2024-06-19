from asm_parser import Node


OPCODES = {
    'add': '000001',
    'sub': '000010',
}

class semanticError(Exception):
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return f'SEMANTIC ERROR - {self.message}'


class Label:
    label = ''

    def __repr__(self) -> str:
        return f'Label Dec: {self.label}'


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
            case "Label Dec":
                return self.labelDec(node)
            case _:
                raise Exception('SEMANTICAL ERROR - Invalid node type.' + node.type)

    def getMachineCode(self) -> list[str|Label]:
        return self.code
    
    def program(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def include(self, node: Node) -> list[str|Label]:
        from compiler import compile

        fileName = node.children[0].lexeme[1:-1]

        with open(fileName, 'r') as f:
            input = f.read()

        return compile(input)

    def dataField(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            code += self.visit(child)

        return code
    
    def space(self, node: Node) -> list[str|Label]:
        number = node.children[0].lexeme

        return ['00000000'] * int(number)
    
    def word(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            number = self.number(child)
            number = bin(number)[2:]

            if len(number) > 16:
                raise semanticError('Number out of bounds.')
            
            number = number.zfill(16) # 16 bits length for a word

            byte1 = number[:8]
            byte2 = number[8:]

            code += [byte1, byte2]

        return code
    
    def byte(self, node: Node) -> list[str|Label]:
        code = []

        for child in node.children:
            number = self.number(child)
            number = bin(number)[2:]

            if len(number) > 8:
                raise Exception('SEMANTICAL ERROR - Byte out of bounds.')
            
            number = number.zfill(8)

            code += [number]

        return code
    
    def number(self, node: Node) -> int:
            return int(node.lexeme)
        
    def ascii(self, node: Node) -> list[str|Label]:
        string = self.string(node.children[0])

        code = []

        for char in string:
            asciiChar = bin(ord(char))[2:].zfill(8)

            code.append(asciiChar)

        return code

    def string(self, node: Node) -> str:
        return node.lexeme[1:-1]

    def instField(self, node: Node) -> list[str|Label]:
        bytes = []

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

                bytes += instBytes

        return bytes
    
    def rTypeInst(self, node: Node) -> list[Byte]:
        opcode = OPCODES[node.lexeme]

        ac = self.visit(node.children[0])
        rf1 = self.visit(node.children[1])
        rf2 = self.visit(node.children[2])

        inst = opcode + ac + rf1 + rf2

        byte1 = Byte(inst[:8])
        byte2 = Byte(inst[8:])

        return [byte1, byte2]
    
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
