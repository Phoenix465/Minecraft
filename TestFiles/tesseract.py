import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *

vertices = ((1,-1,-1),(1,1,-1),(-1,1,-1),(-1,-1,-1),(1,-1,1),(1,1,1),(-1,-1,1),(-1,1,1))
vertices1 = ((2,-2,-2),(2,2,-2),(-2,2,-2),(-2,-2,-2),(2,-2,2),(2,2,2),(-2,-2,2),(-2,2,2))

edges = ((0,1),(0,3),(0,4),(2,1),(2,3),(2,7),(6,3),(6,4),(6,7),(5,1),(5,4),(5,7))

def cube(edges,vertices):
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def lines(vertices1, vertices2):
    for v1, v2 in zip(vertices1, vertices2):
        glBegin(GL_LINES)
        glVertex3fv(v1)
        glVertex3fv(v2)
        glEnd()

def display_cube():
    pygame.init()
    display_window = (800,600)
    pygame.display.set_mode(display_window,DOUBLEBUF | OPENGL)
    gluPerspective(45,(display_window[0]/display_window[1]),0.1,50.0)
    glTranslatef(0.0,0.0,-10)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotate(1,3,10,10) # (angle,x,y,z)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        cube(edges,vertices1) # large cube
        cube(edges,vertices) # small cube
        lines(vertices1, vertices)

        pygame.display.flip()
        pygame.time.wait(10)

display_cube()