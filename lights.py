import sys
import glfw
import OpenGL.GL as gl
from pathlib import Path
import glm
from ctypes import c_float, sizeof, c_void_p

CURDIR = Path(__file__).parent.absolute()
RESDIR = CURDIR.joinpath("resources")
sys.path.append(str(CURDIR))

from shader import Shader

# -- settings
SRC_WIDTH = 800
SRC_HEIGHT = 600

light_pos = glm.vec3([1.2, 1.0, 2.0])


def main():

    if not glfw.init():
        raise ValueError("Failed to initialize glfw")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)

    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(SRC_WIDTH, SRC_HEIGHT, "learnOpenGL", None, None)
    if not window:
        glfw.terminate()
        raise ValueError("Failed to create window")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    gl.glEnable(gl.GL_DEPTH_TEST)

    lamp_shader = Shader(CURDIR / "shaders/lamp.vs", CURDIR / "shaders/lamp.fs")
    lighting_shader = Shader(CURDIR / "shaders/lighting.vs", CURDIR / "shaders/lighting.fs")

    vertices = [
        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5,  0.5, -0.5,
         0.5,  0.5, -0.5,
        -0.5,  0.5, -0.5,
        -0.5, -0.5, -0.5,

        -0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        -0.5, -0.5,  0.5,

        -0.5,  0.5,  0.5,
        -0.5,  0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5, -0.5,
        -0.5, -0.5,  0.5,
        -0.5,  0.5,  0.5,

         0.5,  0.5,  0.5,
         0.5,  0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5,  0.5,
         0.5,  0.5,  0.5,

        -0.5, -0.5, -0.5,
         0.5, -0.5, -0.5,
         0.5, -0.5,  0.5,
         0.5, -0.5,  0.5,
        -0.5, -0.5,  0.5,
        -0.5, -0.5, -0.5,

        -0.5,  0.5, -0.5,
         0.5,  0.5, -0.5,
         0.5,  0.5,  0.5,
         0.5,  0.5,  0.5,
        -0.5,  0.5,  0.5,
        -0.5,  0.5, -0.5,
    ]
    vertices = (c_float * len(vertices))(*vertices)

    cube_vao = gl.glGenVertexArrays(1)
    vbo = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glBindVertexArray(cube_vao)

    # -- position attribute
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    # -- second configure light vao (vbo is the same)
    light_vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(light_vao)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    

    while not glfw.window_should_close(window):
        # -- input
        process_input(window)

        # -- render
        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        lighting_shader.use()
        lighting_shader.set_vec3("objectColor", [1.0, 0.5, 0.31])
        lighting_shader.set_vec3("lightColor", [1.0, 1.0, 1.0])
        model = glm.mat4()
        model = glm.rotate(model, glm.radians(-55.0), glm.vec3([1.0, 0.0, 0.0]))

        view = glm.mat4()
        view = glm.translate(view, glm.vec3([0.0, 0.0, -3.0]))

        projection = glm.perspective(glm.radians(150.0), 800/600, 0.1, 100.0)
        modelLoc = gl.glGetUniformLocation(lighting_shader.ID, "model")
        gl.glUniformMatrix4fv(modelLoc, 1, gl.GL_FALSE, glm.value_ptr(model))

        viewLoc = gl.glGetUniformLocation(lighting_shader.ID, "view")
        gl.glUniformMatrix4fv(viewLoc, 1, gl.GL_FALSE, glm.value_ptr(view))

        projectionLoc = gl.glGetUniformLocation(lighting_shader.ID, "projection")
        gl.glUniformMatrix4fv(projectionLoc, 1, gl.GL_FALSE, glm.value_ptr(projection))

        gl.glBindVertexArray(cube_vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        lamp_shader.use()

        model = glm.mat4()
        model = glm.translate(model, light_pos)
        model = glm.scale(model, glm.vec3(0.2))

        # view = glm.mat4()
        # view = glm.translate(view, glm.vec3([0.0, 0.0, -3.0]))

        # projection = glm.perspective(glm.radians(100.0), 800/600, 0.1, 100.0)

        modelLoc = gl.glGetUniformLocation(lamp_shader.ID, "model")
        gl.glUniformMatrix4fv(modelLoc, 1, gl.GL_FALSE, glm.value_ptr(model))

        viewLoc = gl.glGetUniformLocation(lamp_shader.ID, "view")
        gl.glUniformMatrix4fv(viewLoc, 1, gl.GL_FALSE, glm.value_ptr(view))

        projectionLoc = gl.glGetUniformLocation(lamp_shader.ID, "projection")
        gl.glUniformMatrix4fv(projectionLoc, 1, gl.GL_FALSE, glm.value_ptr(projection))
        

        gl.glBindVertexArray(light_vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        glfw.swap_buffers(window)
        glfw.poll_events()

    gl.glDeleteVertexArrays(1, id(cube_vao))
    gl.glDeleteVertexArrays(1, id(light_vao))
    gl.glDeleteBuffers(1, id(vbo))
    glfw.terminate()


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


def framebuffer_size_callback(window, width, height):
    gl.glViewport(0, 0, width, height)




if __name__ == '__main__':
    main()
