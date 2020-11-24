"""
Handles For Player

Class
-----
Player - Handles A Single Player
"""

from vector import Vector3
from camera import Camera
from blockhandler import Block
from chunkhandler import Chunk


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

    def setHighlightedBlockData(self, chunk: Chunk):
        self.camera.highlightBlock(chunk)

    def drawCrosshair(self):
        self.camera.drawCrosshair()
