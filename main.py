"""
This file will run the sailing game.

The goal is to get up the course as quickly as possible
"""


import matplotlib as plt
import numpy as np

class SailGame():
    def __init__(self) -> None:
        self.acceleration = [0,0] # x,7 acceleration
        self.velocity = [0,0] # x,y velocty vector, assume boat always travels in direction of velocity
        self.position = [0,0] # x,y position
        self.windvector = [-0.5,-0.5] # a simple wind vector # decomposed to cartesian
        self.maxspeed = 5 # m/s # boats wont go much faster then this
        self.MAXTIME = 5000 # maximum amount of time before race ends
        self.racefinished = False # finished flag
        self.setup_race_course()

    def main(self):
        """
        This will run the game
        """

        pass

    def acceleration(self):
        """
        Function to describe the effect of acceleration on the speed vector
        """
        pass

    def change_direction(self):
        """
        Will take an input to change direction
        """
        pass
    
    def setup_race_course(self):
        """
        Will set up the race course, may have this customisable in the future
        """
        self.max_x = 100 # if we reach this we auto tack
        self.max_y = 500 # also defines the win condition
        self.min_x = -100 
        self.min_y = 0

        pass

if __name__ == "__main__":
    SailGame.main()