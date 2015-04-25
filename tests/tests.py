
from pseudo2 import *

#################### TESTS

t1 = "x := 31 + 42.2 + (x / 2) + 3"
#print(t1)
#print(line.parseString(t1))

t2 = "foo[ bar[1]] :=3"
t3 = "foo[bar[1] - 3] := 1 + 2 + 3 * bar[2]"

print(">>"+t2)
print(listAssignment.parseString("foo[ bar[1]] := 3") )
print(">>"+t3)
print(listAssignment.parseString("foo[bar[1] - 3] := 1 + 2 + 3 * bar[2]"))

duowhile = """
while x > 2
  x := x + 1
  foo[x] := x * x
  while x >= 3
    display x
  endwhile
endwhile
"""
print(duowhile)
print(line.parseString(duowhile))
	

if1 = """while x > 3
	x := x * foo[x+1]
	if x > 4
		while x < 2
			y := x + y
			foo[y] := foo[ 2 - bar[ y + 1] ]
			if y < 2
				display y
			endif
		endwhile
	endif
endwhile
"""

print(if1)
print(line.parseString(if1))

decls = """
if x > 1
	list string foo
	number bar
	list logical baz
endif
"""

#print(decls)
#print(line.parseString(decls))

rs = line.parseString(if1)


t3 = """
algorithm Factorial takes number N
	number Accumulate
	Accumulate := 1
	list number B
	get B
	B[N + 1] := 2
	display B
	if N < 3
		display N
	endif
	while N > 1
		Accumulate := Accumulate * N
		N := N - 1
	endwhile
	while N < 2
		Accumulate := Accumulate + 1
		N := N + 1
	endwhile
	display Accumulate
"""
print(t3)
#print(function.parseString(t3))

parsed = function.parseString(t3)
ast = parse_next(parsed)
print(ast.pretty_print(0))
ast.run_as_main(None)

bubblesort = """
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

	display InList
"""
