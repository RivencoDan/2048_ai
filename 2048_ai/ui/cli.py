import random
from typing import Optional

from game.engine import (
    GameState,
    initial_state,
    apply_action,
    spawn_random_tile,
    get_legal_actions,
    is_terminal,
    max_tile,
)
from game.rules import KEY_TO_ACTION, P_TWO


def print_board(state: GameState) -> None:
    print("\nScore:", state.score)
    print("-" * 25)
    for row in state.board:
        print("|", end="")
        for val in row:
            print(f"{('.' if val == 0 else val):>5}", end="")
        print(" |")
    print("-" * 25)
    print("Max tile:", max_tile(state))


def human_play() -> None:
    rng = random.Random()
    state = initial_state(rng)

    print("\n=== 2048 - Human Mode ===")
    print("Use W/A/S/D to move. Q to quit.\n")

    while True:
        print_board(state)

        if is_terminal(state):
            print("\nGame Over!")
            break

        key = input("Move (W/A/S/D or Q): ").strip().upper()
        if key == "Q":
            print("Quitting game.")
            break

        action = KEY_TO_ACTION.get(key)
        if action is None:
            print("Invalid key. Use W/A/S/D.")
            continue

        if action not in get_legal_actions(state):
            print("Illegal move.")
            continue

        state = apply_action(state, action)
        state = spawn_random_tile(state, rng, p_two=P_TWO)

    print("\nFinal Score:", state.score)
    print("Final Max Tile:", max_tile(state))


def ai_play(ai_func, seed: Optional[int] = None) -> None:
    rng = random.Random(seed)
    state = initial_state(rng)

    print("\n=== 2048 - AI Mode ===\n")

    while not is_terminal(state):
        print_board(state)

        action = ai_func(state)
        if action not in get_legal_actions(state):
            print("AI selected illegal move. Ending.")
            break

        state = apply_action(state, action)
        state = spawn_random_tile(state, rng, p_two=P_TWO)

    print_board(state)
    print("\nGame Over!")
    print("Final Score:", state.score)
    print("Final Max Tile:", max_tile(state))


def main():
    print("2048")
    print("1 - Human play")
    print("2 - AI play (Expectimax)")
    choice = input("Select mode: ").strip()

    if choice == "1":
        human_play()
    elif choice == "2":
        from ai.expectimax import ExpectimaxAI

        ai = ExpectimaxAI(depth=4, chance_samples=8, seed=0, p_two=P_TWO)
        ai_play(ai.choose_action, seed=0)
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()