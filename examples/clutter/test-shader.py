# taken from https://github.com/cubicool/clutter-pygobject-examples

import sys
sys.path.insert(0, '../..')
import pgi
pgi.install_as_gi()

import math

from gi.repository import Clutter

FRAGMENT_SHADER_VARS = """
uniform sampler2D tex;
uniform float x_step, y_step;
"""

FRAGMENT_SHADER_BEGIN = """
void main() {
    vec4 color = texture2D(tex, vec2(cogl_tex_coord_in[0]));
"""

FRAGMENT_SHADER_END = """
    gl_FragColor = color;
    gl_FragColor = gl_FragColor * cogl_color_in;
}
"""

FRAGMENTS = FRAGMENT_SHADER_VARS, FRAGMENT_SHADER_BEGIN, FRAGMENT_SHADER_END

SHADERS = {
    # BRIGHTNESS-CONTRAST-1
    "brightness-contrast-1": """
    %s
    uniform float brightness, contrast;
    %s
    color.rgb /= color.a;
    color.rgb = 
        (color.rgb - vec3(0.5, 0.5, 0.5)) * contrast + 
        vec3(brightness + 0.5, brightness + 0.5, brightness + 0.5)
    ;
    color.rgb *= color.a;
    %s
    """ % FRAGMENTS,

    # BRIGHTNESS-CONTRAST-2
    "brightness-contrast-2": """
    %s
    uniform float brightness;
    uniform float contrast;
    %s
    color.rgb /= color.a;
    color.r = (color.r - 0.5) * contrast + brightness + 0.5;
    color.g = (color.g - 0.5) * contrast + brightness + 0.5;
    color.b = (color.b - 0.5) * contrast + brightness + 0.5;
    color.rgb *= color.a;
    %s
    """ % FRAGMENTS,

    # BOX-BLUR-DYNA
    "box-blur-dyna": """
    %s
    uniform float radius;
    %s
    float u, v;
    int count = 1;
    for(u=-radius;u<radius;u++) {
        for(v=-radius;v<radius;v++) {
            color += texture2D(tex, vec2(
                cogl_tex_coord_in[0].s + u * 2.0 * x_step, 
                cogl_tex_coord_in[0].t + v * 2.0 * y_step
            ));
            count ++;
        }
    }
    color = color / float(count);
    %s
    """ % FRAGMENTS,

    # BOX-BLUR
    "box-blur": """
    %s
    vec4 get_rgba_rel(sampler2D tex, float dx, float dy) {
        return texture2D(
            tex,
            cogl_tex_coord_in[0].st + vec2(dx, dy) * 2.0
        );
    }
    %s
    float count = 1.0;
    color += get_rgba_rel (tex, -x_step, -y_step); count++;
    color += get_rgba_rel (tex, -x_step,  0.0);    count++;
    color += get_rgba_rel (tex, -x_step,  y_step); count++;
    color += get_rgba_rel (tex,  0.0,    -y_step); count++;
    color += get_rgba_rel (tex,  0.0,     0.0);    count++;
    color += get_rgba_rel (tex,  0.0,     y_step); count++;
    color += get_rgba_rel (tex,  x_step, -y_step); count++;
    color += get_rgba_rel (tex,  x_step,  0.0);    count++;
    color += get_rgba_rel (tex,  x_step,  y_step); count++;
    color = color / count;
    %s
    """ % FRAGMENTS,

    # INVERT
    "invert": """
    %s
    %s
    color.rgb /= color.a;
    color.rgb = vec3(1.0, 1.0, 1.0) - color.rgb;
    color.rgb *= color.a;
    %s
    """ % FRAGMENTS,

    # GRAY
    "gray": """
    %s
    %s
    float avg = (color.r + color.g + color.b) / 3.0;
    color.r = avg;
    color.g = avg;
    color.b = avg;
    %s
    """ % FRAGMENTS,

    # COMBINED-MIRROR
    "combined-mirror": """
    %s
    %s
    vec4 colorB = texture2D (tex, vec2(cogl_tex_coord_in[0].ts));
    float avg = (color.r + color.g + color.b) / 3.0;
    color.r = avg;
    color.g = avg;
    color.b = avg;
    color = (color + colorB) / 2.0;
    %s
    """ % FRAGMENTS,

    # EDGE-DETECT
    "edge-detect": """
    %s
    float get_avg_rel(sampler2D texB, float dx, float dy)
    {
        vec4 colorB = texture2D (texB, cogl_tex_coord_in[0].st + vec2(dx, dy));
        return (colorB.r + colorB.g + colorB.b) / 3.0;
    }
    %s
    mat3 sobel_h = mat3( 1.0,  2.0,  1.0,
        0.0,  0.0,  0.0,
        -1.0, -2.0, -1.0);
    mat3 sobel_v = mat3( 1.0,  0.0, -1.0,
        2.0,  0.0, -2.0,
        1.0,  0.0, -1.0);
    mat3 map = mat3( get_avg_rel(tex, -x_step, -y_step),
        get_avg_rel(tex, -x_step, 0.0),
        get_avg_rel(tex, -x_step, y_step),
        get_avg_rel(tex, 0.0, -y_step),
        get_avg_rel(tex, 0.0, 0.0),
        get_avg_rel(tex, 0.0, y_step),
        get_avg_rel(tex, x_step, -y_step),
        get_avg_rel(tex, x_step, 0.0),
        get_avg_rel(tex, x_step, y_step) );
    mat3 gh = sobel_h * map;
    mat3 gv = map * sobel_v;
    float avgh = (gh[0][0] + gh[0][1] + gh[0][2] +
        gh[1][0] + gh[1][1] + gh[1][2] +
        gh[2][0] + gh[2][1] + gh[2][2]) / 18.0 + 0.5;
    float avgv = (gv[0][0] + gv[0][1] + gv[0][2] +
        gv[1][0] + gv[1][1] + gv[1][2] +
        gv[2][0] + gv[2][1] + gv[2][2]) / 18.0 + 0.5;
    float avg = (avgh + avgv) / 2.0;
    color.r = avg * color.r;
    color.g = avg * color.g;
    color.b = avg * color.b;
    %s
    """ % FRAGMENTS,

    # NO-OP
    "no-op": """
    %s
    %s
    %s
    """ % FRAGMENTS,

    # VERT-LINES
    "vert-lines": """
    %s
    %s
    if(mod(gl_FragCoord.y, 3.0) >= 1.0) color *= 0.5;
    %s
    """ % FRAGMENTS
}

SHADER_KEYS = list(SHADERS.keys())

def button_release_cb(actor, event, data):
    # If we've been run once, we'll figure out which one to use next.
    if hasattr(actor, "shader_name"):
        index = SHADER_KEYS.index(actor.shader_name)
        
        # Go back to the beginning.
        if index == len(SHADER_KEYS) - 1:
            actor.shader_name = next(iter(SHADERS))

        # Go to the next one.
        else:
            actor.shader_name = SHADER_KEYS[index + 1]

    # Otherwise, this must be the first time the callback has been run.
    # We'll start with the first iterative one.
    else:
        actor.shader_name = next(iter(SHADERS))

    print("Shader: %s" % actor.shader_name)

    # Shaders couldn't be easier to work with in Clutter. We'll start with our
    # basic brightness-contrast-1 example, and iterate from there when the user
    # clicks on the window.
    shader = Clutter.Shader()

    shader.set_fragment_source(SHADERS[actor.shader_name], -1)
    shader.compile()

    # We're going to "brute-force" the shaders here by setting every possible
    # parameter, rather than those only needed per each shader.
    actor.set_shader(shader)
    actor.set_shader_param_int("tex", 0)
    actor.set_shader_param_float("brightness", 0.4)
    actor.set_shader_param_float("contrast", -1.9)
    actor.set_shader_param_float("radius", 3.0)

    np2 = lambda n: 2 ** math.ceil(math.log(n, 2))

    actor.set_shader_param_float("x_step", 1.0 / np2(actor.get_width()))
    actor.set_shader_param_float("x_step", 1.0 / np2(actor.get_height()))

if __name__ == "__main__":
    stage = Clutter.Stage()

    stage.set_title("Shaders")
    stage.set_color(Clutter.Color.new(0x61, 0x64, 0x8c, 0xff))
    stage.set_size(512, 384)
    stage.connect("destroy", Clutter.main_quit)

    # Here we create a texture-based actor from the file on disk.
    # Our actor will toggle through shading on right/left click. Unlike the
    # normal example, we'll start with the basic redhand to let you see how
    # things change...

    actor = Clutter.Texture(filename="logo.png")

    actor.set_position(100, 100)
    actor.set_reactive(True)
    actor.connect("button-release-event", button_release_cb, None)

    stage.add_actor(actor)
    stage.show_all()

    Clutter.main()
