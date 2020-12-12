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
from vector import Vector3, Vector2
import numpy as np
from math import pow
from pprint import pprint
from random import randint
from threading import Thread
from multiprocessing import Process, Pool
from time import time
from ray import raycast, getCloseChunks


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

    def __init__(self, player: Player, displayCentre: tuple):
        self.player = player

        self.noise = OpenSimplex(
            seed=randint(10000, 99999)
        )

        self.chunkSize = Vector3(16, 16, 16)
        self.halfChunk = self.chunkSize / 2
        self.displayCentre = Vector2(*displayCentre)
        self.displaySize = self.displayCentre * 2

        self.adjacentChunkOffsets = [
            Vector3(0, 0, -1),
            Vector3(0, 0, 1),
            Vector3(-1, 0, 0),
            Vector3(1, 0, 0),
        ]

        self.cornerChunksOffsets = [
            Vector3(1, 0, 1),
            Vector3(1, 0, -1),
            Vector3(-1, 0, 1),
            Vector3(-1, 0, -1),
        ]

        self.chunks = {
            # BottomCentrePos : Chunk
        }

        self.currentChunk = None
        self.mouseTouchChunk = None

        self.adjacentCurrentChunk = {

        }

        self.cornerCurrentChunks = {

        }

        self.memoryBlockSee = []

        self.runEveryXFrame = 5
        self.runDiffTime = self.runEveryXFrame / 60
        self.lastRun = time()

        self.framesPassed = 0
        self.threads = []
        self.blocksList = []

    def __del__(self):
        self.delete()

    def tick(self):
        self.framesPassed += 1

    def generateChunks(self):
        s = time()

        size = 1
        for chunkMultX in range(-size, size + 1):
            for chunkMultY in range(-size, size + 1):
                chunkPosition = self.chunkSize * Vector3(chunkMultX, 0, chunkMultY)
                chunkPosition += self.chunkSize/2
                chunkPosition *= Vector3(1, 0, 1)
                #print(chunkPosition)

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
                self.cornerCurrentChunks = chunk.cornerChunks

                return

        self.currentChunk = None
        self.adjacentCurrentChunk = {}
        self.cornerCurrentChunks = {}

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
            cornerData = {}

            for chunkOffset in self.adjacentChunkOffsets:
                newChunkPos = chunkPos + (chunkOffset * self.chunkSize)

                adjacentData[chunkOffset] = self.chunks.get(newChunkPos, None)

            for chunkOffset in self.cornerChunksOffsets:
                newChunkPos = chunkPos + (chunkOffset * self.chunkSize)

                cornerData[chunkOffset] = self.chunks.get(newChunkPos, None)

            chunk.linkChunk(adjacentData, cornerData)

        print("Finished Link Chunks", round(time() - s, 2))

    def setHighlightedBlockData(self):
        if self.mouseTouchChunk:
            highlightedBlock = self.mouseTouchChunk.highlightedBlock

            if highlightedBlock:
                highlightedBlock.drawWireSurfaceShow()

        currentCameraPos = self.player.camera.currentCameraPosition
        chunkCheck = getCloseChunks(currentCameraPos, self.player.camera.lookVector, self)

        self.mouseTouchChunk = self.player.setHighlightedBlockData(chunkCheck)

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
        print("Exiting...")

        for i, chunk in enumerate(self.chunks.values()):
            print(f"Deleting Chunk {i}", end=" ")
            if chunk.chunkVBO:
                chunk.chunkVBO.delete()
            print("FINISHED")

    def updateAllSurfaces(self):
        s = time()

        for chunk in self.chunks.values():
            chunk.updateAllSurface()

        print("Finished Update All Surfaces", round(time() - s, 2))
