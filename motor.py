from config import MIN_STEP_TIME
try:
	import RPi.GPIO as GPIO
	has_gpio = True
except ImportError:
	has_gpio = False

class MotorRegulator(object):
	def __init__(self, motor_number, position=0):
		self.motor = Motor(motor_number)
		self.position = int(position)
		self.last_move_time = None
		self.deadline = None
		self.target = self.position

	def tick(self, t):
		if self.last_move_time is not None and t - self.last_move_time < MIN_STEP_TIME:
			return

		if self.target > self.position:
			self.position += 1
			self.motor.set_position(self.position)
			self.last_move_time = t
			remaining_steps = self.target - self.position
			eta = t + remaining_steps * MIN_STEP_TIME
			if self.deadline is not None and eta > self.deadline:
				print "Warning: going to miss deadline to go from %d to %d (deadline = %f, eta %f)" % (self.position, self.target, self.deadline, eta)
		elif self.target < self.position:
			self.position -= 1
			self.motor.set_position(self.position)
			self.last_move_time = t
			remaining_steps = self.position - self.target
			eta = t + remaining_steps * MIN_STEP_TIME
			if self.deadline is not None and eta > self.deadline:
				print "Warning: going to miss deadline to go from %d to %d (deadline = %f, eta %f)" % (self.position, self.target, self.deadline, eta)

	def done(self):
		return self.target == self.position

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
