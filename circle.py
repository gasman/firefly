import math
from geometry import Arena
from config import TICK_TIME

# how long we should take to trace a full circle
REVOLUTION_TIME = 60.0

# centre coordinates of circle, in metres from top left
CENTRE = (0.22, 0.1)
RADIUS = 0.1

t = 0.0

cx, cy = CENTRE

x = cx + RADIUS * math.sin(0)
y = cy - RADIUS * math.cos(0)

arena = Arena()
arena.goto(x, y)

while True:
	angle = t * 2 * math.pi / REVOLUTION_TIME
	x = cx + RADIUS * math.sin(angle)
	y = cy - RADIUS * math.cos(angle)

	arena.nudge(x, y)
	t += TICK_TIME
