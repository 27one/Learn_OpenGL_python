import glfw
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import numpy as np
from ctypes import c_void_p
vertex_shader_source = """
#version 330 core
in vec3 position;
in vec3 color;
out vec3 new_color;
void main() {
    gl_Position = vec4(position, 1.0f);
    new_color = color;
}
"""
fragment_shader_source = """
#version 330 core
in vec3 new_color;
out vec4 FragColor;
void main() {
    FragColor = vec4(new_color, 1.0f);
}
"""
def main():
    if not glfw.init():
        return -1
    # glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    # glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    window = glfw.create_window(800, 600, "LearnOpenGL", None, None)
    if window is None:
        print("Failed to create glfw window")
        glfw.terminate()
        return -1
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)
    triangle = np.array([-0.5, -0.5,  0.0,  1.0,  0.0,  0.0,
                          0.5, -0.5,  0.0,  0.0,  1.0,  0.0,
                          0.0,  0.5,  0.0,  0.0,  0.0,  1.0,
    ], dtype=np.float32)
    triangle_size = triangle.itemsize * triangle.size
    print(f"triangle size: {triangle_size}")
    vertex_shader = shaders.compileShader(vertex_shader_source, gl.GL_VERTEX_SHADER)
    fragment_shader = shaders.compileShader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)
    shader = shaders.compileProgram(vertex_shader, fragment_shader)
    gl.glDeleteShader(fragment_shader)
    gl.glDeleteShader(vertex_shader)
    vbo = gl.glGenBuffers(1)
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, triangle_size, triangle, gl.GL_STATIC_DRAW)
    position = gl.glGetAttribLocation(shader, "position")
    gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, gl.GL_FALSE, triangle.itemsize * 6, c_void_p(0))
    gl.glEnableVertexAttribArray(position)
    color = gl.glGetAttribLocation(shader, "color")
    gl.glVertexAttribPointer(color, 3, gl.GL_FLOAT, gl.GL_FALSE, triangle.itemsize * 6, c_void_p(12))
    gl.glEnableVertexAttribArray(color)
    gl.glUseProgram(shader)
    gl.glClearColor(0, 0, 0, 0)
    while not glfw.window_should_close(window):
        glfw.poll_events()
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        glfw.swap_buffers(window)
    glfw.terminate()
def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)
if __name__ == "__main__":
    main()