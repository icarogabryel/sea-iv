def byteToHex(byte: str) -> str:
    return hex(int(byte, 2))[2:]

def loader(machineCode: str) -> None:
    with open('program.txt') as file:
        for line in machineCode.split('\n'):
            file.write(byteToHex(line[:8]) + '\n' + byteToHex(line[8:]) + '\n')
