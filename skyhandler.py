import enums
from blockhandler import *


class Sky:
    def __init__(self, camera):
        self.camera = camera


    def drawSky(self):
        skyBlock = Block(self.camera.currentCameraPosition, enums.BlockType.SKY, sideLength=128)
        skyBlock.drawSolid()
