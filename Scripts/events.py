import bge
import bpy
import aud
import random

import Scripts.index as index
import Scripts.accessories as access
from Scripts.hacker import first_message
from Scripts.audioplayer import AudioPlayer
from collections import OrderedDict



class Events(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ('Typing Delay', 5),
        ('Music Volume', .2),
        ('Footsteps SFX', .6),
        ('Traffic SFX', .08),
        ('Keyboard SFX', .3),
    ])

    def start(self, args):
        ## current scene
        self.scene = bge.logic.getCurrentScene()
        self.spawn = self.scene.objects['spawn']

        # timeshirt
        name = f"_timeshirt"
        self.tshirt = self.scene.objects[name] if not index.next_level else ''

        ## character movement for SFX
        self.player = self.scene.objects['Player']
        self.lastPosition = self.player.worldPosition.copy()
        self.moveDirection = None

        ## AUDIO Variables ##
        # start Ambient Music
        self.music_ambient = AudioPlayer()
        self.ambient = 'ambient_v4.mp3'.split()
        song = random.choice(self.ambient)
        self.music_ambient.load(bge.logic.expandPath(f"//Data/Audio/{song}")) ## load sound file SFX
        self.music_ambient.play() # start music
        self.music_ambient.set_volume(args['Music Volume'])
        self.set_volume_music = args['Music Volume']


        # start sfx footsteps
        self.sfx_footsteps = AudioPlayer()
        footsteps = 'footsteps_wood.mp3'
        self.sfx_footsteps.load(bge.logic.expandPath(f"//Data/Audio/sfx/{footsteps}")) ## load sound file SFX
        self.sfx_footsteps.play()
        self.sfx_footsteps.set_volume(args['Footsteps SFX'])

        # start sfx traffic
        self.sfx_traffic = AudioPlayer()
        traffic = 'traffic.mp3'
        self.sfx_traffic.load(bge.logic.expandPath(f"//Data/Audio/sfx/{traffic}")) ## load sound file SFX
        self.traffic_volume = args['Traffic SFX']

        # start sfx keyboard
        self.sfx_keyboard = AudioPlayer()
        keyboard = 'keyboard_typing.wav'
        self.sfx_keyboard.load(bge.logic.expandPath(f"//Data/Audio/sfx/{keyboard}")) ## load sound file SFX
        self.sfx_keyboard.play()
        self.sfx_keyboard.set_volume(args['Keyboard SFX']); self.sfx_keyboard.stop()
        ## AUDIO Variables ##

        self.traffic_hour = [0, 1, 2]
        self.rotation_speed = [[.005, .0010], [.0015, .0025], [.0025, .0040]]
        self.selection = random.choice(self.traffic_hour)

        self.timer = 0
        ## traffic lights through window
        
        self.toggle = 1

        ## Current Level
        self.current_level = index.next_level
        
        ## TYPING FX
        if not self.current_level:
            self.delay = self.args['Typing Delay']

            self.name = 'conv'
            self.text = self.scene.objects[self.name]
            self.text['Text'] = ""

            self.name = 'users'
            self.past_text = self.scene.objects[self.name]
            self.past_text['Text'] = ""

            self.keyboard = bge.logic.keyboard.inputs
            self.J = self.keyboard[bge.events.JKEY]

            self.time = 0
            self.counter = 0
            self.active_msg = 0

            self.done = False
            self.run = True
            self.knock = False

            self.sfx_door_knock = AudioPlayer()
            keyboard = 'knock.mp3'
            self.sfx_door_knock.load(bge.logic.expandPath(f"//Data/Audio/sfx/{keyboard}")) ## load sound file SFX
        ## TYPING FX


    def update(self):
        self.update_move_direction()
        self.play_footsteps_sfx()
        self.traffic() if not self.current_level else ''
        self.level_events(level=self.current_level)


    def play_level_song(self, current_level):
        if not current_level:
            song = random.choice(self.ambient)
            self.music_ambient.load(bge.logic.expandPath(f"//Data/Audio/{song}"))
            self.music_ambient.play() # start music
            self.music_ambient.set_volume(self.set_volume_music)
            
            self.sfx_traffic.play()
            self.sfx_traffic.set_volume(self.traffic_volume)


    def play_footsteps_sfx(self):
        ## Play Footsteps
        if self.moveDirection.length > 0 and not self.sfx_footsteps.handle.status:
            self.sfx_footsteps.play()
        elif self.moveDirection.length == 0:
            self.sfx_footsteps.stop()


    def level_events(self, level: int):
        """Create a way to handle level events"""
        self.play_level_song(index.level)
        if not level:
            ## events for level 0
            ## turn off lights
            # index 1, 2 correlate with light bulb name 1, 2. Controllled by light 'Switch'
            if self.toggle % 2:
                all_lights_lv0 = list(range(3,11))
                for name in all_lights_lv0:
                    light = self.scene.objects[str(name)]
                    if light.visible:
                        light.setVisible(False) # turn off all lights except 2, 3
                light = self.scene.objects['Switch_1']
                light['On'] = True # Set Switch_1 Kitchen to True for lights on
                self.toggle += 1
            
            time = access.timer.get_time()
            if '7:59' in time:
                if self.run:
                    self.first_message()
                if self.knock:
                    self.knock = False
                    index.knock = True
                    self.tshirt.setVisible(True)
                    self.sfx_door_knock.play()


        if level == 'level_1':
            self.timer += 1
            if self.timer == 340 and self.object.scene.name == 'time transition':
                self.object.scene.replace(level)
                return self.object.scene.replace(level) # if self.object.scene.name != level else ''
        elif level == 'level_2':
            pass
        elif level == 'level_3':
            pass
        elif level == 'level_4':
            pass
        elif level == 'level_5':
            pass
        elif level == 'level_6':
            pass
        elif level == 'level_7':
            pass
        elif level == 'level_8':
            pass
        elif level == 'level_9':
            pass
        elif level == 'level_10':
            pass

    
    def first_message(self):
        speed = self.delay if first_message[self.active_msg][0] == "J" else self.delay//2

        if self.counter < speed * len(first_message[self.active_msg]):
            self.counter += 1
        elif self.counter >= speed * len(first_message[self.active_msg]):
            self.done = True
        
        if self.player['sitted'] and self.J.activated and self.done and self.active_msg < len(first_message) - 1:
            self.active_msg += 1
            self.done = False
            self.counter = 0
            line = self.text['Text']
            self.past_text['Text'] += f"{line}\n"
            self.past_text.position.z += 0.064615 + .06
        elif self.active_msg == len(first_message) - 1:
            self.past_text['Text'] = f""
            self.text['Text'] = ""
            self.run = False
            self.knock = True
            return

        fmt = "{:<7} {:<75}"
        if first_message[self.active_msg][0] == "P":
            self.sfx_keyboard.stop()
            name = "PRIVATE: "
            self.text['Text'] = fmt.format(name, first_message[self.active_msg][1:self.counter//speed])
        else:
            self.sfx_keyboard.play() if self.counter == 0 else ""
            name = "   JOHN: "
            self.text['Text'] = fmt.format(name, first_message[self.active_msg][1:self.counter//speed])
            self.sfx_keyboard.stop() if self.counter == speed * len(first_message[self.active_msg]) else ""


    def traffic(self):
        ## traffic lights through window
        if self.timer == 120:
            self.selection = random.choice(self.traffic_hour)
            self.timer = 0
            
        nim, max = self.rotation_speed[self.selection]
        self.scene.objects['TRAFFIC'].applyRotation((0, 0, random.uniform(nim, max)))
        self.timer += 1


    def update_move_direction(self):
        """Updates the move direction"""
        self.moveDirection = self.player.position - self.lastPosition
        self.lastPosition = self.player.position.copy()
