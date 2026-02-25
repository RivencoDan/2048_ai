from __future__ import annotations

import argparse
import random
import statistics
from collections import Counter

from game.engine import initial_state, apply_action, spawn_random_tile, is_terminal, max_tile
from game.rules import P_TWO
from ai.expectimax import ExpectimaxAI


def run_one_game(ai: ExpectimaxAI, seed: int) -> tuple[int, int]:
    rng = random.Random(seed)
    state = initial_state(rng)

    while not is_terminal(state):
        a = ai.choose_action(state)
        state = apply_action(state, a)
        state = spawn_random_tile(state, rng, p_two=P_TWO)

    return state.score, max_tile(state)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--games", type=int, default=50)
    parser.add_argument("--depth", type=int, default=4)
    parser.add_argument("--samples", type=int, default=8)
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    ai = ExpectimaxAI(depth=args.depth, chance_samples=args.samples, seed=args.seed, p_two=P_TWO)

    scores = []
    tiles = []

    for i in range(args.games):
        score, tile = run_one_game(ai, seed=args.seed + i)
        scores.append(score)
        tiles.append(tile)

    dist = Counter(tiles)

    print("\n=== Benchmark Results ===")
    print(f"Games: {args.games}, depth={args.depth}, chance_samples={args.samples}")
    print(f"Mean score: {statistics.mean(scores):.1f}")
    if len(scores) > 1:
        print(f"Std score:  {statistics.pstdev(scores):.1f}")
    print(f"Best score: {max(scores)}")
    print(f"Mean max tile: {statistics.mean(tiles):.1f}")
    print(f"Best max tile: {max(tiles)}")

    print("\nMax tile distribution:")
    for t in sorted(dist.keys()):
        print(f"  {t}: {dist[t]} ({dist[t]/args.games:.0%})")


if __name__ == "__main__":
    main()