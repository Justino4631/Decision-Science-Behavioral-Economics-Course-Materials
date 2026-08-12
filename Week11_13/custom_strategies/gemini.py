def gemini(moves: list, strat_idx: int) -> int:
    my_idx = strat_idx
    opp_idx = 1 - strat_idx
    
    # Extract historical moves
    my_moves = [m[my_idx] for m in moves]
    opp_moves = [m[opp_idx] for m in moves]
    turn = len(moves)
    
    # 1. First move: Cooperate
    if turn == 0:
        return COOPERATE
        
    # 2. Aggression Detection (Defensive Fallback)
    # If the opponent Defects when they shouldn't (non-GBM behavior), switch to Tit-For-Tat
    opp_defects = opp_moves.count(DEFECT)
    if turn <= 5 and opp_defects >= 2:
        return opp_moves[-1]  # Tit-For-Tat
        
    # 3. Anchor Phase (Turns 1-4)
    # Build a small initial pool of Cooperates
    if turn < 5:
        return COOPERATE
        
    # 4. Harvest Phase
    # Count my historical actions
    my_c = my_moves.count(COOPERATE)
    my_d = my_moves.count(DEFECT)
    
    # Since your GBM function cooperates when my_c >= my_d, 
    # we can safely defect whenever my_c > my_d
    if my_c > my_d:
        return DEFECT
    else:
        return COOPERATE
