#! /usr/bin/env python


import rospy as rp
import coverage_planar_planner.msg as cms

import numpy as np
import matplotlib.pyplot as plt
import threading as thd

import landmark as lm
import sensor as sn

rp.init_node('plotter_node')
XLIM = rp.get_param('xlim', (-5,5))
YLIM = rp.get_param('ylim', (-5,5))

plt.ion()
fig = plt.figure()
plt.xlabel(r'$x$')
plt.ylabel(r'$y$')
plt.axis('equal')
plt.axis(XLIM+YLIM)
plt.grid()

lock = thd.Lock()

sensor = sn.Sensor()
draw_sensor_flag = True
def pose_cb(pose):
    global sensor
    global draw_sensor_flag
    p = np.array(pose.position)
    n = np.array(pose.orientation)
    lock.acquire()
    sensor.pos = p
    sensor.ori = n
    draw_sensor_flag = True
    lock.release()
pose_sub = rp.Subscriber('pose', cms.Pose, pose_cb)


landmarks = set()
draw_landmarks_flag = True
def landmarks_cb(msg):
    global landmarks
    global draw_landmarks_flag
    lock.acquire()
    landmarks = [lm.Landmark.from_msg(datum) for datum in msg.data]
    draw_landmarks_flag = True
    lock.release()
landmarks_sub = rp.Subscriber('landmarks', cms.LandmarkArray, landmarks_cb)


point, arrow = sensor.draw()
lmks_artists = [lmk.draw() for lmk in landmarks]
def work():
    global point, arrow, lmks_artists
    global draw_sensor_flag, draw_landmarks_flag
    global sensor, landmarks
    lock.acquire()
    if draw_sensor_flag:
        point.remove()
        if not arrow == None:
            arrow.remove()
        point, arrow = sensor.draw()
        draw_sensor_flag = False
    if draw_landmarks_flag:
        for lp, la in lmks_artists:
            lp.remove()
            if not la == None:
                la.remove()
        lmks_artists = [lmk.draw(draw_orientation=False) for lmk in landmarks]
        draw_landmarks_flag = False
    lock.release()
    plt.draw()




rate = rp.Rate(6e1)
if __name__ == '__main__':
    while not rp.is_shutdown():
        work()
        rate.sleep()