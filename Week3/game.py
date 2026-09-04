import random

INITIAL_FUNDING, TOTAL_QUARTERS, QUARTERLY_EXPENSES, INITIAL_REVENUE = 100_000, 40, 12_000, 8_000
CURRENT_FUNDING, CURRENT_QUARTER, HAS_INSURANCE, QUARTERLY_REVENUE = INITIAL_FUNDING, 1, False, INITIAL_REVENUE

SCENARIOS = [
    ("gwpw", "Big Enterprise Sales", 0.452, 2.15, "Sign Small Clients", "Pitch Fortune 500", "Lock in small contracts or hunt a corporate giant."),
    ("glpl", "Copyright Dispute", 0.225, 2.4, "Pay Settlement Fee", "Hire Lawyers & Fight", "Settle for a known cost or fight in court to pay $0."),
    ("lottery", "Viral Marketing", 0.095, 8.7, "Standard Social Ads", "Hire Celebrity", "Massive influencer push could make you viral or flop."),
    ("gwpw", "Server Upgrades", 0.65, 1.875, "Basic Cloud", "Dedicated Servers", "Private servers cost more but offer far higher reliability."),
    ("sunk", "Slow App Redesign", 0.45, 3.125, "Cut Losses & Patch", "Rebuild App from Scratch", "Patching accepts a small fixed loss, but rebuilding is a gamble."),
    ("glpl", "Data Breach Fallout", 0.25, 3.0, "Pay Security Fine", "Hire PR Firm", "Pay a regulatory penalty or hire PR to contest it."),
    ("gwpw", "Overseas Expansion", 0.40, 2.5, "EU Distributor", "Open London Office", "Partnering is safer, but your own office brings higher rewards."),
    ("sunk", "Failing Feature", 0.35, 3.0, "Shut Down Feature", "Relaunch Feature", "Shut it down to lock in loss, or spend cash on a relaunch.")
]

GUARANTEED_IDX = {"gwpw": 0, "lottery": 0, "glpl": 0, "sunk": 0, "decoy": None}

def _signed(amt: int) -> str:
    return f"{'-' if amt < 0 else '+'}${abs(amt):,}"

def reset_game():
    global CURRENT_FUNDING, CURRENT_QUARTER, HAS_INSURANCE, QUARTERLY_REVENUE
    CURRENT_FUNDING, CURRENT_QUARTER, HAS_INSURANCE, QUARTERLY_REVENUE = INITIAL_FUNDING, 1, False, INITIAL_REVENUE

def is_bankrupt() -> bool:
    return CURRENT_FUNDING <= 0

def apply_finances() -> tuple[int, str]:
    global CURRENT_FUNDING, QUARTERLY_REVENUE
    rev = int(QUARTERLY_REVENUE * random.uniform(0.95, 1.10))
    net = rev - QUARTERLY_EXPENSES
    CURRENT_FUNDING += net
    QUARTERLY_REVENUE = int(QUARTERLY_REVENUE * 1.02)
    
    ins_msg = ""
    if HAS_INSURANCE:
        CURRENT_FUNDING -= 2_000
        ins_msg = f" | Ins: -$2,000"
    elif random.random() < 0.10:
        loss = max(6_000, int(CURRENT_FUNDING * 0.08))
        CURRENT_FUNDING -= loss
        ins_msg = f" | ⚠️ Hardware Failure: {_signed(-loss)}"
        
    return net - (2_000 if HAS_INSURANCE else 0), f"Ops: {_signed(net)} (Rev: ${rev:,}){ins_msg}"

def make_choice(q_type: str, safe: int, risky: int, prob: float, idx: int, opt1: str, opt2: str) -> tuple[int, str]:
    global CURRENT_FUNDING
    net, msg = 0, ""

    if q_type in ("gwpw", "lottery"):
        if idx == 0: 
            net, msg = safe, f"{opt1}: {_signed(safe)}"
        elif random.random() < prob: 
            net, msg = risky, f"{opt2} paid off! {_signed(risky)}"
        else: 
            msg = f"{opt2} fell flat ($0)"
            
    elif q_type == "glpl":
        if idx == 0: 
            net, msg = -safe, f"{opt1}: {_signed(-safe)}"
        elif random.random() < prob: 
            net, msg = -risky, f"{opt2} backfired! {_signed(-risky)}"
        else: 
            msg = f"{opt2} succeeded ($0)"
            
    elif q_type == "sunk":
        if idx == 0: 
            net, msg = -safe, f"{opt1}: {_signed(-safe)}"
        elif random.random() < prob: 
            net, msg = risky, f"{opt2} succeeded! {_signed(risky)}"
        else: 
            net, msg = -risky, f"{opt2} failed! {_signed(-risky)}"
            
    elif q_type == "decoy":
        net = safe if idx == 0 else risky
        msg = f"{opt1 if idx == 0 else opt2}: {_signed(net)}"

    CURRENT_FUNDING += net
    f_net, f_msg = apply_finances()
    return net + f_net, f"{msg} | {f_msg}"

def _build_event(title: str, desc: str, q_type: str, opt1: str, opt2: str, safe: int, risky: int, prob: float) -> dict:
    pct = int(prob * 100)
    
    if q_type == "gwpw":
        o1_txt = f"{opt1} (100% chance for +${safe:,})"
        o2_txt = f"{opt2} ({pct}% chance for +${risky:,})"
    elif q_type == "glpl":
        o1_txt = f"{opt1} (100% chance to lose -${safe:,})"
        o2_txt = f"{opt2} ({pct}% chance to lose -${risky:,})"
    elif q_type == "sunk":
        o1_txt = f"{opt1} (100% chance to lose -${safe:,})"
        o2_txt = f"{opt2} ({pct}% chance for +${risky:,} / {100-pct}% lose -${risky:,})"
    elif q_type == "lottery":
        o1_txt = f"{opt1} (100% chance for +${safe:,})"
        o2_txt = f"{opt2} ({pct}% chance for +${risky:,})"
    else:
        o1_txt = f"{opt1} (100% chance for +${safe:,})"
        o2_txt = f"{opt2} (100% chance for +${risky:,})"

    return {
        "title": title,
        "prompt": f"{desc}\n\nWhat is your decision?",
        "options": [o1_txt, o2_txt],
        "action": lambda idx: make_choice(q_type, safe, risky, prob, idx, opt1, opt2)
    }

def get_current_event() -> dict:
    q = CURRENT_QUARTER
    if q in (10, 20, 30, 40):
        val = int(CURRENT_FUNDING * (0.30 if q == 40 else 0.15))
        return _build_event(f"Quarter {q}: Investor Milestone", "Investors want to allocate reserve funds.", 
                            "gwpw", "High-Yield Savings", "Tech Stock Index", val, int(val * 2.2), 0.50)

    q_type, title, prob, mult, opt1, opt2, desc = SCENARIOS[(q - 1) % len(SCENARIOS)]

    safe = max(4_000, int(CURRENT_FUNDING * 0.08))
    risky = int(safe * mult)

    return _build_event(f"Quarter {q}: {title}", desc, q_type, opt1, opt2, safe, risky, prob)