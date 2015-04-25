import math
standard_library = {}

class lib_function:
	def __init__(self, name=None):
		self.name = name

	def __call__(self, in_func):
		nm = in_func.__name__ if not self.name else self.name
		class Func:
			def apply_function(self, args):
				return in_func(*args)
		global standard_library
		standard_library[nm] = Func()
		return in_func



@lib_function()
def floor(number):
	return math.floor(number)

@lib_function(name="abs")
def absolute(num):
	return abs(num) 

@lib_function(name="exit")
def quit():
	print("Quitting.")
	exit()

@lib_function(name="mod")
def modulus(num, divisor):
	return num % divisor


