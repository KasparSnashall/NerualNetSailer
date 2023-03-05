"""
This file will run the sailing game.

The goal is to get up the course as quickly as possible
"""

import asyncio # going to run several things at the same time
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
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
        x = np.linspace(0, 10, 20)
        y = np.cos(x)
        image_path = 'Boat.png'
        fig, ax = plt.subplots()
        self.imscatter(x, y, image_path, zoom=0.1, ax=ax)
        ax.plot(x, y)
        plt.show()

    def imscatter(self,x, y, image, ax=None, zoom=1):
        if ax is None:
            ax = plt.gca()
        image = plt.imread(image)

        im = OffsetImage(image, zoom=zoom)
        x, y = np.atleast_1d(x, y)
        artists = []
        for x0, y0 in zip(x, y):
            ab = AnnotationBbox(im, (x0, y0), xycoords='data', frameon=False)
            artists.append(ax.add_artist(ab))
        ax.update_datalim(np.column_stack([x, y]))
        ax.autoscale()
        return artists

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
    SailGame().main()