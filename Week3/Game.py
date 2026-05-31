"""
This is a very simple game/simulation teaching loss aversion and risk.
Users transfer their money between checkings, game funds, and savings.
Game funds have a chance to double or halve, and players must strategise
how they allocate their money.

author: Justin Baratta
date: 5/31/2026
version: 3.13
"""

import random
import time

CHECKING_FUNDS = 10_000
GAME_FUNDS = 0
SAVINGS_FUNDS = 0

def welcome() -> None:
    message = f"""\nWelcome to your simulation for Week 3! This is a simple game illustrating loss aversion.
\nYou start with $10K in checkings.
You can, at any time, move money from your checkings to your game funds. Every turn, the money you have in the game
can either double or halve. After each turn, you can move money from your game funds to your savings. Once you put money
in savings, it can never be taken out of savings. You can choose at any time to end the game, and your total portfolio value will be shown.
\nHave fun and consider your potential wins and losses!"""
    
    for char in message:
        print(char, end="", flush=True)
        time.sleep(0.02)

if __name__ == "__main__":
    if(input("Do you want to see the intro (y/n): ")).lower() == "y":
        welcome()
    
    turn = 0
    while True:
        turn += 1
        print(f"\n{'='*20}Turn {turn}{'='*20}")
        print(f"Checking funds: ${CHECKING_FUNDS:.2f}")
        print(f"Game Funds: ${GAME_FUNDS:.2f}")
        print(f"Savings Funds: ${SAVINGS_FUNDS:.2f}")

        if CHECKING_FUNDS > 0:
            checking_to_game = int(input("How much money would you like to transfer from checking funds to game funds: "))

            if checking_to_game <= CHECKING_FUNDS:
                GAME_FUNDS += checking_to_game
                CHECKING_FUNDS -= checking_to_game
            else:
                print("Not enough funds in checking, skipping...")

            checking_to_saving = int(input("How much money would you like to transfer from checkings to savings: "))

            if checking_to_saving <= CHECKING_FUNDS:
                CHECKING_FUNDS -= checking_to_saving
                SAVINGS_FUNDS += checking_to_saving
            else:
                print("Not enough funds in checking, skipping...")

        if GAME_FUNDS > 0:
            num = random.choice([0, 1])
            
            if num == 0:
                GAME_FUNDS *= 2
                print("-> LUCKY TURN! Your game funds doubled!")
            else:
                GAME_FUNDS /= 2
                print("-> UNLUCKY TURN! Your game funds halved!")

            print(f"Game Funds after event: ${GAME_FUNDS:.2f}")
            game_to_saving = int(input("How much money would you like to transfer from game funds to savings: "))
            if game_to_saving <= GAME_FUNDS:
                GAME_FUNDS -= game_to_saving
                SAVINGS_FUNDS += game_to_saving
            else:
                print("Not enough funds in game pool, skipping...")

        quit_choice = input("Would you like to cash out and end the simulation right now? (y/n): ").strip().lower()
        if quit_choice == 'y' or (CHECKING_FUNDS == 0 and GAME_FUNDS == 0):
            total_net_worth = CHECKING_FUNDS + GAME_FUNDS + SAVINGS_FUNDS
            print(f"\n{'='*15} SIMULATION OVER {'='*15}")
            print(f"Final Account Balance Details:")
            print(f" - Remaining Cash in Checkings: ${CHECKING_FUNDS:.2f}")
            print(f" - Vulnerable Assets in Game: ${GAME_FUNDS:.2f}")
            print(f" - Safe Realized Profits in Savings: ${SAVINGS_FUNDS:.2f}")
            print(f"Total Liquid Net Worth Settled: ${total_net_worth:.2f}")
            break