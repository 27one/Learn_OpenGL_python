import glfw
import OpenGL.GL as gl
import OpenGL.GL.shaders as shaders
import numpy as np
from ctypes import c_void_p

# GLSL로 작성된 vertex & fragment shader
vertex_shader_source = """
#version 330 core

in vec3 position;

void main() {
    gl_Position = vec4(position, 1.0f);
}
"""

fragment_shader_source = """
#version 330 core

out vec4 FragColor;

void main() {
    FragColor = vec4(0.5f, 0.5f, 0.2f, 1.0f);
}
"""

def main():
    # glfw init
    if not glfw.init():
        return -1
    # pyopengl version : 3.1!!
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    # glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(800, 600, "Learn OpenGL", None, None)
    if window is None:
        print("Failed to create glfw window")
        glfw.terminate()
        return -1

    # make_context_current 사용될 때 view port 설정됨.
    glfw.make_context_current(window)
    glfw.set_window_size_callback(window, on_resize)

    
    # vertices = np.array([
    #     -0.5, -0.5,  0.0,
    #     0.5, -0.5,  0.0,
    #     0.0,  0.5,  0.0], dtype=np.float32)
    # VERTEX 정보 수정
    vertices = np.array([
        0.5, 0.5,  0.0,
        0.5, -0.5,  0.0,
        -0.5,  -0.5,  0.0,
        -0.5, 0.5, 0.0], dtype=np.float32)
    
    # index 정보
    indices = np.array([    
        0, 1, 3,    
        1, 2, 3    
    ], dtype=np.int32)

    # vertex shader
    vertex_shader = shaders.compileShader(vertex_shader_source, gl.GL_VERTEX_SHADER)

    # fragment shader
    fragment_shader = shaders.compileShader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)

    # ShaderProgram에 연결하고 연결된 Shader 삭제
    shader = shaders.compileProgram(vertex_shader, fragment_shader)
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    # VBO 객체 생성
    VAO = gl.glGenVertexArrays(1)
    VBO = gl.glGenBuffers(1)
    EBO = gl.glGenBuffers(1)

    # VAO 바인드
    gl.glBindVertexArray(VAO)
    # VBO 바인드 하고, VERTEX INFO 입력
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)
    # EBO 바인드하고, INDEX INFO 입력
    gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, EBO)
    gl.glBufferData(gl.GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, gl.GL_STATIC_DRAW)
    # VAO INFO
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, 3*4, 0, c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    # 렌더링 루프에서 바인드하기 위해 unbind
    gl.glBindVertexArray(0)

    # gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_LINE)
    gl.glPolygonMode(gl.GL_FRONT_AND_BACK, gl.GL_FILL)

    # 렌더링 루프
    while not glfw.window_should_close(window):
        process_input(window)

        glfw.poll_events()
        # 배경색 렌더링
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # 사각형 그리기
        gl.glUseProgram(shader)
        gl.glBindVertexArray(VAO)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, None)
        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)

def process_input(window):
    
    if (glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()