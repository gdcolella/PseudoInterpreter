
import pseudo.standard_lib as standard_lib
from pseudo.ast import *
from pseudo.ast import parse_next
import copy
from os import path
from collections import OrderedDict
import pseudo.parser as parser
import pseudo.context as exec_context
import readline




class PseudoException(Exception):
	def __init__(self, error_string):
		super(Exception, self).__init__(self, error_string)


class Logger:
	def __init__(self):
		self.LOG_COLUMN = 75
	
	def verbose_log(self, string, context, names=False):
		if not context.verbose:
			return
		raw = i(context.depth())+string
		padded = raw + " "*(self.LOG_COLUMN - len(raw))

		if exec_context.TRACE:
			trace = "|\t"+context.dump_vars(names=names)
			padded = padded + trace

		print(padded)

	def show_error(self, error_string):
		raise PseudoException(error_string)

exec_context.define_logger(Logger())


class ReplRoot:
	def pretty_print(self, indent):
		return "Repl Root"

def repl_basic():
	rep_statement = ReplRoot()
	exc = exec_context.ExecutionContext(None, rep_statement)
	repl(exc)

def repl(incontext):
	ln = ""
	while ln != quit:
		ln = input("$> ")

		if ln == "VARS":
			print(incontext.dump_vars())
		else:
			try:
				this_ast = parse_next(parser.line.parseString(ln)[0])
				this_ast.execute(incontext)
			except PseudoException as pe:
				print("Error raised: {}".format(pe.args[1]))

			except Exception as e:
				print("{}\nError occured.. use exit() to quit".format(e))
			



