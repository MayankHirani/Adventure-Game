

# Created by Mayank Hirani 2018-2020
# Project given by John Wolff

import random
import numpy as np
import termios
import sys, tty
import interactions
from importlib import reload
reload(interactions)
from interactions import *

monsters = (Zombie, Ghost, Hunter, Phantom, Monster)


def startup():
    
    mode = 'not_int_or_q'

    while True:
        mode = input("\nSelect the mode:\nEasy (1)\nMedium (2)\nHard (3)\n\nMode: ")
        if mode == 'q':
            sys.exit()
        elif mode in ['1', '2', '3', '4']:
            mode = int(mode)
            adventurer.setGameMode(mode)
            break

    
# Getch Function
    print("\n\n| " + BLUE + "Use the WASD keys to move around (" + RED + "Q" + CEND + BLUE + " To Exit)" + CEND + " |\n\n" + '--------------------')
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



    
# Object Creation

    
    easy = {Ghost:1, Zombie:2, AdditionalDamage:3, AdditionalHealth:7, BlazeSword:1, SteelSword:1, Mine:1, Fire:1, Nothing:152}
    medium = {Ghost:3, Zombie:5, AdditionalDamage:2, AdditionalHealth:5, BlazeSword:1, SteelSword:1, Mine:2, Fire:1, Nothing:149}
    hard = {Ghost:4, Zombie:7, AdditionalDamage:1, AdditionalHealth:4, BlazeSword:1, SteelSword:1, Mine:3, Fire:1, Nothing:147}
    secret_mode = {AdditionalDamage:5, AdditionalHealth:10, BlazeSword:3, SteelSword:1, Nothing:150}

    modes = ['ignore_this', easy, medium, hard, secret_mode]
    
    total = 0
    for item in modes[mode]:
        theMap.addObject(item, modes[mode][item])
        total += modes[mode][item]
    if total != 169:
        raise ValueError


    # Inventory Size Depending on Mode
    if mode == '1':
        adventurer.set_inv_size(10)
    elif mode == '2':
        adventurer.set_inv_size(8)
    elif mode == '3':
        adventurer.set_inv_size(6)
    elif mode == '4':
        adventurer.set_inv_size(1000)
    
    theMap.locationGen()
        
    for thing in theMap.objectList:
        if thing.getPosition() == [6, 6]:
            theMap.removeItem(thing)
        if thing.getPosition() == [7, 6]:
            theMap.removeItem(thing)


    # Shuffle order & coordinates
    shuffled_list = theMap.objectList
    random.shuffle(shuffled_list)

    # Coordinates near the center
    coords_near = [ [6, 7], [6, 5], [7, 6], [5, 6], [5, 5], [5, 7], [7, 5], [7, 7] ]

    # Remove items and monsters from area around spawn
    for thing in shuffled_list:
        if (isinstance(thing, (Monster, Weapons, Traps, PowerUps)) and thing.getPosition() in coords_near):
            for item in shuffled_list:
                if isinstance(item, Nothing) and item.getPosition() not in coords_near:
                    save_coord = thing.getPosition()
                    thing.setPosition(item.getPosition())
                    item.setPosition(save_coord)
                    break

    # Putting info scroll near spawn
    for thing in shuffled_list:
        if (thing.getPosition() in [ [6, 7], [6, 5], [5, 6] ]) and isinstance(thing, (Weapons)) == False:
            theMap.addObject(InfoScroll, 1, thing.getPosition())
            theMap.removeItem(thing)
            break

    # Putting boss info scroll on outside of map        
    for thing in shuffled_list:
        if (isinstance(thing, Weapons) == False) and ((thing.getX() == 0 or thing.getX() == 12) ^ (thing.getY() == 0 or thing.getY() == 12)):
            theMap.addObject(BossInfo, 1, thing.getPosition())
            theMap.removeItem(thing)
            break

    # Putting Samuel NPC in upper right
    done = False
    for thing in shuffled_list:
        if (isinstance(thing, (Weapons, Monster)) == False) and (thing.getPosition() in [ [1, 1], [11, 1], [1, 11], [11, 11] ]):
            theMap.addObject(Samuel, 1, thing.getPosition())
            theMap.removeItem(thing)
            done = True
            break

    if done == False:
        for thing in shuffled_list:
            if isinstance(thing, Nothing):
                theMap.addObject(Samuel, 1, thing.getPosition())
                theMap.removeItem(thing)
                break


    theMap.addObject(adventurer, 1, [6, 6])

    theMap.addObject(Edward, 1, [7, 6])

    theMap.setMap()

    boss.initiateHealth()

    
    
# Prompt

    while True:

        theMap.creation(adventurer)
        

        if theMap.reseted == True:
            break

        move = getch()
        
        if move == 'q':
            confirmation = input("\nAre you sure you would like to " + RED + "QUIT" + CEND + " the game? (" + GREEN + "ENTER" + CEND + " for exit)\n\n")
            if confirmation == '':
                sys.exit()
            
        elif move in ['w', 'a', 's', 'd']:
            adventurer.move(move, 1)
            
        elif move == 'e':
            adventurer.openInventory()

        elif move == 'p':
            theMap.legend()

    # After reset end of game
    while True:

        if boss.getHealth() <= 0:
            break

        theMap.creation(adventurer)
        move = getch()
        if move == 'q':
            confirmation = input("\nAre you sure you would like to " + RED + "QUIT" + CEND + " the game? (" + GREEN + "ENTER" + CEND + " for exit)\n\n")
            if confirmation == '':
                sys.exit()

        elif move in ['w', 's']:
            adventurer.move(move, 1)

        elif move == 'e':
            if adventurer.arrow_cooldown == 4:
                theMap.fire(adventurer)
                adventurer.arrow_cooldown = -1

    theMap.endGame()
            
startup()

