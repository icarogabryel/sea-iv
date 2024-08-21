from utils import Byte


class Linker:
    def __init__(self, bytes: list[Byte]) -> None:
        self.bytes: list[Byte] = bytes
        self.rawBytesList = []
        self.labelTable = {}

        self.link()

    def link(self) -> None:
        for i in range(len(self.bytes)):
            if self.bytes[i].label != '':
                self.labelTable[self.bytes[i].label] = i

    def getLabelTable(self) -> dict:
        return self.labelTable