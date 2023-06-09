import bge
import bpy
from mathutils import Vector
import Scripts.index as index
from collections import OrderedDict

class Camera(bge.types.KX_PythonComponent):
    # Put your arguments here of the format ("key", default_value).
    # These values are exposed to the UI.
    args = OrderedDict([
        ("DELAY TIME", 2),
        ('Zoom in', 5.4),
        ('Zoom out', 18.0),
    ])

    def start(self, args):
        # Set the delay time (in seconds)
        self.delay_time = args["DELAY TIME"]

        # Keyboard
        self.keyboard = bge.logic.keyboard.inputs

        ## cam zoom in & out
        self.zoom_out_max = args['Zoom out']
        self.zoom_in_max = args['Zoom in']
        self.mouse = bge.logic.mouse.inputs
        self.wheel_up = self.mouse[bge.events.WHEELUPMOUSE]
        self.wheel_down = self.mouse[bge.events.WHEELDOWNMOUSE]

        self.wheel_count = self.zoom_out_max
        self.current = self.zoom_out_max

        # Get a reference to the player object
        self.player = bge.logic.getCurrentScene().objects["Player"]

        # Store the camera's initial distance from the player
        self.initial_distance = (self.player.worldPosition.xy - self.object.worldPosition.xy).length

        # Initialize variables for the delayed position
        self.delayed_position = self.player.worldPosition.xy.copy()
        self.last_update_time = 0.0

        self.cam = self.object.scene.active_camera
        self.zoom_done = True

        self.K = self.keyboard[bge.events.KKEY]


    def update(self):
        self.object['zoom_done'] = self.zoom_done
        self.object['zoom'] = self.object.ortho_scale
        self.update_camera()

        self.manual_zoom(6 if not self.zoom_done else 12)


        


    def update_camera(self):
        # Calculate the elapsed time since the last update
        current_time = bge.logic.getRealTime()
        elapsed_time = current_time - self.last_update_time
        
        # If enough time has passed, update the delayed position
        if elapsed_time >= self.delay_time:
            self.delayed_position = self.player.position.xy.copy()
            self.last_update_time = current_time
        
        # Calculate the desired camera position (with the delayed X and Y position)
        desired_position = self.player.position.copy()
        desired_position.x += self.initial_distance
        desired_position.y -= self.initial_distance
        desired_position.z = self.object.position.z
        
        # Move the camera towards the desired position
        camera_position = Vector(self.object.position)
        camera_position += (desired_position - camera_position) * 0.2
        
        # Update the camera's position
        self.object.position = camera_position


    def camera(self):
        self.current = self.object.ortho_scale


    def zoom_in(self, amount):
        self.camera()

        if self.current >= amount:
            self.current -= .1
            self.zoom_done = False
        else:
            self.zoom_done = True
        
        return self.current


    # def zoom_out(self, amount):
    #     self.camera()

    #     if self.current <= amount:
    #         self.current += .1
    #         self.zoom_done = False
    #         self.wheel_count = self.current # keep camera at current zoom
    #     else:
    #         self.zoom_done = True

    #     self.object.ortho_scale = self.current

    def manual_zoom(self, amount):
        self.manual = True
        if self.wheel_down.active:
            self.wheel_count += .5
            if self.wheel_count >= self.zoom_out_max:
                self.wheel_count = self.zoom_out_max
            
        elif self.wheel_up.active:
            self.wheel_count -= .5
            if self.wheel_count <= self.zoom_in_max:
                self.wheel_count = self.zoom_in_max

        if index.SIT:
            self.wheel_count = self.zoom_in(amount)
        
        self.object.ortho_scale = self.wheel_count
