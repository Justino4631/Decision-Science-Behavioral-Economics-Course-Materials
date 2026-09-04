#NOTE: Run `pip install tk` before running so you have the package

import tkinter as tk
from tkinter import messagebox, ttk
import game

fmt = lambda amt: f"{'-' if amt < 0 else ''}${abs(amt):,}"

class EnhancedStartupUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Startup Simulator")
        self.root.geometry("980x640")
        self.root.minsize(800, 550)
        self.root.configure(bg="#0b132b")
        self.is_fs, self.ins_var = False, tk.BooleanVar(value=False)

        self.root.bind("<F11>", lambda e: self._fs())
        self.root.bind("<Escape>", lambda e: self._fs(False))

        self._style()
        self._build()
        self._load()

    def _style(self):
        s = ttk.Style()
        s.theme_use("clam")
        s.configure("TFrame", background="#0b132b")
        s.configure("Card.TFrame", background="#1c2541")
        s.configure("H.TLabel", background="#0b132b", foreground="#6fffe9", font=("Segoe UI", 16, "bold"))
        s.configure("C.TLabel", background="#0b132b", foreground="#4ade80", font=("Segoe UI", 16, "bold"))
        s.configure("T.TLabel", background="#1c2541", foreground="#ffffff", font=("Segoe UI", 13, "bold"))
        s.configure("P.TLabel", background="#1c2541", foreground="#e2e8f0", font=("Segoe UI", 10))
        s.configure("Opt.TButton", font=("Segoe UI", 10, "bold"), background="#3a506b", foreground="#ffffff", padding=10)
        s.map("Opt.TButton", background=[("active", "#5bc0be")], foreground=[("active", "#0b132b")])
        s.configure("Chk.TCheckbutton", background="#0b132b", foreground="#ffffff", font=("Segoe UI", 10))

    def _build(self):
        m = ttk.Frame(self.root, padding=15)
        m.pack(fill=tk.BOTH, expand=True)

        top = ttk.Frame(m)
        top.pack(fill=tk.X)
        self.lbl_q = ttk.Label(top, text="", style="H.TLabel")
        self.lbl_q.pack(side=tk.LEFT)
        self.lbl_c = ttk.Label(top, text="", style="C.TLabel")
        self.lbl_c.pack(side=tk.RIGHT)

        self.pbar = ttk.Progressbar(m, maximum=game.TOTAL_QUARTERS)
        self.pbar.pack(fill=tk.X, pady=5)

        ttk.Checkbutton(m, text="Maintain Insurance ($2,000/qtr)", variable=self.ins_var, style="Chk.TCheckbutton",
                        command=lambda: setattr(game, 'HAS_INSURANCE', self.ins_var.get())).pack(anchor=tk.W)

        grid = ttk.Frame(m)
        grid.pack(fill=tk.BOTH, expand=True, pady=5)

        card = ttk.Frame(grid, style="Card.TFrame", padding=15)
        card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        self.lbl_title = ttk.Label(card, text="", style="T.TLabel")
        self.lbl_title.pack(anchor=tk.W)
        self.lbl_prompt = ttk.Label(card, text="", style="P.TLabel", wraplength=450, justify=tk.LEFT)
        self.lbl_prompt.pack(anchor=tk.W, fill=tk.X, pady=10)

        self.btn_box = ttk.Frame(card, style="Card.TFrame")
        self.btn_box.pack(fill=tk.BOTH, expand=True)

        ledger = ttk.Frame(grid, style="Card.TFrame", padding=10)
        ledger.pack(side=tk.RIGHT, fill=tk.BOTH)
        ttk.Label(ledger, text="Ledger", style="T.TLabel").pack(anchor=tk.W)
        self.ledger_list = tk.Listbox(ledger, bg="#0b132b", fg="#6fffe9", font=("Consolas", 9), bd=0, width=30)
        self.ledger_list.pack(fill=tk.BOTH, expand=True)

        self.banner = tk.Frame(m, bg="#1c2541", height=40)
        self.banner.pack(fill=tk.X, pady=(10, 0))
        self.lbl_res = tk.Label(self.banner, text="Make your choice.", font=("Segoe UI", 10, "bold"), bg="#1c2541", fg="#6fffe9", anchor="w")
        self.lbl_res.pack(fill=tk.BOTH, expand=True)

    def _fs(self, state=None):
        self.is_fs = state if state is not None else not self.is_fs
        self.root.attributes("-fullscreen", self.is_fs)

    def _load(self):
        self.lbl_q.config(text=f"Q{game.CURRENT_QUARTER}/{game.TOTAL_QUARTERS}")
        self.lbl_c.config(text=fmt(game.CURRENT_FUNDING))
        self.pbar["value"] = game.CURRENT_QUARTER - 1

        self.event = game.get_current_event()
        self.lbl_title.config(text=self.event["title"])
        self.lbl_prompt.config(text=self.event["prompt"])

        for w in self.btn_box.winfo_children(): w.destroy()
        for i, opt in enumerate(self.event["options"]):
            ttk.Button(self.btn_box, text=opt, style="Opt.TButton", command=lambda idx=i: self._choose(idx)).pack(fill=tk.X, pady=4)

    def _choose(self, idx):
        delta, log = self.event["action"](idx)
        bg = "#064e3b" if delta > 0 else "#7f1d1d" if delta < 0 else "#1e293b"
        fg = "#4ade80" if delta > 0 else "#f87171" if delta < 0 else "#38bdf8"

        self.banner.config(bg=bg)
        self.lbl_res.config(bg=bg, fg=fg, text=f"Result: {log}")
        self.ledger_list.insert(0, f"Q{game.CURRENT_QUARTER:02d}: {fmt(delta)} -> {fmt(game.CURRENT_FUNDING)}")
        self.lbl_c.config(text=fmt(game.CURRENT_FUNDING))

        if game.is_bankrupt() or game.CURRENT_QUARTER >= game.TOTAL_QUARTERS:
            self._end()
        else:
            game.CURRENT_QUARTER += 1
            self._load()

    def _end(self):
        self.pbar["value"] = game.CURRENT_QUARTER
        for w in self.btn_box.winfo_children(): w.destroy()
        fail = game.is_bankrupt()
        title = "Failed" if fail else "Complete!"
        msg = f"Final Capital: {fmt(game.CURRENT_FUNDING)}"
        
        self.lbl_title.config(text=title)
        self.lbl_prompt.config(text=msg)
        ttk.Button(self.btn_box, text="Restart", style="Opt.TButton", command=self._reset).pack(fill=tk.X, pady=10)
        messagebox.showinfo(title, msg)

    def _reset(self):
        game.reset_game()
        self.ins_var.set(False)
        self.ledger_list.delete(0, tk.END)
        self.banner.config(bg="#1c2541")
        self.lbl_res.config(bg="#1c2541", fg="#6fffe9", text="Make your choice.")
        self._load()

if __name__ == "__main__":
    root = tk.Tk()
    EnhancedStartupUI(root)
    root.mainloop()