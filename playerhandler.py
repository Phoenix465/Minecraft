from vector import *
from camera import *
from blockhandler import *
from chunkhandler import *


class Player:
    def __init__(self, startPos: Vector3, displayCentre: tuple):
        self.camera = Camera(startPos, displayCentre)

    def move(self, dt, viewMatrix):
        return self.camera.move(dt, viewMatrix)

    def setHighlightedBlockData(self, chunk: Chunk):
        self.camera.highlightBlock(chunk)

    def drawCrosshair(self):
        self.camera.drawCrosshair()
