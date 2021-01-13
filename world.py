"""
This File Handles A World

Class
-----
World - A Single World Handler
"""

from random import randint
from time import time

from opensimplex import OpenSimplex

from chunkhandler import Chunk
from playerhandler import Player
from ray import getCloseChunks
from vector import Vector3, Vector2


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

    noise : opensimplex.OpenSimplex
        The Noise Data to be shared accross the Chunks

    chunkSize : Vector3
        THe Size of each Chunk

    halfChunk : Vector3
        Half Sie of each Chunk

    displayCentre : Vector2
        The Centre of the Display

    displaySize : Vector2
        The Full-Size of the display based on the displayCentre

    adjacentChunkOffsets : list
        A list containing Vector3 with relative offsets to the adjacent Chunks

    cornerChunksOffsets : list
        A list containing Vector3 with relative offsets to the corner Chunks

    chunks: dict
        Key: Vector3 which is the Bottom Centre
        Value: Chunk

    currentChunk : None/Chunk
        THe Current Chunk the player is in.

    mouseTouchChunk : None/Chunk
        The Chunk that the mouse hits.

    adjacentCurrentChunk : dict
        A Vector3: Chunk which contains the offset key and then the chunk value for the adjacent chunks.

    cornerCurrentChunks : dict
        A Vector3: Chunk which contains the offset key and then the chunk value for the corners chunks.
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

    def __del__(self):
        self.delete()

    def generateChunks(self):
        """
        Generates All the Chunks

        Returns
        -------
        None
        """

        s = time()

        size = 0
        for chunkMultX in range(-size, size + 1):
            for chunkMultY in range(-size, size + 1):
                chunkPosition = self.chunkSize * Vector3(chunkMultX, 0, chunkMultY)
                chunkPosition += self.chunkSize/2
                chunkPosition *= Vector3(1, 0, 1)
                #print(chunkPosition)

                newChunk = Chunk(chunkPosition, self.chunkSize, self.noise)

                self.chunks[chunkPosition] = newChunk

        print("Finished Gen Chunks", round(time() - s, 2))

    def updateCurrentChunk(self):
        """
        Updates The Chunk that the player is in and the adjacent and corner chunks of that.

        Returns
        -------
        None
        """

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
        """
        Draws All the Chunks

        Returns
        -------
        None
        """

        for chunk in self.chunks.values():
            chunk.draw()

    def generateBlocks(self):
        """
        Generates the Blocks of each Chunk

        Returns
        -------
        None
        """

        s = time()

        for chunk in self.chunks.values():
            chunk.generateBlocks()

        print("Finished Gen Blocks", round(time() - s, 2))

    def genChunkVBOs(self):
        """
        Generates the VBO of every Chunk

        Returns
        -------
        None
        """

        s = time()

        for chunk in self.chunks.values():
            chunk.genChunkVBO()

        print("Finished Gen Chunk VBOs", round(time() - s, 2))

    def linkChunks(self):
        """
        Links each Chunk with the Adjacent and Corner Chunks

        Returns
        -------
        None
        """

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
        """
        Sets the Mouse Touch Chunk of the Player

        Returns
        -------
        None
        """

        if self.mouseTouchChunk:
            highlightedBlock = self.mouseTouchChunk.highlightedBlock

            if highlightedBlock:
                highlightedBlock.drawWireSurfaceShow(black=True)

        currentCameraPos = self.player.camera.currentCameraPosition
        chunkCheck = getCloseChunks(currentCameraPos, self.player.camera.lookVector, self)

        self.mouseTouchChunk = self.player.setHighlightedBlockData(chunkCheck)

    def setup(self):
        """
        Sets Up the World

        Returns
        -------
        None
        """

        self.generateChunks()
        self.generateBlocks()
        self.linkChunks()
        self.updateAllSurfaces()
        self.genChunkVBOs()

    def HandleMouseClicks(self):
        """
        Handles the Clicking of the Player

        Returns
        -------
        None
        """

        if self.mouseTouchChunk:
            self.mouseTouchChunk.HandleMouseClicks()

    def delete(self):
        """
        Handles Deletion of the World

        Returns
        -------
        None
        """

        print("Exiting...")

        for i, chunk in enumerate(self.chunks.values()):
            print(f"Deleting Chunk {i}", end=" ")
            if chunk.chunkVBO:
                chunk.chunkVBO.delete()
            print("FINISHED")   

    def updateAllSurfaces(self):
        """
        Updates all Surfaces of each Chunk

        Returns
        -------
        None
        """

        s = time()

        for chunk in self.chunks.values():
            chunk.updateAllSurface()

        print("Finished Update All Surfaces", round(time() - s, 2))
