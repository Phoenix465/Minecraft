import OpenGL.arrays.vbo as glVBO
from OpenGL.GL import *
import numpy as np
from ctypes import c_void_p

#  https://stackoverflow.com/questions/61117412/changing-opengl-vertex-buffer-object-data-via-pyopengl-opengl-arrays-vbo-has-no


class VBOHandler:
    def __init__(self, nestedVectors, nestedColours, normalsVector):
        self.nestedVectors = nestedVectors
        self.nestedColours = nestedColours
        self.normalVectors = normalsVector

        self.combinedData = []
        self._setCombinedData()
        self.combinedData = np.array(self.combinedData, np.float32)

        self.vbo = glVBO.VBO(self.combinedData)
        self.vbo.bind()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        stride = (9)*self.combinedData.itemsize

        glVertexPointer(3, GL_FLOAT, stride, None)
        glColorPointer(3, GL_FLOAT, stride, c_void_p(12))
        glNormalPointer(GL_FLOAT, stride, c_void_p(24))

        glBindVertexArray(0)

    def draw(self):
        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, 9)
        glBindVertexArray(0)

    def _setCombinedData(self):
        #https://stackoverflow.com/questions/61117412/changing-opengl-vertex-buffer-object-data-via-pyopengl-opengl-arrays-vbo-has-no

        for i, vector3 in enumerate(self.nestedVectors):
            colour = self.nestedColours[i]
            combined = vector3.list + colour.RGBList + self.normalVectors[i].list

            for comb in combined:
                self.combinedData.append(comb)
