import glfw
import OpenGL.GL as gl

import numpy as np
import sys
import ctypes

# class VBO:
#     def __init__(self) -> None:
#          self.vbo = gl.glGenBuffers(1)
#          self.component_count = 0
#          self.vertex_count = 0

#     def __del__(self) -> None:
#         gl.glDeleteBuffers(1, [self.vbo])

#     def bind(self) -> None:
#         gl.glBindBuffer(gl.GL_ARRAY_BUFFER, self.vbo)

#     def unbind(self) -> None:
#         gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

#     def set_vertex_attribute(self, component_count: int, bytelength: int, data: any) -> None:

#         self.component_count = component_count
#         stride = 4 * self.component_count
#         self.vertex_count = bytelength// stride
#         self.bind()
#         gl.glBufferData(gl.GL_ARRAY_BUFFER, bytelength, data, gl.GL_STATIC_DRAW)

#     def set_slot(self, slot: int) -> None:
#         self.bind()
#         gl.glEnableVertexAttribArray(slot)
#         gl.glVertexAttribPointer(slot, self.component_count, gl.GL_FLOAT, gl.GL_FALSE, 0, None)

#     def draw(self) -> None:
#         gl.glDrawArrays(gl.GL_TRIANGLES, 0, self.vertex_count)

def main():
    # glfw init
    glfw.init()

    # glfw window hint - version 3.3 for learnopengl document
    # use core profile only
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    vertices = np.array([-0.5, -0.5, 0.0,
                        0.5, -0.5, 0.0,
                        0.0, 0.5, 0.0], dtype='float32')
    # VBO 객체 생성
    VBO = gl.glGenBuffers(1) # 1: buffer의 고유 ID
    # GL_ARRAY_BUFFER로 바인딩, 이후 호출하는 모든 버퍼는 현재 바인딩된 VBO 사용
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    # 바인딩 된 버퍼에 정의된 vertices 데이터 복사
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    # GLSL로 작성된 vertex shader
    vertex_shader_src = """
    #version 330 core
    layout (location = 0) in vec3 aPos;
    void main()
    {
        gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0f);
    }
    """
    # GLSL로 작성된 fragment shader 
    fragment_shader_src = """
    #version 330 core
    out vec4 FragColor;
    void main()
    {
        FragColor = vec4(1.0f, 0.5f, 0.2f 1.0f);
    }
    """
    # vertex shader 객체 생성
    vertex_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    # shader 소스 코드 정보 vertex shader 객체에 입력
    gl.glShaderSource(vertex_shader, vertex_shader_src)
    # 컴파일
    gl.glCompileShader(vertex_shader)

    # fragment shader 객체 생성
    fragment_shader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    # shader 소스 코드 정보 fragment shader 객체에 입력
    gl.glShaderSource(fragment_shader, fragment_shader_src)
    # 컴파일
    gl.glCompileShader(fragment_shader)

    # 컴파일 된 여러 shader를 shader program으로 연결하여 사용
    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertex_shader)
    gl.glAttachShader(shaderProgram, fragment_shader)
    gl.glLinkProgram(shaderProgram)
    
    # program 객체에 연결된 shader 객체들은 삭제
    # gl.glDeleteShader(vertex_shader)
    # gl.glDeleteShader(fragment_shader)

    
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3*sys.getsizeof(float), None)
    gl.glEnableVertexAttribArray(0)

    # 정점 데이터들을 gpu로 보냈고, shaderprogram을 통해 어떻게 처리할 지 지시
    # 메모리상의 정점 데이터에 대한 해석과 정점 데이터를 vertex shader의 속성과 어떻게 연결해야하는 지는 모른다.
    
    # 첫 번쨰 param : vertex 속성 지정 
    # 두 번쨰 param : vertex 속성의 크기 (vec3 : 3)
    # 세 번쨰 param : 데이터 type (GLSL 에서 vec이 실수로 저장되어 있으니 float)
    # 네 번째 param : 정규화 여부 
    # 다섯 번쨰 param : vertex 속성 사이의 간격을 의미 (다음 좌표를 의미 하는 데이터는 3개의 Float 크기 데이터 이후에 존재(x,y,z)값이므로 )
    # 여섯 번째 param : 버퍼에서 데이터가 시작하는 위치의 초기 값 
    
    

    # VAO 객체 생성
    VAO = gl.glGenVertexArrays(1)

    #
    gl.glBindVertexArray(VAO)

    gl.glBufferData(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sys.getsizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 3*sys.getsizeof(float), None)
    gl.glEnableVertexAttribArray(0)

    

    window = glfw.create_window(800, 600, "OpenGL Window!!", None, None)
    if window is None:
        print("Failed to create glfw window!!")
        return 
    
    glfw.make_context_current(window)
    gl.glViewport(0, 0, 800, 600)

    

    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)    

    while not glfw.window_should_close(window):
        processInput(window)

        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        
        # 생성한 shaderProgram 사용
        gl.glUseProgram(shaderProgram)
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0 , 3)



        glfw.swap_buffers(window)
        glfw.poll_events()

    
    glfw.terminate()

    return 

def framebuffer_size_callback(window, width, height):
        gl.glViewport(0,0, width, height)
    
        return
    
def processInput(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        glfw.set_window_should_close(window, True)
    
        return
if __name__ == "__main__":
    main()