import pygame as pg
from pygame.locals import *

from OpenGL.GLU import *
from playerhandler import *
from chunkhandler import *
from skyhandler import *
from vector import Vector3
import camera
help(camera)

FirstChunk = Chunk(Vector3(0, 0, 0), Vector3(16, 16, 16))

clock = pg.time.Clock()


def main():
    pg.init()

    display = (1200, 700)
    displayCentre = tuple(map(lambda num: num / 2, display))
    pg.display.set_mode(display, DOUBLEBUF | OPENGL)

    iconSurface = pg.image.load("images/MinecraftIcon.png")

    pg.display.set_icon(iconSurface)
    pg.display.set_caption("Minecraft")

    pg.mouse.set_visible(False)

    glMatrixMode(GL_PROJECTION)
    gluPerspective(70, (display[0] / display[1]), 0.1, 128.0)

    glMatrixMode(GL_MODELVIEW)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glEnable(GL_DEPTH_TEST)

    glLight(GL_LIGHT0, GL_POSITION, (50, 50, 50, 1))  # point light from the left, top, front
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLoadIdentity()

    player = Player(Vector3(0, 0, 0), displayCentre)
    sky = Sky(player.camera)

    while True:
        dt = clock.tick(30)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        if pg.mouse.get_focused():
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            viewMatrix = player.move(dt, viewMatrix)
            print(type(viewMatrix))
            glPushMatrix()
            FirstChunk.HandleMouseClicks()

            player.setHighlightedBlockData(FirstChunk)

            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

            sky.drawSky()
            FirstChunk.draw()

            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)

            glPopMatrix()

            player.drawCrosshair()

        pg.display.flip()


if __name__ == "__main__":
    main()
