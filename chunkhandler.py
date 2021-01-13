"""
Handler for the Chunks

Class
-----
Chunk - This handle a single Chunk
"""

from math import sqrt
from random import randint
from time import time

import numpy as np
import pygame.mouse as mouse

import enums
from blockhandler import Block
from vbohandler import VBOHandler
from vector import Vector3

colourHandler = enums.BlockColour()


class Chunk:
    """
    This Class handle a single chunk in Minecraft

    Parameters
    ----------
    bottomCentre : Vector3
        The Position of the Chunk for the Bottom Centre

    size : Vector3
        Size of the Chunk

    noise : opensimplex.OpenSimplex
        The OpenSimplex noise, to make sure the noise data is the same across chunks.

    Attributes
    ----------
    scale : int
        Divide Scale for the Noise Library

    size : Vector3
        Size of the Chunk

    halfSize : Vector3
        Half of the Size Vector

    bottomCentre : Vector3
        The Position of the Chunk for the Bottom Centre

    maxVector : Vector3
        The Maximum Point of the Chunk

    minVector : Vector3
        The Minimum Point of the Chunk

    mouse0Debounce : bool
        Debounce for whether the the Left-Mouse Click is already Registered

    mouse2Debounce : bool
        Debounce for whether the the Right-Mouse Click is already Registered

    mouse0LastRegistered : float
        Last Time the Left-Mouse Click was Registered

    mouse2LastRegistered : float
        Last Time the Right-Mouse Click was Registered

    mouse0Timeout : float
        Time before the Debounce of the Left-Mouse Click Ends

    mouse2Timeout : float
        Time before the Debounce of the Right-Mouse Click Ends

    blocks : list
        A empty list originally
        After generation, is a triple layer nested list. The first state is the Y, then X, then Z

    blocksCanSee : list
        A list containing Block(s) that can be seen.

    adjacentBlockData : list
        A list containing Vector3 that are relative to the surfaces on the Block class

    adjacentChunks : dict
        A Dictionary with a Vector3: Chunk format

    cornerChunks : dict
        A Dictionary with a Vector3: Chunk format.

    noise : opensimplex.OpenSimplex
        The OpenSimplex noise, to make sure the noise pattern is the same across chunks.

    highlightedBlock : None/Block
        Update by the Camera Class to check what Block is Highlighted

    highlightedSurfaceIndex : None/int
        The Surface Index of the Highlighted Surface

    chunkVBO : vbohandler.VBOHandler
        A VBO (Vector Buffer Object) of the chunk to make drawing fast.

    """

    def __init__(self, bottomCentre: Vector3, size: Vector3, noise):
        self.scale = 200

        self.size = size
        self.halfSize = size / 2

        self.bottomCentre = bottomCentre

        self.maxVector = self.bottomCentre + Vector3(
            self.halfSize.X,
            self.size.Y,
            self.halfSize.Z
        )

        self.minVector = self.bottomCentre - Vector3(
            self.halfSize.X,
            0,
            self.halfSize.Z,
        )

        self.mouse0Debounce = False
        self.mouse2Debounce = False

        self.mouse0LastRegistered = time()
        self.mouse2LastRegistered = time()

        self.mouse0Timeout = 0.1
        self.mouse2Timeout = 0.1

        self.blocks = np.array([], dtype=Block)
        self.blocksCanSee = np.array([])

        self.noise = noise

        self.adjacentChunks = {
            Vector3(0, 0, -1): None,
            Vector3(0, 0, 1): None,
            Vector3(-1, 0, 0): None,
            Vector3(1, 0, 0): None,
        }

        self.cornerChunks = {
            Vector3(1, 0, 1): None,
            Vector3(1, 0, -1): None,
            Vector3(-1, 0, 1): None,
            Vector3(-1, 0, -1): None,
        }

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

        self.chunkVBO = None

    def generateBlocks(self):
        """
        Generates the Blocks for the self.blocks

        Returns
        -------
        None
        """

        rangeValues = [-sqrt(2) / 2, sqrt(2) / 2]

        self.blocks = np.zeros(self.size.tuple, dtype=Block)
        for y in range(self.size.Y):
            #self.blocks.append([])

            for x in range(self.size.X):
                #self.blocks[y].append([])

                for z in range(self.size.Z):
                    newPos = Vector3(x - self.halfSize.X + self.bottomCentre.X, y, z - self.halfSize.Z + self.bottomCentre.Z)

                    maxSolidPoint = self.noise.noise2d(x=newPos.X / self.scale, y=newPos.Z / self.scale) + rangeValues[1]
                    maxSolidPoint *= self.size.Y / (rangeValues[1] * 2)
                    maxSolidPoint = int(maxSolidPoint)

                    blockType = enums.BlockType.AIR
                    if y == maxSolidPoint:
                        blockType = enums.BlockType.GRASS
                    elif 0 < y < maxSolidPoint:
                        blockType = enums.BlockType.DIRT
                    elif y == 0:
                        blockType = enums.BlockType.STONE

                    newBlock = Block(
                        newPos,
                        blockType,
                        sideLength=1
                    )

                    newBlock.parentChunk = self
                    newBlock.blockPosChunk = Vector3(x, y, z)

                    self.blocks[y][x][z] = newBlock

    def genChunkVBO(self):
        """
        Generates the VBO's for the Chunk

        Returns
        -------
        None
        """

        combinedChunkData = []
        self.chunkVBO = None

        for block in self.blocksCanSee:
            for i, surfaceSee in enumerate(block.surfacesShow):
                if not surfaceSee:
                    continue

                blockQuad = block.surfaces[i]
                normal = block.normals[i]
                colour = colourHandler.get(block.blockType)

                surfacesList = [block.vertices[blockVertex] for blockVertex in blockQuad]

                for vector3 in surfacesList:
                    combined = vector3.list + colour.RGBList + normal.list

                    for comb in combined:
                        combinedChunkData.append(comb)

        self.chunkVBO = VBOHandler(combinedChunkData)

    def linkChunk(self, adjacentChunkData, cornerChunkData):
        """
        Sets the chunk adjacent to this one

        Parameters
        ----------
        adjacentChunkData : dict
            A dict containing the vector offset : chunks adjacent to this one

        Returns
        -------
        None
        """

        self.adjacentChunks = adjacentChunkData
        self.cornerChunks = cornerChunkData

    def updateAllSurface(self):
        """
        Updates All Surfaces of each Block inside the self.Blocks, to see whether a surface should be visible or not

        Returns
        -------
        None
        """

        self.blocksCanSee = []
        for yI, yList in enumerate(self.blocks):
            for xI, xList in enumerate(yList):
                for bI, block in enumerate(xList):
                    self.updateBlockSurfaces(block)

    def updateBlockSurfaces(self, block):
        """
        Updates A Single Block's Surfaces and can either Add or Remove them from self.blocksCanSee

        Parameters
        ----------
        block : Block
            A Block which should be inside the self.blocks

        Returns
        -------
        None
        """

        pos = block.blockPosChunk
        skip = False

        if block.blockType == enums.BlockType.AIR:
            block.surfacesShow = [False] * 6
            skip = True

        for i, adjacentBlockCoordAdjust in enumerate(self.adjacentBlockData):
            if skip:
                break

            adjustCoord = pos + adjacentBlockCoordAdjust

            adjacentBlock = None

            if not (any(map(lambda num: num < 0, adjustCoord.tuple)) or
                    any([num >= self.size.tuple[numI] for numI, num in enumerate(adjustCoord.tuple)])):
                adjacentBlock = self.blocks[adjustCoord.Y][adjustCoord.X][adjustCoord.Z]
            else:
                # Look in the Adjacent Chunk
                offsetCoord = [
                    (num if not num >= self.size.tuple[numI] else 1)
                    if not 0 < num < self.size.tuple[numI] else 0 for numI, num in enumerate(adjustCoord.tuple)
                ]
                offsetCoord = Vector3(*offsetCoord)

                if offsetCoord.Y == 0:
                    adjacentChunk = self.adjacentChunks[offsetCoord]
                    #print(offsetCoord)
                    if adjacentChunk:
                        newCoord = Vector3(*adjustCoord.tuple)

                        if newCoord.X >= self.size.X:
                            newCoord.X = 0
                        elif newCoord.X < 0:
                            newCoord.X = self.size.X - 1

                        if newCoord.Z >= self.size.Z:
                            newCoord.Z = 0
                        elif newCoord.Z < 0:
                            newCoord.Z = self.size.Z - 1

                        adjacentBlock = adjacentChunk.blocks[newCoord.Y][newCoord.X][newCoord.Z]

            if adjacentBlock:
                if adjacentBlock.blockType == enums.BlockType.AIR:
                    block.surfacesShow[i] = True
                else:
                    block.surfacesShow[i] = False
            else:
                block.surfacesShow[i] = True

        if any(block.surfacesShow) and (block not in self.blocksCanSee):
            self.blocksCanSee = np.append(self.blocksCanSee, [block])

            #self.blocksCanSee.append(block)

        elif not any(block.surfacesShow) and (block in self.blocksCanSee):
            self.blocksCanSee = np.delete(self.blocksCanSee, np.where(self.blocksCanSee == block))

            #self.blocksCanSee.remove(block)

    def updateSurfacesAroundBlock(self, block):
        """
        Applies the self.updateBlockSurfaces for the adjacent Blocks around the block Parameter

        Parameters
        ----------
        block : Block
            The Block in which the adjacent Blocks should be Updated

        Returns
        -------
        None
        """

        pos = block.blockPosChunk

        for i, adjacentBlockCoordAdjust in enumerate(self.adjacentBlockData):
            adjustCoord = pos + adjacentBlockCoordAdjust

            if not (any(map(lambda num: num < 0, adjustCoord.tuple)) or
                    any([num >= self.size.tuple[numI] for numI, num in enumerate(adjustCoord.tuple)])):
                self.updateBlockSurfaces(self.blocks[adjustCoord.Y][adjustCoord.X][adjustCoord.Z])
            else:
                # Look in the Adjacent Chunk
                offsetCoord = [
                    (num if not num >= self.size.tuple[numI] else 1)
                    if not 0 < num < self.size.tuple[numI] else 0 for numI, num in enumerate(adjustCoord.tuple)
                ]
                offsetCoord = Vector3(*offsetCoord)

                if offsetCoord.Y == 0:
                    adjacentChunk = self.adjacentChunks[offsetCoord]
                    #print(offsetCoord)
                    if adjacentChunk:
                        newCoord = Vector3(*adjustCoord.tuple)

                        if newCoord.X >= self.size.X:
                            newCoord.X = 0
                        elif newCoord.X < 0:
                            newCoord.X = self.size.X - 1

                        if newCoord.Z >= self.size.Z:
                            newCoord.Z = 0
                        elif newCoord.Z < 0:
                            newCoord.Z = self.size.Z - 1

                        adjacentChunk.updateBlockSurfaces(adjacentChunk.blocks[newCoord.Y][newCoord.X][newCoord.Z])

    def isPointInChunk(self, point: Vector3, isList=False):
        #print(minVector, "||", maxVector)
        if isList:
            return self.minVector.X <= point[0] < self.maxVector.X and self.minVector.Y <= point[1] <= self.maxVector.Y and self.minVector.Z <= point[2] < self.maxVector.Z

        return self.minVector.X <= point.X < self.maxVector.X and self.minVector.Y <= point.Y <= self.maxVector.Y and self.minVector.Z <= point.Z < self.maxVector.Z

    def draw(self):
        """
        Draws the Blocks which can be Seen

        Returns
        -------
        None
        """

        if self.chunkVBO: self.chunkVBO.draw()

    def removeBlock(self, block: Block):
        """
        Removes a Block and Updates it's surfaces and the Blocks around it

        Parameters
        ----------
        block : Block
            The block which should be removed

        Returns
        -------
        None
        """

        self.highlightedBlock.blockType = enums.BlockType.AIR

        self.updateBlockSurfaces(block)
        self.updateSurfacesAroundBlock(block)
        self.genChunkVBO()
        self.updateVBOChunkAdjacent()

    def addBlock(self, block: Block, surfaceIndex: int):
        """
        Adds a Block based on the surfaceIndex and Updates it's surfaces and the Blocks around it

        Parameters
        ----------
        block : Block
            The block which the new Block will be added on Relative to the surfaceIndex

        surfaceIndex : int
            The Surface Relative to the Block

        Returns
        -------
        None
        """

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
        self.genChunkVBO()
        self.updateVBOChunkAdjacent()

    def updateVBOChunkAdjacent(self):
        """
        Updates the Chunk adjacent to this Chunk

        Returns
        -------
        None
        """

        for chunk in self.adjacentChunks.values():
            if chunk:
                chunk.genChunkVBO()

    def HandleMouseClicks(self):
        """
        Handles the Add/Remove Block based on the Mouse Click

        Returns
        -------
        None
        """
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
                self.addBlock(self.highlightedBlock, self.highlightedSurfaceIndex)
            elif self.highlightedBlock:
                pass
                #print(self.highlightedSurfaceIndex)
