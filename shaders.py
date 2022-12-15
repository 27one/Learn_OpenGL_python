import math
import glfw
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
from ctypes import c_float, sizeof, c_void_p


vertex_shader = """
#version 330 core

layout (location = 0) in vec3 aPos;
layout (location = 1) in vec3 aColor;

out vec3 ourColor;

void main() {
    gl_Position = vec4(aPos, 1.0);
    ourColor = aColor;
}
"""

fragment_shader = """
#version 330 core

out vec4 FragColor;
in vec3 ourColor;

void main() {
    FragColor = vec4(ourColor, 1.);
}
"""


def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    
    # glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True) For MacOS

    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if not window:
        print("Window Creation failed!")
        glfw.terminate()

    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)

    # vertexShader 객체 생성
    vertexShader = shaders.compileShader(vertex_shader, gl.GL_VERTEX_SHADER)
    fragmentShader = shaders.compileShader(fragment_shader, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertexShader, fragmentShader)
    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)
    

    
    vertices = [
        -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
         0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
         0.0,  0.5, 0.0, 0.0, 0.0, 1.0
    ]
    vertices = (c_float * len(vertices))(*vertices)

    vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(vao)

    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 6 * sizeof(c_float), c_void_p(3*sizeof(c_float)))
    gl.glEnableVertexAttribArray(1)

    # gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
    # gl.glBindVertexArray(0)

    while not glfw.window_should_close(window):
        process_input(window)

        gl.glClearColor(.2, .3, .3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        gl.glUseProgram(shader)

        time = glfw.get_time()
        green_val = math.sin(time) / 2.0 + 0.5
        ourColor_location = gl.glGetUniformLocation(shader, "ourColor")
        gl.glUniform4f(ourColor_location, 0.0, green_val, 0.0, 1.0)

        gl.glBindVertexArray(vao)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        glfw.poll_events()
        glfw.swap_buffers(window)

    gl.glDeleteVertexArrays(1, id(vao))
    gl.glDeleteBuffers(1, id(vbo))
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)


def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)


if __name__ == '__main__':
    main()