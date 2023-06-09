import os
import bge
import json


ITEMS = []
WORLD_ITEMS =  []
RESTART = False

def selected(location: int) -> list:
    data = ITEMS[location]
    return [data[-1]['category'], data[-1]['name'], data[-1]['ability']]

def display() -> list:
    n, c, d, a = '',  '', '', ''
    for data in ITEMS:
        n += f"{data[-1]['name']}\n"
        c += f"{data[-1]['category']}\n"
        d += f"{data[-1]['description']}\n"
        a += f"{data[-1]['ability']}\n"
    
    return [n, c, d, a]

def add_item(id: int) -> None:
    for idx, item in enumerate(WORLD_ITEMS):
        if item[0] == id:
            ITEMS.append(WORLD_ITEMS.pop(idx))


def drop_item(id: int) -> None:
    for idx, item in enumerate(ITEMS):
        if item[0] == id:
            WORLD_ITEMS.append(ITEMS.pop(idx))


def load_database() -> list:
    file = bge.logic.expandPath('//Database/database.json')
    if os.path.isfile(file):
        with open(file, 'r') as reader:
            ITEMS = json.load(reader)
            return ITEMS
    return []
        
def save_database() -> list:
    file = bge.logic.expandPath('//Database/database.json')
    if os.path.isfile(file):
        with open(file, 'w') as writer:
            database = json.dumps(ITEMS if not RESTART else [], indent=4)
            writer.write(database)
    else:
        raise FileNotFoundError
    """Create a file if it doesn't exits"""