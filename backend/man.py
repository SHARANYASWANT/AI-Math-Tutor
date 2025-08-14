from manim import *
import numpy as np

class ConceptAnimation(Scene):
    def construct(self):
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
        title = Text("Pythagoras' Theorem", font_size=48, color=BLUE)
        title.to_edge(UP, buff=0.8)
        self.play(Write(title), run_time=2)
        self.title = title

    def show_main_content(self):
        # --- Triangle Setup (Right Triangle with legs a, b and hypotenuse c) ---
        A = np.array([0, 0, 0])
        B = np.array([3, 0, 0])   # b = 3
        C = np.array([0, 2, 0])   # a = 2
        
        # Sides
        side_b = Line(A, B, color=BLUE)     # b along x-axis
        side_a = Line(A, C, color=GREEN)    # a along y-axis
        side_c = Line(B, C, color=RED)      # hypotenuse
        
        # Right angle marker at A
        ra = RightAngle(side_b, side_a, length=0.3, color=YELLOW)
        
        # Labels
        label_a = MathTex("a", color=GREEN).scale(0.9)
        label_b = MathTex("b", color=BLUE).scale(0.9)
        label_c = MathTex("c", color=RED).scale(0.9)
        label_a.next_to(side_a, LEFT, buff=0.25)
        label_b.next_to(side_b, DOWN, buff=0.25)
        label_c.next_to(side_c, UP, buff=0.25)
        
        tri_group = VGroup(side_a, side_b, side_c, ra, label_a, label_b, label_c)
        tri_group.move_to(ORIGIN)
        tri_group.scale(0.9)  # Keep safely within viewport
        tri_group.shift(LEFT * 2.6)  # Left content zone
        
        # Narration 1
        narr1 = Paragraph(
            "A right triangle has legs a and b,",
            "and hypotenuse c.",
            line_spacing=0.6,
            alignment="center",
            font_size=26
        )
        narr1.to_edge(DOWN, buff=0.5)
        
        self.play(Create(VGroup(side_a, side_b, side_c)), run_time=2)
        self.play(Create(ra), run_time=0.8)
        self.play(Write(VGroup(label_a, label_b, label_c)), run_time=1)
        self.play(FadeIn(narr1), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(narr1), run_time=0.5)
        
        # --- Area Squares (Proportional and clearly arranged) ---
        a_len = 2.0
        b_len = 3.0
        c_len = (a_len**2 + b_len**2) ** 0.5
        
        k = 0.5  # scale factor for display sizes
        a_side = a_len * k
        b_side = b_len * k
        c_side = c_len * k
        
        sq_a = Square(side_length=a_side, color=GREEN, fill_opacity=0.2, stroke_width=4)
        sq_b = Square(side_length=b_side, color=BLUE, fill_opacity=0.2, stroke_width=4)
        sq_c = Square(side_length=c_side, color=RED, fill_opacity=0.2, stroke_width=4)
        
        lab_a2 = MathTex("a^2", color=GREEN).scale(0.9)
        lab_b2 = MathTex("b^2", color=BLUE).scale(0.9)
        lab_c2 = MathTex("c^2", color=RED).scale(0.9)
        
        lab_a2.next_to(sq_a, DOWN, buff=0.25)
        lab_b2.next_to(sq_b, DOWN, buff=0.25)
        lab_c2.next_to(sq_c, DOWN, buff=0.25)
        
        sum_plus = MathTex("+").scale(1.2).set_color(WHITE)
        equal_sign = MathTex("=").scale(1.2).set_color(WHITE)
        
        # Group and arrange the a^2 + b^2 = c^2 layout
        left_sum = VGroup(sq_a, lab_a2)
        right_sum = VGroup(sq_b, lab_b2)
        left_sum_arranged = VGroup(left_sum)
        right_sum_arranged = VGroup(right_sum)
        left_sum_arranged.arrange(DOWN, buff=0.25, aligned_edge=DOWN)
        right_sum_arranged.arrange(DOWN, buff=0.25, aligned_edge=DOWN)
        
        sum_group = VGroup(left_sum_arranged, sum_plus, right_sum_arranged)
        sum_group.arrange(RIGHT, buff=0.6, aligned_edge=DOWN)
        
        result_group = VGroup(VGroup(sq_c, lab_c2))
        result_group.arrange(DOWN, buff=0.25, aligned_edge=DOWN)
        
        equation_layout = VGroup(sum_group, equal_sign, result_group)
        equation_layout.arrange(RIGHT, buff=0.8, aligned_edge=DOWN)
        equation_layout.scale(1.0)
        equation_layout.move_to(ORIGIN)
        equation_layout.shift(RIGHT * 2.4)  # Right content zone; prevent overlap with triangle
        
        # Narration 2
        narr2 = Paragraph(
            "Squares on the sides have areas",
            "a², b², and c² respectively.",
            line_spacing=0.6,
            alignment="center",
            font_size=26
        )
        narr2.to_edge(DOWN, buff=0.5)
        
        self.play(Create(sum_group), run_time=1.8)
        self.play(Write(equal_sign), run_time=0.6)
        self.play(Create(result_group), run_time=1.2)
        self.play(FadeIn(narr2), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(narr2), run_time=0.5)
        
        # --- Final Equation ---
        eq = MathTex(r"a^2 + b^2 = c^2").scale(1.2).set_color(YELLOW)
        eq.next_to(equation_layout, DOWN, buff=0.6)
        # Ensure it remains in bounds by slightly shifting if needed
        eq.shift(UP * 0.0)
        
        narr3 = Paragraph(
            "Pythagoras' Theorem:",
            "The sum of the areas on the legs equals the area on the hypotenuse.",
            line_spacing=0.6,
            alignment="center",
            font_size=26
        )
        narr3.to_edge(DOWN, buff=0.5)
        
        self.play(Write(eq), run_time=1.2)
        self.play(FadeIn(narr3), run_time=0.8)
        self.wait(1.2)
        self.play(FadeOut(narr3), run_time=0.5)
        
        # Save references for clearing
        self.main_objects = VGroup(tri_group, equation_layout, eq)
        self.add(self.main_objects)

    def clear_screen(self):
        # Remove all objects safely
        self.play(FadeOut(VGroup(*self.mobjects)), run_time=1)
        self.wait(0.5)

    def create_conclusion(self):
        conclusion = Text("a² + b² = c²", font_size=42, color=GREEN)
        conclusion.move_to(ORIGIN + UP * 0.6)
        
        note = Text(
            "Run in notebook:\nnotebooks.gesis.org/.../First Steps with Manim.ipynb\n"
            "with: %%manim -qm ConceptAnimation",
            font_size=26,
            color=WHITE
        )
        note.to_edge(DOWN, buff=0.8)
        
        self.play(Write(conclusion), run_time=1.5)
        self.play(Write(note), run_time=1.2)


        