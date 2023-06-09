import bge
import random
import string

import Scripts.index as index
from collections import OrderedDict
        
        
class Spawn(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args: dict):
        """spawn items"""
        self.scene = bge.logic.getCurrentScene()
        self.levels = [self.distribute_level_1]
        self.IDS = []
        
        self.inventory = index.database

        if index.level == 1:
            index.level = 2
        
        if not index.level:
            locations = {(-4.2, -1, 0.98266): 'health', (-4.3, 3.45, 0.73133): 'watch', 
                         (-2, 4.37, 0.7484): 'screwdriver', (1.5, 4.35, .68834): 'health',
                         (-0.862381, 5.3224, .31/2): 'timeshirt'}

            for location, name in locations.items():
                obj = self.distribute_level_0(name, location)
                if obj['category'] == 'weapons':
                    obj['id'] = self.generated_id()
                    self.inventory.WORLD_ITEMS.append([
                        obj['id'],
                        {"name": obj['item_name'], "category": obj['category'], "description": obj['description'], "ability": obj['ability']},
                        ])
                    
                elif obj['category'] == 'tools':
                    obj['id'] = self.generated_id()
                    obj['ability'] = self.gear_amount()
                    self.inventory.WORLD_ITEMS.append([
                        obj['id'],
                        {"name": obj['item_name'], "category": obj['category'], "description": obj['description'], "ability": obj['ability']},
                        ])
                elif obj['category'] == 'wearables':
                    obj['id'] = self.generated_id()
                    self.inventory.WORLD_ITEMS.append([
                        obj['id'],
                        {"name": obj['item_name'], "category": obj['category'], "description": obj['description'], "ability": obj['ability']},
                        ])

                    if obj['item_name'].lower() == 'TimeShirt'.lower():
                        name = f"_{obj['item_name'].lower()}"
                        _obj = self.scene.objects[name]
                        _obj.setVisible(False)

                elif obj['category'] == 'consumables':
                    obj['ability'] = self.health_amount()
                    obj['id'] = self.generated_id()
                    self.inventory.WORLD_ITEMS.append([
                        obj['id'],
                        {"name": obj['item_name'], "category": obj['category'], "description": obj['description'], "ability": obj['ability']},
                        ])
            index.level = 1
    


    def update(self):
        pass


    def distribute_level_0(self, name: str, location: tuple) -> object:
        self.object.position = location
        return self.object.scene.addObject(name, self.object)


    def distribute_level_1(self, idx: int):
        pass


    def health_amount(self) -> int:
        return random.choice(list(range(5, 35)))


    def gear_amount(self) -> int:
        return random.choice(list(range(7, 55)))
    

    def generated_id(self) -> int:
        while True:
            id = ''.join(random.choices(string.digits, k=5))
            if id not in self.IDS:
                self.IDS.append(id)
                return int(id)