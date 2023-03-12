"""
This file will run the sailing game.

The goal is to get up the course and across the finish line as quickly as possible

Some intial basic rules:
Boats cannot sail directly upwind
Boats acceleration depends on the angle to the wind

"""

import asyncio # going to run several things at the same time
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from numpy import sin, cos
class SailGame():
    def __init__(self) -> None:
        self.acceleration = [0,0] # x,7 acceleration
        self.x_velocity = 0
        self.y_velocty = 0
        self.velocity = [self.x_velocity,self.y_velocity] # x,y velocty vector, assume boat always travels in direction of velocity
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
        fig, ax = plt.subplots()
        for rot in [0, 15, 30, 45, 60, 90, 110, 180, 210, 315, 360]:

            marker, scale = self.gen_arrow_head_marker(rot)
            markersize = 25
            ax.scatter(rot, 0, marker=marker, s=(markersize*scale)**2)

        ax.set_xlabel('Rotation in degree')

        plt.show()

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
    
    def gen_arrow_head_marker(self, rot):

        """generate a marker to plot with matplotlib scatter, plot, ...

        https://matplotlib.org/stable/api/markers_api.html#module-matplotlib.markers

        rot=0: positive x direction
        Parameters
        ----------
        rot : float
            rotation in degree
            0 is positive x direction

        Returns
        -------
        arrow_head_marker : Path
            use this path for marker argument of plt.scatter
        scale : float
            multiply a argument of plt.scatter with this factor got get markers
            with the same size independent of their rotation.
            Paths are autoscaled to a box of size -1 <= x, y <= 1 by plt.scatter
        
        From https://stackoverflow.com/questions/23345565/is-it-possible-to-control-matplotlib-marker-orientation


        """
        arr = np.array([[.1, .3], [.1, -.3], [1, 0], [.1, .3]])  # arrow shape
        angle = rot / 180 * np.pi
        rot_mat = np.array([
            [np.cos(angle), np.sin(angle)],
            [-np.sin(angle), np.cos(angle)]
            ])
        arr = np.matmul(arr, rot_mat)  # rotates the arrow

        # scale
        x0 = np.amin(arr[:, 0])
        x1 = np.amax(arr[:, 0])
        y0 = np.amin(arr[:, 1])
        y1 = np.amax(arr[:, 1])
        scale = np.amax(np.abs([x0, x1, y0, y1]))
        codes = [mpl.path.Path.MOVETO, mpl.path.Path.LINETO,mpl.path.Path.LINETO, mpl.path.Path.CLOSEPOLY]
        arrow_head_marker = mpl.path.Path(arr, codes)
        return arrow_head_marker, scale

if __name__ == "__main__":
    SailGame().main()