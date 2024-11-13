"""
Models module for Planetoids

This module contains the model classes for the Planetoids game. Anything that you
interact with on the screen is model: the ship, the bullets, and the planetoids.

We need models for these objects because they contain information beyond the simple
shapes like GImage and GEllipse. In particular, ALL of these classes need a velocity
representing their movement direction and speed (and hence they all need an additional
attribute representing this fact). But for the most part, that is all they need. You
will only need more complex models if you are adding advanced features like scoring.

You are free to add even more models to this module. You may wish to do this when you
add new features to your game, such as power-ups. If you are unsure about whether to
make a new class or not, please ask on Ed Discussions.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from consts import *
from game2d import *
from introcs import *
import math

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py. If you need extra information from Gameplay, then it should be a 
# parameter in your method, and Wave should pass it as a argument when it calls 
# the method.

# START REMOVE
# HELPER FUNCTION FOR MATH CONVERSION
def degToRad(deg):
    """
    Returns the radian value for the given number of degrees
    
    Parameter deg: The degrees to convert
    Precondition: deg is a float
    """
    return math.pi*deg/180
# END REMOVE


class Bullet(GEllipse):
    """
    A class representing a bullet from the ship
    
    Bullets are typically just white circles (ellipses). The size of the bullet is 
    determined by constants in consts.py. However, we MUST subclass GEllipse, because 
    we need to add an extra attribute for the velocity of the bullet.
    
    The class Wave will need to look at this velocity, so you will need getters for
    the velocity components. However, it is possible to write this assignment with no 
    setters for the velocities. That is because the velocity is fixed and cannot change 
    once the bolt is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GEllipse as a
    helper. This init will need a parameter to set the direction of the velocity.
    
    You also want to create a method to update the bolt. You update the bolt by adding
    the velocity to the position. While it is okay to add a method to detect collisions
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO SET THE POSITION AND VELOCITY
    def __init__(self, velocity, x, y, height = 2 * BULLET_RADIUS, width = 2 * BULLET_RADIUS):
        super().__init__(x = x, y = y, height = height, width = width, fillcolor = BULLET_COLOR)
        self._velocity = velocity
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def _bullet_move(self):

        self.x += self._velocity.x
        self.y += self._velocity.y

    def _shield_Move(self, velocity):
        self.x += velocity.x
        self.y += velocity.y

    def _shield_WrapUp(self):
        if self.x <= -DEAD_ZONE:
            self.x = GAME_WIDTH+DEAD_ZONE

        elif self.x >= GAME_WIDTH+DEAD_ZONE:
            self.x = -DEAD_ZONE

        if self.y <= -DEAD_ZONE:
            self.y = GAME_HEIGHT+DEAD_ZONE

        elif self.y >= GAME_HEIGHT+DEAD_ZONE:
            self.y = -DEAD_ZONE


class Ship(GImage):
    """
    A class to represent the game ship.
    
    This ship is represented by an image. The size of the ship is determined by constants 
    in consts.py. However, we MUST subclass GEllipse, because we need to add an extra 
    attribute for the velocity of the ship, as well as the facing vecotr (not the same)
    thing.
    
    The class Wave will need to access these two values, so you will need getters for 
    them. But per the instructions,these values are changed indirectly by applying thrust 
    or turning the ship. That means you won't want setters for these attributes, but you 
    will want methods to apply thrust or turn the ship.
    
    This class needs an __init__ method to set the position and initial facing angle.
    This information is provided by the wave JSON file. Ships should start with a shield
    enabled.
    
    Finally, you want a method to update the ship. When you update the ship, you apply
    the velocity to the position. While it is okay to add a method to detect collisions 
    in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y, angle):
        super().__init__(x = x, y = y, angle = angle, height = 2 * SHIP_RADIUS, width = 2 * SHIP_RADIUS, source = SHIP_IMAGE)
        self._velocity = Vector2(0, 0)
        self._facing = Vector2(math.cos(degToRad(angle)), math.sin(degToRad(angle)))
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def _turn(self, input):
        if input.is_key_down('right'):
            self.angle -= SHIP_TURN_RATE
            angle = self.angle
            self._facing = Vector2(math.cos(degToRad(self.angle)), math.sin(degToRad(self.angle)))

        if input.is_key_down('left'):
            self.angle += SHIP_TURN_RATE
            angle = self.angle
            self._facing = Vector2(math.cos(degToRad(self.angle)), math.sin(degToRad(self.angle)))


    def _impulse(self, input):
        impulse = self._facing * SHIP_IMPULSE
        if input.is_key_down('up'):
            self._velocity += impulse
            if self._velocity.length() > SHIP_MAX_SPEED: 
                self._velocity = self._velocity.normalize() * SHIP_MAX_SPEED
        self.x += self._velocity.x
        self.y += self._velocity.y


    def _ship_WrapUp(self):
        if self.x <= -DEAD_ZONE:
            self.x = GAME_WIDTH+DEAD_ZONE

        elif self.x >= GAME_WIDTH+DEAD_ZONE:
            self.x = -DEAD_ZONE

        if self.y <= -DEAD_ZONE:
            self.y = GAME_HEIGHT+DEAD_ZONE

        elif self.y >= GAME_HEIGHT+DEAD_ZONE:
            self.y = -DEAD_ZONE


class Asteroid(GImage):
    """
    A class to represent a single asteroid.
    
    Asteroids are typically are represented by images. Asteroids come in three 
    different sizes (SMALL_ASTEROID, MEDIUM_ASTEROID, and LARGE_ASTEROID) that 
    determine the choice of image and asteroid radius. We MUST subclass GImage, because 
    we need extra attributes for both the size and the velocity of the asteroid.
    
    The class Wave will need to look at the size and velocity, so you will need getters 
    for them.  However, it is possible to write this assignment with no setters for 
    either of these. That is because they are fixed and cannot change when the planetoid 
    is created. 
    
    In addition to the getters, you need to write the __init__ method to set the size
    and starting velocity. Note that the SPEED of an asteroid is defined in const.py,
    so the only thing that differs is the velocity direction.
    
    You also want to create a method to update the asteroid. You update the asteroid 
    by adding the velocity to the position. While it is okay to add a method to detect 
    collisions in this class, you may find it easier to process collisions in wave.py.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    
    # INITIALIZER TO CREATE A NEW ASTEROID
    def __init__(self, x, y, size, direction, source, height, width):
        super().__init__(x = x, y = y, size = size, direction = direction, height = height, width = width, source = source)
        self._size = size
        self._direction = direction
    
    # ADDITIONAL METHODS (MOVEMENT, COLLISIONS, ETC)
    def _move_asteroid(self):
        # print(keywords['size'])
        velocity = 0
        direction = Vector2(self._direction[0], self._direction[1])
        # print(keywords['size'])
        if self._size == 'small':
            velocity = SMALL_SPEED * direction.normalize()

        if self._size == 'medium':
            velocity = MEDIUM_SPEED * direction.normalize()

        if self._size == 'large':
            velocity = LARGE_SPEED * direction.normalize()

        # return velocity
        self.x += velocity.x
        self.y += velocity.y

    def _asteroid_wrapUp(self):
        if self.x <= -DEAD_ZONE:
            self.x = GAME_WIDTH+DEAD_ZONE

        elif self.x >= GAME_WIDTH+DEAD_ZONE:
            self.x = -DEAD_ZONE

        if self.y <= -DEAD_ZONE:
            self.y = GAME_HEIGHT+DEAD_ZONE

        elif self.y >= GAME_HEIGHT+DEAD_ZONE:
            self.y = -DEAD_ZONE






# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
