import bge
from collections import OrderedDict
from Scripts.audioplayer import AudioPlayer

class LightSwitch(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        ## get Scene
        scene = bge.logic.getCurrentScene()

        ## keyboard key
        keyboard = bge.logic.keyboard.inputs
        self.J = keyboard[bge.events.JKEY]

        ## SFX
        # start sfx light switch
        self.sfx_switch = AudioPlayer()
        switch = 'switch.mp3'
        self.sfx_switch.load(bge.logic.expandPath(f"//Data/Audio/sfx/{switch}")) ## load sound file SFX
        self.sfx_switch.play()
        self.sfx_switch.set_volume(0.7); self.sfx_switch.stop()

        ## Light Objects
        self.light_a = scene.objects[str(self.object['Light'])]
        self.light_b = scene.objects[str(self.object['Light'] + 1)]


    def update(self):
        self.collision()
    

    def collision(self):
        if self.object.collide('Player')[0]:
            if self.J.activated:
                if self.light_a.visible:
                    self.light_a.setVisible(False)
                    self.light_b.setVisible(False)
                    self.sfx_switch.play() if "no_audio" not in self.object else ""
                elif not self.light_a.visible:
                    self.light_a.setVisible(True)
                    self.light_b.setVisible(True)
                    self.sfx_switch.play() if "no_audio" not in self.object else ""