"""
Handler for the Blocks

Class
-----
Block - This Class handle a single block
"""

from OpenGL.GL import *

import enums
from degreesMath import average
from vector import Vector3
from numpy import array, float32
from vbohandler import VBOHandler

colourHandler = enums.BlockColour()


class Block:
    """
    This Class handle a single block in minecraft

    Parameters
    ----------
    centre : Vector3
        Centre-point of the block

    blockType : enums.BlockType
        Block type of the block

    sideLength : None
        Keyword-Argument, default value is None but is can be set to 1
        When value is None, side length is 1
        Otherwise it uses your current value for sideLength as a side length

    Attributes
    ----------
    side : int
        Side Length of Block - Cube

    halfSide : int
        Half of the side length

    blockType : enums.BlockType
        Current Block Type of the Block

    blockPosChunk : Vector3
        Position of the Block in it's Chunk

    closestSurface : None / int
        During Runtime can change to int based on the surface index otherwise is None

    centre: Vector3
        Vector3 of the Centre of the Block

    vertices: list
        Contains a list of Vector3 Vertices of the block, all relative to the centre point

    edges : list
        Contains a list of tuple which each contain a tuple which refers to two vertex of the block, hence making a edge

    normals : list
        Contains a list of Vector3 used for light diffraction, based on the orientation of the surface

    surfaces : list
        Contains a list of tuple of length 4 which contain the indexes to the Vertex of the cube
        4 indexes referring to a vertex on the block in order

    surfaceMiddle : list
        Originally contains a empty list
        After generation stores Vector3's which are the centre point of each face respective to the centre of the block

    surfaceEdgeLinker : list
        Contains a list of tuple with length 2
        Each refer to the index of the surfaces tuple

    surfacesShow : list
        Contains a list of length 6 (bool) which refer to the surface
        Boolean values refer to whether that surfaces should be drawn
    """

    def __init__(self, centre: Vector3, blockType: enums.BlockType, sideLength=None):
        if sideLength:
            self.side = sideLength
        else:
            self.side = 1
        self.halfSide = self.side / 2

        self.blockType = blockType
        self.blockPosChunk = Vector3(0, 0, 0)

        self.parentChunk = None

        self.closestSurface = None

        self.centre = centre
        self.vertices = [
            Vector3(centre.X - self.halfSide, centre.Y + self.halfSide, centre.Z + self.halfSide),  # 0
            Vector3(centre.X + self.halfSide, centre.Y - self.halfSide, centre.Z + self.halfSide),  # 1
            Vector3(centre.X + self.halfSide, centre.Y + self.halfSide, centre.Z - self.halfSide),  # 2

            Vector3(centre.X - self.halfSide, centre.Y - self.halfSide, centre.Z + self.halfSide),  # 3
            Vector3(centre.X + self.halfSide, centre.Y - self.halfSide, centre.Z - self.halfSide),  # 4
            Vector3(centre.X - self.halfSide, centre.Y + self.halfSide, centre.Z - self.halfSide),  # 5

            Vector3(centre.X - self.halfSide, centre.Y - self.halfSide, centre.Z - self.halfSide),  # 6
            Vector3(centre.X + self.halfSide, centre.Y + self.halfSide, centre.Z + self.halfSide),  # 7
        ]
        # Checking If Two Operators are the same.
        self.edges = [
            (0, 3),
            (0, 5),
            (0, 7),

            (1, 3),
            (1, 4),
            (1, 7),

            (2, 4),
            (2, 5),
            (2, 7),

            (3, 6),

            (4, 6),

            (5, 6),
        ]

        self.normals = [
            Vector3(0, 1, 0),
            Vector3(0, -1, 0),

            Vector3(0, 0, 1),
            Vector3(0, 0, -1),

            Vector3(-1, 0, 0),
            Vector3(1, 0, 0),
        ]

        self.surfaces = [
            (0, 7, 2, 5),  # Top
            (1, 3, 6, 4),  # Bottom

            (0, 7, 1, 3),  # Back
            (2, 4, 6, 5),  # Front

            (0, 3, 6, 5),  # Left
            (1, 4, 2, 7),  # Right
        ]

        self.surfaceMiddle = [
            # Generated Afterwards
        ]

        self.surfaceVBOs = [

        ]

        self.genMiddleSurface()

        self.surfaceEdgeLinker = [(0, 1), (1, 2), (2, 3), (3, 0)]

        self.surfacesShow = [
            True,
            True,
            True,
            True,
            True,
            True,
        ]

    def __repr__(self):
        return "Block"

    def bindData(self):
        # https://cyrille.rossant.net/2d-graphics-rendering-tutorial-with-pyopengl/
        # https://stackoverflow.com/questions/15672720/pyopengl-dynamically-updating-values-in-a-vertex-buffer-objecta
        # http://pyopengl.sourceforge.net/context/tutorials/shader_1.html
        self.surfaceVBOs = []

        vertexColour = colourHandler.get(self.blockType)

        for i, blockQuad in enumerate(self.surfaces):
            surfacesList = [self.vertices[blockVertex] for blockVertex in blockQuad]

            combinedData = []

            for vector3 in surfacesList:
                combined = vector3.list + vertexColour.RGBList + self.normals[i].list

                for comb in combined:
                    combinedData.append(comb)

            self.surfaceVBOs.append(VBOHandler(combinedData))


    def genMiddleSurface(self):
        """
        Generates the Middle Point of each Surface and appends to the list self.surfaceMiddle

        Returns
        -------
        None
        """

        for i, surfaceTuple in enumerate(self.surfaces):
            firstVector = self.vertices[surfaceTuple[0]]
            secondVector = self.vertices[surfaceTuple[2]]

            self.surfaceMiddle.append(Vector3(
                average(firstVector.X, secondVector.X),
                average(firstVector.Y, secondVector.Y),
                average(firstVector.Z, secondVector.Z),
            ))

    def drawWire(self):
        """
        Draws the each Edge of the Block in White

        Parameters
        ----------
        drawSurfacesShown : bool
            Boolean refers to whether the program should only wire the surfaces that can be seen

        Returns
        -------
        None
        """

        glBegin(GL_LINES)

        for blockEdge in self.edges:
            for blockVertex in blockEdge:
                glColor3fv((1, 1, 1))
                glVertex3fv(self.vertices[blockVertex].tuple)

        glEnd()
    
    def drawSolid(self, wireSurface=False):
        """
        Draws the surfaces of the block that can be seen, supports wiring the surfaces that can be seen.

        Parameters
        ----------
        wireSurface : bool
            Boolean Value refers to whether the surfaces that can be seen should be wired

        Returns
        -------
        None
        """

        for i, vbo in enumerate(self.surfaceVBOs):
            if not self.surfacesShow[i]:
                continue

            vbo.draw()

        if wireSurface:
            for i, blockQuad in enumerate(self.surfaces):
                if not self.surfacesShow[i]:
                    continue

                if wireSurface:
                    for linkVertexTuple in self.surfaceEdgeLinker:
                        glBegin(GL_LINES)

                        for linkVertex in linkVertexTuple:
                            glColor3fv((1, 1, 1))
                            glVertex3fv(self.vertices[blockQuad[linkVertex]].tuple)
                        glEnd()

    def drawSolidOld(self, wireSurface=False):
        """
        Draws the surfaces of the block that can be seen, supports wiring the surfaces that can be seen.

        Parameters
        ----------
        wireSurface : bool
            Boolean Value refers to whether the surfaces that can be seen should be wired

        Returns
        -------
        None
        """

        vertexColour = colourHandler.get(self.blockType).RGBTuple

        glBegin(GL_QUADS)
        for i, blockQuad in enumerate(self.surfaces):
            if not self.surfacesShow[i]:
                continue

            glNormal3fv(self.normals[i].tuple)

            for blockVertex in blockQuad:
                glColor3fv(vertexColour)
                glVertex3fv(self.vertices[blockVertex].tuple)

        glEnd()

    def drawWireSurfaceShow(self):
        for i, blockQuad in enumerate(self.surfaces):
            if not self.surfacesShow[i]:
                continue

            for linkVertexTuple in self.surfaceEdgeLinker:
                glBegin(GL_LINES)

                for linkVertex in linkVertexTuple:
                    glColor3fv((1, 1, 1))
                    glVertex3fv(self.vertices[blockQuad[linkVertex]].tuple)
                glEnd()

    def isPointInBlock(self, point: Vector3):
        """
        Checks whether a Point is inside the Block or not

        Parameters
        ----------
        point : Vector3
            The point the block checks is inside itself

        Returns
        -------
        bool
        """

        maxVector = self.vertices[7]
        minVector = self.vertices[6]

        return minVector.X < point.X < maxVector.X and minVector.Y < point.Y < maxVector.Y and minVector.Z < point.Z < maxVector.Z

    def closestSurfaceIndex(self, point: Vector3):
        """
        Given a Point, returns the closest surface index that is closest to it

        Parameters
        ----------
        point : Vector3
            The point that is being used to check for the closest surface

        Returns
        -------
        int
        """

        closestDist = 20
        closestSurfaceI = None

        for i, surfaceMiddle in enumerate(self.surfaceMiddle):
            currentDist = (point - surfaceMiddle).magnitude
            if currentDist < closestDist:
                closestDist = currentDist
                closestSurfaceI = i

        return closestSurfaceI
