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
    return sum(rolls) + m
    
print(handle_damage('fireball', 4))