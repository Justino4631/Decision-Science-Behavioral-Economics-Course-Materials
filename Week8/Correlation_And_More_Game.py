import numpy as np
import random
import scipy.stats as stats
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ============================================================
# THEME - one place to control every color/font so the whole
# app reads as one consistent, smooth UI.
# ============================================================

THEME = {
    "bg":          "#1b2430",   # app background
    "panel":       "#232f3e",   # side panel background
    "card":        "#2c3b4d",   # interaction card background
    "plot_bg":     "#232f3e",   # matplotlib figure/axes background
    "grid":        "#3a4b5f",
    "text":        "#eef2f7",
    "text_muted":  "#8ea0b5",
    "accent":      "#3fa9f5",   # primary accent (blue)
    "good":        "#2ecc71",   # correct / success
    "bad":         "#ff5a5f",   # incorrect / error
    "warn":        "#f5c451",   # highlight / mode label
    "point":       "#3fa9f5",
    "point_dim":   "#5c7185",
    "line":        "#ff9f43",
    "font":        "Segoe UI",
}

# ============================================================
# MULTIPLE-CHOICE QUESTION BANK
# Curated around: correlation, linear regression, outliers,
# expected value, and basic probability / spread.
# ============================================================

BASE_MCQS = [
    # --- Correlation & Regression ---
    {"q": "When you convert a scatterplot's variables to z-scores, what point does the regression line always pass through?",
     "options": ["The minimum", "The maximum", "The mean (0, 0)", "The median"],
     "answer": "The mean (0, 0)"},
    {"q": "A residual plot shows a clear curved (U-shaped) pattern. What does this tell you?",
     "options": ["The linear model fits very well", "A non-linear model would fit better",
                 "The correlation is exactly 0", "Nothing — residual shape never matters"],
     "answer": "A non-linear model would fit better"},
    {"q": "If r = -0.80, what percent of the variation in y is explained by the regression line on x?",
     "options": ["-80%", "80%", "64%", "36%"],
     "answer": "64%"},
    {"q": "Which of these is most sensitive to a single influential outlier?",
     "options": ["The correlation coefficient (r)", "The regression slope",
                 "The regression intercept", "All of the above"],
     "answer": "All of the above"},
    {"q": "If you swap which variable is x and which is y in a scatterplot, what stays exactly the same?",
     "options": ["The slope", "The intercept", "The correlation coefficient (r)", "The residuals"],
     "answer": "The correlation coefficient (r)"},
    {"q": "What does 'homoscedasticity' mean for a linear regression's residuals?",
     "options": ["They must all be positive", "Their spread stays roughly constant across x",
                 "They must sum to a positive number", "They must be normally shaped outliers"],
     "answer": "Their spread stays roughly constant across x"},
    {"q": "An r-value of 0.0 tells you that:",
     "options": ["There's no relationship of any kind", "There's no LINEAR relationship",
                 "The data must be perfectly random", "The sample size is too small"],
     "answer": "There's no LINEAR relationship"},
    {"q": "If the least-squares slope of a line is positive, what must be true of r?",
     "options": ["r is negative", "r is positive", "r is exactly 0", "r is exactly 1"],
     "answer": "r is positive"},
    {"q": "What does r² = 0.95 actually mean?",
     "options": ["95% of points sit exactly on the line", "95% of the variation in y is explained by x",
                 "r must be negative", "The slope is 0.95"],
     "answer": "95% of the variation in y is explained by x"},
    {"q": "'Least squares' regression finds the line that minimizes:",
     "options": ["The sum of the residuals", "The sum of the SQUARED residuals",
                 "The correlation coefficient", "The slope"],
     "answer": "The sum of the SQUARED residuals"},
    {"q": "A strong correlation between x and y tells you that:",
     "options": ["x definitely causes y", "y definitely causes x",
                 "changes in x tend to go with changes in y", "a lurking variable is impossible"],
     "answer": "changes in x tend to go with changes in y"},
    {"q": "A residual plot fans out into a funnel shape as x increases. This violates:",
     "options": ["Linearity", "Constant variance (homoscedasticity)", "Independence", "Normality of x"],
     "answer": "Constant variance (homoscedasticity)"},
    {"q": "On a scatterplot, an outlier in the y-direction that pulls the regression line toward it is called:",
     "options": ["A random point", "An influential point", "The mean", "A residual"],
     "answer": "An influential point"},
    {"q": "If every point in a scatterplot lies exactly on a line with positive slope, r equals:",
     "options": ["0", "0.5", "1", "It depends on the slope's value"],
     "answer": "1"},

    # --- Expected value & basic probability ---
    {"q": "The expected value of a fair six-sided die roll is:",
     "options": ["3", "3.5", "4", "6"],
     "answer": "3.5"},
    {"q": "If a game pays $10 with probability 0.2 and $0 otherwise, the expected payout is:",
     "options": ["$0", "$2", "$5", "$10"],
     "answer": "$2"},
    {"q": "Expected value is best described as:",
     "options": ["The most likely single outcome", "The long-run average outcome over many repeats",
                 "The largest possible outcome", "The middle value of all outcomes"],
     "answer": "The long-run average outcome over many repeats"},
    {"q": "The probability of flipping a fair coin 5 times and getting heads every time is:",
     "options": ["1/5", "1/10", "1/32", "1/64"],
     "answer": "1/32"},
    {"q": "The probability of rolling a sum of 7 with two fair six-sided dice is:",
     "options": ["1/6", "1/12", "1/36", "5/36"],
     "answer": "1/6"},
    {"q": "If events A and B are independent, P(A and B) equals:",
     "options": ["P(A) + P(B)", "P(A) x P(B)", "P(A) - P(B)", "P(A) / P(B)"],
     "answer": "P(A) x P(B)"},
    {"q": "If A and B cannot happen at the same time (mutually exclusive), P(A and B) equals:",
     "options": ["0", "0.5", "1", "P(A) x P(B)"],
     "answer": "0"},
    {"q": "The total area under any probability density curve always equals:",
     "options": ["0.5", "1", "The mean", "It depends on the shape"],
     "answer": "1"},
    {"q": "In a right-skewed distribution, which relationship generally holds?",
     "options": ["mean < median", "mean > median", "mean = median", "mode > mean"],
     "answer": "mean > median"},

    # --- Spread, sampling, testing (kept simple) ---
    {"q": "Standard deviation is defined as:",
     "options": ["The average of the data", "The square root of the variance",
                 "The range divided by 2", "The most common value"],
     "answer": "The square root of the variance"},
    {"q": "As sample size n increases, the width of a confidence interval tends to:",
     "options": ["Get wider", "Get narrower", "Stay exactly the same", "Become negative"],
     "answer": "Get narrower"},
    {"q": "A p-value tells you the probability of:",
     "options": ["The null hypothesis being true", "Results at least this extreme, assuming the null is true",
                 "The alternative hypothesis being true", "Making a Type I error for sure"],
     "answer": "Results at least this extreme, assuming the null is true"},
    {"q": "Rejecting a true null hypothesis is called a:",
     "options": ["Type I error", "Type II error", "Sampling error", "Residual error"],
     "answer": "Type I error"},
    {"q": "Failing to reject a false null hypothesis is called a:",
     "options": ["Type I error", "Type II error", "Sampling error", "Residual error"],
     "answer": "Type II error"},
    {"q": "The critical z-score for a two-tailed 95% confidence interval is approximately:",
     "options": ["1.28", "1.645", "1.96", "2.58"],
     "answer": "1.96"},
]


def generate_procedural_questions():
    """Extra auto-generated questions, kept in the same simple spirit as BASE_MCQS."""
    q = []

    # Empirical rule (68-95-99.7), phrased simply
    for k, pct in [(1, "68%"), (2, "95%"), (3, "99.7%")]:
        q.append({
            "q": f"For a normal distribution, about what percent of values fall within {k} standard deviation(s) of the mean?",
            "options": ["50%", pct if pct != "68%" else "68%", "99.9%", "34%"] if pct == "68%"
                       else ["68%", pct, "99.9%", "34%"],
            "answer": pct
        })

    # Dice sums
    combos = {2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 5, 9: 4, 10: 3, 11: 2}
    for target in [4, 5, 6, 8, 9, 10]:
        correct = f"{combos[target]}/36"
        decoys = {"1/6", "1/12", "5/36", "1/36", "4/36", "3/36", "2/36"}
        decoys.discard(correct)
        opts = [correct] + random.sample(list(decoys), 3)
        random.shuffle(opts)
        q.append({
            "q": f"What is the probability of rolling a sum of {target} with two fair six-sided dice?",
            "options": opts,
            "answer": correct
        })

    # Standard error scaling with sample size
    for multiplier, reduction in [(4, "Cut in half"), (9, "Cut to a third"),
                                   (16, "Cut to a quarter"), (25, "Cut to a fifth")]:
        q.append({
            "q": f"If sample size increases by a factor of {multiplier}, the standard error of the mean is:",
            "options": [reduction, "Doubled", "Unchanged", "Multiplied by the same factor"],
            "answer": reduction
        })

    # IQR outlier fence
    for q1, q3 in [(10, 20), (20, 40), (5, 15)]:
        iqr = q3 - q1
        fence = q3 + 1.5 * iqr
        q.append({
            "q": f"Given Q1 = {q1} and Q3 = {q3}, any value above what threshold counts as an outlier (1.5xIQR rule)?",
            "options": [str(fence), str(q3 + iqr), str(q3 + 3 * iqr), "There is no upper limit"],
            "answer": str(fence)
        })

    # Sample vs population notation
    for param, sample_sym, pop_sym in [
        ("mean", "x-bar", "mu (\u03bc)"),
        ("standard deviation", "s", "sigma (\u03c3)"),
        ("proportion", "p-hat", "p"),
    ]:
        q.append({
            "q": f"Which symbol represents the SAMPLE {param}?",
            "options": [sample_sym, pop_sym, "alpha", "beta"],
            "answer": sample_sym
        })
        q.append({
            "q": f"Which symbol represents the POPULATION {param}?",
            "options": [pop_sym, sample_sym, "theta", "rho"],
            "answer": pop_sym
        })

    # Complement rule
    for p_event in [0.15, 0.25, 0.40, 0.72]:
        comp = f"{1 - p_event:.2f}"
        q.append({
            "q": f"If P(event A) = {p_event:.2f}, what is P(NOT A)?",
            "options": [comp, f"{p_event:.2f}", "0.00", "1.00"],
            "answer": comp
        })

    # Binomial expected value
    for n, p in [(100, 0.20), (50, 0.10), (200, 0.05), (80, 0.25)]:
        ev = str(round(n * p))
        q.append({
            "q": f"Out of {n} independent trials with a {int(p*100)}% success chance each, the EXPECTED number of successes is:",
            "options": [ev, str(round(n * p * 1.5)), str(round(n * p * 0.5)), "1"],
            "answer": ev
        })

    return q


ALL_MCQS = BASE_MCQS + generate_procedural_questions()

MODE_WEIGHTS = ["GTC", "GTC", "REGRESSION", "REGRESSION", "MATCH", "OUTLIER", "OUTLIER", "MCQ", "MCQ"]


# ============================================================
# DATA GENERATORS
# ============================================================

def generate_gtc_data(r, num_pts=140):
    cov = [[1, r], [r, 1]]
    data = np.random.multivariate_normal([0, 0], cov, num_pts)
    return data[:, 0], data[:, 1]


def generate_regression_data():
    slope = round(random.uniform(-3.0, 3.0), 1)
    if abs(slope) < 0.4:
        slope = 1.2
    intercept = round(random.uniform(-5.0, 5.0), 1)

    x = np.linspace(-5, 5, 50)
    y = slope * x + intercept + np.random.normal(0, 1.5, len(x))
    slope_fit, intercept_fit, *_ = stats.linregress(x, y)

    correct_eq = f"y = {slope_fit:.2f}x + {intercept_fit:.2f}"
    decoys = {
        f"y = {-slope_fit:.2f}x + {intercept_fit:.2f}",
        f"y = {slope_fit:.2f}x + {-intercept_fit:.2f}",
        f"y = {random.uniform(-4, 4):.2f}x + {random.uniform(-10, 10):.2f}",
    }
    decoys.discard(correct_eq)
    while len(decoys) < 3:
        decoys.add(f"y = {random.uniform(-4, 4):.2f}x + {random.uniform(-10, 10):.2f}")

    options = [correct_eq] + list(decoys)[:3]
    random.shuffle(options)
    return x, y, slope_fit, intercept_fit, correct_eq, options


def generate_outlier_data():
    """One clean linear cloud plus a single severe outlier. Returns full arrays + its index."""
    slope = random.choice([-1.6, 1.6])
    x = np.linspace(-4, 4, 34)
    y = slope * x + np.random.normal(0, 0.45, len(x))

    outlier_idx = random.randint(6, len(x) - 6)
    y[outlier_idx] += random.choice([-5.5, 5.5])

    return x, y, outlier_idx


def generate_match_round():
    """
    Builds 4 mini scatterplots. A single regression line (fit to the TRUE
    dataset) is drawn on all four panels. Only one dataset's cloud actually
    hugs that line - the other three are decoys the line clearly does not fit.
    Returns: list of (x, y) for 4 panels, correct panel index, the line's (slope, intercept).
    """
    slope = round(random.uniform(-2.2, 2.2), 2)
    if abs(slope) < 0.5:
        slope = 1.1
    intercept = round(random.uniform(-2.5, 2.5), 1)

    x = np.linspace(-5, 5, 45)
    y_true = slope * x + intercept + np.random.normal(0, 0.8, len(x))
    slope_fit, intercept_fit, *_ = stats.linregress(x, y_true)

    datasets = [(x, y_true)]

    # Decoy 1: much noisier cloud, same rough slope -> line drawn but doesn't hug it
    y_noisy = slope * x + intercept + np.random.normal(0, 4.5, len(x))
    datasets.append((x, y_noisy))

    # Decoy 2: opposite/very different slope
    other_slope = -slope if abs(slope) > 0.8 else slope + random.choice([-2.5, 2.5])
    y_wrong_slope = other_slope * x + intercept + np.random.normal(0, 0.8, len(x))
    datasets.append((x, y_wrong_slope))

    # Decoy 3: shifted intercept, offset well away from the drawn line
    y_shifted = slope * x + intercept + random.choice([-6, 6]) + np.random.normal(0, 0.8, len(x))
    datasets.append((x, y_shifted))

    order = [0, 1, 2, 3]
    random.shuffle(order)
    shuffled = [datasets[i] for i in order]
    correct_idx = order.index(0)

    return shuffled, correct_idx, slope_fit, intercept_fit


# ============================================================
# MAIN APPLICATION
# ============================================================

class StatsGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("StatQuest \u2014 Regression & Correlation Edition")
        self.root.geometry("1080x680")
        self.root.configure(bg=THEME["bg"])
        self.root.minsize(920, 600)

        self.score = 0
        self.rounds_played = 0
        self.correct_answer = None
        self.current_mode = None
        self.current_cid = None  # matplotlib event connection id, tracked so we can disconnect

        self._build_styles()
        self._build_layout()
        self.next_question()

    # ---------- styling ----------
    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                         font=(THEME["font"], 11, "bold"),
                         padding=(14, 10),
                         background=THEME["card"],
                         foreground=THEME["text"],
                         borderwidth=0,
                         focuscolor=THEME["card"])
        style.map("TButton",
                   background=[("active", THEME["accent"]), ("disabled", "#26313f")],
                   foreground=[("disabled", THEME["text_muted"])])

        style.configure("Next.TButton",
                         font=(THEME["font"], 12, "bold"),
                         padding=(14, 12),
                         background=THEME["accent"],
                         foreground="#0b1017")
        style.map("Next.TButton",
                   background=[("active", "#63bdf7"), ("disabled", "#26313f")],
                   foreground=[("disabled", THEME["text_muted"])])

        style.configure("Horizontal.TScale", background=THEME["card"], troughcolor="#3a4b5f")

    # ---------- layout ----------
    def _build_layout(self):
        # Header
        header = tk.Frame(self.root, bg=THEME["bg"], pady=14)
        header.pack(side=tk.TOP, fill=tk.X)

        self.score_label = tk.Label(header, text="Score: 0 / 0  (0%)",
                                     font=(THEME["font"], 16, "bold"),
                                     bg=THEME["bg"], fg=THEME["good"])
        self.score_label.pack(side=tk.LEFT, padx=24)

        self.mode_label = tk.Label(header, text="Preparing...",
                                    font=(THEME["font"], 15, "bold"),
                                    bg=THEME["bg"], fg=THEME["warn"])
        self.mode_label.pack(side=tk.RIGHT, padx=24)

        # Body split
        body = tk.Frame(self.root, bg=THEME["bg"])
        body.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 18))

        # Left: plot card
        plot_card = tk.Frame(body, bg=THEME["plot_bg"], highlightthickness=1,
                              highlightbackground="#3a4b5f")
        plot_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 16))

        self.fig = plt.Figure(figsize=(5.8, 4.8), facecolor=THEME["plot_bg"])
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_card)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Right: control panel card
        panel = tk.Frame(body, bg=THEME["panel"], width=380)
        panel.pack(side=tk.RIGHT, fill=tk.BOTH)
        panel.pack_propagate(False)

        self.q_text = tk.Label(panel, text="Starting up...", wraplength=330, justify=tk.LEFT,
                                font=(THEME["font"], 13, "bold"),
                                bg=THEME["panel"], fg=THEME["text"], anchor="w")
        self.q_text.pack(fill=tk.X, padx=18, pady=(20, 6))

        self.hint_label = tk.Label(panel, text="", wraplength=330, justify=tk.LEFT,
                                    font=(THEME["font"], 10), bg=THEME["panel"],
                                    fg=THEME["text_muted"], anchor="w")
        self.hint_label.pack(fill=tk.X, padx=18, pady=(0, 10))

        self.interaction_frame = tk.Frame(panel, bg=THEME["panel"])
        self.interaction_frame.pack(fill=tk.BOTH, expand=True, padx=18)

        bottom = tk.Frame(panel, bg=THEME["panel"])
        bottom.pack(side=tk.BOTTOM, fill=tk.X, padx=18, pady=18)

        self.feedback_label = tk.Label(bottom, text="", font=(THEME["font"], 12, "bold"),
                                        bg=THEME["panel"], fg=THEME["good"], wraplength=330,
                                        justify=tk.LEFT)
        self.feedback_label.pack(pady=(0, 10), anchor="w")

        self.btn_next = ttk.Button(bottom, text="Next Question \u2192", style="Next.TButton",
                                    command=self.next_question)
        self.btn_next.pack(fill=tk.X)
        self.btn_next.state(["disabled"])

    # ---------- shared helpers ----------
    def _style_axes(self, ax, title=""):
        ax.set_facecolor(THEME["plot_bg"])
        ax.grid(True, linestyle="--", alpha=0.25, color=THEME["grid"])
        ax.tick_params(colors=THEME["text_muted"], labelsize=8)
        for spine in ax.spines.values():
            spine.set_color(THEME["grid"])
        if title:
            ax.set_title(title, color=THEME["text"], fontsize=11, fontweight="bold", pad=8)

    def _disconnect_events(self):
        if self.current_cid is not None:
            try:
                self.canvas.mpl_disconnect(self.current_cid)
            except Exception:
                pass
            self.current_cid = None

    def _reset_round(self):
        for widget in self.interaction_frame.winfo_children():
            widget.destroy()
        self.feedback_label.config(text="")
        self.hint_label.config(text="")
        self._disconnect_events()
        self.fig.clear()
        self.fig.patch.set_facecolor(THEME["plot_bg"])
        self.canvas.draw()
        self.btn_next.state(["disabled"])

    def _finish_round(self, correct, message):
        pct_color = THEME["good"] if correct else THEME["bad"]
        self.feedback_label.config(text=message, fg=pct_color)
        if correct:
            self.score += 1
        self._update_score_label()
        self._disconnect_events()
        self.btn_next.state(["!disabled"])

    def _update_score_label(self):
        pct = int(round(100 * self.score / self.rounds_played)) if self.rounds_played else 0
        self.score_label.config(text=f"Score: {self.score} / {self.rounds_played}  ({pct}%)")

    def _disable_children(self, container):
        for w in container.winfo_children():
            if isinstance(w, ttk.Button):
                w.state(["disabled"])

    # ---------- round driver ----------
    def next_question(self):
        self._reset_round()
        self.rounds_played += 1
        self.current_mode = random.choice(MODE_WEIGHTS)

        dispatch = {
            "GTC": self.setup_gtc_question,
            "REGRESSION": self.setup_regression_question,
            "MATCH": self.setup_match_question,
            "OUTLIER": self.setup_outlier_question,
            "MCQ": self.setup_mcq_question,
        }
        dispatch[self.current_mode]()
        self._update_score_label()

    # ---------- MODE: Guess the Correlation ----------
    def setup_gtc_question(self):
        self.mode_label.config(text="Guess the Correlation")
        self.q_text.config(text="Estimate the correlation coefficient (r) shown in this scatterplot.")
        self.hint_label.config(text="Drag the slider, then submit. Within 0.08 of the true value counts as correct.")

        true_r = round(random.uniform(-0.95, 0.95), 2)
        self.correct_answer = true_r
        x, y = generate_gtc_data(true_r)

        ax = self.fig.add_subplot(111)
        self._style_axes(ax, "Correlation Scatterplot")
        ax.scatter(x, y, color=THEME["point"], alpha=0.75, edgecolors="none", s=32)
        self.canvas.draw()

        tk.Label(self.interaction_frame, text="Your guess:", bg=THEME["panel"],
                 fg=THEME["text_muted"], font=(THEME["font"], 10)).pack(anchor="w", pady=(10, 2))

        value_lbl = tk.Label(self.interaction_frame, text="r = 0.00", bg=THEME["panel"],
                              fg=THEME["accent"], font=(THEME["font"], 14, "bold"))
        value_lbl.pack(anchor="w")

        slider_var = tk.DoubleVar(value=0.0)

        def on_slide(_evt=None):
            value_lbl.config(text=f"r = {slider_var.get():.2f}")

        slider = tk.Scale(self.interaction_frame, from_=-1.0, to=1.0, resolution=0.01,
                           orient=tk.HORIZONTAL, variable=slider_var, command=on_slide,
                           bg=THEME["card"], fg=THEME["text"], troughcolor="#3a4b5f",
                           highlightthickness=0, length=320, sliderrelief=tk.FLAT,
                           activebackground=THEME["accent"], font=(THEME["font"], 9))
        slider.pack(pady=14)

        def submit():
            guess = slider_var.get()
            diff = abs(guess - self.correct_answer)
            correct = diff <= 0.08
            msg = f"{'Correct!' if correct else 'Not quite.'} True r was {self.correct_answer:.2f} (you guessed {guess:.2f})."
            btn_submit.state(["disabled"])
            slider.config(state="disabled")
            self._finish_round(correct, msg)

        btn_submit = ttk.Button(self.interaction_frame, text="Submit Guess", command=submit)
        btn_submit.pack(fill=tk.X, pady=6)

    # ---------- MODE: Regression line matching ----------
    def setup_regression_question(self):
        self.mode_label.config(text="Line of Best Fit")
        self.q_text.config(text="Which equation matches this least-squares regression line?")
        self.hint_label.config(text="Pick the equation of the red line drawn through the data.")

        x, y, slope, intercept, correct_eq, options = generate_regression_data()
        self.correct_answer = correct_eq

        ax = self.fig.add_subplot(111)
        self._style_axes(ax, "Which Line is Mine?")
        ax.scatter(x, y, color=THEME["point_dim"], alpha=0.6, s=28, label="Observations")
        line_x = np.linspace(min(x), max(x), 100)
        ax.plot(line_x, slope * line_x + intercept, color=THEME["line"], linewidth=3)
        self.canvas.draw()

        buttons = []

        def select(choice):
            correct = choice == self.correct_answer
            msg = "Perfect match!" if correct else f"Incorrect. Correct fit: {self.correct_answer}"
            self._disable_children(self.interaction_frame)
            self._finish_round(correct, msg)

        for opt in options:
            b = ttk.Button(self.interaction_frame, text=opt, command=lambda o=opt: select(o))
            b.pack(fill=tk.X, pady=5)
            buttons.append(b)

    # ---------- MODE: Match the graph to the regression line (click) ----------
    def setup_match_question(self):
        self.mode_label.config(text="Match the Graph")
        self.q_text.config(text="The same line is drawn on all four scatterplots. Click the one it was actually fit to.")
        self.hint_label.config(text="Look for the panel where the points genuinely hug the line.")

        datasets, correct_idx, slope, intercept = generate_match_round()
        self.correct_answer = correct_idx

        axes = []
        for i, (x, y) in enumerate(datasets):
            ax = self.fig.add_subplot(2, 2, i + 1)
            self._style_axes(ax, f"Panel {chr(65 + i)}")
            ax.scatter(x, y, color=THEME["point"], alpha=0.7, s=18, edgecolors="none")
            line_x = np.linspace(min(x), max(x), 60)
            ax.plot(line_x, slope * line_x + intercept, color=THEME["line"], linewidth=2.2)
            ax.set_xticks([])
            ax.set_yticks([])
            axes.append(ax)

        self.fig.tight_layout(pad=1.6)
        self.canvas.draw()

        tk.Label(self.interaction_frame, text="Click directly on the matching panel\n(or use the buttons below).",
                 bg=THEME["panel"], fg=THEME["text_muted"], font=(THEME["font"], 10),
                 justify=tk.LEFT).pack(anchor="w", pady=(6, 12))

        answered = {"done": False}

        def resolve(chosen_idx):
            if answered["done"]:
                return
            answered["done"] = True
            correct = chosen_idx == correct_idx
            axes[chosen_idx].title.set_color(THEME["good"] if correct else THEME["bad"])
            if not correct:
                axes[correct_idx].title.set_color(THEME["good"])
            self.canvas.draw()
            msg = "Correct! That's the fitted panel." if correct else \
                  f"Not quite \u2014 Panel {chr(65 + correct_idx)} was the real fit."
            self._disable_children(self.interaction_frame)
            self._finish_round(correct, msg)

        def on_click(event):
            if answered["done"] or event.inaxes is None:
                return
            for i, ax in enumerate(axes):
                if event.inaxes == ax:
                    resolve(i)
                    break

        self.current_cid = self.canvas.mpl_connect("button_press_event", on_click)

        btn_row = tk.Frame(self.interaction_frame, bg=THEME["panel"])
        btn_row.pack(fill=tk.X)
        for i in range(4):
            b = ttk.Button(btn_row, text=chr(65 + i), width=4, command=lambda i=i: resolve(i))
            b.grid(row=0, column=i, padx=4, sticky="ew")
            btn_row.columnconfigure(i, weight=1)

    # ---------- MODE: Click the outlier ----------
    def setup_outlier_question(self):
        self.mode_label.config(text="Spot the Outlier")
        self.q_text.config(text="Click directly on the point that looks like a severe outlier.")
        self.hint_label.config(text="Click near a point on the graph \u2014 no buttons needed.")

        x, y, outlier_idx = generate_outlier_data()
        self.correct_answer = outlier_idx

        ax = self.fig.add_subplot(111)
        self._style_axes(ax, "Click the Outlier")
        scatter = ax.scatter(x, y, color=THEME["point"], alpha=0.8, s=55,
                              edgecolors="none", picker=True, pickradius=9)
        self.canvas.draw()

        answered = {"done": False}

        def resolve(idx):
            if answered["done"]:
                return
            answered["done"] = True
            correct = idx == outlier_idx
            colors = [THEME["point_dim"]] * len(x)
            colors[outlier_idx] = THEME["good"]
            if not correct:
                colors[idx] = THEME["bad"]
            scatter.set_color(colors)
            self.canvas.draw()
            msg = "Correct! That point breaks the trend." if correct else \
                  "Not the biggest outlier \u2014 the true one is now marked green."
            self._finish_round(correct, msg)

        def on_pick(event):
            if answered["done"] or event.artist != scatter:
                return
            resolve(int(event.ind[0]))

        self.current_cid = self.canvas.mpl_connect("pick_event", on_pick)

        tk.Label(self.interaction_frame,
                 text="Tip: the outlier is the point that doesn't fit\nthe overall linear pattern.",
                 bg=THEME["panel"], fg=THEME["text_muted"], font=(THEME["font"], 10),
                 justify=tk.LEFT).pack(anchor="w", pady=10)

    # ---------- MODE: Concept trivia ----------
    def setup_mcq_question(self):
        self.mode_label.config(text="Concept Check")
        mcq = random.choice(ALL_MCQS)
        self.q_text.config(text=mcq["q"])
        self.hint_label.config(text="Pick the best answer.")
        self.correct_answer = mcq["answer"]

        ax = self.fig.add_subplot(111)
        ax.set_facecolor(THEME["plot_bg"])
        ax.axis("off")
        ax.text(0.5, 0.5, "Concept\nCheck", fontsize=26, ha="center", va="center",
                 weight="bold", color=THEME["grid"])
        self.canvas.draw()

        buttons = []

        def select(choice):
            correct = choice == self.correct_answer
            msg = "Correct!" if correct else f"Incorrect. Correct answer: {self.correct_answer}"
            self._disable_children(self.interaction_frame)
            self._finish_round(correct, msg)

        options = list(mcq["options"])
        for opt in options:
            b = ttk.Button(self.interaction_frame, text=str(opt), command=lambda o=opt: select(o))
            b.pack(fill=tk.X, pady=5)
            buttons.append(b)


if __name__ == "__main__":
    root = tk.Tk()
    app = StatsGameApp(root)
    root.mainloop()