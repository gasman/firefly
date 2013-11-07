import math
from geometry import Arena
from config import TICK_TIME

# how long we should take to trace one side
SIDE_TIME = 10.0

# top left corner of square, in metres from top left of arena
ORIGIN = (0.1, 0.1)
SIDE_LENGTH = 0.2

t = 0.0

x0, y0 = ORIGIN

arena = Arena()
arena.goto(x0, y0)

while True:
	phase = (t / SIDE_TIME) % 4.0
	side_distance = (phase % 1.0) * SIDE_LENGTH

	if phase < 1.0:
		x, y = (x0 + side_distance, y0)
	elif phase < 2.0:
		x, y = (x0 + SIDE_LENGTH, y0 + side_distance)
	elif phase < 3.0:
		x, y = (x0 + SIDE_LENGTH - side_distance, y0 + SIDE_LENGTH)
	else:
		x, y = (x0, y0 + SIDE_LENGTH - side_distance)

	arena.nudge(x, y)
	t += TICK_TIME
