"""
Handles For Player

Class
-----
Player - Handles A Single Player
"""
from time import time

from camera import Camera
from ray import raycast
from vector import Vector3


class Player:
    """
    This Class Handles The Player Stuff

    Parameters
    ----------
    startPos : Vector3
        Starting Position of the Player

    displayCentre : tuple
        Centre of the Display

    Attributes
    ----------
    camera : Camera
        Camera From the Camera Script
    """

    def __init__(self, startPos: Vector3, displayCentre: tuple):
        self.camera = Camera(startPos, displayCentre)
        self.world = None

        self.reach = 5
        self.raycastUpdateLength = .04

        self.moveConstraints = {
            "q": False,
            "e": False,

            "w": False,
            "a": False,
            "s": False,
            "d": False,

        }

    def move(self, dt, viewMatrix):
        return self.camera.move(dt, viewMatrix, self.moveConstraints)

    def resetConstraints(self):
        for key in self.moveConstraints.keys():
            self.moveConstraints[key] = False

    def bodyDirectionConstraints(self):
        currentPlayerPos = self.camera.currentCameraPosition
        lookVector = self.camera.lookVector
        rayMultiplier = .05

        rayDistance = {
            "e": 2,
            "q": 2,
            "w": 1,
            "s": 1,
            "a": 1,
            "d": 1,
        }

        directionDistanceMultiplier = {
            "e": Vector3(0, 1, 0),
            "q": Vector3(0, 1, 0),
            "w": Vector3(1, 0, 1),
            "s": Vector3(1, 0, 1),
            "a": Vector3(1, 0, 1),
            "d": Vector3(1, 0, 1)
        }

        bodyDirections = {
            "e": Vector3(0, 1, 0),
            "q": Vector3(0, -1, 0),
            "w": lookVector * Vector3( 1, 0,  1) * -1,
            "s": lookVector * Vector3( 1, 0,  1),
            "a": lookVector * Vector3( 1, 0, -1),
            "d": lookVector * Vector3(-1, 0,  1),
        }

        raycastPositions = [currentPlayerPos, currentPlayerPos - Vector3(0, 1, 0)]

        blacklist = {
            raycastPositions[1]: ["q"]
        }

        if self.world.currentChunk:
            for raycastOrigin in raycastPositions:
                for key, vectorDir in bodyDirections.items():
                    if raycastOrigin in blacklist and key in blacklist[raycastOrigin]:
                        continue

                    maxRayDistance = rayDistance[key]
                    s = time()
                    blockHit = raycast(raycastOrigin,
                                       vectorDir.unit * rayMultiplier * -1,
                                       maxRayDistance,
                                       [self.world.currentChunk])[1]
                    e = time() - s
                    #print("Raycasting:", e)

                    if blockHit:
                        blockPos = blockHit.centre
                        directionMultiplier = directionDistanceMultiplier[key]

                        playerPosAdj = raycastOrigin * directionMultiplier
                        blockPosAdj = blockPos * directionMultiplier
                        canConstrain = (playerPosAdj - blockPosAdj).magnitude < maxRayDistance

                        if not self.moveConstraints[key]:
                            self.moveConstraints[key] = canConstrain

    def setHighlightedBlockData(self, chunkList: list):
        """
        Sets the Highlighted Block of the Mouse Hit Chunk

        Parameters
        ----------
        chunkList : A List containing Chunks

        Returns
        -------
        chunk : Chunk
            THe Chunk that the mouse Hit

        """

        currentRayPosition = self.camera.currentCameraPosition
        addVector = self.camera.lookVector * self.raycastUpdateLength

        chunk, block, surfaceI = raycast(currentRayPosition, addVector, self.reach, chunkList)

        if chunk:
            chunk.highlightedBlock = block
            chunk.highlightedSurfaceIndex = surfaceI

        return chunk

    def drawCrosshair(self):
        self.camera.drawCrosshair()
