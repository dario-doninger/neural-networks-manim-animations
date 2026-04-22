"""
01_neural_network_intro.py

This script contains the first two animations of the repository:
1. NeuralNetworkIntro: Shows the architecture and the forward pass of the network.
2. SingleNeuronFunction: Zooms into a specific neuron to explain weights, biases, 
   and activation functions (Sigmoid and ReLU).
"""

from manim import *

class NeuralNetworkIntro(Scene):
    """
    Visualizes the general skeleton of a Neural Network, 
    the input vectors, and the flow of information through the layers.
    """
    def construct(self):
        # ==========================================
        # 1. INTRO: CHAPTER 1 (1.0s)
        # ==========================================
        title_text = VGroup(
            Text("Chapter 1:", font_size=50),
            Text("Neural Networks", font_size=70)
        ).arrange(DOWN, buff=0.5)
        
        # Flash the title on screen
        self.add(title_text) 
        self.wait(1.0)
        self.remove(title_text) 

        # ==========================================
        # 2. SKELETON: NEURONS & DOTS (9.0s)
        # ==========================================
        # Define the number of neurons per layer
        layers_config = [3, 4, 4, 1]
        nodes = VGroup()
        ellipsis_dots = VGroup()
        
        # Build the nodes for each layer
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup()
            for j in range(num_nodes):
                neuron = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
                # Calculate geometric positioning for symmetry
                neuron.move_to(RIGHT * (i * 2.5 - 3.75) + DOWN * (j * 0.9 - (num_nodes-1)*0.45))
                layer.add(neuron)
            
            # Add vertical ellipsis dots under hidden/intermediate neurons
            if num_nodes > 1:
                dots = MathTex(r"\vdots", font_size=30).next_to(layer, DOWN, buff=0.2)
                ellipsis_dots.add(dots)
            
            nodes.add(layer)

        # Slow fade-in animation for the network skeleton
        self.play(FadeIn(nodes, lag_ratio=0.4), FadeIn(ellipsis_dots), run_time=6.0)
        self.wait(3.0)

        # ==========================================
        # 3. CONNECTIONS (4.0s)
        # ==========================================
        layer_connections = VGroup()
        
        # Connect each neuron of layer 'i' to every neuron of layer 'i+1'
        for i in range(len(layers_config) - 1):
            current_layer_links = VGroup()
            for n1 in nodes[i]:
                for n2 in nodes[i+1]:
                    connection_line = Line(
                        n1.get_center(), n2.get_center(), 
                        stroke_width=1, stroke_opacity=0.2, color=WHITE
                    )
                    connection_line.z_index = -1 # Send lines behind the neurons
                    current_layer_links.add(connection_line)
            layer_connections.add(current_layer_links)

        self.play(Create(layer_connections), run_time=4.0)

        # ==========================================
        # 4. INPUT VECTOR (5.0s)
        # ==========================================
        # Create x1, x2, x3 labels inside the input layer
        input_labels = VGroup(*[MathTex(f"x_{j+1}", font_size=24).move_to(nodes[0][j]) for j in range(3)])
        
        # Mathematical representation of the input vector
        input_vector = MathTex(r"x = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}", font_size=35)
        input_vector.next_to(nodes[0], DOWN, buff=1.2)

        self.play(Write(input_labels), run_time=1.5)
        self.play(TransformFromCopy(input_labels, input_vector), run_time=2.5)
        self.wait(1.0)

        # ==========================================
        # 5. INFORMATION FLOW & OUTPUT 8 (4.0s)
        # ==========================================
        # Highlight connections layer by layer to simulate data flow
        for i in range(len(layer_connections)):
            self.play(
                layer_connections[i].animate.set_stroke(color=YELLOW, opacity=1, width=2),
                run_time=1.0,
                rate_func=linear
            )
        
        # Illuminate the final output neuron and display the result
        output_node = nodes[-1][0]
        output_value = Text("8", font_size=24, color=WHITE).move_to(output_node)
        
        self.play(
            output_node.animate.set_fill(YELLOW, opacity=1).scale(1.2),
            Write(output_value),
            run_time=1.0
        )

        # ==========================================
        # 6. FREEZE (2.0s)
        # ==========================================
        self.wait(2.0)


class SingleNeuronFunction(Scene):
    """
    Zooms into a specific node of the Neural Network to break down 
    the mathematical operations (Weights, Bias, Summation, Activation).
    """
    def construct(self):
        # ==========================================
        # 0. INITIAL SETUP (Rebuilding the network state)
        # ==========================================
        layers_config = [3, 4, 4, 1]
        nodes = VGroup()
        ellipsis_dots = VGroup()
        
        for i, num_nodes in enumerate(layers_config):
            layer = VGroup()
            for j in range(num_nodes):
                neuron = Circle(radius=0.2, color=BLUE, fill_opacity=0.8)
                neuron.move_to(RIGHT * (i * 2.5 - 3.75) + DOWN * (j * 0.9 - (num_nodes-1)*0.45))
                layer.add(neuron)
            
            if num_nodes > 1:
                dots = MathTex(r"\vdots", font_size=30).next_to(layer, DOWN, buff=0.2)
                ellipsis_dots.add(dots)
            nodes.add(layer)

        layer_connections = VGroup()
        for i in range(len(layers_config) - 1):
            current_layer_links = VGroup()
            for n1 in nodes[i]:
                for n2 in nodes[i+1]:
                    connection_line = Line(
                        n1.get_center(), n2.get_center(), 
                        stroke_width=2, stroke_opacity=1, color=YELLOW
                    )
                    connection_line.z_index = -1
                    current_layer_links.add(connection_line)
            layer_connections.add(current_layer_links)

        # Re-create vectors and labels from the previous scene
        input_labels = VGroup(*[MathTex(f"x_{j+1}", font_size=24).move_to(nodes[0][j]) for j in range(3)])
        previous_input_vector = MathTex(r"\mathbf{x} = \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix}", font_size=35).next_to(nodes[0], DOWN, buff=1.2)
        
        output_node = nodes[-1][0]
        output_node.set_fill(YELLOW, opacity=1).scale(1.2)
        previous_output_value = Text("8", font_size=24, color=WHITE).move_to(output_node)

        entire_network = VGroup(layer_connections, nodes, ellipsis_dots)
        self.add(entire_network, input_labels, previous_input_vector, previous_output_value)

        # ==========================================
        # 1. RETURN TO NORMAL & REMOVE VECTORS (1.0s)
        # ==========================================
        # Fade out labels and specific elements before the camera zoom
        self.play(
            output_node.animate.set_fill(BLUE, opacity=0.8).scale(1/1.2),
            FadeOut(previous_output_value),
            FadeOut(previous_input_vector),
            FadeOut(input_labels),
            *[l.animate.set_stroke(color=WHITE, opacity=0.2, width=1) for links in layer_connections for l in links],
            run_time=1.0
        )

        # ==========================================
        # 2. SELECTION ZOOM & SMOOTH TRANSFORM (2.0s)
        # ==========================================
        # Select the 3rd neuron from the top in the 2nd layer
        target_neuron = nodes[1][2] 
        
        # Filter incoming and outgoing connections for the selected neuron
        incoming_lines = VGroup(*[l for l in layer_connections[0] if np.linalg.norm(l.get_end() - target_neuron.get_center()) < 0.1])
        outgoing_lines = VGroup(*[l for l in layer_connections[1] if np.linalg.norm(l.get_start() - target_neuron.get_center()) < 0.1])
        
        # Group everything else to fade it out
        background_elements = VGroup(ellipsis_dots)
        for i, layer in enumerate(nodes):
            for j, n in enumerate(layer):
                if not (i == 1 and j == 2):
                    background_elements.add(n)
                    
        for i, links in enumerate(layer_connections):
            for l in links:
                if l not in incoming_lines and l not in outgoing_lines:
                    background_elements.add(l)

        # Calculate shift to center the target neuron
        shift_vector = ORIGIN - target_neuron.get_center()

        self.play(
            FadeOut(background_elements),
            entire_network.animate.shift(shift_vector).scale(1.8, about_point=ORIGIN),
            run_time=2.0
        )

        # ==========================================
        # 3. WEIGHTS & PERCENTAGES (6.0s)
        # ==========================================
        weights_group = VGroup()
        percentages_group = VGroup()
        percentage_strings = [r"=30\%", r"=50\%", r"=20\%"]
        
        for k, line in enumerate(incoming_lines):
            # Place text at the midpoint of the branches, slightly shifted left
            weight_tex = MathTex(f"w_{k+1}", font_size=36).move_to(line.point_from_proportion(0.5) + UP*0.35)
            perc_tex = MathTex(percentage_strings[k], font_size=32).next_to(weight_tex, RIGHT, buff=0.1)
            
            weights_group.add(weight_tex)
            percentages_group.add(perc_tex)
            entire_network.add(weight_tex) # Bind to the network so it scales later

        self.play(FadeIn(weights_group), run_time=1.0)
        self.wait(0.5)
        self.play(Write(percentages_group), run_time=1.0)
        self.wait(2.0)
        self.play(FadeOut(percentages_group), run_time=1.5)

        # ==========================================
        # 4. BIAS AND SCALAR FORMULA (2.5s)
        # ==========================================
        bias_tex = MathTex("b", font_size=40).next_to(target_neuron, UP, buff=0.5)
        entire_network.add(bias_tex)
        self.play(FadeIn(bias_tex), run_time=1.0)

        # Display the summation formula below the neuron
        sum_formula = MathTex(r"z = \sum_{i=1}^3 w_i x_i + b", font_size=45).next_to(target_neuron, DOWN, buff=0.8)
        entire_network.add(sum_formula)
        
        self.play(ReplacementTransform(VGroup(weights_group, bias_tex), sum_formula), run_time=1.5)

        # ==========================================
        # 5. REVEAL & DE-ZOOM WITH VERTICAL DROP (1.5s)
        # ==========================================
        # Temporarily remove elements from the VGroup to prevent visual artifacts
        entire_network.remove(sum_formula)
        entire_network.remove(bias_tex)
        for w in weights_group:
            entire_network.remove(w)

        # Step 1: Reveal the rest of the network while still zoomed (0.5s)
        self.play(FadeIn(background_elements), run_time=0.5)

        # Step 2: Perfect De-zoom. The formula aligns vertically at x = -1.25
        vector_formula = MathTex(r"\mathbf{z} = \mathbf{w} \cdot \mathbf{x} + b", font_size=36)
        vector_formula.move_to(np.array([-1.25, -2.8, 0]))

        self.play(
            entire_network.animate.scale(1/1.8, about_point=ORIGIN).shift(-shift_vector),
            ReplacementTransform(sum_formula, vector_formula),
            run_time=1.0
        )

        # ==========================================
        # 6. ISOLATE Z & ACTIVATION FUNCTION (3.0s)
        # ==========================================
        z_only_formula = MathTex(r"\mathbf{z}", font_size=36).move_to(vector_formula.get_left() + RIGHT * 0.2)
        self.play(ReplacementTransform(vector_formula, z_only_formula), run_time=1.0)

        # Show the general activation formula under the third layer
        activation_formula = MathTex(r"\mathbf{a} = \sigma(\mathbf{z})", font_size=36)
        activation_formula.move_to(np.array([nodes[2].get_x(), -2.8, 0]))
        
        self.play(ReplacementTransform(z_only_formula, activation_formula), run_time=2.0)

        # ==========================================
        # 7. SIGMOID AND ReLU REVEAL (3.5s)
        # ==========================================
        # Setup Sigmoid visuals (Top Right)
        sig_title = Tex("Sigmoid:", font_size=28)
        sig_eq = MathTex(r"\sigma(z) = \frac{1}{1+e^{-z}}", font_size=32)
        sigmoid_group = VGroup(sig_title, sig_eq).arrange(DOWN, aligned_edge=LEFT)
        sigmoid_group.next_to(activation_formula, RIGHT, buff=1.0).shift(UP*1.2)
        sigmoid_arrow = Arrow(activation_formula.get_right(), sigmoid_group.get_left(), buff=0.2, stroke_width=2, max_tip_length_to_length_ratio=0.1, color=YELLOW)

        # Setup ReLU visuals (Bottom Right)
        relu_title = Tex("ReLU (Rectified Linear Unit):", font_size=28)
        relu_eq = MathTex(r"\sigma(z) = \max(0, z)", font_size=32)
        relu_group = VGroup(relu_title, relu_eq).arrange(DOWN, aligned_edge=LEFT)
        relu_group.next_to(activation_formula, RIGHT, buff=1.0).shift(DOWN*0.5)
        relu_arrow = Arrow(activation_formula.get_right(), relu_group.get_left(), buff=0.2, stroke_width=2, max_tip_length_to_length_ratio=0.1, color=YELLOW)

        # Synchronized animation: instant arrows followed by fading formulas
        self.play(
            LaggedStart(
                AnimationGroup(GrowArrow(sigmoid_arrow), FadeIn(sigmoid_group)),
                AnimationGroup(GrowArrow(relu_arrow), FadeIn(relu_group)),
                lag_ratio=0.2
            ),
            run_time=3.5
        )

        self.wait(3.0)
