class Node:
    def __init__(self) -> None:
        self.type = ''
        self.children = []

    def addChild(self, child) -> None:
        self.children.append(child)

class Parser:
    def __init__(self, tokenStream: list) -> None:
        self.tokenStream = tokenStream
        self.index = 0

        self.ast = Node

        self.parse()

    def parse(self) -> None:
        self.ast = self.asmCode()

    def asmCode(self) -> Node:
        node = Node

        while True:
            node = self.instruction()

            if node is None:
                break

        return node