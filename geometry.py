from config import MOTOR_SPACING, SPOOL_RADIUS, STEPS_PER_ROTATION
from motor import MotorRegulator

import time
import math


# number of radians in one motor step
STEP_ANGLE = (2.0 * math.pi) / STEPS_PER_ROTATION

class Arena(object):
	def __init__(self, position=(0, 0)):
		x, y = position
		m0_step, m1_step = self.get_step_values(x, y)

		self.motor0 = MotorRegulator(0, m0_step)
		self.motor1 = MotorRegulator(1, m1_step)

	@staticmethod
	def get_step_values(x, y):
		l0 = math.sqrt(x * x + y * y)
		neg_x = MOTOR_SPACING - x
		l1 = math.sqrt(neg_x * neg_x + y * y)

		m0_angle = l0 / SPOOL_RADIUS  # angle in radians
		m1_angle = l1 / SPOOL_RADIUS

		m0_step = m0_angle / STEP_ANGLE
		m1_step = m1_angle / STEP_ANGLE

		return (m0_step, m1_step)

	def set_position(self, x, y, time):
		m0_step, m1_step = self.get_step_values(x, y)
		self.motor0.set_position(m0_step, time)
		self.motor1.set_position(m1_step, time)


# how long we should take to trace a full circle
REVOLUTION_TIME = 90.0

# centre coordinates of circle, in metres from top left
CENTRE = (0.5, 0.5)
RADIUS = 0.3

t = 0.0

cx, cy = CENTRE

x = cx + RADIUS * math.sin(0)
y = cy - RADIUS * math.cos(0)

arena = Arena(position=(x, y))

while True:
	angle = t * 2 * math.pi / REVOLUTION_TIME
	x = cx + RADIUS * math.sin(angle)
	y = cy - RADIUS * math.cos(angle)

	arena.set_position(x, y, t)

	t += 0.0005  # TODO: a proper clock we can actually query
	time.sleep(0.0005)
