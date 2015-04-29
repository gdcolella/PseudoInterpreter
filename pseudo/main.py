#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

from collections import OrderedDict

import pseudo.parser as pdo_parser
import pseudo.ast as ast
import pseudo.interpreter as interpreter
import pseudo.context as context





################## INTERPRETER

def execute_algorithm(input_string, *arguments):
	tokenized = pdo_parser.function.parseString(input_string)
	code = ast.parse_next(tokenized)
	return code.apply_function(arguments)

#print(bubblesort)
if __name__ == "__main__":
	main()

def main():
	import sys
	from optparse import OptionParser

	parser = OptionParser("usage: %prog [options] filename")
	parser.add_option("-t", "--trace",    action="store_true", dest="trace",    default=False)
	parser.add_option("-v", "--verbose",  action="store_true", dest="verbose",  default=False)
	parser.add_option("-i", "--interact", action="store_true", dest="interact", default=False)
	options, args = parser.parse_args()

	context.verbose_DEFAULT = options.verbose
	context.TRACE = options.trace

	if len(args) < 1:
		interpreter.repl_basic()
	else:
		parsed = pdo_parser.function.parseFile(args[0])
		func = ast.parse_next(parsed)
		inctx = func.run_as_main(None)
		if options.interact:
			interpreter.repl(inctx)








