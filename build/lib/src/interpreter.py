
import standard_lib
from ast import *
from ast import parse_next
import copy
from os import path
from collections import OrderedDict
import parser
import context as exec_context
import readline



class PseudoException(Exception):
	def __init__(self, error_string):
		super(Exception, self).__init__(self, error_string)


class Logger:
	LOG_COLUMN = 75
	def verbose_log(self, string, context, names=False):
		if not context.verbose:
			return
		raw = i(context.depth())+string
		padded = raw + " "*(LOG_COLUMN - len(raw))

		if TRACE:
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
			



