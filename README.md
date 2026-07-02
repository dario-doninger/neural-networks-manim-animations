# Animations on the Mathematics behind Deep Learning

This repository contains a collection of animations built with the python library "**Manim**". These visualizations were originally developed as part of my **Final Graduation Project** for the Bachelor’s Degree in **Mathematical Engineering** at **Politecnico di Milano**, culminated in a video essay about Mathematics in Artificial Intelligence, where I explored **Deep Learning** and **Physics-Informed Neural Networks** in depth from a mathematical perspective.

## Academic Context
* **Institution:** Politecnico di Milano
* **Degree:** B.Sc. in Mathematical Engineering
* **Purpose:** Final Project for the Bachelor's Degree
* **Topics Covered in the video:** Neural Networks theory (**Backpropagation**, **Gradient Descent**, **ADAM Algorithm**, **Universal Approximation Theorem**) and an introduction to **Physics-Informed Neural Networks (PINNs)** from a mathematical perspective.

## Repository Overview
The goal of this collection is purely **educational and outreach-oriented**, I have decided to open-source these scripts to help people create similar visualizations for their own academic or dissemination purposes. It aims to bridge the gap between complex mathematical abstractions and intuitive understanding. This repository focuses only on the best animations of the video about traditional **Neural Networks**.

## Methodology & Tools
The animations were crafted using the **Manim** library in Python, originally created by Grant Sanderson (@3blue1brown on YouTube).
In line with modern development workflows, the coding process followed a **"Vibe Coding"** strategy. I used a Large Language Model (LLM) as a helper to accelerate the drafting of the Python scripts and to handle geometric formatting. However **I was entirely responsible** for the mathematical logic, the pedagogical design, the source study, and the overall video composition.

## Video Showcase
You can see these animations in action in my full video on YouTube: 
https://youtu.be/G8nD9NkgMPA?si=lFgu_zpejn_TMqal

## Repository Structure
Animations included in this repository, along with their corresponding timestamps in the YouTube video:
* **[01_neural_network_intro.py](./animations/01_neural_network_intro.py)** *(Video: 00:30 - 01:15)*
  * **Description:** The initial Neural Network animation, showcasing the architecture and the basic mathematical flow of data.
* **[02_gradient_descent.py](./animations/02_gradient_descent.py)** *(Video: 01:36 - 02:07)*
  * **Description:** A visual representation of the Gradient Descent algorithm.
* **[03_ill_conditioned_canyon.py](./animations/03_ill_conditioned_canyon.py)** *(Video: 03:49 - 03:55)*
  * **Description:** Visualization of an ill-conditioned optimization case, illustrating the "zigzagging" problem of standard Gradient Descent.
* **[04_adam_optimizer.py](./animations/04_adam_optimizer.py)** *(Video: 03:57 - 04:02)*
  * **Description:** Resolution of the ill-conditioned canyon problem using the Adam Optimizer, showing its momentum-based smooth trajectory.
* **[05_parabola_interpolation.py](./animations/05_parabola_interpolation.py)** *(Video: 04:10 - 04:17)*
  * **Description:** Interpolation of a parabola.

## How to Use
1. **Install Manim:**
   ```bash
   pip install manim
2. **Clone this repository**
3. **Render a scene in draft quality (faster testing, 480p 15fps):**
   ```bash
      manim -pql name_of_file.py SceneName
4. **Render a scene in production quality (high resolution, 1080p 60fps):**
   ```bash
      manim -pqh name_of_file.py SceneName
