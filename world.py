"""
This File Handles A World

Class
-----
World - A Single World Handler
"""

from chunkhandler import Chunk
from playerhandler import Player
from opensimplex import OpenSimplex
from sys import getsizeof
from OpenGL.GL import GL_QUADS, glBegin, glEnd
from vector import Vector3
import numpy as np
from math import pow
from pprint import pprint
from random import randint
from threading import Thread
from multiprocessing import Process
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

        self.chunkSize = Vector3(16, 16, 16)
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

        self.currentChunk = None
        self.mouseTouchChunk = None

        self.adjacentCurrentChunk = {

        }

        self.memoryBlockSee = []

        self.lastPlayerPosition = Vector3(0, 0, 0)

    def generateChunks(self):
        s = time()

        size = 1
        for chunkMultX in range(-size, size+1):
            for chunkMultY in range(-size, size+1):
                chunkPosition = self.chunkSize * Vector3(chunkMultX, 0, chunkMultY)

                newChunk = Chunk(chunkPosition, self.chunkSize, self.noise)
                newChunk.parentWorld = self

                self.chunks[chunkPosition] = newChunk

        print("Finished Gen Chunks", round(time() - s, 2))

    def updateCurrentChunk(self):
        playerPos = self.player.camera.currentCameraPosition

        for chunk in self.chunks.values():
            if chunk.isPointInChunk(playerPos):
                self.currentChunk = chunk
                self.adjacentCurrentChunk = chunk.adjacentChunks

                return

        self.currentChunk = None
        self.adjacentCurrentChunk = {}

    def draw(self):
        for chunk in self.chunks.values():
            chunk.draw()

    def generateBlocks(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.generateBlocks()

        print("Finished Gen Blocks", round(time() - s, 2))

    def genChunkVBOs(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.genChunkVBO()

        print("Finished Gen Chunk VBOs", round(time() - s, 2))

    def linkChunks(self):
        s = time()

        for chunkPos, chunk in self.chunks.items():
            adjacentData = {}

            for chunkOffset in self.adjacentChunkOffsets:
                newChunkPos = chunkPos + (chunkOffset * self.chunkSize)

                adjacentData[chunkOffset] = self.chunks.get(newChunkPos, None)

            chunk.linkChunk(adjacentData)

        print("Finished Link Chunks", round(time() - s, 2))

    def setHighlightedBlockData(self):
        def multithreadChecker(chunk: Chunk, blocklist: list):
            blocklist += filter(lambda block: (block.centre - currentCameraPos).magnitude < self.player.camera.maxDist + 1, chunk.blocksCanSee)
            """for block in chunk.blocksCanSee:
                dist = (block.centre - currentCameraPos).magnitude
                if dist < self.player.camera.maxDist + 1:
                    blocklist.append(block)"""

        currentCameraPos = self.player.camera.currentCameraPosition

        s = time()

        blocksCheck = []
        threads = []
        for aroundChunk in np.array([self.currentChunk] + list(self.adjacentCurrentChunk.values())):
            if not aroundChunk:
                continue

            aroundChunk.highlightedBlock = None
            aroundChunk.highlightedSurfaceIndex = None

            threads.append(Thread(target=multithreadChecker, args=(aroundChunk, blocksCheck)))

        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()

        blocksCheck = np.array(blocksCheck)

        self.mouseTouchChunk = self.player.setHighlightedBlockData(blocksCheck)
        end = time() - s
        print("Finished Around Chunk Raycasting", end)

        if self.mouseTouchChunk:
            highlightedBlock = self.mouseTouchChunk.highlightedBlock

            if highlightedBlock:
                highlightedBlock.drawWireSurfaceShow()

        self.lastPlayerPosition = currentCameraPos

    def setup(self):
        self.generateChunks()
        self.generateBlocks()
        self.linkChunks()
        self.updateAllSurfaces()
        self.genChunkVBOs()

    def HandleMouseClicks(self):
        if self.mouseTouchChunk:
            self.mouseTouchChunk.HandleMouseClicks()

    def delete(self):
        for chunk in self.chunks.values():
            if chunk.chunkVBO:
                chunk.chunkVBO.delete()

    def updateAllSurfaces(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.updateAllSurface()

        print("Finished Update All Surfaces", round(time() - s, 2))