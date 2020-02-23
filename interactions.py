
import random
import numpy as np
import termios
import sys, tty
import time

# Colors
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

CEND = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW_GREEN = '\033[33m'
ORANGE = '\033[93m'
BLUE = '\033[94m'
BOLD = '\033[1m'
GRAY = '\033[90m'

# Function that has one character as input
def getch():
    def _getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    return _getch()

# Press enter to continue function
def press_enter():
    a = "a"
    while a != "":
        a = input("\nPress " + GREEN + "ENTER" + CEND + " to continue\n\n")

class Map:
    # Start by making the map as a list
    def __init__(self):
        self.__map = []
        self.objectList = []
        self.__coordinates = []
        self.counter = 0
        self.portal_open = False
        self.reseted = False
        self.map_legend = ("[ + ] : Adventurer\n[ S ] : Scroll\n[ & ] : Villager\n[ Z ] : Zombie\n[ G ] : Ghost\n[ ^ ] : Health Potion\n[ ! ] : Damage Potion\n[ M ] : Fire\n[ % ] : Explosive Mine\n[ $ ] : Blaze Sword\n[ | ] : Steel Sword\n[ A ] : Aqua Sword\n[ ? ] : Key\n[ § ] : Boss")
        self.reset_counter = 0

    # Reset map to only nothing
    def reset(self):

        self.objectList = []
        for x in range(169):
            self.addObject(Nothing, 1)

        self.locationGen()
        


    # For each place on the map, adding a random choice from the list of objects, and having a tester to see if the number of objects exceeds a value    
    def setMap(self):

        self.__map = []

        for x in range(13):
            for y in range(13):
                for thing in self.objectList:
                    if thing.getPosition() == [x, y]:
                        self.__map.append(thing)
                        break



        self.__map = np.array(self.__map).reshape(13, 13)



    # Makes copy with str() method on all the objects
    def getMap(self):
        self.__copyMap = self.__map
        for index, value in np.ndenumerate(self.__copyMap):
            #print(index, value)
            self.__copyMap[index] = str(value)
        return self.__copyMap
    

    # Change a value of the array based on coordinate
    def editMap(self, y, x, item):
        self.__map[y, x] = item

    def removeItem(self, item):
        self.objectList.remove(item)

    # Find an object based on coordinate
    def findObject(self, coordinate, *rest):
        for item in self.objectList:
            if item.getPosition() == coordinate:
                if len(rest) == 0:
                    return item
                elif item != rest[0]:
                    return item

    # Check item based on class
    def check_object(self, class_name):

        for item in self.objectList:
            if isinstance(item, (class_name)):
                return True
        return False

    # Function for adding objects
    def addObject(self, classType, quantity, *rest):
        if classType == adventurer:
            self.objectList.append(adventurer)
            adventurer.setPosition([6,6])
        elif classType == boss:
            self.objectList.append(boss)
            boss.setPosition([0,0])
        else:
            for x in range(quantity):
                a = classType()
                if len(rest) > 0:
                    a.setPosition(rest[0])
                self.objectList.append(a)


    def locationGen(self):
        for x in range(13):
            for y in range(13):
                self.__coordinates.append([x, y])

        random.shuffle(self.objectList)

        for index, thing in enumerate(self.objectList):
            thing.setPosition(self.__coordinates[index])

    # Function to show the legend
    def legend(self):

        print()
        print(BOLD + "LEGEND" + CEND + " (P to close)")
        print(self.map_legend)
        print()
        exit_input = getch()
        while exit_input != 'p':
            exit_input = getch()
        print()

    def monstersCheck(self):

        for thing in self.objectList:
            if isinstance(thing, (Zombie, Ghost)):
                return True

        return False

    def openPortal(self):

        rand_coord = random.choice([ [0, 0], [12, 0], [12, 0], [12, 12] ])

        for item in self.objectList:
            if item.getPosition() == rand_coord and isinstance(item, (Nothing, BlazeSword, SteelSword, AdditionalHealth, AdditionalDamage)):
                coord = item.getPosition()
                self.removeItem(item)
                self.addObject(Portal, 1, coord)
                break

    # Firing mechanism for end game
    def fire(self, thing):

        if thing == adventurer:

            if adventurer.getGameMode() == 'easy':
                boss.setHealth(boss.getHealth() - 10)
            elif adventurer.getGameMode() == 'medium':
                boss.setHealth(boss.getHealth() - 20)
            elif adventurer.getGameMode() == 'hard':
                boss.setHealth(boss.getHealth() - 30)
            elif adventurer.getGameMode() == 'secret_mode':
                boss.setHealth(boss.getHealth() - 40)

    # Method for ending the game
    def endGame(self):

        print('\n' * 40)
        print(GREEN + "Game Over\n" + CEND)
        print("You " + BLUE + "WON" + CEND + "!")
        print('\nGame beaten on:', adventurer.getGameMode(), 'mode\n')
        print('Game Created by ' + BLUE + 'Mayank Hirani' + CEND + ' 2018-2020 (10th Grade to 11th Grade)')
        print('\nProject given by ' + BLUE + 'John Wolff' + CEND + '\n')
        print(BOLD + 'mayank.hirani@icloud.com | MSAH15#9246 | u/MSAH15' + CEND)


    # Function to do any damage or anything every round
    def rotation(self, thing):



        if thing.fire_count == thing.fire_count_max:
            thing.setHealth(thing.getHealth() - 10)
            thing.fire_count -= 1
            print("\n-" + RED + "10" + CEND + " Health!\n")

        elif thing.fire_count > 0:
            thing.setHealth(thing.getHealth() - 5)
            thing.fire_count -= 1
            print("\n-" + RED + "5" + CEND + " Health!\n")

        if isinstance(thing.weapon_equipped, AquaSword):

            if thing.getGameMode() == "easy":
                regen_amount = 75
                regen_rate = 5
            elif thing.getGameMode() == "medium":
                regen_amount = 75
                regen_rate = 1
            elif thing.getGameMode() == "hard":
                regen_amount = 50
                regen_rate = 1
            else:
                regen_amount = 100000000000
                regen_rate = 10000000

            if thing.getHealth() <= regen_amount - regen_rate:
                thing.setHealth(thing.getHealth() + regen_rate)
            elif thing.getHealth() <= regen_amount:
                thing.setHealth(regen_amount)

        
        if self.reseted:

            

            if boss.getHealth() <= 0:
                theMap.endGame()


            # Move each arrow (Interactions are also included here)
            for arrow in self.objectList:

                if isinstance(arrow, Arrow):

                    if arrow.dont_move:
                        arrow.dont_move = False

                    else:

                        theMap.addObject(Nothing, 1, arrow.getPosition())

                        arrow.setPosition([arrow.getPosition()[0], arrow.getPosition()[1] + 1])
                        if isinstance(self.findObject(arrow.getPosition(), arrow), Arrow):
                            theMap.removeItem(self.findObject(arrow.getPosition(), arrow))
                        elif isinstance(self.findObject(arrow.getPosition(), arrow), Adventurer):
                            arrow.interaction(arrow, adventurer)

                        if isinstance(theMap.findObject(arrow.getPosition(), arrow), Nothing):
                            theMap.removeItem(theMap.findObject(arrow.getPosition(), arrow))

                        if arrow.getPosition()[1] not in [x for x in range(13)]:
                            theMap.removeItem(arrow)
            
            # Follow the adventurer around
            if boss.getPosition()[0] != adventurer.getPosition()[0]:

                theMap.removeItem(theMap.findObject([adventurer.getPosition()[0], 0]))
                theMap.addObject(Nothing, 1, boss.getPosition())
                boss.setPosition([adventurer.getPosition()[0], 0])
            
            if self.reset_counter >= 2 and self.reset_counter % 3 != 0:
                # Add an arrow infront of the boss
                theMap.removeItem(theMap.findObject([boss.getPosition()[0], 1]))
                theMap.addObject(Arrow, 1, [boss.getPosition()[0], 1])
            
            self.reset_counter +=1
            if adventurer.arrow_cooldown < 4:
                adventurer.arrow_cooldown += 1
        
        for monster in self.objectList:
            if isinstance(monster, (Zombie, Ghost)):
                if monster.fire_tick > 0:
                    monster.fire_tick -= 1
                    monster.setHealth(monster.getHealth() - (int(thing.getDamage() / 20)))
                    if monster.getHealth() <= 0:
                        self.addObject(Nothing, 1, monster.getPosition())
                        self.removeItem(monster)
                        print(monster.getName() + RED + " burned" + CEND + " to death!")
        

        if self.monstersCheck() == False and thing.visited_bossinfo == True:
            
            if self.portal_open == False:

                self.openPortal()
                self.portal_open = True



    # Is called every cycle

    def creation(self, thing):

        # Make end-game stats

        self.rotation(thing)
        
        if adventurer.getHealth() <= 0:
            print("Game Over! You died!")
            sys.exit()

        # Things to be done every rotation
        self.setMap()

        if self.reseted == False:
            print(BLUE + "Inventory" + CEND + ": Press " + BLUE + "E" + CEND + " to open | " + BLUE + "Legend" + CEND + ": Press " + BLUE + "P" + CEND + " to open")
        else:
            print(BLUE + "Grenade" + CEND + ": Press " + BLUE + "E" + CEND + " to throw")
        print('\n')

        if self.reseted == False:
            print(BLUE + "Weapon Equipped: " + CEND + str(thing.displayWeapon()))
        else:
            print('Cooldown: ' + ('█' * adventurer.arrow_cooldown) + ('░' * (4-adventurer.arrow_cooldown)))
        
        print(self.getMap())
        print(thing.getDisplayPosition() + '\t\t', end='')
        thing.displayHealth()
        if self.reseted == False:
            print('   Damage: ' + ORANGE + str(thing.getDamage()) + CEND)
        else:
            print(' | Boss: ' + boss.displayHealth())
        print('\n\n\n')


    def __str__(self):
        for thing in self.objectList:
            return str(thing)
        
# General class for all objects + creatures + items, should all be able to move

class Things:

    def __init__(self):
        iuh3r = True
        self.__x = "Not set!"
        self.__y = "Not set!"
        self.name = "Not set!"
        self.fire_tick = 0

    def getName(self):
        return self.name

    def getPosition(self):
        return [self.__x, self.__y]

    def getDisplayPosition(self):

        new_x = self.getY()+1
        new_y = 13-self.getX()

        new_coord = "["


        if new_x < 10:
            new_coord += " "
        new_coord += BLUE + str(new_x) + CEND + ", "
        new_coord += BLUE + str(new_y) + CEND
        if new_y < 10:
            new_coord += " "
        
        new_coord += "]"
        
        

        return new_coord


    def setPosition(self, coordinate):
        self.__x = coordinate[0]
        self.__y = coordinate[1]

    def getY(self):
        return self.__y

    def getX(self):
        return self.__x

    def setY(self, value):
        self.__y = value

    def setX(self, value):
        self.__x = value

    def __str__(self):
        return "ERROR!!!"
        
class MovingThings(Things):
    
    def __init__(self):
        Things.__init__(self)
        self.name = "Moving Things"
        self.inventory_size = 6


    def inventorySize(self):
        return self.inventory_size

    def set_inv_size(self, size):
        self.inventory_size = size
        
    def move(self, direction, steps):
        
        self.tempLoc = self.getPosition()
        
        if direction == 'w':
            self.setX(self.getX() - 1)
            if self.canMove() == False:
                self.setPosition(self.tempLoc)
                
        elif direction == 'a':
            self.setY(self.getY() - steps)
            if self.canMove() == False:
                self.setPosition(self.tempLoc)

        elif direction == 's':
            self.setX(self.getX() + steps)
            if self.canMove() == False:
                self.setPosition(self.tempLoc)
                
        elif direction == 'd':
            self.setY(self.getY() + steps)
            if self.canMove() == False:
                self.setPosition(self.tempLoc)

        self.moves.append(self.getPosition())
        
        if self.canMove():
            self.interaction(adventurer, theMap.findObject(adventurer.getPosition(), adventurer))
            
    def canMove(self):

        if self.getX() < 0 or self.getY() < 0 or self.getX() > 12 or self.getY() > 12:
            return False
        else:
            return True



    def interaction(self, thing1, thing2):

        
        
        if isinstance(thing1, Adventurer):

            if isinstance(thing2, Nothing):

                thing1.setPosition(thing2.getPosition())
                thing2.setPosition(self.tempLoc)
                
            if isinstance(thing2, (Zombie, Ghost)):

                if isinstance(thing1.weapon_equipped, BlazeSword):

                    thing2.fire_tick = 5
                

                print("You attack the " + RED + thing2.getName() + CEND)
                time.sleep(1)
                thing2.setHealth(thing2.getHealth() - thing1.getDamage())

                # Make it so that it is not glitchy with printing on same line

                if thing2.getHealth() <= 0:

                    print("Enemy defeated!\n")
                    theMap.removeItem(thing2)
                    theMap.addObject(Nothing, 1, self.tempLoc)
                    thing1.addKill()

                else:
                    thing1.setPosition(self.tempLoc)
                    health_taken = thing2.getDamage()
                    thing1.setHealth(thing1.getHealth()-health_taken)

                    print("Enemy Health Remaining:", thing2.getHealth())
                    time.sleep(1)

                    print(RED + thing2.getName() + CEND + " attacks you!")
                    time.sleep(1)

                    print('\n\n')

            if isinstance(thing2, (AdditionalHealth, AdditionalDamage, BlazeSword, SteelSword)):

                            
                if (len(thing1.getInventory()) >= thing1.inventorySize()) and (thing1.getGameMode() != "secret_mode"):
                    thing1.setPosition(self.tempLoc)
                    print(RED + "\nInventory Full!\n" + CEND)
                else:
                    thing1.addItem(thing2)
                    thing1.setPosition(thing2.getPosition())
                    theMap.removeItem(thing2)
                    theMap.addObject(Nothing, 1, self.tempLoc)

            if isinstance(thing2, (Mine, Fire)):

                if isinstance(thing2, (Fire)):

                    thing1.fire_on()
                    thing1.setPosition(self.tempLoc)

                elif isinstance(thing2, (Mine)):

                    thing1.setHealth(thing1.getHealth() - thing2.getDamage())
                    theMap.removeItem(thing2)
                    thing1.setPosition(thing2.getPosition())
                    theMap.addObject(Nothing, 1, self.tempLoc)
                    print("\n-" + RED + str(thing2.getDamage()) + CEND + " Health!\n")

            if isinstance(thing2, (InfoScroll, BossInfo)):

                if (isinstance(thing2, BossInfo) and thing1.visited_edward == False):

                    print(RED + "\nVisit Edward before you read me!\n" + CEND)
                    thing1.setPosition(self.tempLoc)
                    time.sleep(1)

                else:

                    print("\n" + thing2.getMessage() + "\n")
                    theMap.addObject(Nothing, 1, self.tempLoc)
                    thing1.addItem(thing2)
                    theMap.removeItem(thing2)

                    # GIVE KEY HERE
                    if isinstance(thing2, (BossInfo)):

                        thing1.addItem(key)

                    print("\nPress " + GREEN + "ENTER" + CEND + " to continue\n")
                    a = "a"
                    while a != "":
                        a = input()

                    if isinstance(thing2, BossInfo):
                        thing1.visited_bossinfo = True
                        print("+Item: " + ORANGE + "Key" + CEND + "\n")
                        time.sleep(1)

            if isinstance(thing2, (NPC)):

                if isinstance(thing2, (Edward)):
                    # Make sure they have read info scroll
                    thing1.setPosition(self.tempLoc)

                    press_enter()

                    if theMap.check_object(InfoScroll) != False:
                        print("\nRead the " + GREEN + "INFO SCROLL" + CEND + " near me before you talk to me!\n")
                        time.sleep(2)
                    else:
                        thing2.chat()
                        thing1.visited_edward = True

                elif isinstance(thing2, (Samuel)):


                    thing1.setPosition(self.tempLoc)

                    if thing2.has_won == False:

                        choice = input("Trade" + GREEN + " 10 " + CEND + "health for a chance to win the" + BLUE + " Aqua Sword" + CEND + "?\n\nPress " + GREEN + "ENTER" + CEND + " to continue\n\n")

                        if choice == "":

                            if thing1.getHealth() > 10:

                                thing1.setHealth(thing1.getHealth() - 10)

                                if thing2.has_visited == False:
                                    thing2.chat()

                                doors = [" Door 1 ", " Door 2 ", " Door 3 "]

                                

                                selected = 0
                                user_input = "fdgrrwerw"

                                while user_input != "f":

                                    new_doors = []
                                    for item in doors:
                                        new_doors.append(item)

                                    new_doors[selected] = "[" + doors[selected][1:7] + "]"
                                    print(new_doors, end='\r')
                                    user_input = getch()

                                    if user_input == "a" and selected != 0:
                                        selected -= 1
                                        
                                    elif user_input == "d" and selected != 2:
                                        selected += 1

                                    elif user_input == "f":
                                        if selected == thing2.correct_door:
                                            print()
                                            thing1.addItem(aqua_sword)
                                            print("\n\n+Item: " + BLUE + "Aqua Sword" + CEND + "\n\n")
                                            time.sleep(1)
                                            thing2.has_won = True
                                            
                                        else:
                                            print("\n\n" + RED + "WRONG DOOR!" + CEND + "\n\n")
                                            thing2.has_visited = True
                                            time.sleep(1)

                            elif thing1.getHealth() <= 10:
                                print(RED + "\nYou do not have enough health to attempt the guess!\n" + CEND)
                                time.sleep(1)

                    else:
                        print(RED + "\n\nYou have already acquired the Aqua Sword!\n\n" + CEND)

            if isinstance(thing2, (Portal)):

                # Check to see if they arent using portal after boss has been spawned
                if thing2.been_used == False:

                    enter_input = input("\nPress " + GREEN + "ENTER" + CEND + " to use your " + ORANGE + "key" + CEND + " to unlock the Portal\n\n")

                    if enter_input == "":

                        theMap.reseted = True

                        thing2.been_used = True
                        thing1.removeItem(key)

                        # Create an empty map
                        theMap.reset()
                        
                        theMap.removeItem(theMap.findObject([6, 12]))
                        theMap.addObject(adventurer, 1)
                        thing1.setPosition([6, 12])
                        
                        # Create random coordinate to spawn boss on the left side of map

                        rand_coord = []
                        while rand_coord in [thing1.getPosition(), thing2.getPosition(), [6, 6], []]:
                            rand_coord = [random.randint(0, 12), 0]

                        theMap.removeItem(theMap.findObject(rand_coord))
                        theMap.addObject(boss, 1)
                        boss.setPosition(rand_coord)

                        theMap.setMap()

                        time.sleep(2)

                        boss.is_tired = False
                        
                    else:
                        thing1.setPosition(self.tempLoc)

                else:

                    thing1.setHealth(0)

        elif isinstance(thing1, Arrow):

            # Interaction between arrow and boss/adventurer
            if isinstance(thing2, (Boss, Adventurer)):

                thing2.setHealth(thing2.getHealth() - 50)
                theMap.removeItem(thing1)

                                

                
class Nothing(Things):
    
    def __init__(self):
        Things.__init__(self)

    def __str__(self):
        return " "

# Adventurer class of object class, has health and inventory

class Adventurer(MovingThings):

    def __init__(self):
        
        MovingThings.__init__(self)
        
        self.__health = 100
        self.__inventory = []
        self.name = "Adventurer Name"
        self.__damage = 5
        self.moves = []
        self.game_mode = ""
        self.fire_count = 0
        self.fire_count_max = -1
        self.weapon_equipped = None
        self.weapon_boost = 0
        self.kills = 0
        self.visited_edward = False
        self.visited_bossinfo = False
        self.arrow_cooldown = 4
        

    def setGameMode(self, gamemode):
        if gamemode == 1:
            self.game_mode = "easy"
        elif gamemode == 2:
            self.game_mode = "medium"
        elif gamemode == 3:
            self.game_mode = "hard"
        elif gamemode == 4:
            self.game_mode = "secret_mode"

    def getGameMode(self):
        return self.game_mode
        
    def setHealth(self, newHealth):
        self.__health = newHealth

    def addItem(self, item):
        self.__inventory.append(item)

    def removeItem(self, item):
        self.__inventory.remove(item)

    def getHealth(self):
        return self.__health

    def getInventory(self):
        return self.__inventory

    def getDamage(self):
        return self.__damage

    def setDamage(self, damage):
        self.__damage = damage

    def getKills(self):
        return self.kills

    def addKill(self):
        self.kills += 1

    def displayWeapon(self):

        if self.weapon_equipped == None:

            return "None"

        else:

            name = self.weapon_equipped.getName()

            return name

    def displayHealth(self):

        if self.__health >= 80:
            print('Health: ' + GREEN + str(self.__health) + CEND, end='')

        elif self.__health >= 50:
            print('Health: ' + YELLOW_GREEN + str(self.__health) + CEND, end='')

        elif self.__health >= 30:
            print('Health: ' + ORANGE + str(self.__health) + CEND, end='')

        elif self.__health >= 0:
            print('Health: ' + RED + str(self.__health) + CEND, end='')

    # Where the adventurer can use items in inventory, called in openInventory() function below
    def useItem(self, item):
        
        if isinstance(item, AdditionalHealth):
            self.__health += item.getHealthBoost()
            print("\n+" + GREEN + str(item.getHealthBoost()) + CEND + " Health!\n")

        elif isinstance(item, AdditionalDamage):
            self.__damage += item.getDamageBoost()
            print("\n+" + GREEN + str(item.getDamageBoost()) + CEND + " Damage!\n")

        elif isinstance(item, (BlazeSword, AquaSword, SteelSword)):
            if self.weapon_equipped != None:
                self.__damage -= self.weapon_equipped.getDamageBoost()

            self.weapon_equipped = item
            self.__damage += item.getDamageBoost()
            print("\n" + RED + item.getName() + CEND + " equiped | +" + GREEN + str(item.getDamageBoost()) + CEND + " Damage Boost!\n" + CEND)

        elif isinstance(item, Scrolls):
            print("\n" + str(item.getName()) + ":\n" + item.getMessage() + "\n")
            press_enter()
            




            
    # Used when checking if there is another weapon in inventory
    def check_inv_weapon(self):
        for item in self.__inventory:
            if isinstance(item, weapons):
                return True

    def current_weapon(self):
        for item in self.__inventory:
            if isinstance(item, (Weapons)):
                return item


             
    def openInventory(self):
        
        selected = 0
        new_inv = []
        
        for item in self.__inventory:
            new_inv.append(str(item))
        if len(self.__inventory) > 0:
            new_inv[selected] = '[' + new_inv[selected] + ']'
        print("Inventory (E to close):", new_inv, end='\r')
        choice = 0
        
        while choice != 'e':
            choice = getch()
            
            
            if choice == 'a' and selected != 0 and len(self.__inventory) > 0:
                selected -= 1
                new_inv = []
                for item in self.__inventory:
                    new_inv.append(str(item))
                new_inv[selected] = '[' + new_inv[selected] + ']'
                
            elif choice == 'd' and selected != len(self.__inventory) - 1 and len(self.__inventory) > 0:
                selected += 1
                new_inv = []
                for item in self.__inventory:
                    new_inv.append(str(item))
                new_inv[selected] = '[' + new_inv[selected] + ']'

            # Printing the inventory or using item
            
            elif choice == 'f':

                if len(self.__inventory) > 0:
                    print()
                    self.useItem(self.__inventory[selected])

                    # Keep scrolls in inventory after use, otherwise delete
                    if (isinstance(self.__inventory[selected], Scrolls) == False and self.__inventory[selected] != key) and isinstance(self.__inventory[selected], Sword) == False:
                        del self.__inventory[selected]

                    selected = 0
                    new_inv = []

                    if len(self.__inventory) > 0:
                        for item in self.__inventory:
                            new_inv.append(str(item))
                        new_inv[selected] = '[' + new_inv[selected] + ']'

                    print("Inventory (E to close):", new_inv, end='\r')

            # Equip nothing

            elif choice == 'q':

                if isinstance(self.__inventory[selected], (BlazeSword, AquaSword, SteelSword)):

                    self.__damage -= self.weapon_equipped.getDamageBoost()
                    print('\n')
                    print('Unequipped: ' + self.weapon_equipped.getName())
                    print()
                    time.sleep(1)
                    self.weapon_equipped = None
                    break

                elif isinstance(self.__inventory[selected], (BossInfo, InfoScroll)) == False:

                    self.removeItem(self.__inventory[selected])
                    break


            if choice != 'f':
                print("Inventory (E to close):", new_inv, end='\r')

    # Function to begin the fire count if interaction with fire
    def fire_on(self):

        self.fire_count = 10
        self.fire_count_max = self.fire_count + 0
            
    def __str__(self):
        return "+"

# Talking NPCs

class NPC(MovingThings):

    def __init__(self):

        MovingThings.__init__(self)
        self.name = "Civilian"
        self.messages = []

    def chat(self):

        print(BOLD + self.name + CEND + ":")
        for item in self.messages:
            print("\n" + item + "\n")
            time.sleep(1)
            press_enter()

    def __str__(self):
        return "&"

# NPC at start
class Edward(NPC):

    def __init__(self):

        NPC.__init__(self)
        self.name = "Edward"
        self.message1 = "Hi and welcome to our world!"
        self.message2 = "We are in need of your help."
        self.message3 = "In order to defeat the " + RED + "BOSS" + CEND + " that we told you about, you will need to find the boss info scroll."
        self.message4 = "We have not seen it in years, but we know its somewhere along the " + GREEN + "edge of our world" + CEND

        self.messages = [self.message1, self.message2, self.message3, self.message4]

# NPC who does guessing game for sword
class Samuel(NPC):

    def __init__(self):

        NPC.__init__(self)
        self.name = "Samuel"
        self.message1 = "Thank you for providing me with the 10 health."
        self.message2 = "I will provide you with " + BOLD + "3" + CEND + " doors."
        self.message3 = "Behind one of them is the mystical " + BLUE + "Aqua Sword" + CEND + "."
        self.message4 = "If you guess it correctly, you may take the sword with you."
        self.has_visited = False
        self.has_won = False
        self.correct_door = random.randint(0, 2)

        self.messages = [self.message1, self.message2, self.message3, self.message4]

# The Final Portal unlocked after killing monsters and getting key

class Portal(Things):

    def __init__(self):
        Things.__init__(self)
        self.count = -1
        self.been_used = False

    def __str__(self):

        visuals = ['#', '@', '*', '∂', '∑', 'ø', '◊', 'π', '∆', '£', '√', 'Ω', 'µ']
        if self.count >= 12:
            self.count -= 12
        else:
            self.count += 1
        
        return visuals[self.count]

# Arrows to shoot at end

class Arrow(MovingThings):

    def __init__(self):
        self.direction = 0
        self.fired_by = 0
        self.dont_move = True

    def activate(self, thing):
        if isinstance(thing, Adventurer):
            self.direction = "left"
        elif isinstance(thing, Boss):
            self.direction = "right"

    def __str__(self):
        return ">"

# The key to unlock the portal to boss

class Key(Things):

    def __init__(self):
        pass

    def __str__(self):
        return "?"

key = Key()

# Scrolls Info

class Scrolls(Things):
    
    def __init__(self):
        Things.__init__(self)
        self.message = ""

    def getMessage(self):
        return self.message

    def __str__(self):
        return "S"

class BossInfo(Scrolls):

    def __init__(self):

        Scrolls.__init__(self)
        self.message = "To defeat the evil " + RED + "BOSS" + CEND + ", you must defeat all of his monster henchmen. Once they are all terminated, reach the " + BLUE + "portal " + CEND + "and you will reach the boss.\nTake this key, it will be used to unlock the boss portal:\n"
        self.name = "Boss Info Scroll"


class InfoScroll(Scrolls):

    def __init__(self):
        
        Scrolls.__init__(self)

        self.name = "Info Scroll"
        
        self.message = "The goal of your adventure is to defeat the evil goblin lord, who has been ruling the lands for many decades. Around you, you will see " + BLUE + "weapons" + CEND + ", " + GREEN + "power ups" + CEND + ", and " + RED + "monsters" + CEND + ". The monsters are evil creatures who will stop at nothing to destroy you. Kill and terminate all of the monsters to open the portal to the goblin lord. Once you defeat the goblin lord, you will be able to save the world!"


# Monster class of the object class, has health and damage

class Monster(MovingThings):
    
    def __init__(self):
        MovingThings.__init__(self)
        self.health = 0
        self.damage = 0

    def getDamage(self):
        return self.damage

    def getHealth(self):
        return self.health

    def setHealth(self, newHealth):
        self.health = newHealth

# Zombie class of monster class can move, health + damage from super classes, but has specific number of health/damage

class Zombie(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.health = 10
        self.damage = 5

        self.name = "Zombie"
        
    def __str__(self):
        return "Z"

class Ghost(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.health = random.randint(20, 51)

        self.damage = 50
        self.name = "Ghost"
        
    def __str__(self):
        return "G"

class Hunter(Monster):
    
    def __init__(self):
        Monster.__init__(self)
        self.__health = 15
        self.__damage = 85

    def __str__(self):
        return "H"

class Phantom(Ghost):
    def __init__(self):
        Ghost.__init__(self)

    def __str__(self):
        return "G2"

class Boss(Monster):

    def __init__(self):
        Monster.__init__(self)
        self.count = -1
        self.is_tired = False
        self.tired_count = 15
        self.shoot_arrow_round = False

    def initiateHealth(self):
        healths = {"easy":100, "medium":200, "hard":300, "secret_mode":50}
        self.health = healths[adventurer.getGameMode()]
        self.starting_health = self.health

    def displayHealth(self):
        if self.health == self.starting_health:
            return GREEN + '✔' + CEND
        elif self.health > 0.75 * self.starting_health:
            return YELLOW_GREEN + '¾' + CEND
        elif self.health > 0.50 * self.starting_health:
            return ORANGE + '½' + CEND
        elif self.health > 0.25 * self.starting_health:
            return RED + '¼' + CEND
        else:
            return '✘'

    def __str__(self):

        return "§"


class Weapons(Things):
    
    def __init__(self):
        Things.__init__(self)
        self.damage = 0

    def attack(self, direction):
        return # FIX THIS

class Sword(Weapons):
    
    def __init__(self):
        Weapons.__init__(self)
        self.attackRange = 1
        self.damageBoost = 5

    def getDamageBoost(self):
        return self.damageBoost

class SteelSword(Sword):

    def __init__(self):
        Sword.__init__(self)
        self.damageBoost = 10
        self.name = GRAY + "Steel Sword" + CEND

    def __str__(self):
        return "|"

class BlazeSword(Sword):
    
    def __init__(self):
        Sword.__init__(self)
        self.damageBoost = 30
        self.name = RED + "Blaze Sword" + CEND

    def __str__(self):
        return "$"

class AquaSword(Sword):

    def __init__(self):
        Sword.__init__(self)
        self.damageBoost = 20
        self.name = BLUE + "Aqua Sword" + CEND

    def __str__(self):
        return "A"

aqua_sword = AquaSword()

class Traps(Things):

    def __init__(self):
        Things.__init__(self)

class Mine(Traps):

    def __init__(self):
        Traps.__init__(self)
        self.damage = 10 * random.randint(5, 8)

    def getDamage(self):
        return self.damage

    def __str__(self):
        return "%"

class Fire(Traps):

    def __init__(self):
        pass

    def __str__(self):
        return "M"
        
        
class PowerUps(Things):
    
    def __init__(self):
        Things.__init__(self)


class AdditionalHealth(PowerUps):
    
    def __init__(self):
        PowerUps.__init__(self)
        self.__health_boost = random.randint(1, 11) * 5
        self.__name = "Additional Health"

    def getHealthBoost(self):
        return self.__health_boost

    def __str__(self):
        return "^"

class AdditionalDamage(PowerUps):
    
    def __init__(self):
        PowerUps.__init__(self)
        self.__damage_boost = 10
        self.__name = "Additional Damage"

    def getDamageBoost(self):
        return self.__damage_boost

    def __str__(self):
        return "!"

        
power_ups = (AdditionalHealth, AdditionalDamage)
monsters = (Zombie, Ghost, Phantom, Hunter, Monster)
weapons = (BlazeSword, SteelSword, AquaSword)
adventurer = Adventurer()
boss = Boss()
theMap = Map()
