from itertools import combinations_with_replacement
import random
from strategies import STRATEGIES
import json

class Game():
    def __init__(self, strategies: list = [], num_rounds: int = 200) -> None:
        self.strategies = strategies
        self.num_rounds = num_rounds
        print(f"Rounds for this IPD: {num_rounds}")
        self.results = {}

    def play_round(self, strategy1, strategy2) -> list:
        moves = []

        strat1_idx = 0
        strat2_idx = 1

        for i in range(self.num_rounds):
            strat1_move = strategy1(moves, strat1_idx)
            strat2_move = strategy2(moves, strat2_idx)

            actual1 = 1 - strat1_move if random.random() < 0.05 else strat1_move
            actual2 = 1 - strat2_move if random.random() < 0.05 else strat2_move

            moves.append((actual1, actual2))

        return moves

    def round_robin(self) -> dict:
        games_map = {}

        for strat1, strat2 in combinations_with_replacement(self.strategies, 2):
            moves = self.play_round(strat1, strat2)
            payouts = self._evaluate_round(moves)
            games_map[(strat1, strat2)] = (moves, payouts)

        self.results = games_map
        return games_map

    def _evaluate_round(self, moves) -> tuple:

        strat1_payout = 0
        strat2_payout = 0

        for move in moves:
            if move[0] == 0 and move[1] == 0:
                strat1_payout += 3
                strat2_payout += 3
            elif move[0] == 1 and move[1] == 0:
                strat1_payout += 5
            elif move[0] == 0 and move[1] == 1:
                strat2_payout += 5
            else:
                strat1_payout += 1
                strat2_payout += 1

        return (strat1_payout, strat2_payout)

    def rank_strategies(self) -> dict:
        if not self.results:
            self.round_robin()

        stats = {s.__name__: {"totals": 0, "matches": 0, "wins": 0, "ties": 0, "losses": 0} for s in self.strategies}
        for (s1, s2), (_, (p1, p2)) in self.results.items():
            n1, n2 = s1.__name__, s2.__name__
            stats[n1]["totals"] += p1
            stats[n2]["totals"] += p2
            stats[n1]["matches"] += 1
            stats[n2]["matches"] += 1

            if p1 > p2:
                stats[n1]["wins"] += 1
                stats[n2]["losses"] += 1
            elif p2 > p1:
                stats[n2]["wins"] += 1
                stats[n1]["losses"] += 1
            else:
                stats[n1]["ties"] += 1
                stats[n2]["ties"] += 1

        summary = {
            s: {
                "avg_payout": data["totals"] / data["matches"],
                "wins": data["wins"],
                "ties": data["ties"],
                "losses": data["losses"],
            }
            for s, data in stats.items()
        }
        return dict(sorted(summary.items(), key=lambda x: x[1]["avg_payout"], reverse=True))

# game = Game(strategies=STRATEGIES, num_rounds=random.choice([x for x in range(150, 250)]))
# results = game.rank_strategies()
# print("IPD Executed!")
# with open("Week11_13/IPD_Results.json", "w") as file:
#     json.dump(results, file, indent=4)