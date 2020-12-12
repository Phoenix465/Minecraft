from time import time

import pygame as pg
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from playerhandler import Player
from skyhandler import Sky
from vector import Vector3
from world import World

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
    gluPerspective(70, (display[0] / display[1]), 0.1, 128.0) # 128

    glMatrixMode(GL_MODELVIEW)
    viewMatrix = glGetFloatv(GL_MODELVIEW_MATRIX)

    glEnable(GL_DEPTH_TEST)

    glLight(GL_LIGHT0, GL_POSITION, (50, 50, 50, 1))  # point light from the left, top, front
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0, 0, 0, 1))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1, 1, 1, 1))
    glLoadIdentity()

    player = Player(Vector3(0, 0, 0), displayCentre)
    sky = Sky(player.camera)

    CurrentWorld = World(player, displayCentre)
    CurrentWorld.setup()

    totalSecond = 0
    frameCount = 0

    while True:
        dt = clock.tick(60)

        keyPressed = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                CurrentWorld.delete()
                quit()

        if keyPressed[pg.K_ESCAPE] or keyPressed[pg.K_k]:
            pg.quit()
            CurrentWorld.delete()
            quit()

        if pg.mouse.get_focused():
            sGameLoop = time()

            if frameCount % 60 == 0:
                print("60 Frame:", totalSecond)
                totalSecond = 0

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            viewMatrix = player.move(dt, viewMatrix)
            glPushMatrix()

            CurrentWorld.HandleMouseClicks()
            CurrentWorld.updateCurrentChunk()

            # Long One
            CurrentWorld.setHighlightedBlockData()

            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

            sky.drawSky()

            s = time()
            CurrentWorld.draw()
            end = time() - s
            #print("Draw Time", end)

            glDisable(GL_LIGHT0)
            glDisable(GL_LIGHTING)
            glDisable(GL_COLOR_MATERIAL)

            glPopMatrix()

            player.drawCrosshair()
            CurrentWorld.tick()

            eGameLoop = time() - sGameLoop
            totalSecond += eGameLoop
            frameCount += 1
            print("Game Loop Time", eGameLoop)

        pg.display.flip()


if __name__ == "__main__":
    main()
