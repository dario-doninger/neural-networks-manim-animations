from manim import *

class NeuralNetworkFinal(Scene):
    def construct(self):
        # ==========================================
        # 1. INTRO: CHAPTER 1 (1.0s)
        # ==========================================
        title_text = VGroup(
            Text("Chapter 1:", font_size=50),
            Text("Neural Networks", font_size=70)
        ).arrange(DOWN, buff=0.5)
        
        self.add(title_text) # Appears instantly
        self.wait(1.0)
        self.remove(title_text) # Disappears instantly

        # ==========================================
        # 2. SKELETON: NEURONS & DOTS (9.0s)
        # ==========================================
        layers_config = [3, 4, 4, 1]
        nodes = VGroup()
        dots_group = VGroup()
        
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup()
            for j in range(num_nodes):
                neuron = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
                neuron.move_to(RIGHT * (i * 2.5 - 3.75) + DOWN * (j * 0.9 - (num_nodes-1)*0.45))
                layer.add(neuron)
            
            # Add vertical dots under each layer (except the output layer)
            if num_nodes > 1:
                dots = MathTex(r"\vdots", font_size=30).next_to(layer, DOWN, buff=0.2)
                dots_group.add(dots)
            
            nodes.add(layer)

        # Slow fade-in animation (9 seconds total)
        self.play(FadeIn(nodes, lag_ratio=0.4), FadeIn(dots_group), run_time=6.0)
        self.wait(3.0)

        # ==========================================
        # 3. CONNECTIONS (4.0s)
        # ==========================================
        layer_links_group = VGroup()
        for i in range(len(layers_config) - 1):
            current_layer_links = VGroup()
            for n1 in nodes[i]:
                for n2 in nodes[i+1]:
                    line = Line(n1.get_center(), n2.get_center(), stroke_width=1, stroke_opacity=0.2, color=WHITE)
                    line.z_index = -1
                    current_layer_links.add(line)
            layer_links_group.add(current_layer_links)

        self.play(Create(layer_links_group), run_time=4.0)

        # ==========================================
        # 4. INPUT VECTOR (5.0s)
        # ==========================================
        labels = VGroup(*[MathTex(f"x_{j+1}", font_size=24).move_to(nodes[0][j]) for j in range(3)])
        vector_x = MathTex(r"\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}", font_size=35)
        
        # Positioned exactly below the first layer
        vector_x.next_to(nodes[0], DOWN, buff=1.2)

        self.play(Write(labels), run_time=1.5)
        self.play(TransformFromCopy(labels, vector_x), run_time=2.5)
        self.wait(1.0)

        # ==========================================
        # 5. INFORMATION FLOW & OUTPUT 8 (4.0s)
        # ==========================================
        # Highlight connections layer by layer
        for i in range(len(layer_links_group)):
            self.play(
                layer_links_group[i].animate.set_stroke(color=YELLOW, opacity=1, width=2),
                run_time=1.0,
                rate_func=linear
            )
        
        # Output neuron lights up and the number 8 appears
        output_node = nodes[-1][0]
        value_8 = Text("8", font_size=24, color=WHITE).move_to(output_node)
        
        self.play(
            output_node.animate.set_fill(YELLOW, opacity=1).scale(1.2),
            Write(value_8),
            run_time=1.0
        )

        # ==========================================
        # 6. FREEZE (2.0s)
        # ==========================================
        self.wait(2.0)


class SingleNeuronFunction(Scene):
    def construct(self):
        # ==========================================
        # 0. INITIAL SETUP
        # ==========================================
        layers_config = [3, 4, 4, 1]
        nodes = VGroup()
        dots_group = VGroup()
        
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup()
            for j in range(num_nodes):
                neuron = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
                neuron.move_to(RIGHT * (i * 2.5 - 3.75) + DOWN * (j * 0.9 - (num_nodes-1)*0.45))
                layer.add(neuron)
            
            if num_nodes > 1:
                dots = MathTex(r"\vdots", font_size=30).next_to(layer, DOWN, buff=0.2)
                dots_group.add(dots)
            
            nodes.add(layer)

        layer_links_group = VGroup()
        for i in range(len(layers_config) - 1):
            current_layer_links = VGroup()
            for n1 in nodes[i]:
                for n2 in nodes[i+1]:
                    line = Line(n1.get_center(), n2.get_center(), stroke_width=2, stroke_opacity=1, color=YELLOW)
                    line.z_index = -1
                    current_layer_links.add(line)
            layer_links_group.add(current_layer_links)

        # Vectors and Labels that will disappear immediately
        labels = VGroup(*[MathTex(f"x_{j+1}", font_size=24).move_to(nodes[0][j]) for j in range(3)])
        old_vector_x = MathTex(r"\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}", font_size=35).next_to(nodes[0], DOWN, buff=1.2)
        
        output_node = nodes[-1][0]
        output_node.set_fill(YELLOW, opacity=1).scale(1.2)
        value_8 = Text("8", font_size=24, color=WHITE).move_to(output_node)

        entire_network = VGroup(layer_links_group, nodes, dots_group)
        self.add(entire_network, labels, old_vector_x, value_8)

        # ==========================================
        # 1. RETURN TO NORMAL & REMOVE VECTORS (1.0s)
        # ==========================================
        # Fade out the 8, the vector_x, and the labels BEFORE zooming
        self.play(
            output_node.animate.set_fill(BLUE, opacity=0.8).scale(1/1.2),
            FadeOut(value_8),
            FadeOut(old_vector_x),
            FadeOut(labels),
            *[l.animate.set_stroke(color=WHITE, opacity=0.2, width=1) for current_layer_links in layer_links_group for l in current_layer_links],
            run_time=1.0
        )

        # ==========================================
        # 2. ZOOM SELECTION AND SMOOTH TRANSFORM (2.0s)
        # ==========================================
        target_neuron = nodes[1][2] # Second layer, third from the top
        
        in_lines = VGroup(*[l for l in layer_links_group[0] if np.linalg.norm(l.get_end() - target_neuron.get_center()) < 0.1])
        out_lines = VGroup(*[l for l in layer_links_group[1] if np.linalg.norm(l.get_start() - target_neuron.get_center()) < 0.1])
        
        everything_else = VGroup(dots_group)
        for i, layer in enumerate(nodes):
            for j, n in enumerate(layer):
                if not (i == 1 and j == 2):
                    everything_else.add(n)
        for i, current_layer_links in enumerate(layer_links_group):
            for l in current_layer_links:
                if l not in in_lines and l not in out_lines:
                    everything_else.add(l)

        shift_vector = ORIGIN - target_neuron.get_center()

        self.play(
            FadeOut(everything_else),
            entire_network.animate.shift(shift_vector).scale(1.8, about_point=ORIGIN),
            run_time=2.0
        )

        # ==========================================
        # 3. WEIGHTS AND SPACIOUS PERCENTAGES (6.0s total)
        # ==========================================
        weights = VGroup()
        percs = VGroup()
        perc_strings = [r"=30\%", r"=50\%", r"=20\%"]
        
        for k, line in enumerate(in_lines):
            # Placed decidedly more to the left on the branches
            w = MathTex(f"w_{k+1}", font_size=36).move_to(line.point_from_proportion(0.5) + UP*0.35)
            p = MathTex(perc_strings[k], font_size=32).next_to(w, RIGHT, buff=0.1)
            weights.add(w)
            percs.add(p)
            entire_network.add(w)

        self.play(FadeIn(weights), run_time=1.0)
        self.wait(0.5)
        self.play(Write(percs), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(percs), run_time=1.5)

        # ==========================================
        # 4. BIAS AND SCALAR FORMULA (2.5s)
        # ==========================================
        bias = MathTex("b", font_size=40).next_to(target_neuron, UP, buff=0.5)
        entire_network.add(bias)
        self.play(FadeIn(bias), run_time=1.0)

        sum_formula = MathTex(r"z = \sum_{i=1}^3 w_i x_i + b", font_size=45).next_to(target_neuron, DOWN, buff=0.8)
        entire_network.add(sum_formula)
        
        self.play(ReplacementTransform(VGroup(weights, bias), sum_formula), run_time=1.5)

        # ==========================================
        # 5. REVEAL & DE-ZOOM WITH VERTICAL DROP (1.5s)
        # ==========================================
        # We remove everything from the network to destroy ghost symbols
        entire_network.remove(sum_formula)
        entire_network.remove(bias)
        for w in weights:
            entire_network.remove(w)

        # Step 1: The rest of the network appears while we are still zoomed in (0.5s)
        self.play(FadeIn(everything_else), run_time=0.5)

        # Step 2: Perfect De-zoom. The network returns cleanly and the formula drops vertically.
        vector_formula = MathTex(r"\mathbf{z} = \mathbf{w} \cdot \mathbf{x} + b", font_size=36)
        # x = -1.25 is the exact absolute coordinate of the second layer to drop perfectly vertical
        vector_formula.move_to(np.array([-1.25, -2.8, 0]))

        self.play(
            entire_network.animate.scale(1/1.8, about_point=ORIGIN).shift(-shift_vector),
            ReplacementTransform(sum_formula, vector_formula),
            run_time=1.0
        )

        # ==========================================
        # 6. ISOLATE Z AND ACTIVATION FUNCTION (3.0s)
        # ==========================================
        z_only_formula = MathTex(r"\mathbf{z}", font_size=36).move_to(vector_formula.get_left() + RIGHT * 0.2)
        self.play(ReplacementTransform(vector_formula, z_only_formula), run_time=1.0)

        activation_formula = MathTex(r"\mathbf{a} = \sigma(\mathbf{z})", font_size=36)
        activation_formula.move_to(np.array([nodes[2].get_x(), -2.8, 0]))
        
        self.play(ReplacementTransform(z_only_formula, activation_formula), run_time=2.0)

        # ==========================================
        # 7. SIGMOID AND ReLU (Synchronized and immediate arrows)
        # ==========================================
        # Sigmoid preparation
        sig_title = Tex("Sigmoid:", font_size=28)
        sig_eq = MathTex(r"\sigma(z) = \frac{1}{1+e^{-z}}", font_size=32)
        sig_group = VGroup(sig_title, sig_eq).arrange(DOWN, aligned_edge=LEFT)
        sig_group.next_to(activation_formula, RIGHT, buff=1.0).shift(UP*1.2)
        sig_arrow = Arrow(activation_formula.get_right(), sig_group.get_left(), buff=0.2, stroke_width=2, max_tip_length_to_length_ratio=0.1, color=YELLOW)

        # ReLU preparation
        relu_title = Tex("ReLU (Rectified Linear Unit):", font_size=28)
        relu_eq = MathTex(r"\sigma(z) = \max(0, z)", font_size=32)
        relu_group = VGroup(relu_title, relu_eq).arrange(DOWN, aligned_edge=LEFT)
        relu_group.next_to(activation_formula, RIGHT, buff=1.0).shift(DOWN*0.5)
        relu_arrow = Arrow(activation_formula.get_right(), relu_group.get_left(), buff=0.2, stroke_width=2, max_tip_length_to_length_ratio=0.1, color=YELLOW)

        # Merged animation: GrowArrow for instant tip and LaggedStart for simultaneous appearance
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(sig_arrow), FadeIn(sig_group)),
                AnimationGroup(GrowArrow(relu_arrow), FadeIn(relu_group)),
                lag_ratio=0.2
            ),
            run_time=3.5
        )

        self.wait(3.0)
