# 2048 AI – Expectimax Agent

## Overview

This project implements the game **2048** along with an **AI agent based on the Expectimax search algorithm**.
The AI evaluates possible moves using a heuristic evaluation function and accounts for the stochastic nature of the game (random tile spawning).

The project was developed as part of a board game AI assignment.

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
│   └── cli.py             # Command line interface to play the game
│
├── experiments/
│   └── benchmark.py       # Script to evaluate AI performance
│
├── README.md
└── .gitignore
```

---

# Requirements

* Python **3.9+**
* No external libraries required (standard library only)

---

# Running the Game

Navigate to the project root directory and run:

```
python -m ui.cli
```

This will start the command line version of the game.

You can choose to:

* play **manually**, or
* let the **AI play automatically**.

---

# Running the AI Benchmark

To test the AI performance across multiple games:

```
python -m experiments.benchmark
```

Optional parameters may include:

* number of games
* search depth
* number of chance samples

Example:

```
python -m experiments.benchmark --games 20 --depth 4 --samples 8
```

This will output statistics such as:

* average score
* maximum tile reached
* runtime per game
