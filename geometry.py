from config import MOTOR_SPACING, SPOOL_RADIUS, STEPS_PER_ROTATION, TICK_TIME
from motor import MotorRegulator

import math
import time


# number of radians in one motor step
STEP_ANGLE = (2.0 * math.pi) / STEPS_PER_ROTATION

class Arena(object):
	def __init__(self, position=(0, 0)):
		x, y = position
		m0_step, m1_step = self.get_step_values(x, y)

		self.motor0 = MotorRegulator(0, m0_step)
		self.motor1 = MotorRegulator(1, m1_step)

		self.time = 0

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

	def goto(self, x, y):
		# go to position (x, y), taking as long as required
		m0_step, m1_step = self.get_step_values(x, y)
		self.motor0.target = int(m0_step)
		self.motor0.deadline = None

		self.motor1.target = int(m1_step)
		self.motor1.deadline = None

		while not self.motor0.done() or not self.motor1.done():
			self.tick()

	def tick(self):
		self.motor0.tick(self.time)
		self.motor1.tick(self.time)
		time.sleep(TICK_TIME)
		self.time += TICK_TIME

	def nudge(self, x, y):
		# go to position (x, y) within one tick. Warn if this isn't possible
		m0_step, m1_step = self.get_step_values(x, y)
		self.motor0.target = int(m0_step)
		self.motor0.deadline = self.time + TICK_TIME

		self.motor1.target = int(m1_step)
		self.motor1.deadline = self.time + TICK_TIME

		self.tick()
