"""
05_parabola_interpolation.py

This script visualizes the concept of curve fitting and interpolation using a parabola.
It serves as a visual intuition for the Universal Approximation Theorem in Neural Networks,
demonstrating how adjusting mathematical parameters (like weights and biases) 
allows a function to perfectly map to target data points.
"""

from manim import *
import numpy as np

class ParabolaInterpolator(Scene):
    """
    Animates a parabola adjusting its coefficients (a, b, c) to pass exactly
    through three fixed data points. It concludes by linking these coefficients
    to the learnable parameters (Weights and Biases) of a Neural Network.
    """
    def construct(self):
        # ==========================================
        # 1. SCENE SETUP: AXES AND TARGET POINTS
        # ==========================================
        # Extended Y-axis for safety and positioned slightly upwards
        axes = Axes(
            x_range=[-3, 3], y_range=[-1, 8], 
            x_length=6, y_length=3.5, 
            axis_config={"include_tip": True}
        ).shift(UP * 1.2)
        
        # 3 Fixed target data points to interpolate
        point_coordinates = [[-2, 4], [0, 1], [2, 3]]
        target_dots = VGroup(*[Dot(axes.c2p(x, y), color=RED, radius=0.08) for x, y in point_coordinates])
        
        # ==========================================
        # 2. DYNAMIC PARABOLA AND EQUATION SETUP
        # ==========================================
        # Variable coefficients tracked for smooth animation
        a = ValueTracker(-0.5)
        b = ValueTracker(1.5)
        c = ValueTracker(0.5)
        
        # The parabola curve is continuously redrawn as the trackers change
        parabola = always_redraw(lambda: 
            axes.plot(lambda x: a.get_value()*x**2 + b.get_value()*x + c.get_value(), color=BLUE, x_range=[-3, 3])
        )
        
        # The equation text updates dynamically to show the current values of a, b, c
        dynamic_equation = always_redraw(lambda: MathTex(
            f"y = {a.get_value():.2f} x^2 {b.get_value():+.2f} x {c.get_value():+.2f}",
            font_size=36
        ).next_to(axes, DOWN, buff=0.8))
        
        self.play(Create(axes), FadeIn(target_dots), Create(parabola), FadeIn(dynamic_equation), run_time=0.5)
        
        # ==========================================
        # 3. THE "LEARNING" PROCESS (CURVE FITTING)
        # ==========================================
        # Controlled manual oscillation (avoids wild wiggling so the curve stays within bounds)
        self.play(
            a.animate.set_value(0.1), b.animate.set_value(0.5), c.animate.set_value(2.0),
            run_time=0.8
        )
        self.play(
            a.animate.set_value(0.8), b.animate.set_value(-0.5), c.animate.set_value(1.5),
            run_time=0.8
        )
        
        # Final step: Perfect interpolation mapping the 3 target points
        self.play(
            a.animate.set_value(0.625), b.animate.set_value(-0.25), c.animate.set_value(1.0),
            run_time=1.0
        )
        
        # ==========================================
        # 4. NEURAL NETWORK ANALOGY REVEAL
        # ==========================================
        # Replace the numerical equation with a generic algebraic one
        generic_equation = MathTex("y = ", "a", "x^2 + ", "b", "x + ", "c", font_size=36).move_to(dynamic_equation.get_center())
        
        self.play(ReplacementTransform(dynamic_equation, generic_equation), run_time=0.5)
        
        # Draw arrows to explicitly link polynomial coefficients to neural network Parameters
        parameters_label = Text("W, b (Parameters)", font_size=20, color=YELLOW).next_to(generic_equation, DOWN, buff=0.8)
        parameter_arrows = VGroup(*[
            Arrow(parameters_label.get_top(), generic_equation.get_part_by_tex(tex).get_bottom() + DOWN*0.1, buff=0.05, stroke_width=2, max_tip_length_to_length_ratio=0.15, color=YELLOW)
            for tex in ["a", "b", "c"]
        ])
        
        self.play(FadeIn(parameters_label), *[GrowArrow(arr) for arr in parameter_arrows], run_time=0.5)
        
        # Extended pause at the end (Total 4.0s)
        self.wait(4.0)
