import unittest
from .. import pseudo

# For these tests, write outputs to n.
def wrap_code(in_text):
	pre = "algorithm testAssignment\nnumber n"
	post = "\nreturn n"
	return pre + in_text + post

class TestAssignmentMethods(unittest.TestCase):	
	def test_assignment():
		alg = wrap_code("""
		n := 5
		""")

		self.assertEqual(pseudo.execute_algorithm(alg), 5);
	
	def test_while():
		alg = wrap_code("""
			number x
			x := 0
			while(x < 10)
				n := n + x 
			endwhile
			""")
		self.assertEqual(pseudo.execute_algorithm(alg), 10)

if __name__ == '__main__':
	unittest.main()
