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
#from Indicator import IndicatorBar

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Neural Net Sailer"
WINDSPEED = 2
WINDANGLE = 360
WINDVECTOR = [WINDSPEED*cos(np.deg2rad(WINDANGLE)), WINDSPEED*sin(np.deg2rad(WINDANGLE))]


class Boat(arcade.Sprite):
    """
    Player class
    """
    def __init__(self, filename, scale, bar_list: arcade.SpriteList):
        super().__init__(filename=filename,scale=scale)
        self.sail_angle = 180 # angle of the sail 
        self.boat_data = pd.read_csv('speed.csv')
        self.interp_velocity = interp1d(self.boat_data['angle'],self.boat_data['max velocity (wind fraction)'])
        self.interp_liftcoeff = interp1d(self.boat_data['angle'],self.boat_data['lift coeff'])
        self.change_sail_angle = 0
        self.accel = 0
        self.indicator_bar: Indicatorbar = IndicatorBar(
            self, bar_list, (self.center_x, self.center_y)
            )

    def update(self):
        # Move player.
        # Remove these lines if physics engine is moving player.
        # Will need to add the acc and velocity in here
        self.sail_angle += self.change_sail_angle
        if self.sail_angle < 0:
            self.sail_angle = 0
        if self.sail_angle > 90: # relative to the boat direction
            self.sail_angle = 90

        self.velocity = WINDSPEED*(self.interp_velocity(abs(self.angle)%360)) + self.accel 
        self.move_vector = [self.velocity*cos(np.deg2rad(self.angle)), self.velocity*sin(np.deg2rad(self.angle))]
        
        # need to work out the apprent wind vector
        angle_attack = abs(self.angle)-self.sail_angle
        print(angle_attack)
        # probably need the apprent wind vector to determine angle of attack

        self.center_y += self.velocity*(sin(np.deg2rad(self.angle+90)))
        self.center_x += self.velocity*(cos(np.deg2rad(self.angle+90)))
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
        self.player_sprite = Boat("Boat.png", 0.05, self.player_list)
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


class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.

    :param Player owner: The owner of this indicator bar.
    :param arcade.SpriteList sprite_list: The sprite list used to draw the indicator
  1
  1 initial position of the bar.
    :param arcade.Color full_color: The color of the bar.
    :param arcade.Color background_color: The background color of the bar.
    :param int width: The width of the bar.
    :param int height: The height of the bar.
    :param int border_size: The size of the bar's border.
    """

    def __init__(
        self,
        owner: Boat,
        sprite_list: arcade.SpriteList,
        position: tuple[float, float] = (0, 0),
        full_color: arcade.Color = arcade.color.GREEN,
        background_color: arcade.Color = arcade.color.BLACK,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._box_width: int = width
        self._box_height: int = height
        self._half_box_width: int = self._box_width // 2
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width + border_size,
            self._box_height + border_size,
            background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._box_width,
            self._box_height,
            full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness and position of the bar
        self.fullness: float = 1.0
        self.position: tuple[float, float] = position

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.width = self._box_width * new_fullness
            self.full_box.left = self._center_x - (self._box_width // 2)

    @property
    def position(self) -> tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._box_width // 2)




if __name__ == "__main__":
    game = SailGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    game.setup()
    arcade.run()