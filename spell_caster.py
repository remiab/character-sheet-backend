import random

spell_dict = {
    "fireball": {
    "ndice": 8,
    "sides": 6,
    "modifier": 0,
    "level": 3,
    "targets": ">1"
    },
    "chromatic orb":{
    "ndice":3,
    "sides": 8,
    "modifier": 0,
    "level": 1,
    "targets":  "1"
    },
    "numinous shield":{
    "ndice": 2,
    "sides": 10,
    "modifier": 0,
    "level": 1,
    "targets": ">1"
    },
    "catapult":{
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 1,
    "targets": "1"
    },
    "shatter": {
    "ndice": 3,
    "sides": 8,
    "modifier": 0,
    "level": 2,
    "targets": ">1"
    },
    "lifetap":{
    "ndice": 2,
    "sides": 10,
    "modifier": 5,
    "level": 2,
    "targets": "1"
    },
    "bend time": {
     "ndice": 3,
     "sides": 8,
     "modifier": 0,
     "level": 3,
     "targets": "n/a"
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

def menu():
    menu = ["Dice Roll", "Cast a Spell", "Exit"]
    for i, item in enumerate(menu):
          print(f"{i+1}) {item}")
    choice = input("Enter a number to choose an option: ").strip()
    try:
        choice = int(choice) -1
    except ValueError:
        print("error found")
    else:
         print("good choice")

    
menu()