import bge
import bpy

import Scripts.index as index
import Scripts.accessories as access ## UPBGE Components doesn't like this file

from collections import OrderedDict
from mathutils import Vector, Matrix

"""
    TODO:
    # Fix loop in level_1
    # Create a menu and save game data
"""


class Player(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
    ])

    def start(self, args):
        ## data
        self.inventory = index.database
        self.inventory.load_database()
        
        ## keyboard attr
        self.keyboard = bge.logic.keyboard.inputs
        self.K = self.keyboard[bge.events.KKEY]
        self.move_keys = {bge.events.WKEY: 'W', bge.events.SKEY: 'S',
                          bge.events.AKEY: 'A', bge.events.DKEY: 'D',}
        
        self.object.collisionCallbacks.append(self.collided)


    def update(self):
        pass

    def collided(self, object: object) -> None:
        if 'SIT' in object:
            if self.K.activated and not index.SIT:
                index.SIT_POS_ROT = [object.position, object.orientation]
                object['SIT'] = True
                self.object['sitted'] = True # type: ignore ... Player Object
                
                index.SIT = object['SIT']
            else:
                for key in self.move_keys:
                    if self.keyboard[key].active:
                        self.object['sitted'] = False # type: ignore ... Player Object
                        object['SIT'] = False # [name]_Bound object
                        index.paused = False
                        index.SIT = object['SIT']



class UI(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ('health', 75),
    ])

    def start(self, args):
        ## get Scene
        self.scene = bge.logic.getCurrentScene()
        self.armature = self.scene.objects['ARMATURE']
        self.time_shirt = bpy.data.objects['time-shirt']
        # self.time_shirt.setVisible(False if index.level else True) ### <-- fix this: Shirt needs to appear only if he puts it on.
        ## data
        self.inventory = index.inventory
        self.inventory.ITEMS = self.inventory.load_database()
        
        ## keyboard attr
        self.keyboard = bge.logic.keyboard.inputs
        self.TAB = self.keyboard[bge.events.TABKEY]
        self.J = self.keyboard[bge.events.JKEY]
        self.I = self.keyboard[bge.events.IKEY]
        self.K = self.keyboard[bge.events.KKEY]
        self.UP = self.keyboard[bge.events.UPARROWKEY]
        self.DOWN = self.keyboard[bge.events.DOWNARROWKEY]
        self.RIGHT = self.keyboard[bge.events.RIGHTARROWKEY]
        self.LEFT = self.keyboard[bge.events.LEFTARROWKEY]

        ## UI Setup
        self.item_name = self.scene.objects['name']
        self.item_category = self.scene.objects['category']
        self.item_description = self.scene.objects['description']
        self.item_ability = self.scene.objects['ability']
        self.inv_text = [self.item_name, self.item_category, self.item_description, self.item_ability]
        self.ui_capacity = self.scene.objects['ui_capacity']
        self.ui_capacity['Text'] = "Capacity"
        
        for text in self.inv_text:
            text['Text'] = ' ' 

        self.cursor_icon = self.scene.objects['UI_cursor']

        self.cursor_index = 0
        self.ui_on = False
        self.UI = self.scene.objects['ui_BG']
        self.status = self.UI.playAction
        self.status('off_ui', 0, 24)
        self.ui_state = False

        self.health = self.scene.objects['health_light']
        self.life = args['health']
        self.helpbar_text = self.scene.objects['helpbar_text']
        self.helpbar_text['Text'] = ""

        # spawn obj
        self.spawn = self.scene.objects['spawn']

        ## Time on Watch
        self.time_bg = self.scene.objects['watch_bg']
        self.time_bg.setVisible(False)

        self.display_time = self.scene.objects['watch_time']
        self.display_time.setVisible(False)

    def update(self):
        self.ui_on_off()
        self.cursor_movement(self.cursor_icon)
        self.health_display()
        self.watch_display()

        if self.ui_on:
            self.ui_display()
            self.use_item()
            self.drop_item()
        elif not self.ui_on:
            self.helpbar_text['Text'] = ""

    ## UI TOOLS ##
    def ui_on_off(self):
        if self.TAB.activated:
            if self.ui_on:
                self.status('off_ui', 0, 24)
                self.ui_on = False
            else:
                self.status('on_ui', 0, 24)
                self.ui_on = True

    def ui_display(self) -> int:
        """display inventory"""
        TEXT = self.inventory.display()
        self.item_name['Text'] = TEXT[0]
        self.item_category['Text'] = TEXT[1]
        self.item_description['Text'] = TEXT[2]
        self.item_ability['Text'] = TEXT[3]

    def cursor_movement(self, cursor_icon: object) -> int:
        if self.UP.activated and self.cursor_index:
            cursor_icon.position.y += .05
            self.cursor_index -= 1
            return self.cursor_index

        elif self.DOWN.activated and self.cursor_index <= 7:
            cursor_icon.position.y -= .05
            self.cursor_index += 1
            return self.cursor_index
        return self.cursor_index
    ## UI TOOLS ##


    def health_display(self):
        """map health light location according to health level from 0-100"""
        def map_range(value, low1, high1, low2, high2):
            return low2 + (high2 - low2) * (value - low1) / (high1 - low1)

        x_position = -1.094 # example value
        health_percentage = self.life

        mapped_value = map_range(x_position, -1.094, -0.094, 0, 100)
        mapped_value += health_percentage # adjust for health percentage

        # Ensure that the value is within the range of 0 to 100
        mapped_value = max(0, min(100, mapped_value))
        mapped_x_position = map_range(mapped_value, 0, 100, -1.094, -0.094)
        self.health.position.x = mapped_x_position

    def watch_display(self):
        self.watch_time = access.timer.timing()
        self.display_time['Text'] = self.watch_time
        # access the time globaly


    ## USE and DROP ITEMS ##
    def use_item(self) -> str:
        if self.RIGHT.activated:
            idx = self.cursor_movement(self.cursor_icon)
            category, name, ability = self.inventory.selected(location=idx)

            if category == "consumables":
                self.life += ability
                self.object['health'] = True
                self.inventory.ITEMS.pop(idx)
            elif category == "tool":
                # pass ability int to an object in game to FIX
                pass
            elif category == "wearables":
                if name.lower() == 'watch':
                    self.display_time.setVisible(True if not self.display_time.visible else False)
                    self.time_bg.setVisible(True if not self.time_bg.visible else False)
                if name.lower() == 'timeshirt':
                    print('traveling through time')
                    self.inventory.save_database()
                    
                    self.time_shirt.hide_set(False)
                    
                    self.armature.playAction('tshirt_', 1, 88, blendin=10)
                    index.next_level = f'level_{index.level}'
                    
                    return self.object.scene.replace('time transition')

    def drop_item(self) -> str:
        if self.LEFT.activated:
            items = self.inventory.name_id_list() # returns [id, name]
            try:
                id = items[self.cursor_index][0]
                name = items[self.cursor_index][1].lower()
            except IndexError:
                return "nothing here"
            
            if self.inventory[id].category.lower() == "wearables" and self.inventory[id].name.lower() == "watch":
                self.time_bg.setVisible(False)
                self.display_time.setVisible(False)

            ability = self.inventory[id].ability
            self.inventory.dropped_item(id)
            self.spawn.position = self.object.position
            self.spawn.position.z = .1

            obj = self.object.scene.addObject(name, self.spawn)
            obj['id'] = id
            obj['ability'] = ability

            self.category(obj)

    def category(self, obj: object):
        if obj['category'] == 'weapons':
            index.level_items.append(Weapon(obj['item_name'], obj['description'], obj['ability'], 1, obj['id']))
        elif obj['category'] == 'tools':
            index.level_items.append(Tool(obj['item_name'], obj['description'], obj['ability'], 1, obj['id']))
        elif obj['category'] == 'wearables':
            index.level_items.append(Wearable(obj['item_name'], obj['description'], obj['ability'], 1, obj['id']))
        elif obj['category'] == 'consumables':
            print('dropped spawn creation', obj['ability'])
            index.level_items.append(Consumable(obj['item_name'], obj['description'], obj['ability'], 1, obj['id']))
    ## USE and DROP ITEMS ##            



class Movement(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Walk Speed", 0.03),
        ("Run Speed", 0.06),
        ('Zoom in', 6.0),
        ('Zoom out', 18.0),
        ("Max Jumps", 1),
        ("Static Jump Direction", False),
        ("Static Jump Rotation", False),
        ("Smooth Character Movement", .2),
    ])

    def start(self, args):
        ## character
        self.character = bge.constraints.getCharacter(self.object)
        self.armature = bge.logic.getCurrentScene().objects['ARMATURE']
        
        ## keyboard attr
        self.keyboard = bge.logic.keyboard.inputs
        self.W = self.keyboard[bge.events.WKEY]
        self.S = self.keyboard[bge.events.SKEY]
        self.A = self.keyboard[bge.events.AKEY]
        self.D = self.keyboard[bge.events.DKEY]
        self.shift = self.keyboard[bge.events.LEFTSHIFTKEY]
        self.space = self.keyboard[bge.events.SPACEKEY]
        
        ## walking & running
        self.walk = args['Walk Speed']
        self.run = args['Run Speed']

        self.last_position = self.object.worldPosition.copy()
        self.smooth_sliding_flag = False
        self.smooth_last = Vector([0,0,0])
        self.staticJump = args["Static Jump Direction"]
        self.jump_direction = [0,0,0]
        self.__smoothMov = min(max(args["Smooth Character Movement"], 0), 0.99)
        self.staticJumpRot = args["Static Jump Rotation"]
        self.jump_rotation = Matrix.Identity(3)
        self.character = bge.constraints.getCharacter(self.object)
        self.character.maxJumps = args["Max Jumps"]
        
        
        self.mouse = bge.logic.mouse

        # Get the active camera object
        self.cam = bge.logic.getCurrentScene().active_camera

         # Store the camera's initial distance from the player
        self.initial_distance = (self.object.worldPosition.xy - self.cam.worldPosition.xy).length

        # Initialize variables for the delayed position
        self.delayed_position = self.object.worldPosition.xy.copy()
        self.last_update_time = 0.0


    def update(self):
        self.movement()
        
        ### Object rotate around mouse
        # x, y = self.mouse.position
        # radians = self.get_rotation_degree(x, y)
        # self.armature.localOrientation = self.calculate_rotation(radians)

    # def calculate_rotation(self, rotation_radians):
    #     rotation_matrix = mathutils.Matrix.Rotation(rotation_radians, 3, 'Z')
    #     return rotation_matrix.to_3x3()
    
    # def get_rotation_degree(self, x, y):
    #     radians = math.atan2(y, x) * 2
    #     return radians

    def movement(self):
        """Makes the character walk with W,A,S,D
        (You can run by holding Left Shift)"""
        speed = self.walk if not self.shift.active else self.run

        rotation = [0, 0, 0]
        self.object.localOrientation = rotation if not self.object['sitted'] else self.object.localOrientation # type: ignore

        x = 0
        y = 0

        if self.keyboard[bge.events.WKEY].active:
            y = 1
        elif self.keyboard[bge.events.SKEY].active:
            y = -1
        if self.keyboard[bge.events.AKEY].active:
            x = -1
        elif self.keyboard[bge.events.DKEY].active:
            x = 1

        vec = Vector([x, y, 0])
        self.smooth_sliding_flag = False
        if vec.length != 0:
            self.smooth_sliding_flag = True
            # Normalizing the vector.
            vec.normalize()
            # Multiply by the speed
            vec *= speed

        # This part is to make the static jump Direction works.
        if not self.character.onGround:
            if self.staticJump:
                vec = self.jump_direction
            if self.staticJumpRot:
                self.object.worldOrientation = self.jump_rotation.copy()
        else:
            self.jump_direction = vec
            self.jump_rotation  = self.object.worldOrientation.copy()

        smooth = 1.0 - self.__smoothMov
        vec = self.smooth_last.lerp(vec, smooth)
        self.smooth_last = vec

        self.character.walkDirection = self.object.worldOrientation @ vec

        if vec.length != 0:
            # self.lastDirection = self.object.worldPosition - self.last_position
            self.last_position = self.object.worldPosition.copy()

        if self.space.activated:
            self.character.jump()
