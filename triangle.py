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

    # VERTEX 정보
    vertices = np.array([
        -0.5, -0.5,  0.0,
        0.5, -0.5,  0.0,
        0.0,  0.5,  0.0], dtype=np.float32)
    
    vertices_size = vertices.size * vertices.itemsize


    # VBO 객체 생성
    VBO = gl.glGenBuffers(1)

    # GL_ARRAY_BUFFER로 들어오면 VBO로 저장
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)

    # VERTEX 정보 VBO에 저장
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices_size, vertices, gl.GL_STATIC_DRAW)

    # vertex shader
    vertex_shader = shaders.compileShader(vertex_shader_source, gl.GL_VERTEX_SHADER)

    # fragment shader
    fragment_shader = shaders.compileShader(fragment_shader_source, gl.GL_FRAGMENT_SHADER)

    # ShaderProgram에 연결하고 연결된 Shader 삭제
    shader = shaders.compileProgram(vertex_shader, fragment_shader)
    gl.glDeleteShader(vertex_shader)
    gl.glDeleteShader(fragment_shader)

    # VAO 객체 생성
    VAO = gl.glGenVertexArrays(1)
    # VAO 정보 바인드
    gl.glBindVertexArray(VAO)
    # shaderProgram으로 부터 위치 정보 
    position = gl.glGetAttribLocation(shader, "position")
    # Vertex의 속성 포인터의 시작점과 데이터 정보를 설정
    gl.glVertexAttribPointer(position, 3, gl.GL_FLOAT, gl.GL_FALSE, vertices.itemsize * 3, c_void_p(0))
    gl.glEnableVertexAttribArray(position)
    # 첫 번쨰 param : vertex 속성 지정 
    # 두 번쨰 param : vertex 속성의 크기 (vec3 : 3)
    # 세 번쨰 param : 데이터 type (GLSL 에서 vec이 실수로 저장되어 있으니 float)
    # 네 번째 param : 정규화 여부 
    # 다섯 번쨰 param : vertex 속성 사이의 간격을 의미 (다음 좌표를 의미 하는 데이터는 3개의 Float 크기 데이터 이후에 존재(x,y,z)값이므로 )
    # 여섯 번째 param : 버퍼에서 데이터가 시작하는 위치의 초기 값 

    gl.glUseProgram(shader)
    
    # 렌더링 루프
    while not glfw.window_should_close(window):
        process_input(window)

        glfw.poll_events()
        # 배경색 렌더링
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        # 삼각형 그리기
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)

        glfw.swap_buffers(window)
    glfw.terminate()


def on_resize(window, w, h):
    gl.glViewport(0, 0, w, h)

def process_input(window):
    
    if (glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS):
        glfw.set_window_should_close(window, True)

if __name__ == "__main__":
    main()