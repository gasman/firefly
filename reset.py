from config import TICK_TIME
from motor import MotorRegulator
import time
import sys

motor_number, direction = sys.argv[1:]
motor_number = int(motor_number)
direction = int(direction)

motor = MotorRegulator(motor_number, 0)
if direction > 0:
	motor.target = 10000000
else:
	motor.target = -10000000

t = 0
while True:
	motor.tick(t)
	t += TICK_TIME
	time.sleep(TICK_TIME)
