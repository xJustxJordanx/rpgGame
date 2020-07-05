# This is the final project for phase 1.
# Emulate a DnD, one-on-one battle!
# Goal 1: Must be interactive.
# Goal 2: Use a function in a module we have not yet explored.

# Rules:
# Must use at least one class
# Must use at least one dictionary
# Must use math
# Import and use at least one module
# Must use loops and if/else

# Importing modules
import random
import time

# The adventurer lives!
isAlive = True
hasFleed = False
currentGold = 0

# List of stats for all abilties
weapons = {
#   "example":[atkBonus, dmgBonus, dmgDiceQuantity, dmgDiceSides, healBonus, healDiceQuantity, healDiceSides], 
    "longsword":[4, 2, 1, 8, 0, 0, 0],
    "dagger":[4, 2, 1, 4, 0, 0, 0],
    "shortbow":[4, 2, 1, 6, 0, 0, 0],
    "heal":[0, 0, 0, 0, 0, 3, 4],
    "fireball":[4, 0, 3, 6, 0, 0, 0],
    "slam":[3, 1, 1, 6, 0, 0, 0],
    "scimitar":[4, 2, 1, 6, 0, 0, 0],
    "shortsword":[4, 2, 1, 6, 0, 0, 0]
}

# List of possible enemies
possibleEnemies = [
    ("zombie", 22, 8),
    ("goblin", 7, 15),
    ("skeleton", 13, 13)
]

# Dice-rolling function
def d(qty, sides):
    """Accepts a value for number of sides and quantity of dice, then rolls those dice."""
    value = 0
    while qty > 0:
        value = value + random.randint(1, sides)
        qty = qty - 1
    return value

# Player class information
class dndType:
    isPlayer = False
    def __init__(self, name, maxHP, AC):
        self.name = name
        self.maxHP = maxHP
        self.currentHP = maxHP
        self.AC = AC
        if self.name == "warrior":
            self.actions = ["longsword", "dagger"]
        elif self.name == "mage":
            self.actions = ["heal", "fireball"]
        elif self.name == "rogue":
            self.actions = ["dagger", "shortbow"]
        elif self.name == "zombie":
            self.actions = ["slam"] 
        elif self.name == "goblin":
            self.actions = ["scimitar", "shortbow"] 
        elif self.name == "skeleton":
            self.actions = ["shortsword", "shortbow"]    



# Player action function
def action(user, device, target):
    if weapons[device][0:4] != [0, 0, 0, 0]: # If attacking stats are not zero,
        attackRoll = ( d(1, 20) + weapons[device][0] ) # Roll a d20 and add the attack bonus
        if attackRoll >= target.AC: # Compare the attack roll to the target's AC
            damage = ( d(weapons[device][2], weapons[device][3]) + weapons[device][1] ) # Calculate damage
            target.currentHP = target.currentHP - damage # Remove damage from target's HP
            if user.isPlayer:
                print(f"Your attack hits the {target.name} and does {damage} damage!".format())     
            else:
                print(f"The {user.name} hits you using {device} and does {damage} damage!".format()) 
                print(f"Your HP is {target.currentHP}/{target.maxHP}.\n".format())
        else:
            print(f"{user.name.capitalize()} attacks {target.name} using a {device}, but misses!\n".format())
    if weapons[device][4:7] != [0, 0, 0]: # If healing stats are not zero,
        recovery = ( d(weapons[device][5], weapons[device][6]) + weapons[device][4] ) # Calculate recovery
        user.currentHP = user.currentHP + recovery # Apply recovery to the user's HP
        if user.currentHP > user.maxHP:
            user.currentHP = user.maxHP
        if user.isPlayer:
            print(f"You used {device} and healed for {recovery}HP! Your health is now {user.currentHP}/{user.maxHP}\n".format())
        else:
            print(f"{user} used {device} and healed itself!\n".format())



#
# PROGRAM ACTUALLY STARTS HERE
#

# Opening dialogue/
print("\nWelcome, adventurer!")
print("Hope you enjoy the game!\n")

# Start of while loop for error handling in class selection
while True:
    
    # Ask user which type of character they would like to play
    print("First, which class would you like to take?")
    classSelection = input("1.) Warrior, 2.) Mage, or 3.) Rogue? ")

    # Uses input to define class dndType
    if classSelection == "1" or classSelection.lower() == "warrior":
        player = dndType("warrior", 50, 16)
        break
    elif classSelection == "2" or classSelection.lower() == "mage":
        player = dndType("mage", 30, 12)
        break
    elif classSelection == "3" or classSelection.lower() == "rogue":
        player = dndType("rogue", 40, 14)
        break
    else:
        print("ERROR: Class selection not understood!\n")

# Marks the player as a player in the dndType class
player.isPlayer = True

# Gives the user relevant info about the class they chose
print(f"\nYou have chosen {player.name}!".format())
print(f"{player.name.capitalize()} has an AC (armor class) of {player.AC} and a maximum HP (hit points) of {player.maxHP}.".format())
print(f"It can use a {player.actions[0]} or a {player.actions[1]}.".format())
input("Press ENTER to continue!\n")


# Record time battle begins
startTime = time.time()

# Core gameplay loop
while isAlive == True and hasFleed == False:

    # This will choose from the list of enemies randomly
    randomEnemy = possibleEnemies[random.randint(0, (len(possibleEnemies) - 1))]
    # Define creates the next enemy
    enemy = dndType(randomEnemy[0], randomEnemy[1], randomEnemy[2])

    # Introduce encounter
    print(f"A wild {enemy.name} appears!".format())
    print()

    # Single battle loop
    while True:
    
        # Player action
        playerAction = input(f"What do you do? 1.) {player.actions[0].capitalize()} 2.) {player.actions[1].capitalize()} 3.) Run ".format())
        if playerAction == "1" or playerAction.lower() == player.actions[0]:
            action(player, player.actions[0], enemy)
        elif playerAction == "2" or playerAction.lower() == player.actions[1]:
            action(player, player.actions[1], enemy)
        elif playerAction == "3" or playerAction.lower() == "run away" or playerAction.lower() == "run":
            print("You got scared and ran away!\n")
            hasFleed = True
            break

        # Check if enemy is dead
        if enemy.currentHP <= 0:
            print(f"The {enemy.name} was slain!".format())
            goldEarned = random.randint(5, 15)
            currentGold += goldEarned
            print(f"You found {goldEarned} gold pieces, and now have {currentGold} gold!\n".format())
            break
        # Enemy action
        enemyAction = enemy.actions[random.randint(0, (len(enemy.actions)) - 1)]
        action(enemy, enemyAction, player)
        # Determine how many different actions the enemy has to choose from
        # Randomly choose an action for the enemy to take

        # Check if player is dead
        if player.currentHP <= 0:
            print(f"You were slain by the {enemy.name}! You have lost the game...".format())
            isAlive = False
            break

# Compare start time to end time, return time spent
endTime = time.time()
timeElapsed = int(endTime - startTime)
timeElapsedMinutes = int(timeElapsed // 60)
timeElapsedSeconds = timeElapsed % 60
print("You played for " + str(timeElapsedMinutes) + " minutes and " + str(timeElapsedSeconds) + " seconds!")
if isAlive == True:
    print(f"You earned {currentGold} gold pieces! Congrats!".format())
input("Press ENTER to exit the program. ")
