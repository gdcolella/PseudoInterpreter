import copy
import standard_lib
from collections import OrderedDict

verbose_DEFAULT = False
TRACE = False


logger = None


def i(indents):
	return '  '*indents

def define_logger(in_log):
	global logger
	logger = in_log


class FunctionLibrary:
	def __init__(self):
		self.functions = copy.copy(standard_lib.standard_library) # import the standard library
	
	def get_function(self, func_identifier):
		if func_identifier in self.functions:
			return self.functions[func_identifier]
		else:
			fnc = load_from_file(func_identifier)
			if fnc:
				define_function(func_identifier, fnc)
				return fnc
			else:
				show_error("No such function {} in functions {}".format(func_identifier, self.functions.keys()))
	def define_function(self, func_identifier, func_object):
		self.functions[func_identifier] = func_object

functions = FunctionLibrary()

def load_from_file(fname):
	fle = fname+".pdo"
	if not path.exists(fle):
		return None
	fl = open(fle, 'r')
	parsed = function.parseFile(fle)
	func = parse_next(parsed)
	return func



class ExecutionContext:
	def start_verbose():
		self.verbose = True

	def child(self, stmnt):
		return ExecutionContext(self, stmnt)

	def empty(self, stmnt):
		return ExecutionContext(None, stmnt)

	def __init__(self, super_context, containing_statement):
		self.variables = OrderedDict()
		self.super_context = super_context
		self.containing_statement = containing_statement
		self.verbose = verbose_DEFAULT
		self.trace = TRACE
		self.functions = functions
		self.logger = logger

	def depth(self):
		if not self.super_context:
			return 1
		else:
			return 1 + self.super_context.depth()

	def dump_vars(self, names=False):
		myvars = "\t".join(["{}: {}".format(k,v) for k,v in self.variables.items() ])
		if self.super_context:
			return self.super_context.dump_vars() + " "+myvars
		else:
			return myvars


	def set_variable(self, var_name, value, statement, index = None, bottom_context = None):
		
		btm = bottom_context if bottom_context else self

		if var_name in self.variables:
			if index:
				self.variables[var_name][index - 1] = value
			else:
				self.variables[var_name] = value
		else:
			if self.super_context:
				self.super_context.set_variable(var_name, value, statement, index = index, bottom_context=btm)
			else:
				self.logger.show_error("{} was not found in this execution context.\n\nStatement:\n{}\n\nBlock:\n{}".format(var_name, statement.pretty_print(0), btm.get_stack_trace(statement)))

	def get_stack_trace(self, statement = None):
		print(type(self.containing_statement))
		if statement:
			trace = self.containing_statement.pretty_print(0)+"\t\n"+statement.pretty_print(0)
		else:
			trace = self.containing_statement.pretty_print(0)

		if self.super_context:
			return self.super_context.get_stack_trace() + "\t\n" + trace
		else:
			return trace

	def initialize_variable(self, var_name, statement):
		if var_name in self.variables:
			show_error("{} was already defined in this context.\n{}".format(var_name, self.get_stack_trace(statement)))
		else:
			self.variables[var_name] = None


	def get_variable(self, var_name, statement, index = None, bottom_context = None):
		btm = bottom_context if bottom_context else self

		if var_name in self.variables:
			if self.variables[var_name] == None:
				self.logger.show_error("{} was accessed before initialization.\n{}".format(var_name, btm.get_stack_trace(statement)))
			else:
				if index:
					return self.variables[var_name][index - 1]
				else:
					return self.variables[var_name]
		else:
			if self.super_context:
				return self.super_context.get_variable(var_name, statement, index=index, bottom_context = btm)
			else:
				self.logger.show_error("{} was not found in this execution context.\nStatement:\n{}\nBlock:\n{}".format(var_name, statement.pretty_print(0), btm.get_stack_trace(statement)))
