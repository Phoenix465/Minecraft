from vector import *
import pygame.mouse as mouse
from errors import *
from blockhandler import *
from enums import *
from pprint import pprint
from random import randint
from time import time


class Chunk:
    def __init__(self, bottomCentre: Vector3, size: Vector3):
        self.size = size
        self.bottomCentre = bottomCentre

        self.mouse0Debounce = False
        self.mouse2Debounce = False

        self.mouse0LastRegistered = time()
        self.mouse2LastRegistered = time()

        self.mouse0Timeout = 0.1
        self.mouse2Timeout = 0.1

        self.blocks = []
        self.blocksCanSee = []

        self.adjacentBlockData = [
            Vector3(0, 1, 0),
            Vector3(0, -1, 0),

            Vector3(0, 0, 1),
            Vector3(0, 0, -1),

            Vector3(-1, 0, 0),
            Vector3(1, 0, 0),
        ]

        self.highlightedBlock = None
        self.highlightedSurfaceIndex = None

        for y in range(self.size.Y):
            blockType = BlockType.AIR

            if y == 4:
                blockType = BlockType.GRASS
            elif y == 0:
                blockType = BlockType.STONE
            elif y < 4:
                blockType = BlockType.DIRT

            self.blocks.append([])
            for x in range(self.size.X):
                self.blocks[y].append([])
                for z in range(self.size.Z):
                    newBlock = Block(
                        Vector3(x, y, z),
                        blockType,
                        sideLength=1
                    )
                    newBlock.blockPosChunk = Vector3(x, y, z)
                    self.blocks[y][x].append(newBlock)

        self.updateAllSurface()

    def updateAllSurface(self):
        self.blocksCanSee = []
        for yI, yList in enumerate(self.blocks):
            for xI, xList in enumerate(yList):
                for bI, block in enumerate(xList):
                    self.updateBlockSurfaces(block)

    def updateBlockSurfaces(self, block):
        pos = block.blockPosChunk

        if block.blockType == enums.BlockType.AIR:
            block.surfacesShow = [False] * 6
            return

        for i, adjacentBlockCoordAdjust in enumerate(self.adjacentBlockData):
            adjustCoord = pos + adjacentBlockCoordAdjust

            adjacentBlock = None

            if not (any(map(lambda num: num < 0, adjustCoord.tuple)) or
                    any([num >= self.size.tuple[numI] for numI, num in enumerate(adjustCoord.tuple)])):
                adjacentBlock = self.blocks[adjustCoord.Y][adjustCoord.X][adjustCoord.Z]

            if adjacentBlock:
                if adjacentBlock.blockType == enums.BlockType.AIR:
                    block.surfacesShow[i] = True
                else:
                    block.surfacesShow[i] = False
            else:
                block.surfacesShow[i] = True

        if any(block.surfacesShow) and block not in self.blocksCanSee:
            self.blocksCanSee.append(block)
            block.showBlockPos = len(self.blocksCanSee) - 1
        elif not any(block.surfacesShow) and block in self.blocksCanSee:
            self.blocksCanSee.remove(block)

    def updateSurfacesAroundBlock(self, block):
        pos = block.blockPosChunk

        for i, adjacentBlockCoordAdjust in enumerate(self.adjacentBlockData):
            adjustCoord = pos + adjacentBlockCoordAdjust

            if not (any(map(lambda num: num < 0, adjustCoord.tuple)) or
                    any([num >= self.size.tuple[numI] for numI, num in enumerate(adjustCoord.tuple)])):
                self.updateBlockSurfaces(self.blocks[adjustCoord.Y][adjustCoord.X][adjustCoord.Z])

    def draw(self):
        for block in self.blocksCanSee:
            block.drawSolid()
    
    def removeBlock(self, block: Block):
        self.blocksCanSee.remove(block)

        self.highlightedBlock.blockType = enums.BlockType.AIR
        self.updateBlockSurfaces(block)
        self.updateSurfacesAroundBlock(block)

    def addBlock(self, block: Block, surfaceIndex: int):
        addition = self.adjacentBlockData[surfaceIndex]

        newBlockPos = block.blockPosChunk + addition

        if any([num >= self.size.tuple[numI] for numI, num in enumerate(newBlockPos.tuple)]):
            return

        targetBlock = self.blocks[newBlockPos.Y][newBlockPos.X][newBlockPos.Z]

        if targetBlock.blockType != enums.BlockType.AIR:
            return

        randomBlockType = enums.BlockType(randint(1, 4))
        targetBlock.blockType = randomBlockType
        self.updateBlockSurfaces(targetBlock)
        self.updateSurfacesAroundBlock(targetBlock)

    def HandleMouseClicks(self):
        currrentTime = time()

        if self.mouse0LastRegistered + self.mouse0Timeout < currrentTime:
            self.mouse0Debounce = False

        if self.mouse2LastRegistered + self.mouse2Timeout < currrentTime:
            self.mouse2Debounce = False

        if not self.mouse0Debounce and mouse.get_pressed()[0]:
            self.mouse0Debounce = True
            self.mouse0LastRegistered = time()

            if self.highlightedBlock:
                self.removeBlock(self.highlightedBlock)

        if not self.mouse2Debounce and mouse.get_pressed()[2]:
            self.mouse2Debounce = True
            self.mouse2LastRegistered = time()

            if self.highlightedBlock and (self.highlightedSurfaceIndex is not None):
                print("Spawning Block")
                self.addBlock(self.highlightedBlock, self.highlightedSurfaceIndex)
            elif self.highlightedBlock:
                print(self.highlightedSurfaceIndex)
