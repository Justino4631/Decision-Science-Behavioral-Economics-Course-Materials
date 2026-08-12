import random

COOPERATE, DEFECT = 0, 1
# [(0, 0), (1, 0)]

def tft(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE
    opp_idx = 1 - strat_idx
    return moves[-1][opp_idx]

def generous_tft(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE
    opp_idx = 1 - strat_idx
    if moves[-1][opp_idx] == DEFECT:
        return COOPERATE if random.random() < 0.15 else DEFECT
    return COOPERATE

def tftt(moves: list, strat_idx: int) -> int:
    if not moves or len(moves) < 2:
        return COOPERATE
    opp_idx = 1 - strat_idx
    if moves[-1][opp_idx] == DEFECT and moves[-2][opp_idx] == DEFECT:
        return DEFECT
    return COOPERATE

def hard_tft(moves: list, strat_idx: int) -> int:
    if not moves or len(moves) < 2:
        return COOPERATE
    opp_idx = 1 - strat_idx
    if moves[-1][opp_idx] == DEFECT or moves[-2][opp_idx] == DEFECT:
        return DEFECT
    return COOPERATE

def random_tft(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE
    opp_idx = 1 - strat_idx
    if random.random() < 0.05:
        return random.choice([COOPERATE, DEFECT])
    return moves[-1][opp_idx]

def friedman(moves: list, strat_idx: int) -> int:
    opp_idx = 1 - strat_idx
    opp_moves = [m[opp_idx] for m in moves]
    return DEFECT if DEFECT in opp_moves else COOPERATE

def graaskamp(moves: list, strat_idx: int) -> int:
    round_num = len(moves)
    opp_idx = 1 - strat_idx

    if round_num == 0:
        return COOPERATE

    def tit_for_tat():
        return moves[-1][opp_idx]

    if round_num < 50:
        return tit_for_tat()

    if round_num == 50:
        return DEFECT

    if round_num < 56:
        return tit_for_tat()

    opp_history = [m[opp_idx] for m in moves]
    my_history = [m[strat_idx] for m in moves]

    count_c = opp_history.count(COOPERATE)
    count_d = opp_history.count(DEFECT)
    total_moves = len(opp_history)

    expected = total_moves / 2.0
    chi_square = ((count_c - expected) ** 2 / expected) + (
        (count_d - expected) ** 2 / expected
    )

    is_random = chi_square < 3.841

    if is_random:
        return DEFECT

    tft_matches = sum(
        1 for i in range(1, total_moves) if opp_history[i] == my_history[i - 1]
    )
    is_tft_like = (tft_matches / (total_moves - 1)) >= 0.85

    if is_tft_like:
        return tit_for_tat()

    if round_num % 8 == 0:
        return DEFECT

    return tit_for_tat()

def go_by_majority(moves: list, strat_idx: int) -> int:
    opp_idx = 1 - strat_idx
    opp_moves = [move[opp_idx] for move in moves]
    return COOPERATE if opp_moves.count(COOPERATE) >= opp_moves.count(DEFECT) else DEFECT

def tideman_and_chieruzzi(moves: list, strat_idx: int) -> int:
    opp_idx = 1 - strat_idx
    round_num = len(moves)

    if round_num == 0:
        return COOPERATE

    opp_history = [m[opp_idx] for m in moves]
    my_history = [m[strat_idx] for m in moves]

    opp_defects = opp_history.count(DEFECT)
    opp_coops = opp_history.count(COOPERATE)

    if round_num >= 20 and (opp_defects / round_num) > 0.60:
        return DEFECT

    expected = round_num / 2.0
    chi_square = ((opp_coops - expected) ** 2 / expected) + (
        (opp_defects - expected) ** 2 / expected
    )

    if moves[-1][opp_idx] == DEFECT:
        return DEFECT

    if chi_square > 3.841 and opp_defects > opp_coops:
        if round_num >= 4:
            recent_my_moves = my_history[-4:]
            if recent_my_moves != [DEFECT, DEFECT, COOPERATE, COOPERATE]:
                if my_history[-1] == DEFECT and my_history[-2] != DEFECT:
                    return DEFECT
                return COOPERATE

    return moves[-1][opp_idx]

def pavlov(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE

    opp_moves = [move[1 - strat_idx] for move in moves]
    pavlov_moves = [move[strat_idx] for move in moves]

    if opp_moves[-1] == COOPERATE and pavlov_moves[-1] == COOPERATE:
        return COOPERATE
    elif opp_moves[-1] == DEFECT and pavlov_moves[-1] == COOPERATE:
        return DEFECT
    elif opp_moves[-1] == COOPERATE and pavlov_moves[-1] == DEFECT:
        return DEFECT
    else:
        return COOPERATE

def joss(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE

    opp_idx = 1 - strat_idx
    if moves[-1][opp_idx] == COOPERATE:
        return DEFECT if random.random() < 0.1 else COOPERATE

    return DEFECT

def gradual(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE

    opp_idx = 1 - strat_idx
    opp_history = [m[opp_idx] for m in moves]
    my_history = [m[strat_idx] for m in moves]

    opp_defects = opp_history.count(DEFECT)

    if opp_defects == 0:
        return COOPERATE

    required_defects = (opp_defects * (opp_defects + 1)) // 2
    my_defects = my_history.count(DEFECT)

    if my_defects < required_defects:
        return DEFECT

    if my_history[-1] == DEFECT:
        return COOPERATE
    if len(my_history) >= 2 and my_history[-2] == DEFECT and my_history[-1] == COOPERATE:
        return COOPERATE

    return COOPERATE

def prober(moves: list, strat_idx: int) -> int:
    round_num = len(moves)
    opp_idx = 1 - strat_idx

    if round_num == 0:
        return COOPERATE
    if round_num in (1, 2):
        return DEFECT

    opp_retaliated = (moves[1][opp_idx] == DEFECT) or (moves[2][opp_idx] == DEFECT)

    if opp_retaliated:
        return moves[-1][opp_idx]
    else:
        return DEFECT

def tester(moves: list, strat_idx: int) -> int:
    round_num = len(moves)
    opp_idx = 1 - strat_idx

    if round_num == 0:
        return DEFECT

    if round_num == 1:
        return COOPERATE

    opp_retaliated = (moves[0][opp_idx] == DEFECT) or (moves[1][opp_idx] == DEFECT)

    if opp_retaliated:
        return moves[-1][opp_idx]
    else:
        return COOPERATE if round_num % 2 == 0 else DEFECT

def remorseful_prober(moves: list, strat_idx: int) -> int:
    round_num = len(moves)
    opp_idx = 1 - strat_idx

    if round_num == 0:
        return COOPERATE

    my_history = [m[strat_idx] for m in moves]
    opp_history = [m[opp_idx] for m in moves]

    if round_num >= 2:
        we_probed_2_turns_ago = (
            my_history[-2] == DEFECT and 
            (round_num == 2 or opp_history[-3] == COOPERATE)
        )
        opp_retaliated_last_turn = (opp_history[-1] == DEFECT)

        if we_probed_2_turns_ago and opp_retaliated_last_turn:
            return COOPERATE

    tft_move = opp_history[-1]

    if tft_move == COOPERATE and random.random() < 0.05:
        return DEFECT

    return tft_move

def adaptive(moves: list, strat_idx: int) -> int:
    if len(moves) < 3: return COOPERATE
    if len(moves) < 6: return DEFECT

    payoffs = {(0, 0): 3, (0, 1): 0, (1, 0): 5, (1, 1): 1}
    scores = {0: [0, 0], 1: [0, 0]}

    for m in moves:
        scores[m[strat_idx]][0] += payoffs[(m[strat_idx], m[1 - strat_idx])]
        scores[m[strat_idx]][1] += 1

    avg_c = scores[0][0] / scores[0][1] if scores[0][1] else 0
    avg_d = scores[1][0] / scores[1][1] if scores[1][1] else 0

    return COOPERATE if avg_c > avg_d else (DEFECT if avg_d > avg_c else moves[-1][strat_idx])

def downing(moves: list, strat_idx: int) -> int:
    if len(moves) < 2:
        return DEFECT

    opp_idx = 1 - strat_idx
    c_after_c, total_c = 0, 0
    c_after_d, total_d = 0, 0

    for i in range(1, len(moves)):
        prev_my, curr_opp = moves[i - 1][strat_idx], moves[i][opp_idx]
        if prev_my == COOPERATE:
            total_c += 1
            if curr_opp == COOPERATE:
                c_after_c += 1
        else:
            total_d += 1
            if curr_opp == COOPERATE:
                c_after_d += 1

    alpha = (c_after_c / total_c) if total_c else 0.5
    beta = (c_after_d / total_d) if total_d else 0.5

    ev_c = alpha * 3 + (1 - alpha) * 0
    ev_d = beta * 5 + (1 - beta) * 1

    return COOPERATE if ev_c >= ev_d else DEFECT

def grofman(moves: list, strat_idx: int) -> int:
    if len(moves) < 2:
        return COOPERATE

    opp_idx = 1 - strat_idx
    if moves[-1][strat_idx] == moves[-1][opp_idx]:
        return COOPERATE

    return COOPERATE if random.random() < (2 / 7) else DEFECT

def feld(moves: list, strat_idx: int) -> int:
    if not moves:
        return COOPERATE

    opp_idx = 1 - strat_idx
    if moves[-1][opp_idx] == DEFECT:
        return DEFECT

    prob_coop = max(0.0, 1.0 - (len(moves) / 200.0))
    return COOPERATE if random.random() < prob_coop else DEFECT

def always_c(moves: list, strat_idx: int) -> int:
    return COOPERATE

def always_d(moves: list, strat_idx: int) -> int:
    return DEFECT

def random_strat(moves: list, strat_idx: int) -> int:
    return random.choice([COOPERATE, DEFECT])

STRATEGIES = [strat for strat in globals().values() if callable(strat)]
# STRATEGY_DESCRIPTIONS = {
#     strat.__name__: strat.__doc__
#     for strat in globals().values() if callable(strat)
# }
STRATEGY_DESCRIPTIONS = {'tft': 'Classic tit-for-tat strategy.', 'generous_tft': 'Classic tit-for-tat with 15% to cooperate even when the opponent defected the previous turn.', 'tftt': 'Classic tit-for-two-tats strategy.', 'hard_tft': 'Tit-for-tat that defects when the opponent defected in either of the last two moves.', 'random_tft': 'Tit-for-tat with a 5% chance to make a random move.', 'friedman': 'Cooperate until the opponent defects. Then defect unconditionally.', 'graaskamp': '\nPlay tit-for-tat until move 50, defect on round 50. After that, use\nprobability distributions to figure out what type of strategy the opponent is, and adapt from there.\n', 'go_by_majority': 'Cooperate if the opponent has cooperated more times than defected, and vice versa.', 'tideman_and_chieruzzi': 'Defect if the opponent defects more than 60% of the time. Else, use probability distributions to determine whether to defect or cooperate.', 'pavlov': 'Classic Win-Stay Lose-Shift strategy (pavlov).', 'joss': 'Play tit for tat with a 10% to defect even if the opponent cooperated last turn.', 'gradual': 'Cooperate until the opponent defects. Then, play N consecutive defects where N is the total amount of times the opponent has defected.', 'prober': "\nPlay these moves to start the match: C, D, D. If the opponent retaliated, play tit-for-tat\nthe rest of the game. If they didn't, unconditionally defect.\n", 'tester': '\nStrategy used to probe and exploit strategies like tit-for-two-tats. Play D, C the first two moves.\nIf the opponent retaliated, play tit-for-tat for the rest of the game. If not, alternate cooperating and \ndefecting.\n', 'remorseful_prober': '\nPlay tit-for-tat. 5% of the time, defect when opponent cooperated last turn. If they retaliated, \napologize and cooperate.\n', 'adaptive': 'Start out with CCC, DDD. Then, play whichever move resulted in the highest payoff for this strategy.', 'downing': 'Cooperates if the opponent responds positively to cooperation, otherwise defects to maximize payoff.', 'grofman': 'Cooperate twice to start. Then, if this strategy and the opponent played the same move, cooperate. If not, cooperate with a fixed probability of ~28% (2/7).', 'feld': 'Interesting strategy that pretty much cooperates with a varable probability based on what move it is, or defect if the opponent defected last turn', 'always_c': 'Always cooperate.', 'always_d': 'Always defect.', 'random_strat': 'Play a random move.'}
