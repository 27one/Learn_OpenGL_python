import sys
import math
import glfw
import OpenGL.GL as gl
from pathlib import Path
from pyrr import Vector3, Matrix44, matrix44
from ctypes import c_float, sizeof, c_void_p
from PIL import Image
import os

CURDIR = Path(__file__).parent.absolute()
RESDIR = CURDIR.joinpath("resources")
TEXDIR = RESDIR.joinpath("textures")
sys.path.append(str(CURDIR))

from shader import Shader

# -- settings
SRC_WIDTH = 800
SRC_HEIGHT = 600

view_pos = Vector3([0.0, 0.0, 11.0])

def main():

    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    window = glfw.create_window(SRC_WIDTH, SRC_HEIGHT, "learnOpenGL", None, None)
    if not window:
        glfw.terminate()
        raise ValueError("Failed to create window")

    glfw.make_context_current(window)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)
   
    # glfw.set_input_mode(window, glfw.CURSOR, glfw.CURSOR_DISABLED)

    gl.glEnable(gl.GL_DEPTH_TEST)

    lamp_shader = Shader(CURDIR / "shaders/lamp.vs", CURDIR / "shaders/lamp.fs")
    lighting_shader = Shader(CURDIR / "shaders/multiple_lights.vs", CURDIR / "shaders/multiple_lights.fs")

    vertices = [
        # positions        normals           texture coords
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,
         0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  1.0,  1.0,
        -0.5,  0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  1.0,
        -0.5, -0.5, -0.5,  0.0,  0.0, -1.0,  0.0,  0.0,

        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,
         0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  1.0,  1.0,
        -0.5,  0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  1.0,
        -0.5, -0.5,  0.5,  0.0,  0.0,  1.0,  0.0,  0.0,

        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,
        -0.5,  0.5, -0.5, -1.0,  0.0,  0.0,  1.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5, -0.5, -1.0,  0.0,  0.0,  0.0,  1.0,
        -0.5, -0.5,  0.5, -1.0,  0.0,  0.0,  0.0,  0.0,
        -0.5,  0.5,  0.5, -1.0,  0.0,  0.0,  1.0,  0.0,

         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,
         0.5,  0.5, -0.5,  1.0,  0.0,  0.0,  1.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  1.0,  0.0,  0.0,  0.0,  1.0,
         0.5, -0.5,  0.5,  1.0,  0.0,  0.0,  0.0,  0.0,
         0.5,  0.5,  0.5,  1.0,  0.0,  0.0,  1.0,  0.0,

        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,
         0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  1.0,  1.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
         0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  1.0,  0.0,
        -0.5, -0.5,  0.5,  0.0, -1.0,  0.0,  0.0,  0.0,
        -0.5, -0.5, -0.5,  0.0, -1.0,  0.0,  0.0,  1.0,

        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0,
         0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  1.0,  1.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
         0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  1.0,  0.0,
        -0.5,  0.5,  0.5,  0.0,  1.0,  0.0,  0.0,  0.0,
        -0.5,  0.5, -0.5,  0.0,  1.0,  0.0,  0.0,  1.0
    ]
    vertices = (c_float * len(vertices))(*vertices)

    cube_positions = [
        ( 2.0,  5.0, -15.0),
        (-1.5, -2.2, -2.5),
        (-3.8, -2.0, -12.3),
        ( 2.4, -0.4, -3.5),
        (-1.7,  3.0, -7.5),
        ( 1.3, -2.0, -2.5),
        ( 1.5,  2.0, -2.5),
        ( 1.5,  0.2, -1.5),
        (-1.3,  1.0, -1.5)
    ]

    # cube_positions = [
    #     ( 0.0,  0.0,  0.0),
    #     ( 1.0, 1.0, 1.0)
    # ]

    # point_light_positions = [
    #     ( 0.7,  0.2,  2.0),
    #     ( 2.3, -3.3, -4.0),
    #     (-4.0,  2.0, -12.0),
    #     ( 0.0,  0.0, -3.0),
    # ]

    point_light_positions = [
        (5., 5., 0.)
    ]
    cube_vao = gl.glGenVertexArrays(1)
    vbo = gl.glGenBuffers(1)

    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glBufferData(gl.GL_ARRAY_BUFFER, sizeof(vertices), vertices, gl.GL_STATIC_DRAW)

    gl.glBindVertexArray(cube_vao)

    # position attribute
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)
    # normal attribute
    gl.glVertexAttribPointer(1, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(3 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(1)
    # texture coordinate
    gl.glVertexAttribPointer(2, 2, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(6 * sizeof(c_float)))
    gl.glEnableVertexAttribArray(2)

    # vao for light
    light_vao = gl.glGenVertexArrays(1)
    gl.glBindVertexArray(light_vao)
    
    # use only postion attribute
    gl.glBindBuffer(gl.GL_ARRAY_BUFFER, vbo)
    gl.glVertexAttribPointer(0, 3, gl.GL_FLOAT, gl.GL_FALSE, 8 * sizeof(c_float), c_void_p(0))
    gl.glEnableVertexAttribArray(0)

    # load texture
    load_texture("container.jpg")
    
    while not glfw.window_should_close(window):
        process_input(window)

        gl.glClearColor(0.1, 0.1, 0.1, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        lighting_shader.use()
        lighting_shader.set_vec3("viewPos", view_pos)
        lighting_shader.set_float("material.shininess", 256.0)

        # directional light
        lighting_shader.set_vec3("dirLight.direction", [-0.2, -1.0, -0.3])
        lighting_shader.set_vec3("dirLight.ambient", [0.0, 0.0, 0.0])
        lighting_shader.set_vec3("dirLight.diffuse", [0., 0., 0.])
        theta = glfw.get_time()

        # point light 1
        lighting_shader.set_vec3("pointLights[0].position", [point_light_positions[0][0]*math.sin(theta), point_light_positions[0][1]*math.cos(theta), point_light_positions[0][2]])
        lighting_shader.set_vec3("pointLights[0].ambient", [.1, .1, .1])
        lighting_shader.set_vec3("pointLights[0].diffuse", [2.0, 2.0, 2.0])
        lighting_shader.set_vec3("pointLights[0].specular", [2.0, 2.0, 2.0])
        lighting_shader.set_float("pointLights[0].constant", 1.0)
        lighting_shader.set_float("pointLights[0].linear", 0.09)
        lighting_shader.set_float("pointLights[0].quadratic", 0.032)
        # # point light 2
        # lighting_shader.set_vec3("pointLights[1].position", point_light_positions[1])
        # lighting_shader.set_vec3("pointLights[1].ambient", [0.0, 0.0, 0.0])
        # lighting_shader.set_vec3("pointLights[1].diffuse", [0., 0., 0.])
        # lighting_shader.set_float("pointLights[1].constant", 1.0)
        # lighting_shader.set_float("pointLights[1].linear", 0.09)
        # lighting_shader.set_float("pointLights[1].quadratic", 0.032)
        # # point light 3
        # lighting_shader.set_vec3("pointLights[2].position", point_light_positions[2])
        # lighting_shader.set_vec3("pointLights[2].ambient", [0.0, 0.0, 0.0])
        # lighting_shader.set_vec3("pointLights[2].diffuse", [0., 0., 0.])
        # lighting_shader.set_float("pointLights[2].constant", 1.0)
        # lighting_shader.set_float("pointLights[2].linear", 0.09)
        # lighting_shader.set_float("pointLights[2].quadratic", 0.032)
        # # point light 4
        # lighting_shader.set_vec3("pointLights[3].position", point_light_positions[3])
        # lighting_shader.set_vec3("pointLights[3].ambient", [0.0, 0.0, 0.0])
        # lighting_shader.set_vec3("pointLights[3].diffuse", [0., 0., 0.])
        # lighting_shader.set_float("pointLights[3].constant", 1.0)
        # lighting_shader.set_float("pointLights[3].linear", 0.09)
        # lighting_shader.set_float("pointLights[3].quadratic", 0.032)
        # spotLight
        # lighting_shader.set_vec3("spotLight.position", view_pos)
        # lighting_shader.set_vec3("spotLight.direction", [0.0, 0.0, -1.0])
        # lighting_shader.set_vec3("spotLight.ambient", [0.0, 0.0, 0.0])
        # lighting_shader.set_vec3("spotLight.diffuse", [0.0, 0.0, 0.0])
        # lighting_shader.set_float("spotLight.constant", 1.0)
        # lighting_shader.set_float("spotLight.linear", 0.09)
        # lighting_shader.set_float("spotLight.quadratic", 0.032)
        # lighting_shader.set_float("spotLight.cutOff", math.cos(math.radians(12.5)))
        # lighting_shader.set_float("spotLight.outerCutOff", math.cos(math.radians(15.0)))

        # view.projection transformations
        projection = Matrix44.perspective_projection(45, SRC_WIDTH/SRC_HEIGHT, 0.1, 100.0)
        view = Matrix44.look_at(view_pos, Vector3([0.0, 0.0, -1.0]), Vector3([0. , 1.0, .0]))
        lighting_shader.set_mat4("projection", projection)
        lighting_shader.set_mat4("view", view)

        # world transformation
        model = Matrix44.identity()
        lighting_shader.set_mat4("model", model)

        # draw cubes
        gl.glBindVertexArray(cube_vao)
        for idx, position in enumerate(cube_positions):
            angle = 20.0 * idx
            rotation = matrix44.create_from_axis_rotation([1.0, 0.3, 0.5], math.radians(angle))
            spin = matrix44.create_from_axis_rotation([1.0, 0.3, 0.5], glfw.get_time())
            translation = Matrix44.from_translation(position)
            model = translation * rotation 
            lighting_shader.set_mat4('model', model)
            gl.glDrawArrays(gl.GL_TRIANGLES, 0, 36)

        # draw lamp 
        lamp_shader.use()
        lamp_shader.set_mat4("projection", projection)
        lamp_shader.set_mat4("view", view)

        gl.glBindVertexArray(light_vao)

        for pos in point_light_positions:
            model = Matrix44.identity()
            pos = list(pos)
            pos[0] *= math.sin(theta)
            pos[1] *= math.cos(theta)
            model *= Matrix44.from_translation(pos)
            # model *= matrix44.create_from_axis_rotation([1.0, .0, .0], glfw.get_time())
            model *= Matrix44.from_scale(Vector3([.2, .2, .2]))

            lamp_shader.set_mat4("model", model)
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


def load_texture(path,
                 mag_filter=gl.GL_LINEAR,
                 min_filter=gl.GL_LINEAR_MIPMAP_LINEAR,
                 wrap_s=gl.GL_REPEAT, wrap_t=gl.GL_REPEAT,
                 flip_y=False, flip_x=False,
                 generate_mipmaps=True):

    textureID = gl.glGenTextures(1)
    img = Image.open(os.path.join(TEXDIR, path))
    img = flip_image(img, flip_x, flip_y)

    format_ = {
        1 : gl.GL_RED,
        3 : gl.GL_RGB,
        4 : gl.GL_RGBA,
    }.get(len(img.getbands()))

    gl.glBindTexture(gl.GL_TEXTURE_2D, textureID)
    gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, img.width, img.height, 0, format_, gl.GL_UNSIGNED_BYTE, img.tobytes())
    if generate_mipmaps:
        gl.glGenerateMipmap(gl.GL_TEXTURE_2D)

    # texture wrapping
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, wrap_s)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, wrap_t)
    # texture filterting
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, min_filter)
    gl.glTexParameter(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, mag_filter)

    return textureID

def flip_image(img, flip_y=False, flip_x=False):
    if flip_y:
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    elif flip_x:
        return img.transpose(Image.FLIP_LEFT_RIGHT)
    return img


if __name__ == '__main__':
    main()
