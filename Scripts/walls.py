import bge
from collections import OrderedDict

class HideableWalls(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        ## get Scene
        self.scene = bge.logic.getCurrentScene()
        self.wall = self.scene.objects[self.object.name.lower()]

    def update(self):
        self.collision()
    

    def collision(self):
        if self.object.collide('Player')[0]:
            if self.wall.visible:
                self.wall.setVisible(False)
        else:
            if not self.wall.visible:
                self.wall.setVisible(True)