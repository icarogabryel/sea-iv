from utils import Byte
import re


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

        # if the bytes have notations like {la;_loop;5-0} substitute the label with the address
        for byte in self.bytes:
            haveLabel = re.search(r'\{.*\}', byte.byte)
            
            if haveLabel:
                labelIndication = haveLabel.group(0)[1:-1] # pick the section between the curly braces
                label, bits = labelIndication.split(';') # split the label name and the slice indication

                if label not in self.labelTable:
                    raise Exception(f'Label {label} not found')
                
                labelInBin = bin(self.labelTable[label])[2:].zfill(16)
                bitsRange = bits.split('-')
                start = int(bitsRange[0])
                end = int(bitsRange[1])
                start = len(labelInBin) - start - 1
                end = len(labelInBin) - end
                labelCutted = labelInBin[start:end] # get the slice of the label
                self.rawBytesList.append(re.sub(r'\{.*\}', labelCutted, byte.byte)) # substitute the label with the slice
            else:
                self.rawBytesList.append(byte.byte)
