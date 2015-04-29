import unittest
from pseudo import main as pseudo

# For these tests, write outputs to n.
def wrap_code(in_text):
	pre = """algorithm testAssignment
		number n"""
	post = """
		return n"""
	return pre + in_text + post

class TestAssignmentMethods(unittest.TestCase):	
	def test_assignment(self):
		alg = wrap_code("""
		n := 5
		""")
		self.assertEqual(pseudo.execute_algorithm(alg), 5);
	
	def test_while(self):
		alg = wrap_code("""
			n := 0
			number x
			x := 0
			while(x < 10)
				n := n + x 
				x := x + 1
			endwhile
			""")
		self.assertEqual(pseudo.execute_algorithm(alg), 45)

	def test_bubble_sort(self):
		bubble = """
				algorithm BubbleSort takes list number InList number Size
					number Index
					logical Swapped
					Swapped := True
					while Swapped
						Swapped := False
						Index := Size
						while Index > 1
							if InList[Index] < InList[Index - 1]
								number Temp
								Temp := InList[Index]
								InList[Index] := InList[Index - 1]
								InList[Index - 1] := Temp
								Swapped := True
							endif
							Index := Index - 1
						endwhile
					endwhile

					return InList"""
		self.assertEqual( pseudo.execute_algorithm(bubble, [2, -1, 5, 3, 10, 7, 4], 7), [-1, 2, 3, 4, 5, 7, 10])

	def test_list_indexing(self):
		alg = wrap_code("""
			list number nx
			nx := [0,1,2,3,4,5]
			n := nx[1] 
			""")
		self.assertEqual(pseudo.execute_algorithm(alg), 0)

	def test_nested_indexing(self):
		alg = wrap_code("""
			list number nx
			nx := [0,1,2,3,4,5]
			n := nx[ nx[ 4 ] - 1 ]
			""")
		self.assertEqual(pseudo.execute_algorithm(alg), 1)

	def test_recursion(self):
		fibb = """
			algorithm fib takes number N
				if (N == 1) OR (N == 0)
					return 1
				endif
				return fib(N-2) + fib(N-1)
			"""
		self.assertEqual(pseudo.execute_algorithm(fibb, 15), 987)

	def test_function_calls(self):
		alg = wrap_code("""
			n := floor(5.99)
			""")
		self.assertEqual(pseudo.execute_algorithm(alg), 5)	



	def test_current_directory_load(self):
		import os
		alg = """
		algorithm factorial takes number N
		if N == 1
			return 1	
		endif
		return N * factorial(N - 1)
		"""
		fl = open('factorial.pdo', 'w')
		fl.write(alg)
		fl.flush()
		fl.close()
		runner = wrap_code("""
			n := factorial(5)
			""")
		self.assertEqual(pseudo.execute_algorithm(runner), 120 )
		os.remove('factorial.pdo')






		
if __name__ == '__main__':
	unittest.main()
