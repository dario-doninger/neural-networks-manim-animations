from manim import *
import numpy as np

class AdamResolvedCanyon(ThreeDScene):
    def construct(self):
        
        # 1. 3D SCENE SETUP
        
        self.set_camera_orientation(phi=65 * DEGREES, theta=45 * DEGREES)

        axes = ThreeDAxes(
            x_range=[-2.5, 2.5, 1], y_range=[-2.5, 2.5, 1], z_range=[0, 3, 1],
            x_length=6, y_length=6, z_length=3
        )
        
        x_label = MathTex("w_1").next_to(axes.x_axis.get_end(), RIGHT)
        x_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        y_label = MathTex("w_2").next_to(axes.y_axis.get_end(), UP)
        y_label.rotate(90 * DEGREES, axis=RIGHT).rotate(135 * DEGREES, axis=OUT)
        
        labels_group = VGroup(x_label, y_label)

        # 2. ILL-CONDITIONED SURFACE GENERATION

        # The exact same ill-conditioned canyon function as the previous scene
        def canyon_function(x, y):
            return 0.5 * x**2 + 0.02 * y**2 + 0.5

        surface = Surface(
            lambda u, v: axes.c2p(u, v, canyon_function(u, v)),
            u_range=[-2.2, 2.2], v_range=[-2.2, 2.2], resolution=(40, 40),
            fill_opacity=0.45, checkerboard_colors=[BLUE_D, BLUE_E]
        )

        scene_group = VGroup(axes, labels_group, surface).shift(IN * 1.5)
        
        self.play(Create(axes), FadeIn(labels_group), Create(surface), run_time=1.0)

        # 3. OPTIMIZED TRAJECTORY

        # Simulation of the Adam algorithm converging smoothly in 5 steps
        path_arrows = VGroup()
        convergence_path = [
            np.array([2.0, 2.0]),
            np.array([1.1, 1.5]),
            np.array([0.5, 0.9]),
            np.array([0.15, 0.4]),
            np.array([0.02, 0.1]),
            np.array([0.0, 0.0])
        ]
        
        current_weights = convergence_path[0]
        for target_weights in convergence_path[1:]:
            # Map 2D weight coordinates to 3D space on the floor plane
            point_start = axes.c2p(current_weights[0], current_weights[1], 0)
            point_end = axes.c2p(target_weights[0], target_weights[1], 0)
            
            step_arrow = Arrow(point_start, point_end, buff=0, stroke_width=4, max_tip_length_to_length_ratio=0.2, color=YELLOW)
            path_arrows.add(step_arrow)
            current_weights = target_weights

        scene_group.add(path_arrows)
        
        self.play(LaggedStart(*[GrowArrow(a) for a in path_arrows], lag_ratio=0.3), run_time=3.0)
        
        self.wait(1.0)
