from __future__ import annotations

import math
from typing import Tuple
from game.engine import GameState, BOARD_SIZE


def evaluate(state: GameState) -> float:
    """
    Heuristic evaluation for 2048 board states.
    Higher is better.
    """
    b = state.board

    empty = sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if b[r][c] == 0)
    max_tile = max(max(row) for row in b)

    smooth = smoothness(b)          # typically negative (penalty)
    mono = monotonicity(b)          # typically negative-ish (penalty); closer to 0 is better
    corner = max_in_corner(b)       # 0 or 1

    # Weighted sum (simple + strong)
    val = 0.0
    val += 2.7 * empty
    val += 1.0 * (math.log2(max_tile) if max_tile > 0 else 0.0)
    val += 1.0 * mono
    val += 0.1 * smooth
    val += 1.0 * corner

    # small tie-breaker toward real score
    val += 0.0005 * state.score
    return float(val)


def _log2_or_zero(x: int) -> float:
    return math.log2(x) if x > 0 else 0.0


def smoothness(board: Tuple[Tuple[int, ...], ...]) -> float:
    penalty = 0.0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            v = board[r][c]
            if v == 0:
                continue
            lv = _log2_or_zero(v)

            if c + 1 < BOARD_SIZE and board[r][c + 1] != 0:
                penalty -= abs(lv - _log2_or_zero(board[r][c + 1]))
            if r + 1 < BOARD_SIZE and board[r + 1][c] != 0:
                penalty -= abs(lv - _log2_or_zero(board[r + 1][c]))

    return penalty


def monotonicity(board: Tuple[Tuple[int, ...], ...]) -> float:
    totals = [0.0, 0.0, 0.0, 0.0]  # left, right, up, down

    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE - 1):
            a = _log2_or_zero(board[r][c])
            b = _log2_or_zero(board[r][c + 1])
            if a > b:
                totals[0] += a - b
            else:
                totals[1] += b - a

    for c in range(BOARD_SIZE):
        for r in range(BOARD_SIZE - 1):
            a = _log2_or_zero(board[r][c])
            b = _log2_or_zero(board[r + 1][c])
            if a > b:
                totals[2] += a - b
            else:
                totals[3] += b - a

    # prefer a single direction per axis (avoid “zig-zag”)
    return -min(totals[0], totals[1]) - min(totals[2], totals[3])


def max_in_corner(board: Tuple[Tuple[int, ...], ...]) -> float:
    max_tile = max(max(row) for row in board)
    corners = (
        board[0][0],
        board[0][BOARD_SIZE - 1],
        board[BOARD_SIZE - 1][0],
        board[BOARD_SIZE - 1][BOARD_SIZE - 1],
    )
    return 1.0 if max_tile in corners else 0.0