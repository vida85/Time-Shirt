import bge
from collections import OrderedDict
from Scripts.audioplayer import AudioPlayer


class Doors(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ('sfx_volume', 0.7),
    ])

    def start(self, args):
        ## get Scene
        self.scene = bge.logic.getCurrentScene()

        ## keyboard key
        keyboard = bge.logic.keyboard.inputs
        self.J = keyboard[bge.events.JKEY]

        ## SFX
        # start sfx door
        self.sfx_door_open = AudioPlayer()
        self.sfx_door_close = AudioPlayer()
        door_open = 'door_open.mp3'; door_close = 'door_close.mp3'
        self.sfx_door_open.load(bge.logic.expandPath(f"//Data/Audio/sfx/{door_open}")) ## load sound file SFX
        self.sfx_door_close.load(bge.logic.expandPath(f"//Data/Audio/sfx/{door_close}")) ## load sound file SFX
        self.sfx_door_open.play()
        self.sfx_door_open.set_volume(args['sfx_volume']); self.sfx_door_open.stop()
        self.sfx_door_close.play()
        self.sfx_door_close.set_volume(args['sfx_volume']); self.sfx_door_close.stop()



    def update(self):
        if self.object.collide('Player')[0]:
            if self.J.activated:
                open = self.object['Open']
                door = self.scene.objects[self.object['Door']] ## Object name in lowercase
                if open:
                    self.sfx_door_close.play()
                    door.playAction('close_door', 1, 24)
                    self.object['Open'] = False
                elif not open:
                    print('here')
                    self.sfx_door_open.play()
                    door.playAction('open_door', 1, 24)
                    self.object['Open'] = True