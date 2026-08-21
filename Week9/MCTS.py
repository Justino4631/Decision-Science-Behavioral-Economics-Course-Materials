"""
This is a file that will run the MCTS (Monte Carlo Tree Search Algorithm) for the game Connect 4.
All methods in the Node class are fully given, however you may edit any of them if you want to make
the algorithm run faster (only do so if you got the MCTS to work and have extra time).
NOTE: The TUI (Terminal User Interface) was made by Riaan, edited by me, Justin, to be more concise.

author: Justin Baratta
date: 6/16/2026
version: 3.13
"""

# ------- Import Section -------
from typing import Self
import time
from model import Model
import random
import math
import copy
import numpy as np

# ------- Class Section -------
class Node:

    def __init__(self, state: Model, parent: Self = None) -> None:
        """
        Initialize the Node class
        """
        self.state = state
        self.parent = parent
        self.children = []
        self.wins = 0
        self.visits = 0

    def select_child(self, optimal: bool = False) -> Self:
        """
        Select the best child by win pct if optimal, by UCT score if not optimal
        """
        if optimal: # return the best child
            win_pcts = []
            for child in self.children:
                #Try to append win pct to win_pcts for each node, if there is an error
                #E.g. ZeroDivision (no visits yet) return that child
                try:
                    win_pcts.append(child.wins/child.visits)
                except:
                    return child
                
            return self.children[win_pcts.index(max(win_pcts))] #Return the child node with highest win pct
        else:

            UCTs = []
            for child in self.children:
                if(child.visits == 0): #Again, check whether the node has any visits
                    return child 
                #UCT score is win pct + sqrt(2)*sqrt( log(this node's visits)/child node visits )
                UCTs.append((child.wins/child.visits + 1.414*math.sqrt(math.log(self.visits)/child.visits)))

            return self.children[UCTs.index(max(UCTs))] #Return the child node with highest UCT score

    def expand(self) -> None:
        """
        Expand a node from every possible state that can result from a move in the current state
        """
        top_row = self.state.board[0]
        possible_moves = [x for x in range(len(top_row)) if top_row[x] == 0] #Basically, you know a move is possible if the column isn't full (there is no piece on the top row)

        for move in possible_moves:
            #Set the new states and parameters for each possible new state from the current state
            new_state = Model()
            new_state.board = [row[:] for row in self.state.board]
            new_state.last_action = self.state.last_action
            new_state.last_player = self.state.last_player
            new_state.add_piece(move, 3-new_state.last_player)

            self.children.append(Node(state=new_state, parent=self))

    def simulate(self) -> float:
        """
        Simulate a game out by playing random moves from the state and seeing who wins
        """

        new_state = Model()
        new_state.board = [row[:] for row in self.state.board]
        new_state.last_action = self.state.last_action
        new_state.last_player = self.state.last_player

        while(not new_state.game_over()):
        
            top_row = self.state.board[0]
            possible_moves = [x for x in range(len(top_row)) if top_row[x] == 0]
            
            random_move = random.choice(possible_moves)
            new_state.add_piece(random_move, 3-new_state.last_player) #Play random move
        
        #See if any player is the winner
        if new_state.is_winner(3-self.state.last_player):
            return 1
        elif new_state.is_winner(self.state.last_player):
            return -1
        else:
            return 0

    def backpropagate(self, result: float) -> None:
        """
        Propogate ALL the way along the tree
        """

        #Propogate along the tree (no way, like the tree in "Monts Carlo Tree Search"???) switching signs to account for the two players
        sign = -1
        current = self
        while current.parent is not None:
            current.wins += sign*result
            current.visits += 1
            sign *= -1
            current = current.parent
        current.visits += 1

    def is_terminal(self) -> bool:
        """
        Is the game over?
        """
        return self.state.game_over()

# ------- Function Section -------
def mcts(root: Node, iterations: int, max_seconds: float) -> Node:
    """
    Run the Monte Carlo Tree Search algorithm for a given number of iterations.
    """
    
    if max_seconds is not None:
        end_time = time.time() + max_seconds

    for _ in range(iterations):
        # always start at the root of the tree
        node = root
        # Selection/Traverse
        # Select a child node until we reach a leaf node
        while node.children:
            node = node.select_child()
        # Expansion
        # If the node is not terminal, expand it
        if not node.is_terminal():
            #call the expand function from the node
            node.expand()
            if node.children:
                node = random.choice(node.children)  # Select a random new child to simulate from
        # Simulation
        result = node.simulate()
        # Backpropagation
        node.backpropagate(result)
        # root.print_tree()
        if max_seconds is not None and time.time() > end_time:
            break
    # Choose the best move from the children at the root
    node = root.select_child(optimal=True)
    return node

def main(who_play_first: str | None = None) -> None:
    if who_play_first is None:
        who_play_first = input("Do you want to play first? (y/n) ").strip().lower()

    print("TUI made by Riaan (cleaned up by me)")

    game = Model()
    human_player = 1 if who_play_first == "y" else 2
    ai_player = 3 - human_player
    current_player = 1

    EMPTY_SLOT = "\u2009●\u2009"
    RED_PIECE = "\033[31;1m\u2009●\u2009\033[0m"
    CYAN_PIECE = "\033[36;1m\u2009●\u2009\033[0m" 
    HIGHLIGHT_PIECE = "\033[31;43;1m\u2009●\u2009\033[0m" 

    last_ai_move = None

    while not game.game_over():

        if current_player == human_player:
            valid_cols = [str(col + 1) for col in game.valid_moves()]
            
            while True:
                user_input = input("   column number: (1-7) ").strip()
                if user_input in valid_cols:
                    col = int(user_input) - 1
                    break

            game.add_piece(col, human_player)
            current_player = ai_player

        else:
            prev_board = copy.deepcopy(game.board)

            start_time = time.time()
            best_node = mcts(root=Node(state=game), iterations=100_000, max_seconds=5)
            print(f"mcts time: {time.time() - start_time:.4f}")
            print("move has been chosen!")

            game.set_game_board(copy.deepcopy(best_node.state.board))

            last_ai_move = None
            for r in range(len(game.board)):
                for c in range(len(game.board[0])):
                    if prev_board[r][c] != game.board[r][c]:
                        last_ai_move = (r, c)
                        break

            current_player = human_player

        print("\n   board")
        for r_idx, row in enumerate(game.board):
            row_str = "  "
            for c_idx, cell in enumerate(row):
                if last_ai_move and (r_idx, c_idx) == last_ai_move:
                    row_str += f" {HIGHLIGHT_PIECE}"
                elif cell == 1:
                    row_str += f" {RED_PIECE}"
                elif cell == 2:
                    row_str += f" {CYAN_PIECE}"
                else:
                    row_str += f" {EMPTY_SLOT}"
            print(row_str)

        print("\033[34;1m    1   2   3   4   5   6   7 \033[37m\n")

    if game.is_winner(human_player):
        print("You win!")
    elif game.is_winner(ai_player):
        print("You lose...")
    else:
        print("Tie!")

# ------- Execution Section -------
if __name__ == "__main__":
    main()