import os
import re
import subprocess
import uuid
import shutil
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai
from gen_audio import generate_audio_from_transcript
from moviepy.editor import VideoFileClip, AudioFileClip
from dotenv import load_dotenv
load_dotenv()

# ====== CONFIGURE GEMINI ====== # Replace with your valid key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro")
model2 = genai.GenerativeModel("gemini-1.5-flash")
global content
with open("docs.txt", "r", encoding="utf-8") as f:
    content = f.read()
# ====== FASTAPI APP SETUP ======
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust for your frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure videos folder exists & serve
os.makedirs("videos", exist_ok=True)
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# ====== HARD-CODED VIDEO MAP ======
HARDCODED_VIDEOS = {
    "pythagoras theorem": {
        "videoUrl": "http://localhost:8000/videos/pythagoras.mp4",
        "transcript": "This video demonstrates Pythagoras Theorem step by step with clear visuals and aligned elements.",
        "title": "Explaining Pythagoras Theorem"
    }
}

# ====== REQUEST SCHEMA ======
class PromptRequest(BaseModel):
    prompt: str

# ====== TOPIC-WISE PROMPT BANK ======


# ====== DEFAULT GEMINI PROMPT BUILDER ======
def build_gemini_prompt(topic: str) -> str:
    return f"""You are an EXPERT MANIM COMMUNITY ANIMATOR using ONLY Manim Community Edition v0.19.0 verified functions. 
Output must be ZERO-ERROR, perfectly centered, and layout-safe.  
Every element must remain within defined safe zones, aligned without overlap, and use RELATIVE positions (no hardcoded absolute coordinates).  
Return ONLY the python code— no explanations or CLI commands.
----------------------------------------------------------------------------------------------------------------------------------------------
  Topic which you are going to create manim script is {topic} and first collect correct explanation about the topic how it can be explained and think like a director what come first and 
  next what comes based on that write a screen play where you mention the scene by scene and which is fadeout and comes next to that place you are like perfect on points placement where 
  to place what go to creating the manim script based on that with no error occuring while rendering stick with manim community version 19 so infer their documentations in github 
  so you know what to use what to not use. The alignment should be improved. The rendered video should be next level like revolution the tech world no one ever created and for alignment use sleep and wait so no elements 
  overlap and get a correct measurements to built it. And make sure to fit all the things into layout and perfect alignment and placement of element should be neet and perfect 100%.
  ensure that the used keywords and functions should be from the mentioned one that here other than that should not be used
  here is the functions and key words : [['AS2700', 'Add', 'AddTextLetterByLetter', 'AddTextWordByWord', 'Angle', 'AnimatedBoundary', 'Animation', 'AnimationGroup', 'AnnotationDot', 'AnnularSector', 'Annulus', 'ApplyComplexFunction', 'ApplyFunction', 'ApplyMatrix', 'ApplyMethod', 'ApplyPointwiseFunction', 'ApplyPointwiseFunctionToCenter', 'ApplyWave', 'Arc', 'ArcBetweenPoints', 'ArcBrace', 'ArcPolygon', 'ArcPolygonFromArcs', 'Arrow', 'Arrow3D', 'ArrowCircleFilledTip', 'ArrowCircleTip', 'ArrowSquareFilledTip', 'ArrowSquareTip', 'ArrowTip', 'ArrowTriangleFilledTip', 'ArrowTriangleTip', 'ArrowVectorField', 'Axes', 'BLACK', 'BLUE', 'BLUE_A', 'BLUE_B', 'BLUE_C', 'BLUE_D', 'BLUE_E', 'BOLD', 'BOOK', 'BS381', 'BackgroundColoredVMobjectDisplayer', 'BackgroundRectangle', 'BarChart', 'Blink', 'Brace', 'BraceBetweenPoints', 'BraceLabel', 'Broadcast', 'BulletedList', 'CHOOSE_NUMBER_MESSAGE', 'CONTEXT_SETTINGS', 'CTRL_VALUE', 'CairoRenderer', 'Camera', 'CapStyleType', 'ChangeDecimalToValue', 'ChangeSpeed', 'ChangingDecimal', 'Circle', 'Circumscribe', 'ClockwiseTransform', 'Code', 'ComplexHomotopy', 'ComplexPlane', 'ComplexValueTracker', 'Cone', 'ConvexHull', 'ConvexHull3D', 'CoordinateSystem', 'CounterclockwiseTransform', 'Create', 'Cross', 'Cube', 'CubicBezier', 'CurvedArrow', 'CurvedDoubleArrow', 'CurvesAsSubmobjects', 'Cutout', 'CyclicReplace', 'Cylinder', 'DARKER_GRAY', 'DARKER_GREY', 'DARK_BLUE', 'DARK_BROWN', 'DARK_GRAY', 'DARK_GREY', 'DEFAULT_ARROW_TIP_LENGTH', 'DEFAULT_DASH_LENGTH', 'DEFAULT_DOT_RADIUS', 'DEFAULT_FONT_SIZE', 'DEFAULT_MOBJECT_TO_EDGE_BUFFER', 'DEFAULT_MOBJECT_TO_MOBJECT_BUFFER', 'DEFAULT_POINTWISE_FUNCTION_RUN_TIME', 'DEFAULT_POINT_DENSITY_1D', 'DEFAULT_POINT_DENSITY_2D', 'DEFAULT_QUALITY', 'DEFAULT_SMALL_DOT_RADIUS', 'DEFAULT_STROKE_WIDTH', 'DEFAULT_WAIT_TIME', 'DEGREES', 'DL', 'DOWN', 'DR', 'DVIPSNAMES', 'DashedLine', 'DashedVMobject', 'DecimalMatrix', 'DecimalNumber', 'DecimalTable', 'DefaultSectionType', 'DiGraph', 'DictAsObject', 'Difference', 'Dodecahedron', 'Dot', 'Dot3D', 'DotCloud', 'DoubleArrow', 'DrawBorderThenFill', 'EPILOG', 'Elbow', 'Ellipse', 'Exclusion', 'FadeIn', 'FadeOut', 'FadeToColor', 'FadeTransform', 'FadeTransformPieces', 'Flash', 'FocusOn', 'FullScreenRectangle', 'FunctionGraph', 'GOLD', 'GOLD_A', 'GOLD_B', 'GOLD_C', 'GOLD_D', 'GOLD_E', 'GRAY', 'GRAY_A', 'GRAY_B', 'GRAY_BROWN', 'GRAY_C', 'GRAY_D', 'GRAY_E', 'GREEN', 'GREEN_A', 'GREEN_B', 'GREEN_C', 'GREEN_D', 'GREEN_E', 'GREY', 'GREY_A', 'GREY_B', 'GREY_BROWN', 'GREY_C', 'GREY_D', 'GREY_E', 'Graph', 'Group', 'GrowArrow', 'GrowFromCenter', 'GrowFromEdge', 'GrowFromPoint', 'HEAVY', 'HSV', 'Homotopy', 'IN', 'INVALID_NUMBER_MESSAGE', 'ITALIC', 'Icosahedron', 'ImageMobject', 'ImageMobjectFromCamera', 'ImplicitFunction', 'Indicate', 'Integer', 'IntegerMatrix', 'IntegerTable', 'Intersection', 'LARGE_BUFF', 'LEFT', 'LIGHT', 'LIGHTER_GRAY', 'LIGHTER_GREY', 'LIGHT_BROWN', 'LIGHT_GRAY', 'LIGHT_GREY', 'LIGHT_PINK', 'LOGO_BLACK', 'LOGO_BLUE', 'LOGO_GREEN', 'LOGO_RED', 'LOGO_WHITE', 'Label', 'LabeledArrow', 'LabeledDot', 'LabeledLine', 'LabeledPolygram', 'LaggedStart', 'LaggedStartMap', 'Line', 'Line3D', 'LineJointType', 'LinearBase', 'LinearTransformationScene', 'LogBase', 'MAROON', 'MAROON_A', 'MAROON_B', 'MAROON_C', 'MAROON_D', 'MAROON_E', 'MEDIUM', 'MED_LARGE_BUFF', 'MED_SMALL_BUFF', 'MaintainPositionRelativeTo', 'ManimBanner', 'ManimColor', 'ManimColorDType', 'ManimMagic', 'MappingCamera', 'MarkupText', 'MathTable', 'MathTex', 'Matrix', 'Mobject', 'Mobject1D', 'Mobject2D', 'MobjectMatrix', 'MobjectTable', 'MoveAlongPath', 'MoveToTarget', 'MovingCamera', 'MovingCameraScene', 'MultiCamera', 'NORMAL', 'NO_SCENE_MESSAGE', 'NumberLine', 'NumberPlane', 'OBLIQUE', 'ORANGE', 'ORIGIN', 'OUT', 'Octahedron', 'OldMultiCamera', 'OpenGLPGroup', 'OpenGLPMPoint', 'OpenGLPMobject', 'PGroup', 'PI', 'PINK', 'PMobject', 'PURE_BLUE', 'PURE_GREEN', 'PURE_RED', 'PURPLE', 'PURPLE_A', 'PURPLE_B', 'PURPLE_C', 'PURPLE_D', 'PURPLE_E', 'Paragraph', 'ParametricFunction', 'ParsableManimColor', 'PhaseFlow', 'Point', 'PointCloudDot', 'PolarPlane', 'Polygon', 'Polygram', 'Polyhedron', 'Prism', 'QUALITIES', 'R3_to_complex', 'RED', 'RED_A', 'RED_B', 'RED_C', 'RED_D', 'RED_E', 'RESAMPLING_ALGORITHMS', 'RGBA', 'RIGHT', 'Rectangle', 'RegularPolygon', 'RegularPolygram', 'RemoveTextLetterByLetter', 'RendererType', 'ReplacementTransform', 'Restore', 'RightAngle', 'Rotate', 'Rotating', 'RoundedRectangle', 'SCALE_FACTOR_PER_FONT_POINT', 'SCENE_NOT_FOUND_MESSAGE', 'SEMIBOLD', 'SEMILIGHT', 'SHIFT_VALUE', 'SMALL_BUFF', 'START_X', 'START_Y', 'SVGMobject', 'SVGNAMES', 'SampleSpace', 'ScaleInPlace', 'Scene', 'SceneFileWriter', 'ScreenRectangle', 'Section', 'Sector', 'ShowIncreasingSubsets', 'ShowPartial', 'ShowPassingFlash', 'ShowPassingFlashWithThinningStrokeWidth', 'ShowSubmobjectsOneByOne', 'ShrinkToCenter', 'SingleStringMathTex', 'SmoothedVectorizedHomotopy', 'SpecialThreeDScene', 'Sphere', 'SpinInFromNothing', 'SpiralIn', 'SplitScreenCamera', 'Square', 'Star', 'StealthTip', 'StreamLines', 'Succession', 'Surface', 'SurroundingRectangle', 'Swap', 'TAU', 'TEAL', 'TEAL_A', 'TEAL_B', 'TEAL_C', 'TEAL_D', 'TEAL_E', 'THIN', 'Table', 'TangentLine', 'Tetrahedron', 'Tex', 'TexFontTemplates', 'TexTemplate', 'TexTemplateLibrary', 'Text', 'ThreeDAxes', 'ThreeDCamera', 'ThreeDScene', 'ThreeDVMobject', 'TipableVMobject', 'Title', 'Torus', 'TracedPath', 'Transform', 'TransformAnimations', 'TransformFromCopy', 'TransformMatchingShapes', 'TransformMatchingTex', 'Triangle', 'TrueDot', 'TypeWithCursor', 'UL', 'ULTRABOLD', 'ULTRAHEAVY', 'ULTRALIGHT', 'UP', 'UR', 'Uncreate', 'Underline', 'Union', 'UnitInterval', 'UntypeWithCursor', 'Unwrite', 'UpdateFromAlphaFunc', 'UpdateFromFunc', 'VDict', 'VGroup', 'VMobject', 'VMobjectFromSVGPath', 'ValueTracker', 'Variable', 'Vector', 'VectorField', 'VectorScene', 'VectorizedPoint', 'WHITE', 'Wait', 'Wiggle', 'Write', 'X11', 'XKCD', 'X_AXIS', 'YELLOW', 'YELLOW_A', 'YELLOW_B', 'YELLOW_C', 'YELLOW_D', 'YELLOW_E', 'Y_AXIS', 'Z_AXIS', 'ZoomedScene', 'builtins', 'cached', 'doc', 'file', 'loader', 'main', 'name', 'package', 'path', 'spec', 'version', '_config', 'add_extension_if_not_present', 'adjacent_n_tuples', 'adjacent_pairs', 'all_elements_are_instances', 'always', 'always_redraw', 'always_rotate', 'always_shift', 'angle_axis_from_quaternion', 'angle_between_vectors', 'angle_of_vector', 'animation', 'annotations', 'assert_is_mobject_method', 'average_color', 'bezier', 'bezier_remap', 'binary_search', 'camera', 'capture', 'cartesian_to_spherical', 'center_of_mass', 'change_to_rgba_array', 'choose', 'cli', 'cli_ctx_settings', 'clip', 'clockwise_path', 'color', 'color_gradient', 'color_to_int_rgb', 'color_to_int_rgba', 'color_to_rgb', 'color_to_rgba', 'compass_directions', 'complex_func_to_R3_func', 'complex_to_R3', 'concatenate_lists', 'config', 'console', 'constants', 'core', 'counterclockwise_path', 'cross2d', 'cycle_animation', 'double_smooth', 'drag_pixels', 'earclip_triangulation', 'ensure_executable', 'error_console', 'exponential_decay', 'f_always', 'find_intersection', 'frame', 'get_3d_vmob_end_corner', 'get_3d_vmob_end_corner_index', 'get_3d_vmob_end_corner_unit_normal', 'get_3d_vmob_gradient_start_and_end_points', 'get_3d_vmob_start_corner', 'get_3d_vmob_start_corner_index', 'get_3d_vmob_start_corner_unit_normal', 'get_3d_vmob_unit_normal', 'get_det_text', 'get_dir_layout', 'get_full_raster_image_path', 'get_full_sound_file_path', 'get_ipython', 'get_plugins', 'get_shaded_rgb', 'get_smooth_cubic_bezier_handle_points', 'get_unit_normal', 'get_video_metadata', 'get_winding_number', 'guarantee_empty_existence', 'guarantee_existence', 'gui', 'hex_to_rgb', 'index_labels', 'integer_interpolate', 'interpolate', 'interpolate_color', 'inverse_interpolate', 'invert_color', 'invert_image', 'ipy', 'is_closed', 'is_gif_format', 'is_mov_format', 'is_mp4_format', 'is_png_format', 'is_webm_format', 'line_intersection', 'linear', 'lingering', 'list_difference_update', 'list_plugins', 'list_update', 'listify', 'logger', 'make_even', 'make_even_by_cycling', 'manim_colors', 'match_interpolate', 'matrix_to_mobject', 'matrix_to_tex_string', 'merge_dicts_recursively', 'mid', 'midpoint', 'mobject', 'modify_atime', 'normalize', 'not_quite_there', 'np', 'open_file', 'opengl', 'override_animate', 'override_animation', 'partial_bezier_points', 'path_along_arc', 'perpendicular_bisector', 'plugins', 'point_lies_on_bezier', 'print_family', 'proportions_along_bezier_curve_for_point', 'quaternion_conjugate', 'quaternion_from_angle_axis', 'quaternion_mult', 'random_bright_color', 'random_color', 'rate_functions', 'register_font', 'regular_vertices', 'remove_list_redundancies', 'remove_nones', 'renderer', 'rgb_to_color', 'rgb_to_hex', 'rgba_to_color', 'rotate_vector', 'rotation_about_z', 'rotation_matrix', 'running_start', 'rush_from', 'rush_into', 'scene', 'seek_full_path_from_defaults', 'shoelace', 'shoelace_direction', 'sigmoid', 'slow_into', 'smooth', 'smoothererstep', 'smootherstep', 'smoothstep', 'spherical_to_cartesian', 'split_bezier', 'squish_rate_func', 'straight_path', 'stretch_array_to_length', 'subdivide_bezier', 'tempconfig', 'there_and_back', 'there_and_back_with_pause', 'thick_diagonal', 'tuplify', 'turn_animation_into_updater', 'typing', 'unit', 'update_dict_recursively', 'utils', 'version', 'wiggle', 'write_to_movie', 'z_to_vector']]
  Also fix the alignment issue if you can and no overlap should be there.
  Refer this documentation for refering the latest version:{content}

  Now focus on equations and its explanation via text now you not need to use shapes stick with equation and explanation so use intractive transformation and focus on center alignment since it comes one by one so use sleep and wait fade out the elements if the current element place occupied by the others be careful on alignment and layout problem
  ---------------------------------------------------------------------------------------------------------------------------------------------------------------

-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------  
## ABSOLUTE FORBIDDEN:
- ManimGL imports/syntax
- Deprecated methods: get_graph(), get_graph_label(), get_slope_field(), get_corner() without direction, or any pre-v0.19.0 plotting API
- Custom VMobject classes (unless defined inline & necessary)
- Mixing VMobject & Mobject in VGroup
- List arithmetic on coordinates
- Elements beyond safe bounds (MAX_X=5.5, MAX_Y=2.8)
- Overlapping text/shapes
- Browser/OpenGL renderers

## AUTO API UPGRADE RULES (MANDATORY):
- Replace get_graph(...) → plot(...)
- Replace get_graph_label(...) → use MathTex/Text positioned via axes.coords_to_point()
- All function plotting must use:
  axes.plot(lambda x: ..., x_range=[min, max], color=COLOR)
- All labels must be created separately (Text or MathTex) and positioned with next_to(), move_to(), or coords_to_point()

## ALLOWED IMPORTS:
from manim import *
import numpy as np  

## SAFE BUILT-IN SHAPES:
Circle(), Square(), Rectangle(), Triangle(), Line(), Arrow(), Dot(), Polygon([...])

## COORDINATE & POSITIONING RULES:
- Use np.array() for all calculations
- Safe zone: X in [-5.5, 5.5], Y in [-2.8, 2.8]
- Position with: .move_to(), .to_edge(), .next_to(), .shift()
- Always maintain MIN_SPACING=0.5 between objects
- Grid layout or relative positions only

## TEXT & MATH:
- Text("...", font_size=..., color=...)
- MathTex("...") — simple LaTeX only, no special packages
- Built-in colors only: RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK, WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY

## SAFE ANIMATIONS:
Create(), Write(), FadeIn(), FadeOut(), Transform(), Shift(), Wiggle()

## FINAL REQUIREMENTS:
- No overlaps
- No off-screen elements
- Only verified v0.19.0 syntax
- Relative positioning tied to {topic} context
- Output transcript and Python code only
"""

def refinement(code: str) -> str:
    return f"""
# ULTIMATE MANIM COMMUNITY ALIGNMENT SPECIALIST
## ACHIEVE 10000% PERFECT POSITIONING - ZERO TOLERANCE FOR ALIGNMENT ERRORS

You are the *SUPREME MANIM ALIGNMENT AUTHORITY* - the final word on perfect positioning. Your singular obsession is creating flawless visual layouts that work on EVERY screen, EVERY time, with ZERO overlaps, ZERO cutoffs, and ZERO spacing inconsistencies.
for this below code
     ------------>{code}
---

## 🎯 MISSION: ABSOLUTE POSITIONING PERFECTION

*ZERO TOLERANCE POLICY:*
- ❌ NO overlapping elements (not even 1 pixel)
- ❌ NO screen boundary violations  
- ❌ NO inconsistent spacing
- ❌ NO hardcoded coordinates
- ❌ NO missing buffers
- ❌ NO readability issues

*PERFECTION STANDARD:*
- ✅ Every element perfectly visible
- ✅ Every spacing mathematically consistent  
- ✅ Every label clearly readable
- ✅ Every animation maintains alignment
- ✅ Every scene transition preserves positioning

---

## 📐 SACRED POSITIONING CONSTANTS - MEMORIZE THESE

python
# ABSOLUTE SCREEN BOUNDARIES - NEVER EXCEED
SCREEN_SAFE_WIDTH = 13.0     # Maximum safe width
SCREEN_SAFE_HEIGHT = 7.0     # Maximum safe height  
SAFE_LEFT_EDGE = LEFT * 6.2   # Leftmost safe position
SAFE_RIGHT_EDGE = RIGHT * 6.2 # Rightmost safe position
SAFE_TOP_EDGE = UP * 3.2     # Topmost safe position
SAFE_BOTTOM_EDGE = DOWN * 3.2 # Bottommost safe position

# SACRED BUFFER DISTANCES - USE THESE EXACTLY
MICRO_BUFFER = 0.15    # Tightest possible spacing
TIGHT_BUFFER = 0.25    # Close related elements
NORMAL_BUFFER = 0.4    # Standard element separation  
LOOSE_BUFFER = 0.6     # Between different sections
SECTION_BUFFER = 0.9   # Major scene components
MEGA_BUFFER = 1.2      # Maximum separation

# POSITIONING ZONES - ASSIGN ELEMENTS TO THESE
TITLE_ZONE = UP * 2.8        # Reserved for main titles
SUBTITLE_ZONE = UP * 2.2     # Reserved for subtitles  
UPPER_CONTENT = UP * 1.4     # Upper content area
CENTER_CONTENT = ORIGIN      # Main content center
LOWER_CONTENT = DOWN * 1.4   # Lower content area
FOOTER_ZONE = DOWN * 2.8     # Bottom information


---

## 🔧 FOOLPROOF FIXING METHODOLOGY

### STEP 1: BOUNDARY VIOLATION SCAN
*Check EVERY element against these limits:*

python
# TITLE POSITIONING - ALWAYS SAFE
title.to_edge(UP, buff=0.6)  # Never use buff < 0.5

# EQUATION POSITIONING - STACK VERTICALLY
eq1.move_to(TITLE_ZONE)
eq2.move_to(SUBTITLE_ZONE) 
eq3.move_to(UPPER_CONTENT)

# AXES POSITIONING - CENTERED AND SAFE
axes = Axes(
    x_range=[-5, 5, 1],     # NEVER exceed [-6, 6]
    y_range=[-3, 3, 1],     # NEVER exceed [-4, 4]
    x_length=9,             # NEVER exceed 10
    y_length=5.5,           # NEVER exceed 6
).move_to(ORIGIN)

# SIDE LABELS - SAFE EDGE POSITIONING
left_label.to_edge(LEFT, buff=1.0)    # NEVER buff < 0.8
right_label.to_edge(RIGHT, buff=1.0)  # NEVER buff < 0.8


### STEP 2: OVERLAP ELIMINATION PROTOCOL

*VERTICAL STACKING - ZERO OVERLAPS:*
python
# PERFECT VERTICAL SEQUENCE
element_1.to_edge(UP, buff=0.6)
element_2.next_to(element_1, DOWN, buff=NORMAL_BUFFER)
element_3.next_to(element_2, DOWN, buff=NORMAL_BUFFER)
element_4.next_to(element_3, DOWN, buff=NORMAL_BUFFER)

# HORIZONTAL DISTRIBUTION - PERFECT SPACING  
left_item.to_edge(LEFT, buff=1.0)
center_item.move_to(ORIGIN)
right_item.to_edge(RIGHT, buff=1.0)

# DIAGONAL LABEL POSITIONING - NO OVERLAPS
label.next_to(object, UP + RIGHT, buff=TIGHT_BUFFER)


### STEP 3: MATHEMATICAL CONTENT ALIGNMENT

*EQUATION SYSTEMS - PIXEL PERFECT:*
python
# SYSTEM TITLE
system_title = Text("System of Equations", font_size=36)
system_title.to_edge(UP, buff=0.5)

# EQUATION ALIGNMENT - LEFT JUSTIFIED
eq1 = MathTex("2x + 3y = 7", font_size=32)
eq1.next_to(system_title, DOWN, buff=0.8)
eq1.to_edge(LEFT, buff=2.5)

eq2 = MathTex("x - y = 1", font_size=32)
eq2.next_to(eq1, DOWN, buff=0.4)
eq2.align_to(eq1, LEFT)  # CRITICAL: Align left edges

eq3 = MathTex("3x + 2y = 9", font_size=32)  
eq3.next_to(eq2, DOWN, buff=0.4)
eq3.align_to(eq1, LEFT)  # CRITICAL: Align left edges

# SOLUTION SECTION - PROPER SEPARATION
solution_title = Text("Solution:", font_size=32)
solution_title.next_to(eq3, DOWN, buff=SECTION_BUFFER)
solution_title.align_to(eq1, LEFT)


### STEP 4: COORDINATE SYSTEM PERFECTION

*AXES WITH PERFECT LABELS:*
python
# MAIN AXES - CENTERED AND SAFE
axes = Axes(
    x_range=[-4, 4, 1], 
    y_range=[-3, 3, 1],
    x_length=8,
    y_length=5.5,
    axis_config=["color": BLUE, "include_numbers": True]
).move_to(ORIGIN)

# AXIS LABELS - PERFECT POSITIONING
x_label = axes.get_x_axis_label("x", edge=RIGHT, direction=DOWN, buff=0.2)
y_label = axes.get_y_axis_label("y", edge=UP, direction=LEFT, buff=0.2)

# FUNCTION LABELS - CLEAR AND READABLE
func_label = MathTex("f(x) = x^2", font_size=28)
func_label.next_to(axes, UP + LEFT, buff=0.3)
func_label.shift(RIGHT * 0.5)  # Fine adjustment


---

## 🚨 CRITICAL ERROR PATTERNS TO ELIMINATE

### PATTERN 1: Hardcoded Death Coordinates
python
# ❌ WRONG - WILL CAUSE OVERLAPS
text.move_to([3.2, 2.7, 0])
equation.shift(UP * 4.5)
label.set_coord([−7, 1, 0])

# ✅ CORRECT - RESPONSIVE POSITIONING  
text.to_edge(RIGHT, buff=1.0).shift(UP * 1.5)
equation.to_edge(UP, buff=0.6)
label.to_edge(LEFT, buff=1.0).shift(UP * 0.5)


### PATTERN 2: Missing Buffer Disasters  
python
# ❌ WRONG - GUARANTEED OVERLAPS
title.next_to(subtitle)
label.next_to(point)  
eq1.next_to(eq2, DOWN)

# ✅ CORRECT - PROPER BUFFERS
title.next_to(subtitle, UP, buff=NORMAL_BUFFER)
label.next_to(point, UP, buff=TIGHT_BUFFER)
eq1.next_to(eq2, DOWN, buff=NORMAL_BUFFER)


### PATTERN 3: Screen Violation Catastrophes
python  
# ❌ WRONG - GOES OFF SCREEN
massive_title.scale(3).move_to(UP * 4)
wide_equation.scale(2).move_to(RIGHT * 8)
tall_content.move_to(DOWN * 5)

# ✅ CORRECT - SCREEN SAFE
massive_title.scale(1.5).to_edge(UP, buff=0.6)  
wide_equation.scale(0.8).move_to(ORIGIN)
tall_content.to_edge(DOWN, buff=0.6)


---

## 📋 SYSTEMATIC FIXING CHECKLIST

*Before you return ANY code, verify EVERY item:*

### ✅ BOUNDARY CHECK
- [ ] No element extends beyond SAFE_LEFT_EDGE (-6.2)
- [ ] No element extends beyond SAFE_RIGHT_EDGE (+6.2)  
- [ ] No element extends beyond SAFE_TOP_EDGE (+3.2)
- [ ] No element extends beyond SAFE_BOTTOM_EDGE (-3.2)
- [ ] All text fits within screen bounds
- [ ] All mathematical expressions are fully visible

### ✅ OVERLAP CHECK  
- [ ] No two text elements overlap
- [ ] No labels cover important visual elements
- [ ] No equations overlap with axes or grids
- [ ] All elements have minimum TIGHT_BUFFER spacing
- [ ] Diagonal positioning used where needed

### ✅ SPACING CONSISTENCY
- [ ] All similar elements use identical buffer values
- [ ] Vertical stacking uses consistent DOWN spacing
- [ ] Horizontal alignment uses consistent positioning
- [ ] Section separations use SECTION_BUFFER or larger

### ✅ POSITIONING ACCURACY
- [ ] All .to_edge() calls include buff parameter
- [ ] All .next_to() calls include direction and buff
- [ ] No hardcoded coordinates [x, y, z] used
- [ ] All relative positioning uses proper references

### ✅ READABILITY VERIFICATION
- [ ] All text is clearly separated from backgrounds  
- [ ] All mathematical expressions are unobstructed
- [ ] All labels point clearly to their targets
- [ ] Font sizes are appropriate for screen space

---

## 💯 PERFECTION VERIFICATION PROTOCOL

*FINAL QUALITY CHECK - MUST PASS ALL:*

1. *VISUAL SCAN TEST:* Mentally render each scene - can you see every element clearly?

2. *OVERLAP DETECTION:* Check every pair of elements - do any boundaries intersect?

3. *BOUNDARY VERIFICATION:* Confirm every element fits within safe screen zones

4. *SPACING MEASUREMENT:* Verify all buffers meet minimum requirements

5. *ANIMATION CONSISTENCY:* Ensure positioning maintained through all transformations

---

## 🎯 OUTPUT REQUIREMENTS

*DELIVER:*
1. *COMPLETE corrected Manim script* - no truncation
2. *ZERO positioning errors* - perfect alignment
3. *CONSISTENT formatting* - readable code structure  
4. *PRESERVED functionality* - all original animations intact
5. *OPTIMIZED performance* - efficient positioning code

*RESPONSE FORMAT:*

ALIGNMENT ANALYSIS COMPLETE ✅
CORRECTIONS IMPLEMENTED: [X] positioning fixes
ZERO OVERLAPS GUARANTEED ✅
SCREEN BOUNDARIES RESPECTED ✅
SPACING PERFECTED ✅

[COMPLETE CORRECTED CODE HERE]


---

## 🔥 EXTREME QUALITY ENFORCEMENT

*IF YOU FIND ANY:*
- Overlapping elements → IMMEDIATE CORRECTION REQUIRED
- Screen violations → EMERGENCY REPOSITIONING NEEDED  
- Missing buffers → CRITICAL ERROR - ADD BUFFERS NOW
- Hardcoded coordinates → REPLACE WITH RELATIVE POSITIONING
- Inconsistent spacing → STANDARDIZE ALL BUFFERS

*REMEMBER:* You are the FINAL authority on Manim positioning. Every pixel matters. Every spacing decision is critical. Accept NOTHING less than absolute perfection.

*YOUR REPUTATION depends on delivering FLAWLESS alignment that works perfectly regardless of screen size, resolution, or viewing conditions.*

---

## 🏆 SUCCESS METRICS

*PERFECT SCORE requires:*
- 🎯 100% elements within screen boundaries
- 🎯 100% overlap-free positioning  
- 🎯 100% consistent buffer usage
- 🎯 100% readable text placement
- 🎯 100% maintained functionality

*Anything less than perfect is UNACCEPTABLE.*

Now analyze the provided Manim script and deliver ABSOLUTE POSITIONING PERFECTION!

I need only the code no other unnecessay stuffs needed like explanation or any commands[strictly].
--- CODE END ---
"""

import re

def combine_video_audio(video_path, audio_path, output_video="final_explanation.mp4"):
    """
    Combines a generated video with an audio explanation.
    """
    print(f"📂 Checking paths:\nVideo: {video_path}\nAudio: {audio_path}")
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"⚠️ Video file not found: {video_path}")

    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"⚠️ Audio file not found: {audio_path}")

    video = VideoFileClip(video_path)
    audio = AudioFileClip(audio_path)

    # Ensure audio length matches video length
    audio = audio.subclip(0, min(video.duration, audio.duration))

    final_video = video.set_audio(audio)
    final_video.write_videofile(output_video, codec="libx264")

    if os.path.exists(output_video):
        print(f"✅ Final video generated successfully: {output_video}")
    else:
        print("⚠️ Error: Final video was not created!")

    return output_video


def extract_clean_manim_code(content: str) -> str:
    """
    Extracts and cleans Manim code from mixed LLM output.
    Returns clean Manim code as a string.
    """
    # Extract code block fenced by triple backticks (with optional python)
    code_match = re.search(r"```(?:python)?\s*([\s\S]*?)```", content)
    if code_match:
        manim_code = code_match.group(1).strip()
    else:
        # No fenced code found — guess by looking for relevant lines
        code_lines = []
        for line in content.splitlines():
            if (
                line.strip().startswith("from manim import")
                or line.strip().startswith("import ")
                or line.strip().startswith("class ")
                or line.strip().startswith("    def ")
            ):
                code_lines.append(line)
        manim_code = "\n".join(code_lines).strip()

    # Sanitize code
    manim_code = manim_code.replace(r"\c", r"\\c")
    manim_code = re.sub(r"class\s+\w+\s*\(", "class GeneratedScene(", manim_code)
    
    # Ensure proper Scene inheritance if missing
    if "class GeneratedScene" in manim_code and "Scene" not in manim_code.split("class GeneratedScene")[1]:
        manim_code = manim_code.replace("class GeneratedScene(", "class GeneratedScene(Scene):")

    # Provide fallback minimal scene if no code extracted
    if not manim_code.strip():
        manim_code = (
            "from manim import *\n\n"
            "class GeneratedScene(Scene):\n"
            "    def construct(self):\n"
            "        self.add(Text('Error: Scene could not be generated'))\n"
        )
    return manim_code.strip()


def extract_transcript(content: str) -> str:
    """
    Extracts and cleans transcript text by removing Manim code blocks
    and related code lines from the content.
    Returns the cleaned transcript as a string.
    """
    # Remove fenced code blocks
    transcript = re.sub(r"```(?:python)?[\s\S]*?```", "", content)
    # Remove import lines
    transcript = re.sub(r"from\s+manim\s+import\s+\*.*", "", transcript)
    transcript = re.sub(r"import\s+\w+.*", "", transcript)
    # Remove class definitions and function definitions lines
    transcript = re.sub(r"^\s*class\s+\w+\s*\(.*\):.*", "", transcript, flags=re.MULTILINE)
    transcript = re.sub(r"^\s*def\s+\w+\(.*\):.*", "", transcript, flags=re.MULTILINE)
    # Normalize multiple blank lines to two
    transcript = re.sub(r"\n\s*\n+", "\n\n", transcript).strip()
    return transcript

def gen_trans(manim: str) -> str:
    return f"""
  You are supreme voice over creator.
  create a transcript (voice over) 
  that align wwith this code {manim} so i can integrate the audio to the video that created by the video. 
  No use of special character strictly and give only the backgroud dialogue use only characters(words) that going to 
  integrated with the video. and should be sync perfectly. No special characte perfectly should match with code and 
  explanation should be look like how a teacher would have handled that explanation. It should match with the video syn perfectly.

  output format: need only the dialogu no other stuffs needed any commands or explanation of what you did for user and no need to mention the timing only need the dialogues.

    """


# ====== HYBRID VIDEO GENERATION ENDPOINT WITH AUTO-FIX ======
@app.post("/generate-video")
def generate_video(request: PromptRequest):
    prompt = request.prompt.strip().lower()
    print(f"Prompt received: {prompt}")

    # 1. Hardcoded videos
    if prompt in HARDCODED_VIDEOS:
        print(f"Serving hardcoded video for: {prompt}")
        return HARDCODED_VIDEOS[prompt]

    # 2. Build Gemini prompt
    k = build_gemini_prompt(prompt)

    # 3. Get content from Gemini
    response = model.generate_content(k)
    print(response)

    # transcript = extract_transcript(response.text)
    # print(transcript)

    # 4. Split code and transcript
    parts = response.text.split("---EXPLANATION_STARTS_HERE---")
    manim_code = extract_clean_manim_code(parts[0].strip())
    trans = gen_trans(manim_code)
    transcript = model.generate_content(trans).text
    print(transcript)
    


    
    #refine_pr = refinement(manim_code)
    #response_refined =  model.generate_content(refine_pr)
    #print(response_refined)
    # parts_ref = response_refined.text
    # manim_code_2 = clean_manim_code(parts_ref[0].strip())
    # Retry loop for rendering + fixing

    MAX_RETRIES = 3
    for attempt in range(MAX_RETRIES):
        print(f"--- Rendering attempt {attempt+1} ---")

        # Save Manim script
        script_filename = f"video_{uuid.uuid4().hex}.py"
        with open(script_filename, "w", encoding="utf-8") as f:
            f.write(manim_code)

        print(f"Saved Manim code to {script_filename}")

        try:
            # Try rendering
            subprocess.run(
                ["manim", "-ql", script_filename, "GeneratedScene"],
                check=True,
                capture_output=True,
                text=True
            )
            print("Rendering successful ✅")
            break

        except subprocess.CalledProcessError as e:
            error_message = e.stderr or e.stdout or str(e)
            print(f"❌ Rendering failed:\n{error_message}")

            # Delete broken script before retry
            os.remove(script_filename)

            if attempt < MAX_RETRIES - 1:
                # Ask Gemini to fix the code
                fix_prompt = (
                    "The following Manim code caused a rendering error.\n"
                    "Fix it so it works in Manim Community Edition(v.19) without syntax or runtime errors.\n"
                    "Return ONLY the corrected code.\n\n"
                    "ensure that the used keywords and functions should be from the mentioned one that here other than that should not be used" 
                    "here is the functions and key words ; [['AS2700', 'Add', 'AddTextLetterByLetter', 'AddTextWordByWord', 'Angle', 'AnimatedBoundary', 'Animation', 'AnimationGroup', 'AnnotationDot', 'AnnularSector', 'Annulus', 'ApplyComplexFunction', 'ApplyFunction', 'ApplyMatrix', 'ApplyMethod', 'ApplyPointwiseFunction', 'ApplyPointwiseFunctionToCenter', 'ApplyWave', 'Arc', 'ArcBetweenPoints', 'ArcBrace', 'ArcPolygon', 'ArcPolygonFromArcs', 'Arrow', 'Arrow3D', 'ArrowCircleFilledTip', 'ArrowCircleTip', 'ArrowSquareFilledTip', 'ArrowSquareTip', 'ArrowTip', 'ArrowTriangleFilledTip', 'ArrowTriangleTip', 'ArrowVectorField', 'Axes', 'BLACK', 'BLUE', 'BLUE_A', 'BLUE_B', 'BLUE_C', 'BLUE_D', 'BLUE_E', 'BOLD', 'BOOK', 'BS381', 'BackgroundColoredVMobjectDisplayer', 'BackgroundRectangle', 'BarChart', 'Blink', 'Brace', 'BraceBetweenPoints', 'BraceLabel', 'Broadcast', 'BulletedList', 'CHOOSE_NUMBER_MESSAGE', 'CONTEXT_SETTINGS', 'CTRL_VALUE', 'CairoRenderer', 'Camera', 'CapStyleType', 'ChangeDecimalToValue', 'ChangeSpeed', 'ChangingDecimal', 'Circle', 'Circumscribe', 'ClockwiseTransform', 'Code', 'ComplexHomotopy', 'ComplexPlane', 'ComplexValueTracker', 'Cone', 'ConvexHull', 'ConvexHull3D', 'CoordinateSystem', 'CounterclockwiseTransform', 'Create', 'Cross', 'Cube', 'CubicBezier', 'CurvedArrow', 'CurvedDoubleArrow', 'CurvesAsSubmobjects', 'Cutout', 'CyclicReplace', 'Cylinder', 'DARKER_GRAY', 'DARKER_GREY', 'DARK_BLUE', 'DARK_BROWN', 'DARK_GRAY', 'DARK_GREY', 'DEFAULT_ARROW_TIP_LENGTH', 'DEFAULT_DASH_LENGTH', 'DEFAULT_DOT_RADIUS', 'DEFAULT_FONT_SIZE', 'DEFAULT_MOBJECT_TO_EDGE_BUFFER', 'DEFAULT_MOBJECT_TO_MOBJECT_BUFFER', 'DEFAULT_POINTWISE_FUNCTION_RUN_TIME', 'DEFAULT_POINT_DENSITY_1D', 'DEFAULT_POINT_DENSITY_2D', 'DEFAULT_QUALITY', 'DEFAULT_SMALL_DOT_RADIUS', 'DEFAULT_STROKE_WIDTH', 'DEFAULT_WAIT_TIME', 'DEGREES', 'DL', 'DOWN', 'DR', 'DVIPSNAMES', 'DashedLine', 'DashedVMobject', 'DecimalMatrix', 'DecimalNumber', 'DecimalTable', 'DefaultSectionType', 'DiGraph', 'DictAsObject', 'Difference', 'Dodecahedron', 'Dot', 'Dot3D', 'DotCloud', 'DoubleArrow', 'DrawBorderThenFill', 'EPILOG', 'Elbow', 'Ellipse', 'Exclusion', 'FadeIn', 'FadeOut', 'FadeToColor', 'FadeTransform', 'FadeTransformPieces', 'Flash', 'FocusOn', 'FullScreenRectangle', 'FunctionGraph', 'GOLD', 'GOLD_A', 'GOLD_B', 'GOLD_C', 'GOLD_D', 'GOLD_E', 'GRAY', 'GRAY_A', 'GRAY_B', 'GRAY_BROWN', 'GRAY_C', 'GRAY_D', 'GRAY_E', 'GREEN', 'GREEN_A', 'GREEN_B', 'GREEN_C', 'GREEN_D', 'GREEN_E', 'GREY', 'GREY_A', 'GREY_B', 'GREY_BROWN', 'GREY_C', 'GREY_D', 'GREY_E', 'Graph', 'Group', 'GrowArrow', 'GrowFromCenter', 'GrowFromEdge', 'GrowFromPoint', 'HEAVY', 'HSV', 'Homotopy', 'IN', 'INVALID_NUMBER_MESSAGE', 'ITALIC', 'Icosahedron', 'ImageMobject', 'ImageMobjectFromCamera', 'ImplicitFunction', 'Indicate', 'Integer', 'IntegerMatrix', 'IntegerTable', 'Intersection', 'LARGE_BUFF', 'LEFT', 'LIGHT', 'LIGHTER_GRAY', 'LIGHTER_GREY', 'LIGHT_BROWN', 'LIGHT_GRAY', 'LIGHT_GREY', 'LIGHT_PINK', 'LOGO_BLACK', 'LOGO_BLUE', 'LOGO_GREEN', 'LOGO_RED', 'LOGO_WHITE', 'Label', 'LabeledArrow', 'LabeledDot', 'LabeledLine', 'LabeledPolygram', 'LaggedStart', 'LaggedStartMap', 'Line', 'Line3D', 'LineJointType', 'LinearBase', 'LinearTransformationScene', 'LogBase', 'MAROON', 'MAROON_A', 'MAROON_B', 'MAROON_C', 'MAROON_D', 'MAROON_E', 'MEDIUM', 'MED_LARGE_BUFF', 'MED_SMALL_BUFF', 'MaintainPositionRelativeTo', 'ManimBanner', 'ManimColor', 'ManimColorDType', 'ManimMagic', 'MappingCamera', 'MarkupText', 'MathTable', 'MathTex', 'Matrix', 'Mobject', 'Mobject1D', 'Mobject2D', 'MobjectMatrix', 'MobjectTable', 'MoveAlongPath', 'MoveToTarget', 'MovingCamera', 'MovingCameraScene', 'MultiCamera', 'NORMAL', 'NO_SCENE_MESSAGE', 'NumberLine', 'NumberPlane', 'OBLIQUE', 'ORANGE', 'ORIGIN', 'OUT', 'Octahedron', 'OldMultiCamera', 'OpenGLPGroup', 'OpenGLPMPoint', 'OpenGLPMobject', 'PGroup', 'PI', 'PINK', 'PMobject', 'PURE_BLUE', 'PURE_GREEN', 'PURE_RED', 'PURPLE', 'PURPLE_A', 'PURPLE_B', 'PURPLE_C', 'PURPLE_D', 'PURPLE_E', 'Paragraph', 'ParametricFunction', 'ParsableManimColor', 'PhaseFlow', 'Point', 'PointCloudDot', 'PolarPlane', 'Polygon', 'Polygram', 'Polyhedron', 'Prism', 'QUALITIES', 'R3_to_complex', 'RED', 'RED_A', 'RED_B', 'RED_C', 'RED_D', 'RED_E', 'RESAMPLING_ALGORITHMS', 'RGBA', 'RIGHT', 'Rectangle', 'RegularPolygon', 'RegularPolygram', 'RemoveTextLetterByLetter', 'RendererType', 'ReplacementTransform', 'Restore', 'RightAngle', 'Rotate', 'Rotating', 'RoundedRectangle', 'SCALE_FACTOR_PER_FONT_POINT', 'SCENE_NOT_FOUND_MESSAGE', 'SEMIBOLD', 'SEMILIGHT', 'SHIFT_VALUE', 'SMALL_BUFF', 'START_X', 'START_Y', 'SVGMobject', 'SVGNAMES', 'SampleSpace', 'ScaleInPlace', 'Scene', 'SceneFileWriter', 'ScreenRectangle', 'Section', 'Sector', 'ShowIncreasingSubsets', 'ShowPartial', 'ShowPassingFlash', 'ShowPassingFlashWithThinningStrokeWidth', 'ShowSubmobjectsOneByOne', 'ShrinkToCenter', 'SingleStringMathTex', 'SmoothedVectorizedHomotopy', 'SpecialThreeDScene', 'Sphere', 'SpinInFromNothing', 'SpiralIn', 'SplitScreenCamera', 'Square', 'Star', 'StealthTip', 'StreamLines', 'Succession', 'Surface', 'SurroundingRectangle', 'Swap', 'TAU', 'TEAL', 'TEAL_A', 'TEAL_B', 'TEAL_C', 'TEAL_D', 'TEAL_E', 'THIN', 'Table', 'TangentLine', 'Tetrahedron', 'Tex', 'TexFontTemplates', 'TexTemplate', 'TexTemplateLibrary', 'Text', 'ThreeDAxes', 'ThreeDCamera', 'ThreeDScene', 'ThreeDVMobject', 'TipableVMobject', 'Title', 'Torus', 'TracedPath', 'Transform', 'TransformAnimations', 'TransformFromCopy', 'TransformMatchingShapes', 'TransformMatchingTex', 'Triangle', 'TrueDot', 'TypeWithCursor', 'UL', 'ULTRABOLD', 'ULTRAHEAVY', 'ULTRALIGHT', 'UP', 'UR', 'Uncreate', 'Underline', 'Union', 'UnitInterval', 'UntypeWithCursor', 'Unwrite', 'UpdateFromAlphaFunc', 'UpdateFromFunc', 'VDict', 'VGroup', 'VMobject', 'VMobjectFromSVGPath', 'ValueTracker', 'Variable', 'Vector', 'VectorField', 'VectorScene', 'VectorizedPoint', 'WHITE', 'Wait', 'Wiggle', 'Write', 'X11', 'XKCD', 'X_AXIS', 'YELLOW', 'YELLOW_A', 'YELLOW_B', 'YELLOW_C', 'YELLOW_D', 'YELLOW_E', 'Y_AXIS', 'Z_AXIS', 'ZoomedScene', 'builtins', 'cached', 'doc', 'file', 'loader', 'main', 'name', 'package', 'path', 'spec', 'version', '_config', 'add_extension_if_not_present', 'adjacent_n_tuples', 'adjacent_pairs', 'all_elements_are_instances', 'always', 'always_redraw', 'always_rotate', 'always_shift', 'angle_axis_from_quaternion', 'angle_between_vectors', 'angle_of_vector', 'animation', 'annotations', 'assert_is_mobject_method', 'average_color', 'bezier', 'bezier_remap', 'binary_search', 'camera', 'capture', 'cartesian_to_spherical', 'center_of_mass', 'change_to_rgba_array', 'choose', 'cli', 'cli_ctx_settings', 'clip', 'clockwise_path', 'color', 'color_gradient', 'color_to_int_rgb', 'color_to_int_rgba', 'color_to_rgb', 'color_to_rgba', 'compass_directions', 'complex_func_to_R3_func', 'complex_to_R3', 'concatenate_lists', 'config', 'console', 'constants', 'core', 'counterclockwise_path', 'cross2d', 'cycle_animation', 'double_smooth', 'drag_pixels', 'earclip_triangulation', 'ensure_executable', 'error_console', 'exponential_decay', 'f_always', 'find_intersection', 'frame', 'get_3d_vmob_end_corner', 'get_3d_vmob_end_corner_index', 'get_3d_vmob_end_corner_unit_normal', 'get_3d_vmob_gradient_start_and_end_points', 'get_3d_vmob_start_corner', 'get_3d_vmob_start_corner_index', 'get_3d_vmob_start_corner_unit_normal', 'get_3d_vmob_unit_normal', 'get_det_text', 'get_dir_layout', 'get_full_raster_image_path', 'get_full_sound_file_path', 'get_ipython', 'get_plugins', 'get_shaded_rgb', 'get_smooth_cubic_bezier_handle_points', 'get_unit_normal', 'get_video_metadata', 'get_winding_number', 'guarantee_empty_existence', 'guarantee_existence', 'gui', 'hex_to_rgb', 'index_labels', 'integer_interpolate', 'interpolate', 'interpolate_color', 'inverse_interpolate', 'invert_color', 'invert_image', 'ipy', 'is_closed', 'is_gif_format', 'is_mov_format', 'is_mp4_format', 'is_png_format', 'is_webm_format', 'line_intersection', 'linear', 'lingering', 'list_difference_update', 'list_plugins', 'list_update', 'listify', 'logger', 'make_even', 'make_even_by_cycling', 'manim_colors', 'match_interpolate', 'matrix_to_mobject', 'matrix_to_tex_string', 'merge_dicts_recursively', 'mid', 'midpoint', 'mobject', 'modify_atime', 'normalize', 'not_quite_there', 'np', 'open_file', 'opengl', 'override_animate', 'override_animation', 'partial_bezier_points', 'path_along_arc', 'perpendicular_bisector', 'plugins', 'point_lies_on_bezier', 'print_family', 'proportions_along_bezier_curve_for_point', 'quaternion_conjugate', 'quaternion_from_angle_axis', 'quaternion_mult', 'random_bright_color', 'random_color', 'rate_functions', 'register_font', 'regular_vertices', 'remove_list_redundancies', 'remove_nones', 'renderer', 'rgb_to_color', 'rgb_to_hex', 'rgba_to_color', 'rotate_vector', 'rotation_about_z', 'rotation_matrix', 'running_start', 'rush_from', 'rush_into', 'scene', 'seek_full_path_from_defaults', 'shoelace', 'shoelace_direction', 'sigmoid', 'slow_into', 'smooth', 'smoothererstep', 'smootherstep', 'smoothstep', 'spherical_to_cartesian', 'split_bezier', 'squish_rate_func', 'straight_path', 'stretch_array_to_length', 'subdivide_bezier', 'tempconfig', 'there_and_back', 'there_and_back_with_pause', 'thick_diagonal', 'tuplify', 'turn_animation_into_updater', 'typing', 'unit', 'update_dict_recursively', 'utils', 'version', 'wiggle', 'write_to_movie', 'z_to_vector']]"
                    "also fix the alignment issue if you can and no overlap should be there"
                    "---- Original Code ----\n"
                    f"{manim_code}\n\n"
                    "---- Error Message ----\n"
                    f"{error_message}\n"
                )
                fix_response = model.generate_content(fix_prompt)
                manim_code = extract_clean_manim_code(fix_response.text.strip())

                print("Code has been fixed by LLM, retrying...")
                continue
            else:
                raise HTTPException(status_code=500, detail=f"Rendering failed after {MAX_RETRIES} attempts.")

    # 7. Locate generated video
    script_name_without_ext = os.path.splitext(script_filename)[0]
    manim_output_dir = os.path.join("media", "videos", script_name_without_ext, "480p15")
    manim_video_path = os.path.join(manim_output_dir, "GeneratedScene.mp4")

    if not os.path.exists(manim_video_path):
        raise HTTPException(status_code=404, detail=f"Video not found: {manim_video_path}")

    # 8. Move video to public folder with retry
    # Move video to public folder
    final_video_name = f"{script_name_without_ext}.mp4"
    final_video_path = os.path.join("videos", final_video_name)
    os.makedirs(os.path.dirname(final_video_path), exist_ok=True)
    shutil.copy(manim_video_path, final_video_path)
    
    # Generate audio
    audio_file_path = f"{script_name_without_ext}.mp3"
    new_video = "final_out.mp4"
    final_video_path_on_disk = os.path.join("videos", new_video)
    os.makedirs("videos", exist_ok=True)
    generate_audio_from_transcript(transcript, audio_file_path, speed=1.2)
    final_out = combine_video_audio(final_video_path, audio_file_path, output_video=final_video_path_on_disk)
    # Delete temp script
    if os.path.exists(script_filename):
        os.remove(script_filename)

    # Return API response
    video_url = f"http://localhost:8000/videos/{new_video}"

    return {
        "videoUrl": video_url,
        "transcript": transcript,
        "title": f"Explaining {prompt}"
    }