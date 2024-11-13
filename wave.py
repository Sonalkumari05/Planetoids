"""
Subcontroller module for Planetoids

This module contains the subcontroller to manage a single level (or wave) in the 
Planetoids game.  Instances of Wave represent a single level, and should correspond
to a JSON file in the Data directory. Whenever you move to a new level, you are 
expected to make a new instance of the class.

The subcontroller Wave manages the ship, the asteroids, and any bullets on screen. These 
are model objects. Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Ed Discussions and we will answer.

# YOUR NAME(S) AND NETID(S) HERE
# DATE COMPLETED HERE
"""
from game2d import *
from consts import *
from models import *
import random
import datetime

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Level is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)

class Wave(object):
    """
    This class controls a single level or wave of Planetoids.
    
    This subcontroller has a reference to the ship, asteroids, and any bullets on screen.
    It animates all of these by adding the velocity to the position at each step. It
    checks for collisions between bullets and asteroids or asteroids and the ship 
    (asteroids can safely pass through each other). A bullet collision either breaks
    up or removes a asteroid. A ship collision kills the player. 
    
    The player wins once all asteroids are destroyed.  The player loses if they run out
    of lives. When the wave is complete, you should create a NEW instance of Wave 
    (in Planetoids) if you want to make a new wave of asteroids.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 25 for an example.  This class will be similar to
    than one in many ways.
    
    All attributes of this class are to be hidden. No attribute should be accessed 
    without going through a getter/setter first. However, just because you have an
    attribute does not mean that you have to have a getter for it. For example, the
    Planetoids app probably never needs to access the attribute for the bullets, so 
    there is no need for a getter there. But at a minimum, you need getters indicating
    whether you one or lost the game.
    """
    # LIST ANY ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    # THE ATTRIBUTES LISTED ARE SUGGESTIONS ONLY AND CAN BE CHANGED AS YOU SEE FIT
    # Attribute _data: The data from the wave JSON, for reloading 
    # Invariant: _data is a dict loaded from a JSON file
    #
    # Attribute _ship: The player ship to control 
    # Invariant: _ship is a Ship object
    #
    # Attribute _asteroids: the asteroids on screen 
    # Invariant: _asteroids is a list of Asteroid, possibly empty
    #
    # Attribute _bullets: the bullets currently on screen 
    # Invariant: _bullets is a list of Bullet, possibly empty
    #
    # Attribute _lives: the number of lives left 
    # Invariant: _lives is an int >= 0
    #
    # Attribute _firerate: the number of frames until the player can fire again 
    # Invariant: _firerate is an int >= 0
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    @property
    def ship(self):
        return self._ship
    

    @ship.setter
    def ship(self, other):
        json = other
        self._ship = Ship(x = json['ship']['position'][0], y = json['ship']['position'][1], angle = json['ship']['angle'])

    @property
    def data(self):
        return self._data
    

    
    # INITIALIZER (standard form) TO CREATE SHIP AND ASTEROIDS
    def __init__(self, json):
        self._data = json
        self._ship = Ship(x = json['ship']['position'][0], y = json['ship']['position'][1], angle = json['ship']['angle'])
        self._asteroids = [Asteroid(x = json['asteroids'][0]['position'][0], y = json['asteroids'][0]['position'][1], size = json['asteroids'][0]['size'], direction = json['asteroids'][0]['direction'], source = LARGE_IMAGE, height = 2 * LARGE_RADIUS, width = 2 * LARGE_RADIUS),
        Asteroid(x = json['asteroids'][1]['position'][0], y = json['asteroids'][1]['position'][1], size = json['asteroids'][1]['size'], direction = json['asteroids'][1]['direction'], source = LARGE_IMAGE, height = 2 * LARGE_RADIUS, width = 2 * LARGE_RADIUS),
        Asteroid(x = json['asteroids'][2]['position'][0], y = json['asteroids'][2]['position'][1], size = json['asteroids'][2]['size'], direction = json['asteroids'][2]['direction'], source = MEDIUM_IMAGE, height = 2 * MEDIUM_RADIUS, width = 2 * MEDIUM_RADIUS),
        Asteroid(x = json['asteroids'][3]['position'][0], y = json['asteroids'][3]['position'][1], size = json['asteroids'][3]['size'], direction = json['asteroids'][3]['direction'], source = MEDIUM_IMAGE, height = 2 * MEDIUM_RADIUS, width = 2 * MEDIUM_RADIUS),
        Asteroid(x = json['asteroids'][4]['position'][0], y = json['asteroids'][4]['position'][1], size = json['asteroids'][4]['size'], direction = json['asteroids'][4]['direction'], source = SMALL_IMAGE, height = 2 * SMALL_RADIUS, width = 2 * SMALL_RADIUS),
        Asteroid(x = json['asteroids'][5]['position'][0], y = json['asteroids'][5]['position'][1], size = json['asteroids'][5]['size'], direction = json['asteroids'][5]['direction'], source = SMALL_IMAGE, height = 2 * SMALL_RADIUS, width = 2 * SMALL_RADIUS)]

        self._bullets = []
        self._firerate = 30
        self._shieldRate = 0
        self._lives = SHIP_LIVES
        self._shield = Bullet(x= self._ship.x, y = self._ship.y, width = 2 * SHIELD_SCALE * SHIP_RADIUS, height = 2 * SHIELD_SCALE * SHIP_RADIUS, velocity = self._ship._velocity)
        self._sounds = {'bulletAst' : Sound('blast1.wav'), 'shipAst' : Sound('explosion.wav'), 'bullet': Sound('pew1.wav'), 'thruster' : Sound('afterburner.wav')}
        self._thruster = GSprite(source='flame-sprites.png',format=(4,1),width = 2 * SHIP_RADIUS,height = 2 * SHIP_RADIUS, x = self._ship.x, y = self._ship.y, angle = self._ship.angle)
        self._score = 0

    
    # UPDATE METHOD TO MOVE THE SHIP, ASTEROIDS, AND BULLETS
    def update(self, input):
        if not self._ship is None:
            if not self._shield is None:
                self._shield._shield_Move(self._ship._velocity)
            self._ship._turn(input)
            self._ship._impulse(input)
            self._thruster.frame = 0
            # self._sounds['thruster'].play()
            # self._Applythrust(input)
            # self._sounds['thruster'].play(loop = False)
            self._ship._ship_WrapUp()
            # self._shield._shield_WrapUp()
            self._bullet_create(input)
            self._firerate += 1
            self._shieldRate += 1

            self._collision_btw_ship_asteroid()
            self._collision_btw_bullet_asteroid()

            j = 0 
            while j < len(self._bullets):
                self._bullets[j]._bullet_move()
                j += 1

        i = 0
        while i < len(self._asteroids):
            self._asteroids[i]._move_asteroid()
            self._asteroids[i]._asteroid_wrapUp()
            i += 1 

            
    # DRAW METHOD TO DRAW THE SHIP, ASTEROIDS, AND BULLETS
    def draw(self,view):
        if not self._ship is None:
            if not self._shield is None:
                self._shield.draw(view)
                if self._shieldRate >= SHIELD_TIME:
                    self._shield = None

            self._ship.draw(view)
            if not self._thruster is None:
                self._thruster.draw(view)

        i = 0
        while i < len(self._asteroids):
            self._asteroids[i].draw(view)
            i += 1

        j = 0 
        while j < len(self._bullets):
            self._bullets[j].draw(view)
            bullet = self._bullets[j]
            if bullet.x <= -DEAD_ZONE or bullet.x >= GAME_WIDTH+DEAD_ZONE or bullet.y <= -DEAD_ZONE or bullet.y >= GAME_HEIGHT+DEAD_ZONE:
                del self._bullets[j]

            j += 1

    
    # RESET METHOD FOR CREATING A NEW LIFE
    def _ship_reset(self):
        json = self._data
        self._ship = Ship(x = json['ship']['position'][0], y = json['ship']['position'][1], angle = json['ship']['angle'])

    def _shield_reset(self):
        # print(self._shieldRate)
        self._shield = Bullet(x= self._ship.x, y = self._ship.y, width = 2 * SHIELD_SCALE * SHIP_RADIUS, height = 2 * SHIELD_SCALE * SHIP_RADIUS, velocity = self._ship._velocity)
        self._shieldRate = 0    

    
    # HELPER METHODS FOR PHYSICS AND COLLISION DETECTION

    def _bullet_create(self, input):
        if input.is_key_down('spacebar') and self._firerate >= BULLET_RATE:

            self._sounds['bullet'].play()   # Sound for bullet.

            tip = (self._ship._facing * SHIP_RADIUS) + Vector2(self._ship.x, self._ship.y)
            # print(- tip.x, tip.y)
            velocity = self._ship._facing * BULLET_SPEED

            bullet = Bullet( velocity , x = tip.x , y = tip.y)
            self._bullets.append(bullet)

            self._firerate = 0           # Reset to Zero for new bullet.
            self._sounds['bullet'].play(loop = False)


    def _Applythrust(self, input):
        # self._thruster.x += self._ship._velocity.x
        # self._thruster.y += self._ship._velocity.y
        # self._thruster.frame += 1
        
        if input.is_key_down('up') and self._thruster.frame < 4:
            self._sounds['thruster'].play()
            self._thruster.frame += 1

        # else:
            # self._sounds['thruster'].play(loop = False)

            # bottom = - (self._ship._facing * SHIP_RADIUS) + Vector2(self._ship.x, self._ship.y)
            # self._thruster.x += self._ship._velocity.x
            # self._thruster.y += self._ship._velocity.y

            

        # if input.is_key_down('up') and self._thruster.frame == 4:

        #     self._thruster = 


            # self._thruster = None

        # elif self._thruster.count > 0:
            # self._thruster.frame -= 1


    def _collision_btw_ship_asteroid(self):
        i = 0
        while i < len(self._asteroids):

            a = self._ship.x - self._asteroids[i].x
            b = self._ship.y - self._asteroids[i].y

            distance = (a ** 2 + b ** 2) ** 0.5
            radius_Sum = self._asteroids[i].width / 2 + self._ship.width / 2

            if distance < radius_Sum:
                self._sounds['shipAst'].play()
                self._asteroid_break(self._asteroids[i], self._ship)
                if self._shield is None:
                    self._ship = None
                    self._lives -= 1
                del self._asteroids[i]
                self._sounds['shipAst'].play(loop = False)
                break
            

            i += 1


    def _collision_btw_bullet_asteroid(self):
        j = 0
        while j < len(self._bullets):
            bullet = self._bullets[j]

            i = 0
            while i < len(self._asteroids):
                a = bullet.x - self._asteroids[i].x
                b = bullet.y - self._asteroids[i].y 

                distance = (a ** 2 + b ** 2) ** 0.5
                radius_Sum = self._asteroids[i].width / 2 + self._bullets[j].width / 2

                if distance < radius_Sum:
                    self._sounds['bulletAst'].play()
                    self._asteroid_break(self._asteroids[i], self._bullets[j])
                    if self._asteroids[i]._size == LARGE_ASTEROID:
                        self._score += 50
                    elif self._asteroids[i]._size == MEDIUM_ASTEROID:
                        self._score += 80

                    elif self._asteroids[i]._size == SMALL_ASTEROID:
                        self._score += 100
                    del self._asteroids[i]
                    del self._bullets[j]
                    self._sounds['bulletAst'].play(loop = False)
                    break

                i += 1

            j += 1

    def _asteroid_break(self, asteroid, other):
        if other._velocity.x == 0 and other._velocity.y == 0:
            v0 = Vector2(other._facing.x, other._facing.y)
            v1 = Vector2(other._facing.x * math.cos(degToRad(120)) - other._facing.y * math.sin(degToRad(120)), other._facing.x * math.sin(degToRad(120)) + other._facing.y * math.cos(degToRad(120)))
            v2 = Vector2(other._facing.x * math.cos(degToRad(240)) - other._facing.y * math.sin(degToRad(240)), other._facing.x * math.sin(degToRad(240)) + other._facing.y * math.cos(degToRad(240)))
        else:
            v0 = Vector2(other._velocity.x, other._velocity.y).normalize()
            v1 = Vector2(other._velocity.x * math.cos(degToRad(120)) - other._velocity.y * math.sin(degToRad(120)), other._velocity.x * math.sin(degToRad(120)) + other._velocity.y * math.cos(degToRad(120))).normalize()
            v2 = Vector2(other._velocity.x * math.cos(degToRad(240)) - other._velocity.y * math.sin(240), other._velocity.x * math.sin(degToRad(240)) + other._velocity.y * math.cos(degToRad(240))).normalize()

        if asteroid._size == LARGE_ASTEROID :
            self._asteroids.append(Asteroid(x = asteroid.x + (v0 * MEDIUM_RADIUS).x, y = asteroid.y + (v0 * MEDIUM_RADIUS).y, size = 'medium', direction = [v0.x , v0.y], height = 2 * MEDIUM_RADIUS, width = 2 * MEDIUM_RADIUS, source = MEDIUM_IMAGE))
            self._asteroids.append(Asteroid(x = asteroid.x + (v1 * MEDIUM_RADIUS).x, y = asteroid.y + (v1 * MEDIUM_RADIUS).y, size = 'medium', direction = [v1.x , v1.y], height = 2 * MEDIUM_RADIUS, width = 2 * MEDIUM_RADIUS, source = MEDIUM_IMAGE))
            self._asteroids.append(Asteroid(x = asteroid.x + (v2 * MEDIUM_RADIUS).x, y = asteroid.y + (v2 * MEDIUM_RADIUS).y, size = 'medium', direction = [v2.x , v2.y], height = 2 * MEDIUM_RADIUS, width = 2 * MEDIUM_RADIUS, source = MEDIUM_IMAGE))


        elif asteroid._size == MEDIUM_ASTEROID :
            self._asteroids.append(Asteroid(x = asteroid.x + (v0 * SMALL_RADIUS).x, y = asteroid.y + (v0 * SMALL_RADIUS).y, size = 'small', direction = [v0.x , v0.y], height = 2 * SMALL_RADIUS, width = 2 * SMALL_RADIUS, source = SMALL_IMAGE))
            self._asteroids.append(Asteroid(x = asteroid.x + (v1 * SMALL_RADIUS).x, y = asteroid.y + (v1 * SMALL_RADIUS).y, size = 'small', direction = [v1.x , v1.y], height = 2 * SMALL_RADIUS, width = 2 * SMALL_RADIUS, source = SMALL_IMAGE))
            self._asteroids.append(Asteroid(x = asteroid.x + (v2 * SMALL_RADIUS).x, y = asteroid.y + (v2 * SMALL_RADIUS).y, size = 'small', direction = [v2.x , v2.y], height = 2 * SMALL_RADIUS, width = 2 * SMALL_RADIUS, source = SMALL_IMAGE))
