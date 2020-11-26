"""
This File Handles A World

Class
-----
World - A Single World Handler
"""

from chunkhandler import Chunk
from playerhandler import Player
from opensimplex import OpenSimplex
from OpenGL.GL import GL_QUADS, glBegin, glEnd
from vector import Vector3
import numpy as np
from math import pow
from pprint import pprint
from random import randint
from threading import Thread
from time import time


class World:
    """
    This Class Handles the World in Minecraft

    Parameters
    ----------
    player : Player
        Player Class To get the Camera Class within it

    Attributes
    ----------
    player : Player
        Player Class To get the Camera Class within it

    chunks: dict
        Key: Vector3 which is the Bottom Centre
        Value: Chunk
    """

    def __init__(self, player: Player):
        self.player = player
        
        self.noise = OpenSimplex(
            seed=randint(10000, 99999)
        )

        self.chunkSize = Vector3(8, 8, 8)
        self.halfChunk = self.chunkSize / 2

        self.adjacentChunkOffsets = [
            Vector3(0, 0, -1),
            Vector3(0, 0, 1),
            Vector3(-1, 0, 0),
            Vector3(1, 0, 0),
        ]

        self.chunks = {
            # BottomCentrePos : Chunk
        }

    def generateChunks(self):
        s = time()

        size = 1
        for chunkMultX in range(-size, size+1):
            for chunkMultY in range(-size, size+1):
                chunkPosition = self.chunkSize * Vector3(chunkMultX, 0, chunkMultY)
                self.chunks[chunkPosition] = Chunk(chunkPosition, self.chunkSize, self.noise)

        print("Finished Gen Chunks", round(time() - s, 2))

    def draw(self):
        for chunk in self.chunks.values():
            chunk.draw()

    def generateBlocks(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.generateBlocks()

        print("Finished Gen Blocks", round(time() - s, 2))

    def bindBlocks(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.bindBlocks()

        print("Finished Bind Blocks", round(time() - s, 2))

    def linkChunks(self):
        s = time()

        for chunkPos, chunk in self.chunks.items():
            adjacentData = {}

            for chunkOffset in self.adjacentChunkOffsets:
                newChunkPos = chunkPos + (chunkOffset * self.chunkSize)

                adjacentData[chunkOffset] = self.chunks.get(newChunkPos, None)

            chunk.linkChunk(adjacentData)

        print("Finished Link Chunks", round(time() - s, 2))

    def updateAllSurfaces(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.updateAllSurface()

        print("Finished Update All Surfaces", round(time() - s, 2))