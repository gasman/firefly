import time
import math
from geometry import Arena

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
