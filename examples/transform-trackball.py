#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Copyright (c) 2014, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License.
# -----------------------------------------------------------------------------
""" This example shows reactive trackball transform """

import numpy as np
from glumpy import app, gl, glm, gloo
from glumpy.geometry import colorcube
from glumpy.transforms import Trackball, Position


vertex = """
uniform vec4 u_color;
attribute vec3 position;
attribute vec4 color;
varying vec4 v_color;
void main()
{
    v_color = u_color * color;
    gl_Position = <transform>;
}
"""

fragment = """
varying vec4 v_color;
void main()
{
    gl_FragColor = v_color;
}
"""

window = app.Window(width=1024, height=1024,
                    color=(0.30, 0.30, 0.35, 1.00))

@window.event
def on_draw(dt):
    window.clear()

    # Filled cube
    gl.glDisable(gl.GL_BLEND)
    gl.glEnable(gl.GL_DEPTH_TEST)
    gl.glEnable(gl.GL_POLYGON_OFFSET_FILL)
    cube['u_color'] = 1, 1, 1, 1
    cube.draw(gl.GL_TRIANGLES, faces)

    # Outlined cube
    gl.glDisable(gl.GL_POLYGON_OFFSET_FILL)
    gl.glEnable(gl.GL_BLEND)
    gl.glDepthMask(gl.GL_FALSE)
    cube['u_color'] = 0, 0, 0, 1
    cube.draw(gl.GL_LINES, outline)
    gl.glDepthMask(gl.GL_TRUE)


# Build cube data
V, I, O = colorcube()
vertices = V.view(gloo.VertexBuffer)
faces    = I.view(gloo.IndexBuffer)
outline  = O.view(gloo.IndexBuffer)

cube = gloo.Program(vertex, fragment)
cube.bind(vertices)
transform = Trackball(Position("position"))
cube['transform'] = transform
window.attach(transform)

# OpenGL initalization
gl.glEnable(gl.GL_DEPTH_TEST)
gl.glPolygonOffset(1, 1)
gl.glEnable(gl.GL_LINE_SMOOTH)
gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
gl.glLineWidth(0.75)

# Run
app.run()
