# Tic-Tac-Toe AI

This repository contains an implementation of the Tic-Tac-Toe game with various AI agents to play against. The project includes the following components:

- A `utils.py` file where all the utility functions for the game are defined.
- An `agent.py` file containing the implementation of different player strategies, including:
  - Random Player
  - Greedy Player
  - Min-Max Player
  - Human Player
- A `main.py` file where the game can be played with any of the agents.

## Table of Contents

- [Project Structure](#project-structure)
- [Installation](#installation)
- [How to Play](#how-to-play)
  - [Agents](#agents)
  - [Game Execution](#game-execution)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

├── agent.py Contains all player classes (Random, Greedy, Min-Max, Human)   
├── utils.py  Utility functions (e.g., checking win conditions, board printing)   
├── main.py  The entry point to run the game   
├── README.md  Project description and usage instructions   
└── requirements.txt  Dependencies.   


## Installation

To set up and run the Tic-Tac-Toe AI locally, follow these steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/HarolReyes0/Tik-Tak-Toe-AI.git
    cd tic-tac-toe-ai
    ```

2. Create and activate a virtual environment:

    ```bash
    python -m venv env
    source env/bin/activate   # On Windows use `env\Scripts\activate`
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## How to Play

### Agents

This game supports four types of players, implemented in `agent.py`:

1. **Random Player**: Randomly selects available moves.
2. **Greedy Player**: Chooses the best immediate move without looking ahead.
3. **Min-Max Player**: Uses the Min-Max algorithm to find the optimal strategy.
4. **Human Player**: Allows you to manually input your moves.

### Game Execution

To start the game, run the `main.py` file:

```bash
python main.py
```
![Demo](https://github.com/user-attachments/assets/c9c2516b-8963-4048-9a93-8d4ab2fd6625)

