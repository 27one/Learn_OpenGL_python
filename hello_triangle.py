import glfw
import OpenGL.GL as gl
import numpy as np
from ctypes import c_void_p

SCR_WIDTH = 800
SCR_HEIGHT = 600

# GLSL로 작성된 vertex & fragment shader
vertexShaderSource = """
#version 330 core
layout (location = 0) in vec3 aPos;
void main()
{
    gl_Position = vec4(aPos.x, aPos.y, aPos.z, 1.0);
}"""

fragmentShaderSource = """  
#version 330 core
out vec4 FragColor;
void main()
{
    FragColor = vec4(1.0f, 0.5f, 0.2f, 1.0f);
}"""


def main():
    # glfw init
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)

    
    # glfw window 생성
    window = glfw.create_window(SCR_WIDTH, SCR_HEIGHT, "OpenGL Window!!", None, None)
    if window is None:
        glfw.terminate()
        raise Exception("Failed to create GLFW window!!")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    # vertexShader 객체 생성
    vertexShader = gl.glCreateShader(gl.GL_VERTEX_SHADER)
    # shader 소스 코드 정보 
    gl.glShaderSource(vertexShader, vertexShaderSource) 
    # 컴파일
    gl.glCompileShader(vertexShader)

    # vertexShader 컴파일 에러 체크
    success = gl.glGetShaderiv(vertexShader, gl.GL_COMPILE_STATUS)
    if not success:
        info_log = gl.glGetShaderInfoLog(vertexShader, 512, None)
        raise Exception("VERTEX_SHADER_COMPILE_ERROR\n%s" % info_log)

    # fragmentShader 객체 생성
    fragmentShader = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)
    # shader 소스 코드 정보 fragment shader 객체에 입력
    gl.glShaderSource(fragmentShader, fragmentShaderSource)  
    # 컴파일
    gl.glCompileShader(fragmentShader)

    # fragmentShader 컴파일 에러 체크
    success = gl.glGetShaderiv(fragmentShader, gl.GL_COMPILE_STATUS)
    if not success:
        info_log = gl.glGetShaderInfoLog(fragmentShader, 512, None)
        raise Exception("FRAGMENT_SHADER_COMPILE_ERROR\n%s" % info_log)

    # 컴파일 된 Shader를 shaderProgram으로 연결하여 사용dd
    shaderProgram = gl.glCreateProgram()
    gl.glAttachShader(shaderProgram, vertexShader)
    gl.glAttachShader(shaderProgram, fragmentShader)
    gl.glLinkProgram(shaderProgram)

    # shader link 에러 체크
    success = gl.glGetProgramiv(shaderProgram, gl.GL_LINK_STATUS)
    if not success:
        info_log = gl.glGetProgramInfoLog(shaderProgram, 512, None)
        raise Exception("SHADER_PROGRAM_LINK_ERROR\n%s" % info_log)
    
    # Program 객체에 연결된 shader 객체들은 삭제
    gl.glDeleteShader(vertexShader)
    gl.glDeleteShader(fragmentShader)

    # vertex 정보 
    vertices = np.array([
        -0.5, -0.5, 0.0,  
        0.5, -0.5, 0.0,  
        0.0, 0.5, 0.0  
    ], dtype="float32")   

    # VAO 객체 생성
    VAO = gl.glGenVertexArrays(1)
    # VBO 객체 생성
    VBO = gl.glGenBuffers(1)
    # bind the Vertex Array Object first, then bind and set vertex buffer(s), and then configure vertex attributes(s).
    gl.glBindVertexArray(VAO)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, VBO)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, vertices.nbytes, vertices, gl.GL_STATIC_DRAW)  # INFO: use np.array with nsize
    
    # Vertex의 속성 포인터의 시작점과 데이터 정보를 설정
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 0, c_void_p(0))  
    # 정점 데이터들을 gpu로 보냈고, shaderprogram을 통해 어떻게 처리할 지 지시
    # 메모리상의 정점 데이터에 대한 해석과 정점 데이터를 vertex shader의 속성과 어떻게 연결해야하는 지는 모른다.

    # 첫 번쨰 param : vertex 속성 지정 
    # 두 번쨰 param : vertex 속성의 크기 (vec3 : 3)
    # 세 번쨰 param : 데이터 type (GLSL 에서 vec이 실수로 저장되어 있으니 float)
    # 네 번째 param : 정규화 여부 
    # 다섯 번쨰 param : vertex 속성 사이의 간격을 의미 (다음 좌표를 의미 하는 데이터는 3개의 Float 크기 데이터 이후에 존재(x,y,z)값이므로 )
    # 여섯 번째 param : 버퍼에서 데이터가 시작하는 위치의 초기 값 
    gl.glEnableVertexAttribArray(0)

    # note that this is allowed, the call to glVertexAttribPointer registered VBO as the vertex attribute's bound vertex buffer object so afterwards we can safely unbind
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)

    # You can unbind the VAO afterwards so other VAO calls won't accidentally modify this VAO, but this rarely happens. Modifying other
    # VAOs requires a call to glBindVertexArray anyways so we generally don't unbind VAOs (nor VBOs) when it's not directly necessary.
    gl.glBindVertexArray(0)

    # 렌더링 루프
    while not glfw.window_should_close(window):
        
        process_input(window)

        # 배경색 렌더링
        gl.glClearColor(0.2, 0.3, 0.3, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        # 
        gl.glUseProgram(shaderProgram)
        gl.glBindVertexArray(VAO)
        gl.glDrawArrays(gl.GL_TRIANGLES, 0, 3)
        # gl.glBindVertexArray(0) # no need to unbind it every time

        # glfw: swap buffers and poll IO events (keys pressed/released, mouse moved etc.)
        glfw.swap_buffers(window)
        glfw.poll_events()

    # optional: de-allocate all resources once they've outlived their purpose:
    gl.glDeleteVertexArrays(1, VAO)
    gl.glDeleteBuffers(1, VBO)
    gl.glDeleteProgram(shaderProgram)

    # glfw: terminate, clearing all previously allocated GLFW resources.
    glfw.terminate()
    return 0


# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
def process_input(window):
    if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
        print("Escape key pressed.")
        glfw.set_window_should_close(window, True)


# glfw: whenever the window size changed (by OS or user resize) this callback function executes
def framebuffer_size_callback(window, width, height):
    print("Window resized.")
    # make sure the viewport matches the new window dimensions; note that width and
    gl.glViewport(0, 0, width, height)


if __name__ == '__main__':
    main()