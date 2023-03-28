import random
import json
import math
import time

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

ithen = {
    "max_level": 4,
    "ATK": 10,
    "DC": 18
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

    return handle_roll(n, d, m)

def select_spell():
    choice = print_menu(spell_dict)

    spell_name = list(spell_dict.keys())[choice]
    spell_stats = spell_dict[spell_name]

    ll = spell_stats["level"]
    ul = 4
    string1 = f"Enter level to cast {spell_name.title()}: "
    string2 = f"Enter a number greater than or equal to {ll} (up to {ul}): "
    level = input_int(string1, string2, ul, ll)
    cast_spell(spell_name, level)

def cast_spell(spell, level):
    spell_name = spell
    spell = spell_dict[spell]
    s, m = spell["sides"], spell["modifier"]
    n = check_upcast(spell, level, spell["ndice"])

    behaviour = spell["HIT/DC"]
    if behaviour == None:
        pass
    else:
        if behaviour == "HIT":
            spell_attack(spell_name, level, n, s, m)
        else:
            print(f"Affected creatures must make a DC {ithen['DC']} {behaviour} save")

def check_upcast(spell, level, n):
    a = n
    spell_level = spell["level"]
    upcast = spell_level < level
    if upcast:
         a += (level-spell_level)
    else:
         pass
    return a
    

def spell_attack(_name, level, n, s, m):
    q_ad = check_yn(f"Are you rolling this attack at advantage or disadvantage? Y/N: ")
    if q_ad == 'y':
        hit = handle_roll(2, 20, ithen["ATK"])
    else:
        hit = handle_roll(1, 20, ithen["ATK"])
    
    q_hit = check_yn(f"You rolled a {hit} to hit, did this hit? Y/N: ")
    if q_hit == 'y':
        dmg = handle_roll(n, s, m)
        print(f"For your level {level} {_name} you rolled {n}d{s} + {m} for a total of {dmg} damage\n")
        time.sleep(2)
        main_menu()
    else:
        main_menu()


def check_yn(string1):
    q = input(string1).strip().lower()
    if q == 'y' or q == 'n':
        return q
    else: 
        q = check_yn(string1)
        return q


def custom_roll():
    dice = {"d4": 4, "d6": 6, "d8": 8, "d10": 10, "d12": 12, "d20": 20, "d100": 100 }
    sides = [dice[key] for key in dice.keys()]
    choice = print_menu(dice)

    if type(choice) == int:
        s = sides[choice]
        n = input_int("Enter number of dice: ", "Enter number of dice")
        m = input_int("Enter modifer: ", "Enter modifier")
        total = handle_roll(n, s, m)
        print(f"For your roll of {n}d{s} + {m} you rolled a total of : {total}")
        main_menu()
        
    else:
        custom_roll()

def input_int(string1, string2= "Enter a number to choose an option: ", 
              u_limit=20, l_limit=0, ):
    
    num = input(f"{string1}").strip()

    if check_int(num, l_limit, u_limit):
        return int(num)
    else:
        num = input_int(string2, string2, u_limit, l_limit)
        return int(num)
    
    
def check_int(input_val, l_limit=0, u_limit=20):
    try:
        num = int(input_val)
        if num < l_limit or num > u_limit:
            raise Exception
        # return True
    except:
        return False
    
    else:
        return True
    

def handle_roll(n, s, m, hs=1):
    if s == 20:
        rolls = [random.randint(1,s) + m for i in range(n)]
    else:
        rolls = [random.randint(1,s) for i in range(n)]
        print(rolls)
        rolls = math.ceil((sum(rolls))/hs + m)
    return rolls
    

def print_menu(iterable):
    for i, item in enumerate(iterable):
        print(f"{i+1}) {item}")
    choice = int(input_int("Enter a number to choose an option: ",
                       f"Please enter a number between 1 and {len(iterable)}: ",
                       len(iterable))) -1
    return choice
    
    # try:
    #     choice = int(choice)
    #     if choice <0 or choice > len(iterable):
    #         raise Exception
    #     choice -= 1

    # except:
    #     print(f"Please enter a number between 1 and {len(iterable)}")
    #     choice = None
    
    # finally: return choice


def main_menu():
    _main_menu = ["Dice Roll", "Cast a Spell", "Exit"] 
    choice = print_menu(_main_menu)

    if choice == 0:
        custom_roll()
    
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