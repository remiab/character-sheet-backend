import random
import json

spell_dict = {
    "fireball": {
    "ndice": 8,
    "sides": 6,
    "modifier": 0,
    "level": 3,
    "targets": ">1",
    "HIT/DC": "DEX"
    },
    "chromatic orb":{
    "ndice":3,
    "sides": 8,
    "modifier": 0,
    "level": 1,
    "targets":  "1",
    "HIT/DC": "HIT"
    },
    "numinous shield":{
    "ndice": 2,
    "sides": 10,
    "modifier": 0,
    "level": 1,
    "targets": ">1",
    "HIT/DC": "WIS"
    },
    "catapult":{
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 1,
    "targets": "1",
    "HIT/DC": "DEX"
    },
    "shatter": {
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 2,
    "targets": ">1",
    "HIT/DC": "CON"
    },
    "lifetap":{
    "ndice": 2,
    "sides": 10,
    "modifier": 5,
    "level": 2,
    "targets": "1",
    "HIT/DC": "HIT"
    },
    "bend time": {
     "ndice": 3,
     "sides": 8,
     "modifier": 0,
     "level": 3,
     "targets": "n/a",
     "HIT/DC": None
    }
}

def handle_damage(spell, level):
    n = spell_dict[spell]["ndice"]
    d = spell_dict[spell]["sides"]
    m = spell_dict[spell]["modifier"]

    spell_level = spell_dict[spell]["level"]
    upcast = spell_level != level
    if upcast:
         n += (level-spell_level)
    else:
         pass

    rolls =[random.randint(1, d) for i in range(n)]
    return rolls, sum(rolls) + m

def select_spell():
     print("select spell")

def dice_roll():
    dice = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12, "d20": 20, "d100": 100 }
    sides = [dice[key] for key in dice.keys()]
    choice = print_menu(dice)
    if type(choice) == int:
        d = sides[choice]
        print(d)
    else:
        dice_roll()
    
     

def print_menu(iterable):
    for i, item in enumerate(iterable):
        print(f"{i+1}) {item}")
    choice = input("Enter a number to choose an option: ").strip()
    
    try:
        choice = int(choice)
        if choice <0 or choice > len(iterable):
            raise Exception
        choice -= 1

    except:
        print(f"Please enter a number between 1 and {len(iterable)}")
        choice = None
    
    finally: return choice


def main_menu():
    _main_menu = ["Dice Roll", "Cast a Spell", "Exit"] 
    choice = print_menu(_main_menu)

    if choice == 0:
        dice_roll()
    
    else:
        if choice == 1:
             select_spell()
        
        else:
            if choice == 2:
                print("Exit")
                quit()
            else:
                 main_menu()
            



main_menu()