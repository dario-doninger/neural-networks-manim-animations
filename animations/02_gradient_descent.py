"""
02_gradient_descent.py

This script contains the animation for the Gradient Descent algorithm in 3D.
It visualizes:
1. A 3D cost function surface (Loss Landscape).
2. The global minimum.
3. The calculation of the gradient vector.
4. The concept of Learning Rate (\eta) scaling the gradient.
5. The iterative zigzag path towards the minimum.
"""

from manim import *
import numpy as np

class GradientDescent3D(ThreeDScene):
    def construct(self):
        # ==========================================
        # 1. 3D CARTESIAN SPACE SETUP (2.0s)
        # ==========================================
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)
        
        axes = ThreeDAxes(
            x_range=[-3.5, 3.5, 1],
            y_range=[-3.5, 3.5, 1],
            z_range=[0, 3.5, 1],
            x_length=7,
            y_length=7,
            z_length=3.5
        )
        
        x_label = MathTex("w_1").next_to(axes.x_axis.get_end(), RIGHT)
        x_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        y_label = MathTex("w_2").next_to(axes.y_axis.get_end(), UP)
        y_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        z_label = MathTex("C(w_1, w_2)").next_to(axes.z_axis.get_end(), UP)
        z_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        labels_group = VGroup(x_label, y_label, z_label)

        scene_group = VGroup(axes, labels_group)
        scene_group.shift(IN * 1.8)

        self.play(Create(axes), FadeIn(labels_group), run_time=2.0)

        # ==========================================
        # 2. COST FUNCTION SURFACE & 360 CAMERA ROTATION (8.0s)
        # ==========================================
        def cost_func(x, y):
            quad = 0.04 * (x - 1.5)**2 + 0.1 * (y + 1.5)**2
            waves = 0.02 * np.sin(4*x) + 0.02 * np.cos(4*y)
            return quad + waves + 1.5

        surface = Surface(
            lambda u, v: axes.c2p(u, v, cost_func(u, v)),
            u_range=[-3.2, 3.2],
            v_range=[-3.2, 3.2],
            resolution=(45, 45),
            fill_opacity=0.45, 
            checkerboard_colors=[BLUE_D, BLUE_E]
        )
        scene_group.add(surface)

        self.play(Create(surface), run_time=1.0)
        self.move_camera(theta=45 * DEGREES + 360 * DEGREES, run_time=7.0)

        # ==========================================
        # 3. HIGHLIGHTING GLOBAL MINIMUM (2.0s)
        # ==========================================
        min_plane_coords = axes.c2p(1.5, -1.5, 0)
        min_surface_coords = axes.c2p(1.5, -1.5, cost_func(1.5, -1.5))
        
        global_min_dot = Dot3D(point=min_plane_coords, color=RED, radius=0.1)
        dashed_projection = DashedLine(min_plane_coords, min_surface_coords, color=YELLOW, dash_length=0.1)
        scene_group.add(global_min_dot)

        self.play(FadeIn(global_min_dot), Create(dashed_projection), run_time=1.0)
        self.play(FadeOut(dashed_projection), run_time=1.0)

        # ==========================================
        # 4. INTRO TITLE (5.0s)
        # ==========================================
        title_text = Text("Gradient Descent, Augustin-Louis Cauchy, 1847", font_size=30).to_edge(UP, buff=0.5)
        self.add_fixed_in_frame_mobjects(title_text)
        title_text.set_opacity(0)

        self.play(title_text.animate.set_opacity(1), run_time=1.0)
        self.wait(4.0)

        # ==========================================
        # 5. RIGHT SIDE TEXT OVERLAY (5.0s)
        # ==========================================
        gradient_text = Text("Direction of\nmaximum decrease:", font_size=24)
        gradient_math = MathTex(r"-\nabla C(w_1, w_2)", font_size=32)
        gradient_group = VGroup(gradient_text, gradient_math).arrange(DOWN).to_edge(RIGHT, buff=0.5).shift(UP*1.0)
        
        self.add_fixed_in_frame_mobjects(gradient_group)
        gradient_group.set_opacity(0)

        self.play(gradient_group.animate.set_opacity(1), run_time=1.0)
        self.wait(4.0)

        # ==========================================
        # 6. INITIAL GRADIENT VECTOR (3.0s)
        # ==========================================
        start_weights = np.array([-2.0, 2.0])
        start_point_3d = axes.c2p(start_weights[0], start_weights[1], 0)
        start_dot = Dot3D(point=start_point_3d, color=YELLOW, radius=0.08)
        scene_group.add(start_dot)

        def get_gradient(w):
            x, y = w
            dx = 0.08*(x - 1.5) + 0.08*np.cos(4*x)
            dy = 0.2*(y + 1.5) - 0.08*np.sin(4*y)
            return np.array([dx, dy])

        grad_vector = get_gradient(start_weights)
        vector_direction = -grad_vector / np.linalg.norm(grad_vector)
        
        end_weights = start_weights + vector_direction * 0.8
        end_point_3d = axes.c2p(end_weights[0], end_weights[1], 0)
        initial_gradient_arrow = Arrow(start_point_3d, end_point_3d, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.15)
        scene_group.add(initial_gradient_arrow)

        self.play(FadeIn(start_dot), GrowArrow(initial_gradient_arrow), run_time=1.0)
        self.wait(2.0)

        # ==========================================
        # 7. LEARNING RATE EXTENSION & UPDATE FORMULA (5.0s)
        # ==========================================
        extended_end_weights = start_weights + vector_direction * 2.8
        extended_end_point_3d = axes.c2p(extended_end_weights[0], extended_end_weights[1], 0)
        extended_arrow = Arrow(start_point_3d, extended_end_point_3d, buff=0, color=YELLOW, stroke_width=4, max_tip_length_to_length_ratio=0.15)

        learning_rate_brace = BraceBetweenPoints(start_point_3d, extended_end_point_3d, color=YELLOW)
        scene_group.add(learning_rate_brace)

        mid_weights = start_weights + vector_direction * 1.4
        eta_label = MathTex(r"\eta \text{ (Learning Rate)}", font_size=24, color=YELLOW)
        eta_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        eta_label.move_to(axes.c2p(mid_weights[0], mid_weights[1], 0.8))
        scene_group.add(eta_label)

        update_title = Text("Update:", font_size=24, color=YELLOW)
        update_math = MathTex(r"\theta_{t+1} = \theta_t - \eta \nabla C(\theta_t)", font_size=28)
        update_group = VGroup(update_title, update_math).arrange(DOWN).next_to(gradient_group, DOWN, buff=1.0)
        self.add_fixed_in_frame_mobjects(update_group)

        self.play(
            ReplacementTransform(initial_gradient_arrow, extended_arrow, rate_func=smooth),
            FadeIn(learning_rate_brace),
            FadeIn(eta_label),
            FadeIn(update_group),
            run_time=1.5
        )
        self.wait(2.5)
        
        self.play(FadeOut(eta_label), FadeOut(learning_rate_brace), run_time=1.0)

        # ==========================================
        # 8. THE ZIGZAG CONVERGENCE PATH (3.0s)
        # ==========================================
        convergence_path = [
            extended_end_weights,         
            np.array([0.5, -1.8]),        
            np.array([1.1, -1.2]),        
            np.array([1.4, -1.6]),        
            np.array([1.5, -1.5])         
        ]

        path_arrows = VGroup()
        path_arrows.add(extended_arrow) 
        
        current_w = extended_end_weights
        for target_w in convergence_path[1:]:
            p1 = axes.c2p(current_w[0], current_w[1], 0)
            p2 = axes.c2p(target_w[0], target_w[1], 0)
            
            step_arrow = Arrow(p1, p2, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.2, color=YELLOW)
            path_arrows.add(step_arrow)
            current_w = target_w

        scene_group.add(path_arrows)
        
        self.play(LaggedStart(*[GrowArrow(a) for a in path_arrows[1:]], lag_ratio=0.3), run_time=3.0)
