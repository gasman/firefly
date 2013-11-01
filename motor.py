from config import MIN_STEP_TIME
try:
	import RPi.GPIO as GPIO
	has_gpio = True
except ImportError:
	has_gpio = False

class MotorRegulator(object):
	def __init__(self, motor_number, position=0):
		self.motor = Motor(motor_number)
		self._position = int(position)
		self.last_move_time = None

	def set_position(self, new_pos, time):
		new_pos_int = int(new_pos)
		if new_pos_int == self._position:
			pass
		elif (new_pos_int == self._position - 1) or (new_pos_int == self._position + 1):

			# check that it's been more than MIN_STEP_TIME seconds since the last move
			if self.last_move_time is not None:
				time_diff = time - self.last_move_time
				if time_diff < (MIN_STEP_TIME - 0.000001):
					raise Exception("Moved too fast! Steps were %fs apart, but minimum interval is %fs" % (time_diff, MIN_STEP_TIME))

			self.last_move_time = time

			self.motor.set_position(new_pos_int)
			self._position = new_pos_int

		else:
			raise Exception("Moved too fast! Tried to move from %d to %d in one step" % (self._position, new_pos_int))

	def stop(self):
		self.motor.stop()

if has_gpio:
	class Motor(object):
		sequence = [
			[1, 1, 0, 0],
			[0, 1, 1, 0],
			[0, 0, 1, 1],
			[1, 0, 0, 1],
		]

		def __init__(self, motor_number, position=0):
			if motor_number == 0:
				self.pins = (17, 18, 27, 22)
			elif motor_number == 1:
				self.pins = (23, 24, 25, 4)
			else:
				raise Exception("Invalid motor number %d" % motor_number)

			# set pin directions
			GPIO.setmode(GPIO.BCM)
			for pin in self.pins:
				GPIO.setup(pin, GPIO.OUT)

		def set_position(self, pos):
			seq = Motor.sequence[pos % 4]
			GPIO.output(self.pins[0], seq[0])
			GPIO.output(self.pins[1], seq[1])
			GPIO.output(self.pins[2], seq[2])
			GPIO.output(self.pins[3], seq[3])

		def stop(self):
			for pin in self.pins:
				GPIO.output(pin, 0)

else:
	# fake Motor class for testing
	class Motor(object):
		def __init__(self, motor_number, position=0):
			self.motor_number = motor_number

		def set_position(self, pos):
			print "motor %d => %d" % (self.motor_number, pos)

		def stop(self):
			pass
