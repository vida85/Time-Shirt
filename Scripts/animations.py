import bge
from math import pi
import Scripts.index as index
from collections import OrderedDict
from mathutils import Vector, Matrix

def clamp(x, a, b):
    return min(max(a, x), b)

class Animations(bge.types.KX_PythonComponent):
    args = OrderedDict([
        ("Activate", True),
        ("Max Walk Speed", 0.004),
        ("Max Run Speed", 0.008),
        ("Suspend Children's Physics", True),
        ("Align To Move Direction", True),
        ("Align Smooth", 0.5),

        ("Idle Animation", "idle"),
        ("Idle Frame Start-End", Vector([1, 114])),

        ("Walk Animation", "walk"),
        ("Walk Frame Start-End", Vector([1, 29])),

        ("Run Animation", "running"),
        ("Run Frame Start-End", Vector([0, 18])),

        ("Jump Up Animation", "jumping"),
        ("Jump Up Frame Start-End", Vector([0, 25])),

        ("Jump Down Animation", "jumping"),
        ("Jump Down Frame Start-End", Vector([26, 58])),

        ("Sit Down Animation", "sit_down"),
        ("Sit Down Frame Start-End", Vector([0, 55])),

        ("Sit Idle Animation", "sit_idle"),
        ("Sit Idle Frame Start-End", Vector([0, 50])),

        ("Health Animation", "health"),
        ("Health Frame Start-End", Vector([0, 40])),

        ("Push Animation", "push"),
        ("Push Frame Start-End", Vector([0, 193])),

        ("Tshirt Animation", "tshirt_"),
        ("Tshirt Frame Start-End", Vector([0, 193])),
    ])

    def start(self, args):
        self.keyboard = bge.logic.keyboard.inputs
        self.K = self.keyboard[bge.events.KKEY]
        # Get the player object from the scene
        scene = bge.logic.getCurrentScene()
        self.player = scene.objects['Player']
        
        # Start Function #
        self.active = args["Activate"]
        
        self.lastPosition = self.object.worldPosition.copy()
        self.moveDirection = None
        self.alignMoveDir = args["Align To Move Direction"]
        self.alignSmooth = 1 - clamp( args["Align Smooth"], 0, 1)

        self.push = [args["Push Animation"], args["Push Frame Start-End"]]
        self.health = [args["Health Animation"], args["Health Frame Start-End"]]
        self.animIdle = [args["Idle Animation"], args["Idle Frame Start-End"]]
        self.animWalk = [args["Walk Animation"], args["Walk Frame Start-End"]]
        self.animRun  = [args["Run Animation"], args["Run Frame Start-End"]]
        self.sit_down = [args["Sit Down Animation"], args["Sit Down Frame Start-End"]]
        self.sit_idle = [args["Sit Idle Animation"], args["Sit Idle Frame Start-End"]]
        self.animJumpUp  = [args["Jump Up Animation"], args["Jump Up Frame Start-End"]]
        self.animJumpDown = [args["Jump Down Animation"], args["Jump Down Frame Start-End"]]

        self.maxWalkSpeed = args["Max Walk Speed"]
        self.maxRunSpeed  = args["Max Run Speed"]

        self.PUSH = False
        self.HEALTH = False

        # Suspend physics:
        if args["Suspend Children's Physics"]:
            self.object.suspendPhysics()
            for child in self.object.children:
                child.suspendPhysics()

        self.character = bge.constraints.getCharacter(self.object.parent)
        # Error:
        if self.character == None:
            print("[Animator] Error: Can't get the Character constraint from the armature parent.")

    def update_move_direction(self):
        """Updates the move direction"""
        self.moveDirection = self.object.worldPosition - self.lastPosition
        self.lastPosition = self.object.worldPosition.copy()

    def animate(self, animData, blend=4):
        """Runs an animation"""
        self.object.playAction(animData[0], animData[1][0], animData[1][1], blendin=blend)


    def handle_sit_animations(self):
        """Handles animations on ground Sit"""
        if not index.paused:
            print("playing sit_down animation")
            # Play the transition animation and pause the animation controller
            self.animate(self.sit_down)
            index.paused = True
            return
        
        # If the transition animation is finished, play the idle animation
        if not self.object.isPlayingAction():
            print("playing sit_idle animation")
            self.animate(self.sit_idle)
            return
        
        # Otherwise, keep playing the transition animation
        return

    def handle_health_animations(self):
        """Handles animations on ground Health"""
        if self.moveDirection.length > 0:
            self.player['health'] = False
        elif self.moveDirection.length <= 0 and not index.paused:
            index.paused = True
        
        return self.animate(self.health, blend=6)


    def handle_ground_animations(self):
        """Handles animations on ground (Walk, Run, Idle)."""
        # Map different speed ranges to different animations
        speed_anim_map = {
            (0.0, 0.0019): self.animIdle,
            (0.002, self.maxWalkSpeed + 0.001): self.animWalk,
            (self.maxWalkSpeed + 0.001, float("inf")): self.animRun, }

        # Determine the animation based on the character's speed
        # vec = index.sit_orientation
        # self.player.alignAxisToVect(vec, 0, .5)
        speed = self.moveDirection.length
        for speed_range, anim in speed_anim_map.items():
            if speed_range[0] <= speed <= speed_range[1]:
                self.animate(anim, blend=6)
                break


    def handle_air_animations(self):
        """Handles animations on air (Jump)."""
        if self.moveDirection[2] > 0:
            self.animate(self.animJumpUp, 6)
        else:
            self.animate(self.animJumpDown, 5)


    def get_move_direction(self):
        """Returns the current move direction"""
        return self.moveDirection


    def align_move_direction(self):
        """Align the armature to the move direction"""

        length = self.moveDirection.length
        if length >= 0.:
            vec = self.object.worldOrientation @ Vector([0,1,0])
            try:
                if vec.angle(self.moveDirection) >= pi - 0.01:
                    self.object.applyRotation([0,0,0.01], False)
            except:
                pass

            length = clamp(length * 20, 0, 1) * self.alignSmooth
            self.object.alignAxisToVect(-(self.moveDirection), 1, length)
            self.object.alignAxisToVect([0,0,1], 2, 1)


    def update(self):
        """Update Function"""
        self.update_move_direction()

        if self.active:
            if self.alignMoveDir:
                self.align_move_direction()

            if self.character.onGround:
                if self.player['sitted']:
                    self.handle_sit_animations()
                elif self.player['health']:
                    self.handle_health_animations()
                elif self.player['timeshirt']:
                    self.handle_health_animations()
                else:
                    self.handle_ground_animations()
            else:
                self.handle_air_animations()
                