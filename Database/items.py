import bge
import Scripts.index as index
from Scripts.audioplayer import AudioPlayer

from collections import OrderedDict


class Item(bge.types.KX_PythonComponent):
    args = OrderedDict([
    ])
    
    def start(self, args):
        ## data
        self.inventory = index.database
        self.inventory.load_database()
        
        ## keyboard attr
        self.keyboard = bge.logic.keyboard.inputs
        self.K = self.keyboard[bge.events.KKEY]
        
        # start sfx item pickup
        self.sfx_item = AudioPlayer()
        item = 'item_equip.mp3'
        self.sfx_item.load(bge.logic.expandPath(f"//Data/Audio/sfx/{item}")) ## load sound file SFX
        self.sfx_item.play()
        self.sfx_item.set_volume(0.7); self.sfx_item.stop()

        self.item_toggle = 0 # control double call back to once per activated key

    def update(self):
        if self.object.collide('Player')[0]:
            if self.object.name.lower() == "timeshirt" and not index.knock:
                return
                
            if self.K.activated:
                # if self.item_toggle % 2:
                self.sfx_item.play()
                self.inventory.add_item(id=self.object['id'])
                self.object.endObject() # remove spawn item from game
                # self.item_toggle += 1
                return