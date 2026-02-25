# engine.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple
import random

Action = str  # "U", "D", "L", "R"
BOARD_SIZE = 4


@dataclass(frozen=True)
class GameState:
    board: Tuple[Tuple[int, ...], ...]
    score: int = 0

    def __post_init__(self):
        if len(self.board) != BOARD_SIZE:
            raise ValueError("Board must be 4 rows.")
        for row in self.board:
            if len(row) != BOARD_SIZE:
                raise ValueError("Each row must have 4 columns.")
            for v in row:
                if v != 0 and (v & (v - 1)) != 0:
                    raise ValueError(f"Tile value must be 0 or a power of 2, got {v}.")


def initial_state(rng: Optional[random.Random] = None) -> GameState:
    rng = rng or random.Random()
    empty_board = tuple(tuple(0 for _ in range(BOARD_SIZE)) for _ in range(BOARD_SIZE))
    s = GameState(empty_board, 0)
    s = spawn_random_tile(s, rng=rng)
    s = spawn_random_tile(s, rng=rng)
    return s


def is_terminal(state: GameState) -> bool:
    return len(get_legal_actions(state)) == 0


def get_legal_actions(state: GameState) -> List[Action]:
    actions: List[Action] = []
    for a in ("U", "D", "L", "R"):
        moved = apply_action(state, a)
        if moved.board != state.board:
            actions.append(a)
    return actions


def apply_action(state: GameState, action: Action) -> GameState:
    if action not in ("U", "D", "L", "R"):
        raise ValueError(f"Invalid action {action}. Use one of U, D, L, R.")

    board = state.board
    score_gain = 0

    if action in ("L", "R"):
        new_rows = []
        for r in range(BOARD_SIZE):
            row = list(board[r])
            if action == "R":
                row.reverse()
            merged, gained = _slide_and_merge_line(row)
            score_gain += gained
            if action == "R":
                merged.reverse()
            new_rows.append(tuple(merged))
        new_board = tuple(new_rows)

    else:  
        cols = []
        for c in range(BOARD_SIZE):
            col = [board[r][c] for r in range(BOARD_SIZE)]
            if action == "D":
                col.reverse()
            merged, gained = _slide_and_merge_line(col)
            score_gain += gained
            if action == "D":
                merged.reverse()
            cols.append(merged)

        new_board_list = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        for c in range(BOARD_SIZE):
            for r in range(BOARD_SIZE):
                new_board_list[r][c] = cols[c][r]
        new_board = tuple(tuple(row) for row in new_board_list)

    return GameState(new_board, state.score + score_gain)


def spawn_random_tile(
    state: GameState,
    rng: Optional[random.Random] = None,
    p_two: float = 0.9,
) -> GameState:
    rng = rng or random.Random()
    empties = _empty_cells(state.board)
    if not empties:
        return state

    (r, c) = rng.choice(empties)
    value = 2 if rng.random() < p_two else 4

    board_list = [list(row) for row in state.board]
    board_list[r][c] = value
    new_board = tuple(tuple(row) for row in board_list)
    return GameState(new_board, state.score)


def max_tile(state: GameState) -> int:
    return max(max(row) for row in state.board)

# Internal helpers
def _empty_cells(board: Tuple[Tuple[int, ...], ...]) -> List[Tuple[int, int]]:
    empties: List[Tuple[int, int]] = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == 0:
                empties.append((r, c))
    return empties


def _slide_and_merge_line(line: Sequence[int]) -> Tuple[List[int], int]:
    tiles = [x for x in line if x != 0]

    merged: List[int] = []
    score_gain = 0
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            new_val = tiles[i] * 2
            merged.append(new_val)
            score_gain += new_val
            i += 2
        else:
            merged.append(tiles[i])
            i += 1

    while len(merged) < BOARD_SIZE:
        merged.append(0)

    return merged, score_gain