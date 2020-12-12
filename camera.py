"""
Handler for the Camera Class

Class
-----
Camera - This Class handles the Client's Camera
"""

from vector import Vector3, Vector2
from pygame import K_w, K_a, K_s, K_d, K_q, K_e
from OpenGL.GL import *
import pygame.key as key
from pygame.mouse import set_pos, get_pos
from degreesMath import *
import enums
from blockhandler import Block
from chunkhandler import Chunk
from time import time
import numpy as np
from operator import attrgetter


# https://towardsdatascience.com/speeding-up-python-code-fast-filtering-and-slow-loops-8e11a09a9c2f


class Camera:
    """
    This Class handles the player Camera

    Parameters
    ----------
    startPos : Vector3
        Start Position of the Camera

    displayCentre : tuple
        Centre of the window size

    Attributes
    ----------
    currentCameraPosition : Vector3
        A Vector3 of the current camera position

    lookVector : Vector3
        A Normalised Vector3 of the camera looking direction

    raycastUpdateLength : float
        The Accuracy of the highlight-block raycasting
        
    lastMousePosition : Vector3
        A Vector2 of the mouse's current position on the window

    distance : flaot
        The distance moved per frame - sensitive to change

    sentivity : float
        Mouse Sensitivity when moving the mouse

    upDownAngle : int
        The Up-Down angle of the Camera - Foward:0, Up:90, Dowm:-90

    leftRightAndle : int
        The Left-Right angle of the Camera - Forward:0, Left: -90, Right: 90

    displayCentre: tuple
        Centre of the window size

    displaySize : tuple
        Double the displayCentre - Size of window

    updatePos : Vector2
        Vector2 used for postion of the crosshair
    """

    def __init__(self, startPos: Vector3, displayCentre: tuple):
        self.currentCameraPosition = startPos
        self.lookVector = Vector3(0, 0, 0)
        self.raycastUpdateLength = 0.1
        self.maxDist = 5

        self.deltaVector = Vector2(0, 0)

        self.distance = 0.005  # 0.005
        self.sentivity = 0.1

        self.upDownAngle = 0
        self.leftRightAngle = 0

        self.displayCentre = displayCentre
        self.displaySize = (displayCentre[0] * 2, displayCentre[1] * 2)
        self.updatePos = Vector2(*self.displayCentre)

    def updateLookVector(self):
        """
        Updates the Look Vector of the Camera and stores it in self.lookVector

        Returns
        -------
        None
        """

        xzLength = cos(self.upDownAngle)
        trigAddVector = Vector3(sin(-self.leftRightAngle) * xzLength,
                                sin(self.upDownAngle),
                                cos(-self.leftRightAngle) * xzLength)

        self.lookVector = trigAddVector

    def turnCamera(self, firstStage: bool):
        if firstStage:
            currentMousePosition = Vector2(*get_pos())
            set_pos(self.displayCentre)

            self.deltaVector = (currentMousePosition - self.displayCentre) * self.sentivity

            self.upDownAngle += self.deltaVector.Y
            self.leftRightAngle += self.deltaVector.X

            if self.upDownAngle < -80:
                self.upDownAngle = -80

            elif self.upDownAngle > 80:
                self.upDownAngle = 80

            self.updateLookVector()

            glRotatef(self.upDownAngle, 1, 0, 0)
        else:
            glRotatef(self.deltaVector.X, 0.0, 1.0, 0.0)

    def moveCamera(self, dt: float, flyMode: bool = True):
        directionalXVector = Vector3(
            sin(-self.leftRightAngle),
            0,
            cos(-self.leftRightAngle)
        )

        directionalZVector = Vector3(
            sin(-self.leftRightAngle - 90),
            0,
            cos(-self.leftRightAngle - 90)
        )

        frameDistance = self.distance * dt
        directionalXVector = directionalXVector.unit * frameDistance
        directionalZVector = directionalZVector.unit * frameDistance

        moveVector = Vector3(0, 0, 0)
        keysPressed = key.get_pressed()

        if keysPressed[K_w]:
            self.currentCameraPosition -= directionalXVector
            moveVector.Z += frameDistance

        if keysPressed[K_s]:
            self.currentCameraPosition += directionalXVector
            moveVector.Z -= frameDistance

        if keysPressed[K_a]:
            self.currentCameraPosition += directionalZVector
            moveVector.X += frameDistance

        if keysPressed[K_d]:
            self.currentCameraPosition -= directionalZVector
            moveVector.X -= frameDistance

        if keysPressed[K_q] and flyMode:
            self.currentCameraPosition.Y -= frameDistance
            moveVector.Y += frameDistance

        if keysPressed[K_e] and flyMode:
            self.currentCameraPosition.Y += frameDistance
            moveVector.Y -= frameDistance

        glTranslatef(*moveVector.tuple)

    def move(self, dt, viewMatrix):
        """
        Controls the Movement of the Camera

        Parameters
        ----------
        dt : float
            Time passed since last frame

        viewMatrix : OpenGL.arrays.ctypesarrays.c_float_Array_4_Array_4
            Used to transform from world-space into view-space

        Returns
        -------
        OpenGL.arrays.ctypesarrays.c_float_Array_4_Array_4
        """

        glLoadIdentity()

        self.turnCamera(True)

        glPushMatrix()
        glLoadIdentity()

        self.moveCamera(dt)

        self.turnCamera(False)

        glMultMatrixf(viewMatrix)
        viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

        # apply view matrix
        glPopMatrix()
        glMultMatrixf(viewMatrix)
        return viewMatrix

    def drawCrosshair(self):
        """
        Draws the Crosshair in the Centre of the Screen

        Returns
        -------
        None
        """

        def Crosshair(x, y, w):
            glColor3f(1.0, 1.0, 1.0)
            glBegin(GL_LINES)
            glVertex2f(x - w, y)
            glVertex2f(x + w, y)
            glVertex2f(x, y - w)
            glVertex2f(x, y + w)
            glEnd()

        # https://stackoverflow.com/questions/54084020/how-to-display-a-2d-shape-over-opengl-with-python-and-pygame

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0.0, self.displaySize[0], 0.0, self.displaySize[1], -1.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)

        Crosshair(self.updatePos.X, self.updatePos.Y, 20)

        glEnable(GL_DEPTH_TEST)

        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
        glPopMatrix()

    def highlightBlock(self, possibleChunk: list):
        """
               Sets the Highlighted Block Data on the Chunk
               Can set the chunk data to None

               Parameters
               ----------
               currentChunk : chunkhandler.Chunk
                   Chunk that is to be tested for the highlighted block

               maxDist : int
                   Maximum Distance of the Camera Raycast

               Returns
               -------
               None
               """

        sTotal = time()

        distDiff = 0
        currentRayPosition = self.currentCameraPosition
        addVector = self.lookVector * self.raycastUpdateLength

        if len(possibleChunk) == 0:
            return

        """
        Set Up: 0.001997232437133789
        Centring: 0.0
        Calculate Mag: 0.001993894577026367
        Filter Length: 204
        Raycasting 0.004956245422363281
        Total Raycasting: 0.008947372436523438
        """

        def convert(num):
            if num < 0:
                return num + 16

            if num >= 16:
                return num % 16

            return num

        lastPos = None

        while distDiff < self.maxDist:
            closestBlockPos = Vector3(*[round(posP) for posP in currentRayPosition.tuple])

            if closestBlockPos != lastPos:
                targetChunk = None

                for chunk in possibleChunk:
                    if chunk.isPointInChunk(closestBlockPos):
                        targetChunk = chunk

                if targetChunk:
                    posChunk = closestBlockPos.copy()

                    posChunk.X = convert(posChunk.X)
                    posChunk.Z = convert(posChunk.Z)

                    targetBlock = targetChunk.blocks[posChunk.Y][posChunk.X][posChunk.Z]

                    if any(targetBlock.surfacesShow):
                        targetChunk.highlightedBlock = targetBlock
                        targetChunk.highlightedSurfaceIndex = targetBlock.closestSurfaceIndex(currentRayPosition)

                        eTotal = time() - sTotal
                        #print("Total Raycasting Finshed:", eTotal)

                        return targetChunk

            lastPos = closestBlockPos
            currentRayPosition -= addVector
            distDiff += self.raycastUpdateLength

        eTotal = time() - sTotal
        #print("Total Raycasting Fail:", eTotal)

        return None
