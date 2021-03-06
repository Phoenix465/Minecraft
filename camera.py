"""
Handler for the Camera Class

Class
-----
Camera - This Class handles the Client's Camera
"""

import pygame.key as key
from OpenGL.GL import *
from pygame import K_w, K_a, K_s, K_d, K_q, K_e
from pygame.mouse import set_pos, get_pos

from degreesMath import *
from vector import Vector3, Vector2


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

    maxDist : int/float
        Block Edit Range from the Camera Position

    deltaVector : Vector2
        Change in Position of the Mouse

    lastMousePosition : Vector3
        A Vector2 of the mouse's current position on the window

    distance : flaot
        The distance moved per frame - sensitive to change

    sensitivity : float
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

        self.deltaVector = Vector2(0, 0)

        self.distance = 0.005  # 0.005
        self.sensitivity = 0.1

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
        """
        Handles the Turning of the Camera

        Parameters
        ----------
        firstStage : bool
            A bool which represents whether the Y or X part os the camera should be turned.

        Returns
        -------
        None
        """

        if firstStage:
            currentMousePosition = Vector2(*get_pos())
            set_pos(self.displayCentre)

            self.deltaVector = (currentMousePosition - self.displayCentre) * self.sensitivity

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

    def moveCamera(self, dt: float, moveConstraints: dict):
        """
        Handles the Turning of the Camera

        Parameters
        ----------
        dt : float
            Time since the last frame in ms

        Returns
        -------
        None
        """

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

        if keysPressed[K_w] and not moveConstraints["w"]:
            self.currentCameraPosition -= directionalXVector
            moveVector.Z += frameDistance

        if keysPressed[K_s] and not moveConstraints["s"]:
            self.currentCameraPosition += directionalXVector
            moveVector.Z -= frameDistance

        if keysPressed[K_a] and not moveConstraints["a"]:
            self.currentCameraPosition += directionalZVector
            moveVector.X += frameDistance

        if keysPressed[K_d] and not moveConstraints["d"]:
            self.currentCameraPosition -= directionalZVector
            moveVector.X -= frameDistance

        if keysPressed[K_q] and not moveConstraints["q"]:
            self.currentCameraPosition.Y -= frameDistance
            moveVector.Y += frameDistance

        if keysPressed[K_e] and not moveConstraints["e"]:
            self.currentCameraPosition.Y += frameDistance
            moveVector.Y -= frameDistance

        glTranslatef(*moveVector.tuple)

    def move(self, dt, viewMatrix, moveConstraints):
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

        self.moveCamera(dt, moveConstraints)

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
