def shruthi(moves: list, strat_idx: int) -> int:
    return DEFECT if random.random() < 0.1 else COOPERATE
