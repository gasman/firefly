from config import MOTOR_SPACING, SPOOL_RADIUS, STEPS_PER_ROTATION
from motor import MotorRegulator

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
