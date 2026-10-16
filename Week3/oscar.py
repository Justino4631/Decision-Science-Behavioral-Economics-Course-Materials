import random
import re

WELCOME = """
=============================================================
          ORBITAL VENTURES -- MISSION CONTROL
=============================================================

You've just raised $20 MILLION in seed funding. Turn it into
as much profit as you can before the money runs out.

-------------------------------------------------------------
THE PROGRAMS  ($1M per attempt)
-------------------------------------------------------------
 [1] SATELLITE DELIVERY   20% success -> stake + $1.1M
     Routine payloads to low orbit.

 [2] REUSABLE BOOSTER     10% success -> stake + $2.5M
     Land the first stage, fly it again.

 [3] ORBITAL FUEL DEPOT    5% success -> stake + $10M
     Nobody has ever made this work.

 Failed attempts lose the money.

-------------------------------------------------------------
HOW TO PLAY
-------------------------------------------------------------
 Enter your allocation each round like this:

     Project 1: 3  Project 2: 0  Project 3: 1

 That spends $4M -- three attempts at Satellite Delivery,
 one at the Fuel Depot. Each million is rolled separately,
 so three attempts at 20% is three separate chances.

 Type  "Expected value Project 2"  at any time to see your
 current success rate, break-even point, and expected
 return per million on that program.

-------------------------------------------------------------
FAILURE STILL TEACHES YOU
-------------------------------------------------------------
 Every attempt -- win or lose -- buys engineering expertise
 and raises your success rate. But learning gets harder the
 more you know: your fourth flight teaches you far less
 than your first.

 All three programs start as LOSING bets. You aren't
 investing for the payout at first; you're paying tuition.
 Programs 1 and 2 need about five attempts before they turn
 profitable. Program 3 needs only four -- but at 5% odds you
 may burn $10M without a single success.

-------------------------------------------------------------
 You cannot afford to learn everything, and you cannot
 afford to go quiet while you learn it.

                    GOOD LUCK, DIRECTOR.
=============================================================
"""

NAMES = ["Satellite Delivery", "Reusable Booster", "Orbital Fuel Depot"]
RATES = [0.20, 0.10, 0.05]
PAYOUTS = [2.1, 3.5, 11.0]
K = [1.5, 1.45, 1.3]


def grow(p, k):
    """Multiply the odds by k. Keeps p below 1 and gives diminishing returns."""
    odds = (p / (1 - p)) * k
    return odds / (odds + 1)


def show_ev(i):
    p = RATES[i]
    payout = PAYOUTS[i]
    ev = p * payout - 1
    print(f"\n  {NAMES[i]}")
    print(f"    Success rate now .... {p*100:.1f}%")
    print(f"    Break-even rate ..... {100/payout:.1f}%")
    print(f"    Expected value ...... ${ev:+.2f}M per $1M invested")
    print(f"    Next attempt raises rate to {grow(p, K[i])*100:.1f}%\n")


print(WELCOME)

money = 10.0
round_num = 1

while money > 0:
    print(f"\n--- Round {round_num} --- Capital: ${money:.1f}M")
    for i in range(3):
        print(f"    [{i+1}] {NAMES[i]}: {RATES[i]*100:.1f}%")
    response = input("Your allocation: ")

    if "expected" in response.lower():
        found = re.search(r'[123]', response)
        if found:
            show_ev(int(found.group()) - 1)
        else:
            print("  Which program? e.g. Expected value Project 2")
        continue

    nums = re.findall(r':\s*(\d+)', response)
    if len(nums) < 3:
        nums = re.findall(r'\d+', response)
    if len(nums) < 3:
        print("  Enter it like: Project 1: 3  Project 2: 0  Project 3: 1")
        continue
    inv = [int(n) for n in nums[:3]]

    total = sum(inv)
    if total > money:
        print(f"  You only have ${money:.1f}M.")
        continue
    if total == 0:
        print("  You sat out the round.")
        round_num += 1
        continue

    money -= total
    for i in range(3):
        if inv[i] == 0:
            continue
        hits = 0
        for _ in range(inv[i]):
            if random.random() < RATES[i]:
                hits += 1
            RATES[i] = grow(RATES[i], K[i])
        money += hits * PAYOUTS[i]
        print(f"  {NAMES[i]}: {hits}/{inv[i]} succeeded "
              f"(rate now {RATES[i]*100:.1f}%)")

    round_num += 1

print(f"\nOut of funding after {round_num - 1} rounds.")