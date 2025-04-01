# ♟️ Goldfish Chess Engine

🚀 **Work in Progress**

Goldfish Chess Engine is a chess engine implemented in Python, designed to follow standard chess rules, including special moves such as **castling** and **pawn promotion**. The project is actively being developed with the goal of creating a fully functional chess engine capable of playing against users and evaluating board positions.

---

## ✨ Features

- 🏰 **Complete Chess Gameplay** – Implements full chess rules, including castling, en passant, and promotion.
- 🤖 **Basic AI (Coming Soon!)** – Future updates will introduce a basic AI opponent.
- 📊 **Board Visualization** – Displays the chessboard in text format after every move.
- 🎯 **Game State Detection** – Supports check, checkmate, and stalemate detection.

---

## 📁 Project Structure

The project is divided into several key modules:

- **`board.py`** – Manages board configuration, move execution, and game state.
- **`pieces.py`** – Defines classes for each chess piece (**Pawn, Knight, Bishop, Rook, Queen, King**).
- **`rules.py`** – Implements move validation, check detection, checkmate, and stalemate conditions.
- **`main.py`** – Handles user interaction and game loop execution.

---

## 🧩 Core Functionalities

### 🏆 `board.py`

#### Chess Class

The `Chess` class serves as the core of the engine, responsible for:

- 🏗️ **Initializing the Board** – Loads the starting position and manages piece placement.
- 🎯 **Move Execution** – Handles player moves, verifying their validity.
- ⚠️ **Game State Checks** – Detects **check, checkmate, and stalemate** conditions.

### 🏇 `pieces.py`

Defines chess piece classes, each implementing a `movement()` method to determine valid moves based on board position.

### 📜 `rules.py`

Implements chess rules through various functions:

- ✅ `is_valid_move()` – Verifies if a move is legal.
- 👑 `is_check()` – Checks if a king is in check.
- 🏁 `is_checkmate()` – Determines checkmate scenarios.
- 🤝 `is_stalemate()` – Identifies stalemate conditions.

### 🎮 `main.py`

Manages the game loop and user interaction:

- 🎤 **Player Input Handling** – Reads and processes player moves.
- 🎯 **Move Validation** – Ensures moves are legal before execution.
- 🎭 **Board Display** – Outputs the chessboard state after each move.

---

## ⚙️ Installation and Usage

### 🔧 Requirements

- 🐍 **Python 3.x** (No external dependencies required)

### 📥 Installation Steps

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/goldfish-chess.git
   cd goldfish-chess
   ```
2. Run the game:
   ```sh
   python main.py
   ```

---

## 🚀 Future Enhancements

Planned updates include:

- 🤖 **AI Opponent** – Develop an AI capable of strategic decision-making.
- 📊 **Move Evaluation** – Implement position analysis to improve AI performance.
- 🎨 **Graphical Interface** – Add a visual board representation for an improved user experience.
- 🏆 **PGN Support** – Enable import/export of games in **Portable Game Notation** format.

---

## 📬 Feedback and Contributions

If you have any **questions, comments, or suggestions**, feel free to reach out! Contributions, pull requests, and forks are **welcome** on GitHub. 

---

## 👨‍💻 Credits

This project was created by **Gabriele Meucci**. 🏁
