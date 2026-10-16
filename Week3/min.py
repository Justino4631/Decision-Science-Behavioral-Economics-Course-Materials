import random,time


current_expected_value=0
max_expected_value=0
money=0
max_money=0
i=5

print("Welcome to my game! In this game, I am going to test you on your skills of expected value. This is TOTALLY not a gambling simulator, trust me. Anyways...")
input("Enter to continue")
print("The rules are simple. There are five rounds, each with two options at a chance to make some big bucks for you to choose from. Your goal is to get the maximum amount of money and expected value possible. So without further ado, good luck and have fun!")
input("Enter to continue")
print()

def gameloop():
    
    global current_expected_value,max_expected_value,money,max_money,i
    
    option1=random.randint(500,1500)
    option2=abs((random.randint(10,500)))
    chance1=random.randint(1,30)
    chance2=random.randint(30,100)
    
    if (option1*chance1>=option2*chance2):
        max_expected_value+=option1/chance1
    else:
        max_expected_value+=option2/chance2
        
    if (option1>=option2):
        max_money+=option1
    else:
        max_money+=option2
    
    print()
    
    print("There are ",i," round(s) left. Good luck!")
    
    print()
    
    print("Here are the two options for this round:")
    print()
    print("Option 1: A chance to gain $",option1," at the odds of ",chance1,"%")
    print()
    print("Option 2: A chance to gain $",option2," at the odds of ",chance2,"%")
    
    print()
    
    choice=input("Choose option [1] or option [2]")
    if choice=='1':
        current_expected_value+=option1*chance1
        
        
        print()
        print("You chose option 1! Let's cross our fingers and hope for the best!")
        time.sleep(1)
        print("The wheel is spinning...")
        time.sleep(3)
        print()
        
        draw=random.randint(1,100)
        if draw<=chance1:
            money+=option1
            print("Congratulations! You just won $",option1," !")
            time.sleep(1)
            print("Current money:$ ",money)
        else:
            print("I'm sorry. Seems like python's random.randint() is not on your side today!")
            time.sleep(1)
            print("Current money:$ ",money)
            
    elif choice=='2':
        
        current_expected_value+=option2*chance2
        
        
        print()
        print("You chose option 2! Let's cross our fingers and hope for the best!")
        time.sleep(1)
        print("The wheel is spinning...")
        time.sleep(3)
        print()
        
        draw=random.randint(1,100)
        if draw<=chance2:
            money+=option2
            print("Congratulations! You just won $",option2," !")
            time.sleep(1)
            print("Current money:$ ",money)
        else:
            print("I'm sorry. Seems like python's random.randint() is not on your side today!")
            time.sleep(1)
            print("Current money:$ ",money)
        
    else:
        print("You obviously do not have a sane mind at the moment. \
        Unfortunately, since you were talking gibberish, you were disqualified from this round.")
        
    time.sleep(1)
    
    next_round=input("When you are ready, enter any character.")
    
    print("__________________________________________________________________")


while(i>0):
    gameloop()
    i-=1
    

time.sleep(1)
print()

print("That's all the rounds! Now, let's see how well you did (I'm guessing not well at all):")

time.sleep(1)
print()
print("Calculating...")
print()
time.sleep(3)
    
if max_expected_value==current_expected_value:
    print("Wow! You really know your stuff! Your expected value from playing this game is the maximum possible of $",round(max_expected_value),"! Good job!")
    
else:
    print("Hmm... I guess SLS Decision Making is just not burned into your brain hard enough. \
    Your expected value is $",max_expected_value - current_expected_value," away from the optimal expected value of $",max_expected_value,". In other words, I wouldn't reccomend gambling.")
    
print("How much money you earned, however...")

print()

time.sleep(2)

print()

print("Your money: $",money)

print()

print("Maximum amount of money possible: $",max_money)

time.sleep(1)

print()

if money>=max_money:
    print("Wait. You got the maximum amount possible?!?! Stop hacking.")
else:
    if max_expected_value==current_expected_value:
        print("Well, you were doing pretty well on expected value, but sometimes you gotta take chances in life, you know?")
    else:
        print("Shocker. You failed on expected value and still expected something here? I suggest you do some homework next time.")