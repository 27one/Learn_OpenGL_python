import sys
import glfw
import OpenGL.GL as gl
import glm
from PIL import Image
from pathlib import Path
from ctypes import c_uint, c_float, sizeof, c_void_p

CURDIR = Path(__file__).parent.absolute()
RESDIR = CURDIR.joinpath("resources")
sys.path.append(str(CURDIR))

from shader import Shader


def Tex(fn):
    return RESDIR.joinpath("textures", fn)


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if not window:
        print("Window Creation failed!")
        glfw.terminate()

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)

    shader = Shader(CURDIR / 'shaders/trans.vs', CURDIR / 'shaders/trans.fs')

    print(shader)
    vertices = [
     # positions         colors          tex_coords
     0.5,  0.5, 0.0,  1.0, 0.0, 0.0,  1.0, 1.0,  # top right
     0.5, -0.5, 0.0,  0.0, 1.0, 0.0,  1.0, 0.0,  # bottom right
    -0.5, -0.5, 0.0,  0.0, 0.0, 1.0,  0.0, 0.0,  # bottom left
    -0.5,  0.5, 0.0,  1.0, 1.0, 0.0,  0.0, 1.0,  # top left
    ]
    vertices = (c_float * len(vertices))(*vertices)

    indices = [
        0, 1, 3,
        1, 2, 3
    ]
    indices = (c_uint * len(indices))(*indices)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    ebo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, ebo)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, sizeof(indices), indices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(1)

    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(2)

    # -- load texture
    texture = gl.glGenTextures(1)
    gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
    # -- texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_REPEAT)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_REPEAT)
    # -- texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR_MIPMAP_LINEAR)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)

    img = Image.open(Tex('avikus.jpg')).transpose(Image.FLIP_TOP_BOTTOM)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width, img.height, 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, img.tobytes())
    gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    # vec = glm.vec4([1.0, 0.0,  0.0, 1.0])
    # trans = glm.mat4()
    # trans = glm.translate(trans, glm.vec3([1.0,1.0,0.0]))
    # vec = trans*vec

    # trans = glm.mat4()
    # trans = glm.rotate(trans, glm.radians(90.0), glm.vec3([0.0, 0.0, 1.0]))
    # trans = glm.scale(trans, glm.vec3([0.5, 0.5, 0.5]))

    
    
    while not glfw.window_should_close(window):
        process_input(window)

        gl.glClearColor(.2, .3, .3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glBindTexture(gl.GL_TEXTURE_2D, texture)
        trans = glm.mat4()
        # trans = glm.translate(trans, glm.vec3([0.5, -0.5, 0.0]))
        trans = glm.rotate(trans, glfw.get_time(), glm.vec3([0.0, 0.0, 1.0]))
        shader.use()
        # shader.set_mat4('transform', glm.value_ptr(trans))
        transformLoc = gl.glGetUniformLocation(shader.ID, "transform")
        gl.glUniformMatrix4fv(transformLoc, 1, gl.GL_FALSE, glm.value_ptr(trans))      
        gl.glBindVertexArray(vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, c_void_p(0))

        glfw.poll_events()
        glfw.swap_buffers(window)

    gl.glDeleteVertexArrays(1, id(vao))
    gl.glDeleteBuffers(1, id(vbo))
    gl.glDeleteBuffers(1, id(ebo))
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == '__main__':
    main()