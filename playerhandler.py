"""
Handles For Player

Class
-----
Player - Handles A Single Player
"""

from camera import Camera
from vector import Vector3
from ray import raycast


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

    def move(self, dt, viewMatrix):
        return self.camera.move(dt, viewMatrix)

    def setHighlightedBlockData(self, chunkList: list):
        currentRayPosition = self.camera.currentCameraPosition
        addVector = self.camera.lookVector * self.camera.raycastUpdateLength

        chunk, block, surfaceI = raycast(currentRayPosition, addVector, self.camera.maxDist, chunkList)

        if chunk:
            chunk.highlightedBlock = block
            chunk.highlightedSurfaceIndex = surfaceI

        return chunk

    def drawCrosshair(self):
        self.camera.drawCrosshair()
