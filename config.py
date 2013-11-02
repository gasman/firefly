# Shortest time interval (in seconds) between steps that the motor can handle
MIN_STEP_TIME = 0.002

# Number of steps per rotation that the motor provides
CYCLES_PER_ROTATION = 512.0  # we repeat the cycle (1, 2, 3, 4) 512 times to perform one rotation
STEPS_PER_ROTATION = CYCLES_PER_ROTATION * 4

# Distance between motors, in metres
MOTOR_SPACING = 0.44

# Radius of each spool in metres
SPOOL_RADIUS = 0.025

# Interval (in seconds) between successive position calculations
TICK_TIME = 0.0005
