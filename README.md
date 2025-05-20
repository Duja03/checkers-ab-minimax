# Checkers using Minimax with Alpha-Beta Pruning, and Iterative Deepening

This is a Python implementation of the classic Checkers game with an AI opponent powered by the Minimax algorithm, optimized using Alpha-Beta (𝛼−𝛽) pruning and Iterative Deepening search to determine the best possible move within a limited time frame.

## Features

- Two game modes available: 
  - **Player vs Player** – play locally with a friend
  - **Player vs Computer** – challenge the AI with varying difficulty

## How It Works

- **Minimax** evaluates all possible moves up to a certain depth to choose the best one.
- **Alpha-Beta Pruning** skips unnecessary branches, improving performance without affecting accuracy.
- **Iterative Deepening** starts with shallow searches and deepens gradually, allowing the AI to return the best move found within a time limit.

![Main menu]("screenshots/main menu.png")

![Initial state]("screenshots/initial state.png")

![Eating a Piece]("screenshots/jumping.png")

![Queen jumping]("screenshots/queen jumping.png")
