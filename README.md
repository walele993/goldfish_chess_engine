# Goldfish Chess Engine

**Work in Progress**

Goldfish Chess Engine is a chess engine implemented in Python, designed to adhere to the standard rules of chess, including special moves such as castling and pawn promotion. The project is actively being developed with the goal of creating a fully functional chess engine capable of playing against users and evaluating game positions.

## Features

- **Complete Chess Gameplay:** Implements full chess rules, including special moves like castling and pawn promotion.
- **Basic Artificial Intelligence:** Aiming to include gameplay against a human player with AI capabilities. Currently in progress.
- **Board Visualization:** Displays the chessboard in text format after each move.

## Project Structure

The project is divided into the following modules:

- **board.py:** Contains the `Chess` class managing the board configuration, initial position loading, and move execution interface.
- **pieces.py:** Defines classes for each chess piece type (Pawn, Knight, Bishop, Rook, Queen, King).
- **rules.py:** Includes game rules such as move validity, check control, checkmate, and stalemate.
- **main.py:** Entry point handling user interface and game loop.

## Details of Functionality

### board.py

#### Chess Class

The `Chess` class is the core of the game engine. Here are its main functionalities:

- `__init__()`: Loads the initial board configuration and initializes players.
- `move_piece()`: Handles the movement of a piece on the board and verifies the validity of the move.
- `is_check()`: Checks if a player's king is in check.
- `is_checkmate()`: Determines if a player's king is in checkmate, ending the game if so.
- `is_stalemate()`: Checks if the game is in stalemate, ending the game if so.

### pieces.py

This module defines classes for each type of chess piece (Pawn, Knight, Bishop, Rook, Queen, King). Here's the primary role of each piece class:

- **Base Piece class**: Defines basic attributes of a piece such as color and valid movement positions.
- Each piece class (e.g., Pawn, Knight, Bishop, etc.): Implements the `movement()` method that returns a list of all valid moves for that piece at a given position on the board.

### rules.py

#### Rule Functions

This module contains functions implementing specific chess rules:

- `is_valid_move()`: Checks if a given move is valid for the specified piece type, considering general movement rules.
- `is_check()`: Determines if a king is in check after a given move.
- `is_checkmate()`: Checks if a king is in checkmate, ending the game if so.
- `is_stalemate()`: Checks if the game is in stalemate, ending the game if so.

### main.py

This module manages the user interface and game loop:

- `play_game()`: Starts and manages a game between two human players. Handles move input and controls the game loop until checkmate or stalemate occurs.

## Requirements

- Python 3.x
- No additional packages are required beyond standard Python.

## Installation

- Clone the repository:
git clone https://github.com/your-username/goldfish-chess.git cd goldfish-chess
- Run the game:
python main.py

## Future Goals

- **Single-Player AI:** Development of an AI to play against users. The AI's initial implementation is underway, with plans to enhance its strategy and decision-making.
- **Move Evaluation:** Future updates will include functionality to evaluate game positions to further improve the AI.

### Feedback and Contributions

If you have any questions, comments, or suggestions, feel free to contact me. Contributions, pull requests, and forks are welcome on GitHub.

## Credits

This project was created by Gabriele Meucci.
