import numpy as np
import matplotlib.pyplot as plt
import random as rdm

import utilities as uts
import coverage_planar_planner.msg as cms



class Landmark(object):


    def __init__(self,
            pos=np.array([0.0,0.0]),
            ori=np.array([1.0,0.0]),
            color='black'
            ):
        self._pos = np.array(pos)
        self._ori = uts.normalize(ori)
        self._color = color


    @classmethod
    def from_msg(cls, msg):
        """Constructs a Landmark object from a Landmark ROS message."""
        pos = np.array(msg.position)
        ori = uts.normalize(np.array(msg.orientation))
        return cls(pos, ori)


    @classmethod
    def random(cls,
            xlim=(-1.0, 1.0),
            ylim=(-1.0, 1.0),
            ):
        """Constructs a Landmark object with random position and orientation.
        The position is chosen within the given boundaries.
        """
        x = rdm.uniform(*xlim)
        y = rdm.uniform(*ylim)
        pos = np.array([x,y])
        ori = uts.normalize(np.random.rand(2)-0.5)
        return cls(pos, ori)

    def to_msg(self):
        """Converts a Landmark object into a Landmark ROS message."""
        msg = cms.Landmark(position=self._pos, orientation=self._ori)
        return msg


    def __str__(self):
        string = "Landmark object for the coverage planner"
        string += "\nPosition: " + str(self._pos)
        string += "\nOrientation: " + str(self._ori)
        return string


    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = np.array(value)


    @property
    def ori(self):
        return self._ori

    @ori.setter
    def ori(self, value):
        self._ori = uts.normalize(value)


    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value



    def draw(self,
            draw_orientation=True,
            scale=1.0,
            alpha=0.6,
            color=None
            ):
        """Draws the landmark as a point.
        If `draw_orientation` is `True`, it draws the orientation as an arrow.
        """

        if color==None:
            color=self._color
        x = self.pos[0]
        y = self.pos[1]
        point = plt.scatter(x,y,
            s=scale*20.0,
            marker='s',
            color=color,
            alpha=alpha,
            edgecolor=color,
            linewidth=2
            )
        arrow = None
        if draw_orientation:
            vec = self._ori*scale*0.4
            arrow = plt.arrow(x, y, vec[0], vec[1],
                head_width=scale*0.12,
                head_length=scale*0.12,
                alpha=alpha,
                facecolor=color,
                edgecolor=color)
        return point, arrow





if __name__ == '__main__':
    lmk = Landmark()
    plt.figure()
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    print lmk.pos
    print lmk.ori
    print lmk.to_msg()
    lmk.draw()
    plt.show()
