import bge
from collections import OrderedDict

class Sit(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        scene = bge.logic.getCurrentScene()
        self.character = bge.constraints.getCharacter(self.object)
        self.player = scene.objects['Player']
        self.armature = scene.objects['ARMATURE']

        keyboard = bge.logic.keyboard.inputs
        self.K = keyboard[bge.events.KKEY]
        self.toggle = 0
        

    def update(self):
        if self.object.collide('Player')[0] and self.K.activated:
            distance = self.object.position - self.player.position
            distance.z = 0
            self.player.position += distance

            self.armature.orientation = self.object.orientation
