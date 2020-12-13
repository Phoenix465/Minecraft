"""
Handler for the VBO

Class
-----
VBOHandler - Handles a Single VBO
"""

from ctypes import c_void_p

import OpenGL.arrays.vbo as glVBO
import numpy as np
from OpenGL.GL import *


class VBOHandler:
    def __init__(self, combinedData):
        self.combinedData = combinedData
        self.combinedData = np.array(self.combinedData, np.float32)

        self.vbo = glVBO.VBO(self.combinedData)
        self.vbo.bind()

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        glEnableClientState(GL_VERTEX_ARRAY)
        glEnableClientState(GL_COLOR_ARRAY)
        glEnableClientState(GL_NORMAL_ARRAY)

        stride = (3+3+3)*self.combinedData.itemsize

        glVertexPointer(3, GL_FLOAT, stride, None)
        glColorPointer(3, GL_FLOAT, stride, c_void_p(12))
        glNormalPointer(GL_FLOAT, stride, c_void_p(24))

        glBindVertexArray(0)

    def draw(self):
        """
        Draws the VBO

        Returns
        -------
        None
        """

        glBindVertexArray(self.vao)
        glDrawArrays(GL_QUADS, 0, len(self.combinedData))
        glBindVertexArray(0)

    def delete(self):
        del self.vao
        del self.vbo