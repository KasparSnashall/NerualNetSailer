"""
This file will run the sailing game.

The goal is to get up the course and across the finish line as quickly as possible

Some intial basic rules:
Boats cannot sail directly upwind
Boats acceleration depends on the angle to the wind

Arcade will be used to make the game, 
we will try to keep game and display logic seperately

"""

import asyncio # going to run several things at the same time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from numpy import sin, cos
import arcade # using this for the game
import pandas as pd 
from scipy.interpolate import interp1d

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Neural Net Sailer"
WINDSPEED = 2

class Boat(arcade.Sprite):
    """
    Player class
    """
    sail_angle = 180 # angle of the sail 
    boat_data = pd.read_csv('speed.csv')
    interp_velocity = interp1d(boat_data['angle'],boat_data['max velocity (wind fraction)'])
    interp_liftcoeff = interp1d(boat_data['angle'],boat_data['lift coeff'])
    change_sail_angle = 0
    accel = 0

    def update(self):
        # Move player.
        # Remove these lines if physics engine is moving player.
        # Will need to add the acc and velocity in here
        self.sail_angle += self.change_sail_angle
        if self.sail_angle < 0:
            self.sail_angle = 0
        if self.sail_angle > 180:
            self.sail_angle = 180
    
        velocity = WINDSPEED*(self.interp_velocity(abs(self.angle)%360)) + self.accel
        angle_attack = abs(self.angle-self.sail_angle)%180

        self.center_y += velocity*(sin(np.deg2rad(self.angle+90)))
        self.center_x += velocity*(cos(np.deg2rad(self.angle+90)))
        self.angle += self.change_angle
        self.angle = abs(self.angle%360) # no need to be greater than 360 
        


        # Check for out-of-bounds
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1 
        
class SailGame(arcade.Window):
    def __init__(self, width, height, title) -> None:
        super().__init__(width, height, title)
        self.acceleration = [0,0] # x,7 acceleration
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = [self.x_velocity, self.y_velocity] # x,y velocty vector, assume boat always travels in direction of velocity
        self.position = [100,100] # x,y position
        self.wind_angle = 90 # to the map, i.e. sout
        self.wind_speed = 5 # knots
        self.maxspeed = 5 # m/s # boats wont go much faster then this
        self.MAXTIME = 5000 # maximum amount of time before race ends
        self.racefinished = False # finished flag
        #self.setup_race_course()
        arcade.set_background_color(arcade.color.SEA_BLUE)

        self.player_list = None
        self.player_sprite = None
        self.score = 0
        self.set_mouse_visible(False)
        
    def acceleration(self):
        """
        Function to describe the effect of acceleration on the speed vector
        """
        # needs to take into account the angle of the wind to the boat
        # if sub 20 degrees to the wind it will need to be negative
        # Probably want a cardiod shape otherwise
        
        pass

    def setup_race_course(self):
        """
        Will set up the race course, may have this customisable in the future
        """
        self.max_x = 100 # if we reach this we auto tack
        self.max_y = 500 # also defines the win condition
        self.min_x = -100 
        self.min_y = 0
        self.start_line_y = 25 # the start line
        self.finish_line_y = 450 # the finish line, intially just a line
    
    def setup(self):
        """ Set up the game variables. Call to re-start the game. """
        # Create your sprites and sprite lists here
        self.player_list = arcade.SpriteList()
        self.player_sprite = Boat("Boat.png", 0.05)
        self.player_sprite.center_x = self.position[0]
        self.player_sprite.center_y = self.position[1]
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        self.clear()
        self.player_list.draw()
        # Call draw() on all your sprite lists below

    def on_update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        self.player_list.update()

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        
        Suppose the AI will just be able to call this
        """

         # If the player presses a key, update the speed
         # This will in the future either control the tiller or control the line
         # The position will have to change dependent on acceleration
        if key == arcade.key.UP:
            self.player_sprite.change_sail_angle = 1
        elif key == arcade.key.DOWN:
            self.player_sprite.change_sail_angle = -1

        elif key == arcade.key.LEFT:
            self.player_sprite.change_angle = -2 # seems about right 
            self.player_sprite.accel = -0.05 # small penality for using rudder
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 2
            self.player_sprite.accel = -0.05


    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        # If a player releases a key, zero out the speed.
        # This doesn't work well if multiple keys are pressed.
        # Use 'better move by keyboard' example if you need to
        # handle this.
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_sail_angle = 0
            
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_angle = 0    
            self.player_sprite.accel = 0    

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


if __name__ == "__main__":
    game = SailGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()