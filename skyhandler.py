"""
Handler For The Sky

Class
-----
Sky - The Sky
"""

import enums
from blockhandler import *


class Sky:
    """
    This Class Handles THe Sky

    Parameters
    ----------
    camera : Camera
        The Player's Camera Object

    Attributes
    ----------
    camera : Camera
        This Player's Camera Object
    """

    def __init__(self, camera):
        self.camera = camera

    def drawSky(self):
        skyBlock = Block(self.camera.currentCameraPosition, enums.BlockType.SKY, sideLength=128)
        skyBlock.drawSolid()
