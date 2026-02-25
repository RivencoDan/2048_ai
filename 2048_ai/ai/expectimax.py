from __future__ import annotations

import random
from typing import Optional, List, Tuple

from game.engine import (
    GameState,
    apply_action,
    get_legal_actions,
    is_terminal,
    BOARD_SIZE,
)
from game.rules import P_TWO
from ai.eval import evaluate


class ExpectimaxAI:
    def __init__(
        self,
        depth: int = 4,
        chance_samples: int = 8,
        seed: Optional[int] = None,
        p_two: float = P_TWO,
    ):
        self.depth = depth
        self.chance_samples = chance_samples
        self.rng = random.Random(seed)
        self.p_two = p_two

    def choose_action(self, state: GameState) -> str:
        actions = get_legal_actions(state)
        if not actions:
            return "U"

        best_a = actions[0]
        best_v = float("-inf")

        for a in actions:
            after = apply_action(state, a)
            v = self._chance_value(after, self.depth - 1)
            if v > best_v:
                best_v = v
                best_a = a

        return best_a

    def _max_value(self, state: GameState, depth: int) -> float:
        if depth <= 0 or is_terminal(state):
            return evaluate(state)

        actions = get_legal_actions(state)
        if not actions:
            return evaluate(state)

        best = float("-inf")
        for a in actions:
            after = apply_action(state, a)
            best = max(best, self._chance_value(after, depth - 1))
        return best

    def _chance_value(self, state_after_move: GameState, depth: int) -> float:
        board = state_after_move.board
        empties = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if board[r][c] == 0]

        if not empties:
            return self._max_value(state_after_move, depth)

        # Sample K random outcomes to approximate expectation
        k = min(self.chance_samples, len(empties) * 2)
        total = 0.0

        for _ in range(k):
            r, c = self.rng.choice(empties)
            val = 2 if self.rng.random() < self.p_two else 4
            nxt = _place_tile(state_after_move, r, c, val)
            total += self._max_value(nxt, depth)

        return total / k


def _place_tile(state: GameState, r: int, c: int, val: int) -> GameState:
    board_list = [list(row) for row in state.board]
    board_list[r][c] = val
    new_board = tuple(tuple(row) for row in board_list)
    return GameState(new_board, state.score)