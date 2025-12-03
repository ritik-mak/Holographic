
import math
import random
import numpy as np
import pygame
from pygame.locals import *
from OpenGL.GL import *
from typing import List, Tuple

from . import config


class IllusionScene:
    def __init__(self, window_width: int = config.WINDOW_WIDTH, window_height: int = config.WINDOW_HEIGHT):
        pygame.init()
        self.display = (window_width, window_height)
        pygame.display.set_mode(self.display, DOUBLEBUF | OPENGL)
        pygame.display.set_caption("Holographic Entity (Press 'C' to Calibrate)")

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Pre-generate tunnel data
        self.tunnel_objects: List[Tuple[float, float, float, float, float]] = []
        for i in range(40):
            angle = i * 0.5
            radius = 3.0 + random.uniform(0, 1.0)
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = -i * 1.5
            rot_x = random.uniform(0, 360)
            rot_y = random.uniform(0, 360)
            self.tunnel_objects.append((x, y, z, rot_x, rot_y))

        # Display lists
        self.cube_list = 0
        self.octahedron_list = 0
        self.grid_list = 0
        self.compile_display_lists()

    def compile_display_lists(self) -> None:
        # Cube wireframe
        self.cube_list = glGenLists(1)
        glNewList(self.cube_list, GL_COMPILE)
        self.draw_cube_geometry(1.0)
        glEndList()

        # Octahedron
        self.octahedron_list = glGenLists(1)
        glNewList(self.octahedron_list, GL_COMPILE)
        self.draw_octahedron_geometry(1.0)
        glEndList()

        # Grid
        self.grid_list = glGenLists(1)
        glNewList(self.grid_list, GL_COMPILE)
        self.draw_grid_geometry()
        glEndList()

    def set_off_axis_frustum(self, eye_x: float, eye_y: float, eye_z: float) -> None:
        near = 1.0
        far = 1000.0

        hw = (config.SCREEN_WIDTH_CM / 2.0)
        hh = (config.SCREEN_HEIGHT_CM / 2.0)

        dist = abs(eye_z)
        if dist < 0.1:
            dist = 0.1

        left = (-hw - eye_x) * (near / dist)
        right = (hw - eye_x) * (near / dist)
        bottom = (-hh - eye_y) * (near / dist)
        top = (hh - eye_y) * (near / dist)

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glFrustum(left, right, bottom, top, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(-eye_x, -eye_y, -eye_z)

    def draw_grid_geometry(self) -> None:
        glColor3f(*config.GRID_COLOR)
        glLineWidth(1)
        size = 50.0
        step = 5.0
        glBegin(GL_LINES)
        for x in np.arange(-size, size + step, step):
            glVertex3f(x, 0, -size)
            glVertex3f(x, 0, size)
        for z in np.arange(-size, size + step, step):
            glVertex3f(-size, 0, z)
            glVertex3f(size, 0, z)
        glEnd()

    def draw_cube_geometry(self, size: float) -> None:
        hs = size / 2.0
        glBegin(GL_LINES)
        # Front
        glVertex3f(-hs, -hs, hs); glVertex3f(hs, -hs, hs)
        glVertex3f(hs, -hs, hs); glVertex3f(hs, hs, hs)
        glVertex3f(hs, hs, hs); glVertex3f(-hs, hs, hs)
        glVertex3f(-hs, hs, hs); glVertex3f(-hs, -hs, hs)
        # Back
        glVertex3f(-hs, -hs, -hs); glVertex3f(hs, -hs, -hs)
        glVertex3f(hs, -hs, -hs); glVertex3f(hs, hs, -hs)
        glVertex3f(hs, hs, -hs); glVertex3f(-hs, hs, -hs)
        glVertex3f(-hs, hs, -hs); glVertex3f(-hs, -hs, -hs)
        # Connect
        glVertex3f(-hs, -hs, hs); glVertex3f(-hs, -hs, -hs)
        glVertex3f(hs, -hs, hs); glVertex3f(hs, -hs, -hs)
        glVertex3f(hs, hs, hs); glVertex3f(hs, hs, -hs)
        glVertex3f(-hs, hs, hs); glVertex3f(-hs, hs, -hs)
        glEnd()

    def draw_octahedron_geometry(self, size: float) -> None:
        glBegin(GL_TRIANGLES)
        # Top half
        glVertex3f(0, size, 0); glVertex3f(-size, 0, size); glVertex3f(size, 0, size)
        glVertex3f(0, size, 0); glVertex3f(size, 0, size); glVertex3f(size, 0, -size)
        glVertex3f(0, size, 0); glVertex3f(size, 0, -size); glVertex3f(-size, 0, -size)
        glVertex3f(0, size, 0); glVertex3f(-size, 0, -size); glVertex3f(-size, 0, size)
        # Bottom half
        glVertex3f(0, -size, 0); glVertex3f(size, 0, size); glVertex3f(-size, 0, size)
        glVertex3f(0, -size, 0); glVertex3f(size, 0, -size); glVertex3f(size, 0, size)
        glVertex3f(0, -size, 0); glVertex3f(-size, 0, -size); glVertex3f(size, 0, -size)
        glVertex3f(0, -size, 0); glVertex3f(-size, 0, size); glVertex3f(-size, 0, -size)
        glEnd()

    def draw_scene(self) -> None:
        glClearColor(*config.DARK_BG)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        ticks = pygame.time.get_ticks()

        # Grids
        glPushMatrix()
        glTranslatef(0, -5.0, 0)
        glCallList(self.grid_list)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(0, 5.0, 0)
        glCallList(self.grid_list)
        glPopMatrix()

        # Tunnel
        glColor3f(1.0, 1.0, 1.0)
        glLineWidth(1)
        for (x, y, z, rx, ry) in self.tunnel_objects:
            glPushMatrix()
            glTranslatef(x, y, z)
            glRotatef(rx + ticks * 0.02, 1, 0, 0)
            glRotatef(ry + ticks * 0.02, 0, 1, 0)
            glCallList(self.cube_list)
            glPopMatrix()

        # Entity
        glPushMatrix()
        glTranslatef(0, 0, -5)
        glRotatef(ticks * 0.05, 0, 1, 0)
        glRotatef(ticks * 0.03, 1, 0, 1)

        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        glLineWidth(2)
        glColor3f(*config.NEON_GREEN)
        glPushMatrix()
        glScalef(1.5, 1.5, 1.5)
        glCallList(self.octahedron_list)
        glPopMatrix()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        scale_pulse = 0.5 + (math.sin(ticks * 0.005) * 0.1)
        glScalef(scale_pulse * 1.5, scale_pulse * 1.5, scale_pulse * 1.5)
        glColor4f(config.NEON_GREEN[0], config.NEON_GREEN[1], config.NEON_GREEN[2], 0.6)
        glCallList(self.octahedron_list)

        glPopMatrix()

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        pygame.display.flip()


__all__ = ["IllusionScene"]
