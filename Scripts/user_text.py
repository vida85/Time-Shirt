import bge
from collections import OrderedDict

class UserText(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        scene = bge.logic.getCurrentScene()
        self.text_obj = scene.objects["Text"]
        self.text_obj["Text"] = ': '
        self.backspace = bge.events.BACKSPACEKEY
        self.input = {
         'A': bge.events.AKEY,
         'B': bge.events.BKEY,
         'C': bge.events.CKEY,
         'D': bge.events.DKEY,
         'E': bge.events.EKEY,
         'F': bge.events.FKEY,
         'G': bge.events.GKEY,
         'H': bge.events.HKEY,
         'I': bge.events.IKEY,
         'J': bge.events.JKEY,
         'K': bge.events.KKEY,
         'L': bge.events.LKEY,
         'M': bge.events.MKEY,
         'N': bge.events.NKEY,
         'O': bge.events.OKEY,
         'P': bge.events.PKEY,
         'Q': bge.events.QKEY,
         'R': bge.events.RKEY,
         'S': bge.events.SKEY,
         'T': bge.events.TKEY,
         'U': bge.events.UKEY,
         'V': bge.events.VKEY,
         'W': bge.events.WKEY,
         'X': bge.events.XKEY,
         'Y': bge.events.YKEY,
         'Z': bge.events.ZKEY,
         'back': bge.events.BACKSPACEKEY,
         ' ': bge.events.SPACEKEY,}


    

    def update(self):
        self.update_text()
        # Add update_text() function to pre_draw list
#        bge.logic.getCurrentScene().pre_draw.append(self.update_text)


    def update_text(self):
        keyboard = bge.logic.keyboard.inputs
        for letter, key in self.input.items():
            if keyboard[key].activated and letter == 'back':
                self.text_obj["Text"] = self.text_obj["Text"][:-1]
            
            elif keyboard[key].activated:
                # Update text object
                self.text_obj["Text"] += letter
