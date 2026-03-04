# ui/gui.py
import random
import tkinter as tk
from tkinter import ttk

from game.engine import (
    initial_state,
    apply_action,
    spawn_random_tile,
    get_legal_actions,
    is_terminal,
    max_tile,
)
from game.rules import P_TWO, KEY_TO_ACTION


TILE_FONT = ("Helvetica", 18, "bold")
INFO_FONT = ("Helvetica", 12)


def _tile_text(v: int) -> str:
    return "" if v == 0 else str(v)


class Game2048GUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("2048 AI")

        # --- Model state ---
        self.rng = random.Random(0)
        self.state = initial_state(self.rng)

        self.mode = tk.StringVar(value="human")  # "human" or "ai"
        self.ai_running = False
        self.ai_delay_ms = 120  # adjust for faster/slower AI

        # Lazy import AI to keep GUI responsive at import time
        self._ai = None

        # --- Layout ---
        self._build_ui()
        self._bind_keys()

        self._render()

    def _build_ui(self):
        outer = ttk.Frame(self.root, padding=12)
        outer.grid(row=0, column=0, sticky="nsew")

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        outer.columnconfigure(0, weight=1)

        # Top info row
        info = ttk.Frame(outer)
        info.grid(row=0, column=0, sticky="ew")
        info.columnconfigure(3, weight=1)

        self.score_var = tk.StringVar()
        self.max_var = tk.StringVar()
        self.status_var = tk.StringVar()

        ttk.Label(info, text="Score:", font=INFO_FONT).grid(row=0, column=0, sticky="w")
        ttk.Label(info, textvariable=self.score_var, font=INFO_FONT).grid(row=0, column=1, sticky="w", padx=(6, 18))

        ttk.Label(info, text="Max tile:", font=INFO_FONT).grid(row=0, column=2, sticky="w")
        ttk.Label(info, textvariable=self.max_var, font=INFO_FONT).grid(row=0, column=3, sticky="w", padx=(6, 18))

        ttk.Label(info, textvariable=self.status_var, font=INFO_FONT).grid(row=0, column=4, sticky="e")

        # Board frame
        board_frame = ttk.Frame(outer, padding=(0, 12, 0, 12))
        board_frame.grid(row=1, column=0, sticky="nsew")
        board_frame.columnconfigure(tuple(range(4)), weight=1)
        board_frame.rowconfigure(tuple(range(4)), weight=1)

        self.tiles = []
        for r in range(4):
            row = []
            for c in range(4):
                lbl = tk.Label(
                    board_frame,
                    text="",
                    font=TILE_FONT,
                    width=5,
                    height=2,
                    relief="ridge",
                    borderwidth=2,
                    anchor="center",
                )
                lbl.grid(row=r, column=c, padx=4, pady=4, sticky="nsew")
                row.append(lbl)
            self.tiles.append(row)

        # Controls
        controls = ttk.Frame(outer)
        controls.grid(row=2, column=0, sticky="ew")
        controls.columnconfigure(6, weight=1)

        ttk.Label(controls, text="Mode:", font=INFO_FONT).grid(row=0, column=0, sticky="w")

        ttk.Radiobutton(controls, text="Human", value="human", variable=self.mode, command=self._on_mode_change)\
            .grid(row=0, column=1, sticky="w", padx=(6, 14))
        ttk.Radiobutton(controls, text="AI (Expectimax)", value="ai", variable=self.mode, command=self._on_mode_change)\
            .grid(row=0, column=2, sticky="w", padx=(6, 14))

        self.ai_btn = ttk.Button(controls, text="Start AI", command=self._toggle_ai)
        self.ai_btn.grid(row=0, column=3, padx=6)

        ttk.Button(controls, text="Reset", command=self._reset).grid(row=0, column=4, padx=6)
        ttk.Button(controls, text="Quit", command=self.root.destroy).grid(row=0, column=5, padx=6)

        hint = "Keys: Arrow keys or WASD. (In AI mode: Start/Stop)"
        ttk.Label(outer, text=hint, font=("Helvetica", 10)).grid(row=3, column=0, sticky="w")

    def _bind_keys(self):
        # Arrow keys
        self.root.bind("<Up>", lambda e: self._try_move("U"))
        self.root.bind("<Down>", lambda e: self._try_move("D"))
        self.root.bind("<Left>", lambda e: self._try_move("L"))
        self.root.bind("<Right>", lambda e: self._try_move("R"))

        # WASD
        self.root.bind("w", lambda e: self._try_move(KEY_TO_ACTION["W"]))
        self.root.bind("a", lambda e: self._try_move(KEY_TO_ACTION["A"]))
        self.root.bind("s", lambda e: self._try_move(KEY_TO_ACTION["S"]))
        self.root.bind("d", lambda e: self._try_move(KEY_TO_ACTION["D"]))

    def _on_mode_change(self):
        # Stop AI if switching away
        if self.mode.get() != "ai":
            self.ai_running = False
            self.ai_btn.configure(text="Start AI")
        self._render()

    def _ensure_ai(self):
        if self._ai is None:
            from ai.expectimax import ExpectimaxAI
            self._ai = ExpectimaxAI(depth=4, chance_samples=8, seed=0, p_two=P_TWO)

    def _toggle_ai(self):
        if self.mode.get() != "ai":
            self.mode.set("ai")
            self._on_mode_change()

        if self.ai_running:
            self.ai_running = False
            self.ai_btn.configure(text="Start AI")
        else:
            self._ensure_ai()
            self.ai_running = True
            self.ai_btn.configure(text="Stop AI")
            self._ai_step()

    def _reset(self):
        self.ai_running = False
        self.ai_btn.configure(text="Start AI")
        self.rng = random.Random(0)
        self.state = initial_state(self.rng)
        self._render()

    def _try_move(self, action: str):
        # In AI mode, ignore manual moves unless AI is stopped
        if self.mode.get() == "ai" and self.ai_running:
            return

        if is_terminal(self.state):
            self._render()
            return

        legal = get_legal_actions(self.state)
        if action not in legal:
            self.status_var.set("Illegal move")
            return

        self.state = apply_action(self.state, action)
        self.state = spawn_random_tile(self.state, self.rng, p_two=P_TWO)
        self._render()

    def _ai_step(self):
        if not self.ai_running:
            return

        if is_terminal(self.state):
            self.ai_running = False
            self.ai_btn.configure(text="Start AI")
            self._render()
            return

        action = self._ai.choose_action(self.state)
        if action not in get_legal_actions(self.state):
            self.status_var.set("AI chose illegal move (stopping).")
            self.ai_running = False
            self.ai_btn.configure(text="Start AI")
            self._render()
            return

        self.state = apply_action(self.state, action)
        self.state = spawn_random_tile(self.state, self.rng, p_two=P_TWO)
        self._render()

        self.root.after(self.ai_delay_ms, self._ai_step)

    def _render(self):
        self.score_var.set(str(self.state.score))
        self.max_var.set(str(max_tile(self.state)))

        if is_terminal(self.state):
            self.status_var.set("Game Over")
        else:
            self.status_var.set("")

        # Update board
        for r in range(4):
            for c in range(4):
                v = self.state.board[r][c]
                self.tiles[r][c].configure(text=_tile_text(v))


def main():
    root = tk.Tk()
    # Optional: nicer scaling on HiDPI
    try:
        root.tk.call("tk", "scaling", 1.2)
    except tk.TclError:
        pass
    Game2048GUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()