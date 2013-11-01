from config import MIN_STEP_TIME
from motor import MotorRegulator
import time
import sys

motor_number, direction = sys.argv[1:]
motor_number = int(motor_number)
direction = int(direction)

pos = 0
motor = MotorRegulator(motor_number, pos)
t = 0
while True:
	motor.set_position(pos, t)
	pos += direction
	t += MIN_STEP_TIME
	time.sleep(MIN_STEP_TIME)
