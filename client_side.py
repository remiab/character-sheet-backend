import random
import pprint
import math
import time
import requests
import json

spell_dict = {
    "fireball": {
    "ndice": 8,
    "sides": 6,
    "modifier": 0,
    "level": 3,
    "targets": ">1",
    "HIT/DC": "DEX",
    "success": 0.5
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
    "HIT/DC": "WIS",
    "success": 0
    },
    "catapult":{
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 1,
    "targets": "1",
    "HIT/DC": "DEX",
    "success": 0
    },
    "shatter": {
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 2,
    "targets": ">1",
    "HIT/DC": "CON",
    "success": 0.5
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

def view_spell_list():
    result = requests.get('http://127.0.0.1:5000/prepared_spells')
    result_code = result
    result = result.json()
    for i, record in enumerate(result):
        print(f"{i+1}) {record['spell_name'].title()}; prepared: {record['prepared']}")


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
            aoe_attack(spell, n, s, m)


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


def aoe_attack(spell, n, s, m):
    succ = spell["success"]

    fail = handle_roll(n, s, m)
    success = math.ceil(fail * succ)
    print(f"Creatures which failed their save take {fail} damage, creatures which succeeded take {success} damage\n")
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
    

def handle_roll(n, s, m):
    if s == 20:
        rolls = [random.randint(1,s) + m for i in range(n)]
    else:
        rolls = [random.randint(1,s) for i in range(n)]
        print(rolls)
        rolls = (sum(rolls)) + m
    return rolls
    

def print_menu(iterable):
    for i, item in enumerate(iterable):
        print(f"{i+1}) {item}")
    choice = int(input_int("Enter a number to choose an option: ",
                       f"Please enter a number between 1 and {len(iterable)}: ",
                       len(iterable))) -1
    return choice
    
def chose_exit():
    print("Exit")
    quit()


def select_spell_to_update(spell_name, ud_status):
    update = {
        "spell_name": spell_name,
        "spell_status": ud_status
    }
    result = requests.put(f"http://127.0.0.1:5000/update/prepare/{spell_name}",
                        headers={'content-type': 'application/json'},
                        data= json.dumps(update))
    print(result.status_code)
    # print(result.json())



def main_menu():
    menu_dict = {
        "Dice Roll": custom_roll,
        "Cast a Spell": select_spell,
        "View Spell List": view_spell_list,
        "Exit": chose_exit
    }

    _main_menu = ["Dice Roll", "Cast a Spell", "View Spell List", "Exit"] 
    choice = print_menu(_main_menu)

    if choice in range(len(_main_menu)):
        menu_dict[_main_menu[choice]]()
    else:
        main_menu()

def call_levels():
    result = requests.get('https://www.dnd5eapi.co/api/classes/wizard/levels/9')
    result_code = result
    result = result.json()
    print(result_code)
    pprint.pprint(result)
    arcane_recovery = requests.get('https://www.dnd5eapi.co/api/features/arcane-recovery')
    pprint.pprint(arcane_recovery.json())

# call_levels()

def call_combat_expendables():
    result = requests.get('http://127.0.0.1:5000/ithen/spell_slots/1st Level,2nd Level')
    print(result)
    pprint.pprint(result.json())

call_combat_expendables()

# select_spell_to_update("fireball", "Y")
# main_menu()
