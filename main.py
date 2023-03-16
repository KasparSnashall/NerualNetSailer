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

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Neural Net Sailer"

class SailGame(arcade.Window):
    def __init__(self, width, height, title) -> None:
        super().__init__(width, height, title)
        self.acceleration = [0,0] # x,7 acceleration
        self.x_velocity = 0
        self.y_velocity = 0
        self.velocity = [self.x_velocity, self.y_velocity] # x,y velocty vector, assume boat always travels in direction of velocity
        self.position = [100,100] # x,y position
        self.windvector = [-0.5,-0.5] # a simple wind vector # decomposed to cartesian
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
        pass

    def change_direction(self, rotation):
        """
        Will take an input to change direction
        """
        self.x_velocity = self.x_velocity*cos(rotation) - sin(rotation)*self.y_velocty
        self.y_velocty = self.x_velocity*cos(rotation) + cos(rotation)*self.y_velocty
    
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
        self.player_sprite = arcade.Sprite("Boat.png", 0.05)
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
        pass

    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        https://api.arcade.academy/en/latest/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

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