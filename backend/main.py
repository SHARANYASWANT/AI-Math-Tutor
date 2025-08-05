import os
import re
import subprocess
import uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import google.generativeai as genai

# ====== CONFIGURE GEMINI ======
GEMINI_API_KEY = "" # Replace with your valid key
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-pro")

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
TOPIC_PROMPTS = {
    "pythagoras": """
Create a *Manim Community Edition* script (Python) that visually explains the **Pythagorean Theorem**.
Ensure the triangle is right-angled, sides a² + b² = c² are highlighted, and include verification with area squares.
Follow these phases:
- Intro with title
- Construct triangle and squares
- Show relationship step-by-step
- Verify and conclude

Final format: Python code only, class name should be `GeneratedScene`. Narration must follow:
---EXPLANATION_STARTS_HERE---
Narration goes here...
""",
    "system of equations": """
Create a *Manim Community Edition* script (Python) that demonstrates solving a **System of Linear Equations** graphically.
Plot two equations with different slopes, show intersection point, and narrate steps clearly.
Animation flow:
- Title and introduction
- Plot lines from equations
- Highlight intersection point
- Explain meaning visually

Final format: Python code only, class name should be `GeneratedScene`. Narration must follow:
---EXPLANATION_STARTS_HERE---
Narration goes here...
"""
}
kj="""Generate a Manim animation script that visually explains the given mathematical problem step by step.
                    The animation should include text explanations, dynamic equation transformations, relevant geometrical 
                    or graphical representations (if applicable), and smooth transitions using animations like FadeIn, Transform, 
                    and DrawBorderThenFill. Ensure the animations maintain engagement and clarity. Align the animation in proper manner
                    and one important main thing is I only want the code alone not any strings another than the code because the manim script give syntactical error so give only code alone compulsorily and also exclude (```python and ''') in the script.
                    One important main thing is you have to import all the necessary packages and make sure no runtime error or no inclusion of not imported variable if using then import the package and use.

                    Additional requirements:
                    1. Use consistent color coding: blue for variables, green for final answers, red for important transformations
                    2. Add wait() commands between key steps with appropriate timing (0.5-2 seconds) for better pacing
                    3. Group related mathematical operations using VGroups for cleaner animations
                    4. Use proper self references for all scene elements and camera operations
                    5. Add progress_bar=True to animations that benefit from showing progression
                    6. Ensure all text is properly positioned with appropriate font size (MathTex(...).scale(0.8))
                    7. Include self.wait(3) at the end of the animation
                    8. Use TracedPath for any graphical representations that involve motion
                    9. Set background color with config.background_color = "#1f1f1f" at the class definition level

                    Topic-specific animation techniques (3Blue1Brown style):
                    - For trigonometry: Use the UnitCircle class with animated angles, include DashedLine for projections, and animate sine/cosine waves growing from the circle
                    - For calculus: Use NumberPlane with animated slopes/tangent lines that change color based on values, zoom in progressively to show limits, and use area filling animations for integrals
                    - For algebra: Transform equations with color highlighting for each step, use coordinate shifts to show operations, and grow/shrink terms during simplification
                    - For geometry: Use opacity changes to reveal cross-sections, include dotted construction lines, and animate 3D objects rotating to show different perspectives
                    - For statistics: Create animated histograms that transform into probability curves, use color gradients to show probability regions, and animate individual data points
                    - For vectors: Show arrows in coordinate systems that transform/combine with smooth animations, use shadowing for projections
                    - For series: Create animated stacking of terms, use color gradients to show convergence/divergence, and include partial sum tracking
                    - For logarithms: Use area stretching/compressing to visualize log properties, animate exponential growth with highlighting
                    - For complex numbers: Use the ComplexPlane class with transformations, animate mapping between rectangular and polar forms with rotating vectors

                    Remember, provide ONLY executable code with NO explanatory text or markdown formatting.
                    : [algebra]
"""

# ====== DEFAULT GEMINI PROMPT BUILDER ======
def build_gemini_prompt(topic: str) -> str:
    return f"""You are an EXPERT MANIM COMMUNITY ANIMATOR. Generate ZERO-ERROR animations using ONLY verified Manim Community Edition syntax. Every line must execute perfectly without compilation errors.

Topic : {topic}

## 🚫 ABSOLUTE FORBIDDEN ELEMENTS

*NEVER USE THESE:*
- ❌ from manimgl import * or ANY ManimGL syntax
- ❌ Custom classes like Checkmark, CustomShape without proper definition
- ❌ .get_corner() without direction parameter
- ❌ Interactive widgets or real-time manipulations
- ❌ Deprecated functions from older Manim versions
- ❌ Complex custom VMobject classes
- ❌ Browser-based outputs or OpenGL renderers
- ❌ Methods that don't exist in Community Edition
- ❌ List arithmetic (e.g., A + 0.5 * (B - A) where A, B are lists)
- ❌ Mixing VMobject and Mobject in VGroup
- ❌ Elements extending beyond screen boundaries
- ❌ Overlapping text or objects

## ✅ MANDATORY REQUIREMENTS

### *1. IMPORTS - ONLY THIS:*
python
from manim import *
import numpy as np  # Only if needed for calculations


### *2. VERIFIED BASIC SHAPES ONLY:*
python
# USE THESE BUILT-IN SHAPES ONLY:
Circle()
Square() 
Rectangle()
Triangle()
Line()
Arrow()
Dot()
Polygon([points])  # For custom shapes

# NEVER create custom VMobject classes unless absolutely necessary
# ALWAYS use np.array() for coordinate calculations


### *3. POSITION SYSTEM - SAFE COORDINATES:*
python
# SCREEN BOUNDARIES (NEVER EXCEED):
MAX_X = 5.5    # Left/Right limit (safe zone)
MAX_Y = 2.8    # Up/Down limit (safe zone)

# COORDINATE CALCULATIONS - ALWAYS USE np.array():
A = np.array([0, 0, 0])              # Origin point
B = np.array([2, 1, 0])              # Example point
C = A + 0.5 * (B - A)                # Correct vector math

# SAFE POSITIONING METHODS:
obj.move_to(ORIGIN)                    # Center
obj.to_edge(UP, buff=0.8)             # Top edge with buffer
obj.to_edge(DOWN, buff=0.8)           # Bottom edge with buffer  
obj.to_edge(LEFT, buff=0.8)           # Left edge with buffer
obj.to_edge(RIGHT, buff=0.8)          # Right edge with buffer
obj.next_to(other_obj, UP, buff=0.4)  # Relative positioning
obj.shift(UP * 1.5)                   # Relative movement (within bounds)

# PREVENT OVERLAPPING:
obj1.move_to(LEFT * 2)               # Left position
obj2.move_to(RIGHT * 2)              # Right position (no overlap)
obj3.move_to(UP * 1.5)               # Top position
obj4.move_to(DOWN * 1.5)             # Bottom position


### *4. TEXT AND MATH - SIMPLE ONLY:*
python
# TEXT (ALWAYS WORKS):
title = Text("Title Here", font_size=48)
subtitle = Text("Subtitle", font_size=32)

# MATH - SIMPLE EXPRESSIONS ONLY:
equation = MathTex(r"x^2 + y^2 = r^2")
formula = MathTex(r"f(x) = 2x + 1")

# AVOID: Complex LaTeX, special symbols, or advanced formatting


### *5. COLORS - BUILT-IN ONLY:*
python
# USE THESE COLORS ONLY:
RED, BLUE, GREEN, YELLOW, ORANGE, PURPLE, PINK
WHITE, BLACK, GRAY, LIGHT_GRAY, DARK_GRAY


### *6. AXES AND GRAPHS - VERIFIED TEMPLATE:*
python
# SAFE AXES CONFIGURATION:
axes = Axes(
    x_range=[-4, 4, 1],
    y_range=[-3, 3, 1],
    x_length=8,
    y_length=6,
    tips=False  # Avoid tip issues
)

# SIMPLE FUNCTION PLOTTING:
curve = axes.plot(lambda x: x**2, x_range=[-2, 2], color=BLUE)


## 🏗 MANDATORY SCENE STRUCTURE

python
from manim import *

class ConceptAnimation(Scene):
    def construct(self):
        # Step 1: Create title
        self.create_title()
        self.wait(1)
        
        # Step 2: Main content
        self.show_main_content()
        self.wait(1)
        
        # Step 3: Clear and conclude
        self.clear_screen()
        self.create_conclusion()
        self.wait(2)
    
    def create_title(self):
        title = Text("Concept Title", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.title = title
    
    def show_main_content(self):
        # Your main animation code here
        # Use only verified elements
        pass
    
    def clear_screen(self):
        # Remove all objects safely
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)
        self.wait(0.5)
    
    def create_conclusion(self):
        conclusion = Text("Conclusion", font_size=36, color=GREEN)
        conclusion.move_to(ORIGIN)
        self.play(Write(conclusion), run_time=1.5)


## 🔧 ERROR PREVENTION RULES

### *Rule 1: Method Verification*
python
# CORRECT: Always provide required parameters
corner = square.get_corner(UP + RIGHT)  # Direction required

# WRONG: Missing parameters
corner = square.get_corner()  # Will cause error


### *Rule 2: VGroup for VMobjects Only*
python
# CORRECT: Only VMobjects in VGroup
shapes = VGroup(circle, square, triangle)  # All VMobjects
self.play(Create(shapes), run_time=2)

# CORRECT: Mixed types - use Group instead
from manim import Group
mixed_objects = Group(*self.mobjects)  # For mixed Mobject types
self.play(FadeOut(mixed_objects), run_time=1)

# WRONG: Mixing VMobject and Mobject in VGroup
objects = VGroup(*self.mobjects)  # May cause TypeError


### *Rule 3: Simple Animations Only*
python
# SAFE ANIMATIONS:
self.play(Create(obj), run_time=2)
self.play(Write(text), run_time=1.5)
self.play(Transform(obj1, obj2), run_time=2)
self.play(FadeIn(obj), run_time=1)
self.play(FadeOut(obj), run_time=1)
self.play(obj.animate.shift(UP), run_time=1)

# AVOID: Complex custom animations


### *Rule 4: Screen Layout Management*
python
# TITLE AREA (Top 15% of screen):
title.to_edge(UP, buff=0.8)           # Safe title position

# MAIN CONTENT AREA (Middle 70% of screen):
content.move_to(ORIGIN)               # Center for main content
left_content.move_to(LEFT * 3)        # Left side content
right_content.move_to(RIGHT * 3)      # Right side content

# FOOTER AREA (Bottom 15% of screen):
footer.to_edge(DOWN, buff=0.8)        # Safe footer position

# PREVENT OVERLAPPING - Minimum spacing:
MIN_SPACING = 0.5                     # Minimum distance between objects
obj2.next_to(obj1, RIGHT, buff=MIN_SPACING)

# GRID LAYOUT for multiple objects:
objects = [obj1, obj2, obj3, obj4]
positions = [LEFT*2 + UP, RIGHT*2 + UP, LEFT*2 + DOWN, RIGHT*2 + DOWN]
for obj, pos in zip(objects, positions):
    obj.move_to(pos)


## 📝 VERIFIED TEMPLATES

### *Template 1: Simple Geometric Demo*
python
from manim import *

class GeometryDemo(Scene):
    def construct(self):
        # Title
        title = Text("Geometry Basics", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Create shapes
        circle = Circle(radius=1, color=RED)
        circle.move_to(LEFT * 3)
        
        square = Square(side_length=2, color=GREEN)
        square.move_to(ORIGIN)
        
        triangle = Triangle(color=YELLOW)
        triangle.move_to(RIGHT * 3)
        
        # Animate creation
        shapes = VGroup(circle, square, triangle)
        self.play(Create(shapes), run_time=3)
        self.wait(2)
        
        # Clean exit
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)
        self.wait(1)


### *Template 2: Mathematical Function*
python
from manim import *

class FunctionPlot(Scene):
    def construct(self):
        # Title
        title = Text("Function: f(x) = x²", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.wait(1)
        
        # Create axes
        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[0, 6, 1],
            x_length=8,
            y_length=5,
            tips=False
        )
        axes.move_to(ORIGIN)
        
        # Create function
        parabola = axes.plot(lambda x: x**2, x_range=[-2.5, 2.5], color=RED)
        
        # Labels
        x_label = axes.get_x_axis_label("x")
        y_label = axes.get_y_axis_label("y")
        
        # Animate
        self.play(Create(axes), run_time=2)
        self.play(Write(x_label), Write(y_label), run_time=1)
        self.wait(0.5)
        self.play(Create(parabola), run_time=3)
        self.wait(2)
        
        # Clean exit
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)
        self.wait(1)     : {topic}


"""

# ====== CLEAN GEMINI OUTPUT ======
def clean_manim_code(manim_code: str) -> str:
    # Remove markdown fences
    manim_code = re.sub(r"^```(?:python)?", "", manim_code, flags=re.MULTILINE)
    manim_code = re.sub(r"```$", "", manim_code, flags=re.MULTILINE).strip()

    # Fix invalid escape sequence like \c
    manim_code = manim_code.replace(r"\c", r"\\c")

    # Force class name to GeneratedScene(Scene)
    manim_code = re.sub(r"class\s+\w+\s*\(", "class GeneratedScene(", manim_code)

    # Ensure it inherits Scene explicitly
    if "class GeneratedScene" in manim_code and "Scene" not in manim_code.split("class GeneratedScene")[1]:
        manim_code = manim_code.replace("class GeneratedScene(", "class GeneratedScene(Scene):")

    # If no GeneratedScene at all, fallback minimal class
    if "class GeneratedScene" not in manim_code:
        manim_code = (
            "from manim import *\n\n"
            "class GeneratedScene(Scene):\n"
            "    def construct(self):\n"
            "        self.add(Text('Error: Scene could not be generated'))\n"
        )

    return manim_code

# ====== HYBRID VIDEO GENERATION ENDPOINT ======
@app.post("/generate-video")
def generate_video(request: PromptRequest):
    prompt = request.prompt.strip().lower()
    print(f"Prompt received: {prompt}")

    # 1. Hardcoded videos
    if prompt in HARDCODED_VIDEOS:
        print(f"Serving hardcoded video for: {prompt}")
        return HARDCODED_VIDEOS[prompt]
    k=build_gemini_prompt(prompt)

    # 2. Determine Gemini prompt
    matched_topic = next((k for k in TOPIC_PROMPTS if k in prompt), None)
    gemini_prompt = TOPIC_PROMPTS.get(matched_topic, build_gemini_prompt(prompt))

    # 3. Get content from Gemini
    response = model.generate_content(k)

    # 4. Split code and transcript
    parts = response.text.split("---EXPLANATION_STARTS_HERE---")
    manim_code = clean_manim_code(parts[0].strip())
    transcript = parts[1].strip() if len(parts) > 1 else f"Step-by-step explanation for {prompt}"

    # 5. Save Manim script to temp file
    script_filename = f"video_{uuid.uuid4().hex}.py"
    with open(script_filename, "w") as f:
        f.write(manim_code)

    print(f"Saved Manim code to {script_filename}")

    # 6. Render video using Manim CLI
    try:
        subprocess.run(
            ["manim", "-pql", script_filename, "GeneratedScene"],
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise HTTPException(status_code=500, detail=f"Manim rendering failed: {e}")

    # 7. Locate generated video
    script_name_without_ext = os.path.splitext(script_filename)[0]
    manim_output_dir = os.path.join("media", "videos", script_name_without_ext, "480p15")
    manim_video_path = os.path.join(manim_output_dir, "GeneratedScene.mp4")

    if not os.path.exists(manim_video_path):
        raise HTTPException(status_code=404, detail=f"Video not found: {manim_video_path}")

    # 8. Move video to public folder
    final_video_name = f"{script_name_without_ext}.mp4"
    final_path = os.path.join("videos", final_video_name)
    os.rename(manim_video_path, final_path)

    # 9. Delete temp script
    os.remove(script_filename)

    # 10. Return API response
    video_url = f"http://localhost:8000/videos/{final_video_name}"
    return {
        "videoUrl": video_url,
        "transcript": transcript,
        "title": f"Explaining {prompt}"
    }
