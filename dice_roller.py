from random import randint
import os


popular_dice_amount_of_sides = [4,6,8,12,20,100]
def rollDice(sides: int) -> int:
    return randint(1, sides)
def rollMultipleDice(sides:int or list, times: int) -> int:
    rolls = []
    for count in range(times):
        if type(sides) == int:
            rolls.append(rollDice(sides))
        elif type(sides) == list:
            rolls.append(rollDice(sides[count]))
    return rolls

def proballityOfRoll(data: list[dict]) -> int:
    rolls = 0
    chance = 1
    for entry in data:
        rolls += 1 if entry.get("times") is None else int(entry.get("times"))
        chance *= int(entry.get("sides"))
        

    return float(rolls/chance)

all_rolls = []
while True:
    i = 0
    if input("Use a conventional number dice? (yes/no) ").strip().lower() == "yes":
        i = int(input("Which one out of {} would you like to used? (yes/no) ".format(str(popular_dice_amount_of_sides)))) 
    else:
        i = int(input("What Number Dice?  "))
    print("\n")
    d = int(input("How Many Dice? "))
    if d == 1:
        all_rolls.append({"sides":i})
        print(rollDice(i))
    else:
        all_rolls.append({"sides":i, "times":d})
        print("Rolls are: " + str(rollMultipleDice(i, d)))
    if input("Get total probability of all number combinations you've recieved in this session? (yes/no) ").strip().lower() == "yes":
        print("Change of happening " + str(proballityOfRoll(all_rolls)*100) + "%")
    
    if input("Do you want to continue? (yes/no) ").strip().lower() == "yes":
        os.system("clear")
        continue
    else:
        break

print(all_rolls)