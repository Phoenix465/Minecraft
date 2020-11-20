from enum import Enum
from colour import Colour


class BlockType(Enum):
    AIR = 1
    GRASS = 2
    DIRT = 3
    STONE = 4
    SKY = 5


class BlockColour():
    def __init__(self):
        self.coloursDict = {
            1: Colour(135, 206, 235, convertToDecimal=True),
            2: Colour(82, 105, 53, convertToDecimal=True),
            3: Colour(146, 108, 77, convertToDecimal=True),
            4: Colour(169, 163, 163, convertToDecimal=True),
            5: Colour(135, 206, 235, convertToDecimal=True),
        }

    def get(self, blockState: BlockType):
        return self.coloursDict.get(blockState.value, None)


if __name__ == "__main__":
    pass