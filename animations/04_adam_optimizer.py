"""
04_adam_optimizer.py

This script visualizes the resolution of the ill-conditioned canyon problem
using the Adam Optimizer. It demonstrates how momentum-based optimization methods 
dampen the erratic zigzagging of standard Gradient Descent, resulting 
in a smooth and stable convergence trajectory towards the global minimum.
"""

from manim import *
import numpy as np

class AdamResolvedCanyon(ThreeDScene):
    """
    Renders the same 3D canyon function but plots a smooth, optimized 
    trajectory representing the Adam algorithm successfully navigating the valley.
    """
    def construct(self):
        # ==========================================
        # 1. 3D SCENE SETUP (Axes and Camera)
        # ==========================================
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 3, 1],
            x_length=6, y_length=6, z_length=3
        )
        
        # Labels for the weights, rotated to face the camera properly
        x_label = MathTex("w_1").next_to(axes.x_axis.get_end(), RIGHT)
        x_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        y_label = MathTex("w_2").next_to(axes.y_axis.get_end(), UP)
        y_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        labels_group = VGroup(x_label, y_label)

        # ==========================================
        # 2. ILL-CONDITIONED SURFACE GENERATION
        # ==========================================
        # The exact same ill-conditioned canyon function as the previous scene
        def canyon_function(x, y):
            return 0.5 * x**2 + 0.02 * y**2 + 0.5

        surface = Surface(
            lambda u, v: axes.c2p(u, v, canyon_function(u, v)),
            u_range=[-2.2, 2.2], v_range=[-2.2, 2.2], resolution=(40, 40),
            fill_opacity=0.45, checkerboard_colors=[BLUE_D, BLUE_E]
        )

        # Group the environment and push it slightly into the screen
        scene_group = VGroup(axes, labels_group, surface).shift(IN * 1.5)
        
        # FIRST SECOND: Scene appearance
        self.play(Create(axes), FadeIn(labels_group), Create(surface), run_time=1.0)

        # ==========================================
        # 3. OPTIMIZED TRAJECTORY (Adam Optimizer)
        # ==========================================
        # Simulation of the Adam algorithm converging smoothly in 5 steps
        path_arrows = VGroup()
        convergence_path = [
            np.array([2.0, 2.0]),    # Start
            np.array([1.1, 1.5]),    # Step 1
            np.array([0.5, 0.9]),    # Step 2
            np.array([0.15, 0.4]),   # Step 3
            np.array([0.02, 0.1]),   # Step 4
            np.array([0.0, 0.0])     # Step 5 (Exact global minimum)
        ]
        
        current_weights = convergence_path[0]
        for target_weights in convergence_path[1:]:
            # Map 2D weight coordinates to 3D space on the floor plane
            point_start = axes.c2p(current_weights[0], current_weights[1], 0)
            point_end = axes.c2p(target_weights[0], target_weights[1], 0)
            
            # We use thick yellow arrows to symbolize stability and success
            step_arrow = Arrow(point_start, point_end, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.2, color=YELLOW)
            path_arrows.add(step_arrow)
            current_weights = target_weights

        scene_group.add(path_arrows)
        
        # THREE SECONDS: Animation of the smooth descent
        self.play(LaggedStart(*[GrowArrow(a) for a in path_arrows], lag_ratio=0.3), run_time=3.0)
        
        # FINAL SECOND: Fixed pause to avoid abruptly cutting the video (Total: 5s)
        self.wait(1.0)
