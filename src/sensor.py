import numpy as np
import matplotlib.pyplot as plt

import utilities as uts
import footprints as fps

import rospy as rp


class Sensor(object):


    def __init__(
	        self,
	        pos=np.array([0.0,0.0]),
	        ori=np.array([1.0,0.0]),
	        fp=fps.EggFootprint(),
	        color = 'black',
	        landmarks = []
	        ):
        self._pos = np.array(pos)
        self._ori = uts.normalize(ori)
        self._fp = fp
        self._color = color


    def __str__(self):
	    string = "Sensor object for the coverage planner."
	    string += "\nPosition: " + str(self._pos)
	    string += "\nOrientation: " + str(self._ori)
	    string += "\nFootprint: " + str(self._fp)
	    return string


    def perception(self, lmk):
	    p = self._pos
	    n = self._ori
	    q = lmk.pos
	    m = lmk.ori
	    return self._fp(p,n,q,m)


    def coverage(self, landmarks):
	    return sum([self.perception(lmk)
		    for lmk in landmarks], 0.0)


    def per_pos_grad(self, lmk):
	    p = self._pos
	    n = self._ori
	    q = lmk.pos
	    m = lmk.ori
	    return self._fp.pos_grad(p,n,q,m)


    def cov_pos_grad(self, landmarks):
	    return sum([self.per_pos_grad(lmk)
		    for lmk in landmarks], np.zeros(2))


    def per_ori_grad(self, lmk):
	    p = self._pos
	    n = self._ori
	    q = lmk.pos
	    m = lmk.ori
	    return self._fp.ori_grad(p,n,q,m)


    def cov_ori_grad(self, landmarks):
	    return sum([self.per_ori_grad(lmk)
		    for lmk in landmarks], np.zeros(2))


    @property
    def pos(self):
	    return np.array(self._pos)

    @pos.setter
    def pos(self, value):
	    self._pos = np.array(value)

    @property
    def ori(self):
	    return np.array(self._ori)

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
            scale=10.0,
            alpha=1,
            color=None
            ):
        if color==None:
            color=self._color
        x = self.pos[0]
        y = self.pos[1]
        point = plt.scatter(x,y,
            s=1.5*scale,
            color='#121f1f',
            alpha=alpha,
            edgecolor='#121f1f',
            linewidth=2)
        arrow = None
        if draw_orientation:
            vec = self._ori*0.05*scale
            arrow = plt.arrow(x, y, vec[0], vec[1],
	            head_width=scale*0.03,
	            head_length=scale*0.03,
	            alpha=alpha,
	            facecolor=color,
	            edgecolor='#121f1f',
	            linewidth=2)
        return point, arrow









if __name__ == '__main__':
	import landmark as lm
	lmk = lm.Landmark()
	srr = Sensor()
	print srr.perception(lmk)
	print srr.coverage([lmk])
	print srr.per_pos_grad(lmk)
	print srr.cov_pos_grad([lmk])
	print srr.per_ori_grad(lmk)
	print srr.cov_ori_grad([lmk])
	plt.figure()
	plt.xlim(-5,5)
	plt.ylim(-5,5)
	lmk.draw()
	srr.draw()
	plt.grid()
	plt.show()
