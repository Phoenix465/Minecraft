from vector import *
from OpenGL.GL import *
import enums
from degreesMath import average

colourHandler = enums.BlockColour()


class Block:
    def __init__(self, centre: Vector3, blockType: enums.BlockType, sideLength=None):
        if sideLength:
            self.side = sideLength
        else:
            self.side = 1
        self.halfSide = self.side / 2

        self.blockType = blockType
        self.blockPosChunk = Vector3(0, 0, 0)

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
            (0, 1, 0),
            (0, -1, 0),

            (0, 0, 1),
            (0, 0, -1),

            (-1, 0, 0),
            (1, 0, 0),
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

    def genMiddleSurface(self):
        for i, surfaceTuple in enumerate(self.surfaces):
            firstVector = self.vertices[surfaceTuple[0]]
            secondVector = self.vertices[surfaceTuple[2]]

            self.surfaceMiddle.append(Vector3(
                average(firstVector.X, secondVector.X),
                average(firstVector.Y, secondVector.Y),
                average(firstVector.Z, secondVector.Z),
            ))

    def drawWire(self, drawSurfacesShown=False):
        glBegin(GL_LINES)

        if not drawSurfacesShown:
            for blockEdge in self.edges:
                for blockVertex in blockEdge:
                    glColor3fv((1, 1, 1))
                    glVertex3fv(self.vertices[blockVertex].tuple)
        else:
            for i, blockQuad in enumerate(self.surfaces):
                if not self.surfacesShow[i]:
                    continue

                for linkVertexTuple in self.surfaceEdgeLinker:
                    for linkVertex in linkVertexTuple:
                        glColor3fv((1, 1, 1))
                        glVertex3fv(self.vertices[blockQuad[linkVertex]].tuple)
        glEnd()

    def drawSolid(self, wireSurface=False):
        # print(self.blockType, )
        vertexColour = colourHandler.get(self.blockType).RGBTuple

        glBegin(GL_QUADS)
        for i, blockQuad in enumerate(self.surfaces):
            if not self.surfacesShow[i]:
                continue

            glNormal3fv(self.normals[i])

            for blockVertex in blockQuad:
                glColor3fv(vertexColour)
                glVertex3fv(self.vertices[blockVertex].tuple)

        glEnd()

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

    def isPointInBlock(self, point: Vector3):
        maxVector = self.vertices[7]
        minVector = self.vertices[6]

        return minVector.X < point.X < maxVector.X and minVector.Y < point.Y < maxVector.Y and minVector.Z < point.Z < maxVector.Z

    def closestSurfaceIndex(self, point: Vector3):
        closestDist = 20
        closestSurfaceI = None

        for i, surfaceMiddle in enumerate(self.surfaceMiddle):
            currentDist = (point - surfaceMiddle).magnitude
            if currentDist < closestDist:
                closestDist = currentDist
                closestSurfaceI = i

        return closestSurfaceI
