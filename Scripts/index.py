from Database import database as inventory

## Animation Variables
up_orientation = 0
PUSH = False
HEALTH = False
paused = None
consumed = False
SIT_POS_ROT = []
SIT = False


## HUD
hud_toggle = False
idx = 0

## level info
level = 0


## Player Info
life = 100

## Game Items
database = inventory

knock = False
level_items = []
remove_item = None
item = None
item_type = 'NONE'
once = 0
drop_item = False
drop_location = {}

time_shirt = False

yes_list = ["yes", "yep", "yeah", "yup", "affirmative", "certainly", "absolutely", "indeed", "most certainly", "for sure", "definitely", "positively", "agreed", "roger", "acknowledged", "accepted", "understood", "OK", "okay", "aye", "aye aye", "you bet", "sure thing", "no problem", "no sweat", "all right", "all righty", "of course", "by all means", "very well", "righto", "fine", "great", "good", "excellent", "wonderful", "fantastic", "terrific", "awesome", "outstanding", "superb", "marvelous", "splendid", "brilliant", "dandy", "peachy", "tops", "rad", "neat", "cool", "hip", "groovy", "far out", "super", "mega", "ultra", "sweet", "nice", "good to go", "ready", "aye-aye", "totally", "completely", "utterly", "wholly", "thoroughly", "entirely", "absolutely right", "exactly", "precisely", "correct", "right on", "bingo", "gotcha", "indeedy", "yessiree", "most assuredly", "without a doubt", "beyond question", "unquestionably", "undeniably", "unmistakably", "emphatically", "yay", "hooray", "woo-hoo", "alright", "aye, aye, captain"]
no_list = ["no", "nah", "nay", "not really", "not exactly", "not quite", "negative", "absolutely not", "certainly not", "by no means", "under no circumstances", "never", "no way", "nope", "no can do", "not on your life", "not a chance", "no siree", "no thanks", "no way José", "forget it", "I don't think so", "I'd rather not", "I'm afraid not", "sorry, no", "negative ghost rider", "not even close", "not by a long shot", "no dice", "not for all the tea in China", "not on your nelly", "not likely", "not at all", "not now, not ever", "out of the question", "over my dead body", "veto", "decline", "refuse", "rejection", "denial", "repudiation", "turndown", "dismissal", "opposition", "contradiction", "disagreement", "disapproval", "disclaimer", "objection", "protestation", "withholding", "rebuke", "non-acceptance", "non-compliance", "nonconcurrence", "no go", "thumbs down", "nix", "not so fast", "not in a million years", "don't count on it", "don't hold your breath", "not happening", "not in this lifetime", "not on my watch", "overruled", "shut down", "zilch", "zip", "nothing doing", "not a bit", "not one bit", "never ever", "never in a million years", "nevermore", "neither", "none", "nowhere", "nobody", "nothing", "never mind", "not important"]


['__class__', '__contains__', '__delattr__', '__delitem__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__',
 '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setitem__', '__sizeof__', '__str__',
 '__subclasshook__',
 'actuators',
 'addDebugProperty',
 'alignAxisToVect',
 'angularDamping',
 'angularVelocity',
 'angularVelocityMax',
 'angularVelocityMin',
 'applyForce',
 'applyImpulse',
 'applyMovement', 
 'applyRotation', 
 'applyTorque', 
 'attrDict', 
 'blenderObject', 
 'channels', 
 'children', 
 'childrenRecursive', 
 'collide', 
 'collisionCallbacks', 
 'collisionGroup', 
 'collisionMask', 
 'color', 
 'components', 
 'constraints', 
 'controllers', 
 'currentLodLevel', 
 'debug', 
 'debugRecursive', 
 'disableRigidBody', 
 'draw', 
 'enableRigidBody', 
 'endObject', 
 'friction', 
 'get', 
 'getActionFrame', 
 'getActionName', 
 'getAngularVelocity', 
 'getAxisVect', 
 'getDistanceTo', 
 'getLinearVelocity', 
 'getPhysicsId', 
 'getPropertyNames', 
 'getReactionForce', 
 'getVectTo', 
 'getVelocity', 
 'gravity', 
 'groupMembers', 
 'groupObject', 
 'invalid', 
 'isPlayingAction', 
 'isSuspendDynamics', 
 'layer', 
 'life', 
 'linVelocityMax', 
 'linVelocityMin', 
 'linearDamping', 
 'linearVelocity', 
 'localAngularVelocity', 
 'localInertia', 
 'localLinearVelocity', 
 'localOrientation', 
 'localPosition', 
 'localScale', 
 'localTransform', 
 'lodManager', 
 'logger', 
 'loggerName', 
 'logicCulling', 
 'logicCullingRadius', 
 'mass', 
 'meshes', 
 'name', 
 'occlusion', 
 'onRemove', 
 'orientation', 
 'parent', 
 'physicsCulling', 
 'physicsCullingRadius', 
 'playAction', 
 'position', 
 'rayCast', 
 'rayCastTo', 
 'reinstancePhysicsMesh', 
 'removeParent', 
 'replaceMesh', 
 'replacePhysicsShape', 
 'restoreDynamics', 
 'restorePhysics', 
 'scaling', 
 'scene', 
 'sendMessage', 
 'sensors', 
 'setActionFrame', 
 'setAngularVelocity', 
 'setCcdMotionThreshold', 
 'setCcdSweptSphereRadius', 
 'setCollisionMargin', 
 'setDamping', 
 'setLinearVelocity', 
 'setOcclusion', 
 'setParent', 
 'setVisible', 
 'state', 
 'stopAction', 
 'suspendDynamics', 
 'suspendPhysics', 
 'timeOffset', 
 'update', 
 'visible', 
 'worldAngularVelocity', 
 'worldLinearVelocity', 
 'worldOrientation', 
 'worldPosition', 
 'worldScale', 
 'worldTransform']