# 2048 AI – Expectimax Agent

## Overview

This project implements the game **2048** along with an **AI agent based on the Expectimax search algorithm**.
The AI evaluates possible moves using a heuristic evaluation function and accounts for the stochastic nature of the game (random tile spawning).

The game can be played either through a **command line interface (CLI)** or through a **graphical window (GUI)**.

---

# Project Structure

```
2048_ai/
│
├── ai/
│   ├── expectimax.py      # Expectimax AI implementation
│   └── eval.py            # Heuristic evaluation function
│
├── game/
│   ├── engine.py          # Game state representation and transitions
│   └── rules.py           # Game rules and legal move logic
│
├── ui/
│   ├── cli.py             # Command line interface
│   └── gui.py             # Graphical user interface
│
├── experiments/
│   └── benchmark.py       # Script to evaluate AI performance
│
├── README.md
└── .gitignore
```

---

# Requirements

* Python **3.9 or newer**
* No external libraries required (uses Python standard library only)

---

# Running the Game (GUI Window)

To launch the **graphical version of the game**, run:

```
python -m ui.gui
```

This will open a **window where the game can be played visually**.

Features of the GUI:

* Displays the **2048 board in a window**
* Shows **current score and maximum tile**
* Supports **keyboard controls**
* Can run the **AI automatically**

Controls:

* **Arrow keys or WASD** → move tiles
* **Start AI / Stop AI** → toggle the Expectimax AI player
* **Reset** → restart the game
* **Quit** → close the window

---

# Running the Game (Command Line)

To run the **text-based version** of the game:

```
python -m ui.cli
```

Controls:

```
W or ↑  : Move Up
A or ←  : Move Left
S or ↓  : Move Down
D or →  : Move Right
Q       : Quit
```

---

# Running the AI Benchmark

To evaluate the AI performance across multiple games:

```
python -m experiments.benchmark
```

Example with parameters:

```
python -m experiments.benchmark --games 20 --depth 4 --samples 8
```

This outputs statistics such as:

* Average score
* Maximum tile reached
* Runtime per game

---


