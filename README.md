# Overview

This project is a simple Pong game developed using the Python Arcade library. The goal of the project was to deepen my understanding of 2D game development, event handling, collision detection, and real-time game loop logic. As a software engineer, this helped me practice structuring a game with multiple interactive elements, managing user inputs, and implementing responsive gameplay mechanics.

The game is a classic two-player Pong match. Each player controls a paddle on one side of the screen (W/S for the left player and UP/DOWN arrows for the right player). The objective is to prevent the ball from passing your paddle and try to score against your opponent. The game features scoring, sound effects, randomized ball direction, and customizable number of rounds. The winner is declared once a player reaches the chosen number of points.

This project was a way for me to challenge myself with interactive, event-driven programming, and to learn how to design a small but complete arcade-style game from scratch.

[Software Demo Video](http://youtu.be/5kDdeWU80X4)

# Development Environment

- **IDE**: VS Code  
- **Python Version**: 3.11  
- **Libraries**:  
  - [`arcade`](https://api.arcade.academy/en/latest/) (for rendering sprites, handling collisions, and managing game window)
  - `random` (for ball direction randomness)
  - `os` (for managing sound file paths)

# Useful Websites

* [Arcade Library Documentation](https://api.arcade.academy/en/latest/)
* [Python Official Documentation](https://docs.python.org/3/)

# Future Work

* Add a main menu screen with start and settings options  
* Implement single-player mode with simple AI  
* Animate the paddles and ball for smoother visual effects  
* Display countdown before the ball starts moving after each point  
* Add background music and sound toggle option  
* Improve collision physics to vary bounce angles based on paddle hit location
