from random import randint

cost = 100
paid = 0
earned = 0
trials = 0
while earned <= paid:
    trials+=1
    paid+=cost
    earning = 1
    heads = True
    while heads:
        earning *= 2
        heads = randint(0,1)
    earned+=earning
    print(paid, earned, cost, earning)
print("You paid: $"+str(paid), "\nYou earned: $"+str(earned), "\nYou played "+str(trials)+" times")
