import pseudo.standard_lib as standard_lib
tokens = {}
from pseudo.context import ExecutionContext


def i(indents):
	return '  '*indents

def parse_next(list):
	tok = list[0]
	if not tok in tokens:
		print("Unrecognized next token: {}".format(tok))
		print(tokens.keys())
	tk = tokens[tok]()
	tk.parse(list)
	return tk

def ld(token, cls):
	tokens[token] = cls


class Declaration:
	def parse(self, list):
		self.typ = list[1].type
		self.vn = list[1].name
		self.list = bool(list[1].list)
	def pretty_print(self, indent):
		stri = "{} {}".format(self.typ, self.vn)
		if self.list:
			stri = "list "+stri

		return i(indent)+stri

	def execute(self, context):
		context.initialize_variable(self.vn, self)
		if context.verbose:
			context.logger.verbose_log("Declared {}".format(self.pretty_print(0)), context, names=True)



ld("DECLARE", Declaration)

class HaltStackFrame(Exception):
	def __init__(self, retval):
		self.retval = retval
	def get_return(self):
		return self.retval

class Algorithm:
	
	def parse(self, list):
		#import pdb; pdb.set_trace()
		self.name = list[2]
		self.raw_decls = list.decls
		self.declarations = [parse_next(l) for l in self.raw_decls[0]] if self.raw_decls else []

		self.sub_statements = [parse_next(l) for l in list.blocks ]

	def pretty_print(self, indent):
		title = i(indent)+"algorithm {} takes {}\n".format(self.name, " ".join([ p.pretty_print(0) for p in self.declarations ] ))
		statements = "\n".join([(s.pretty_print(indent+1)) for s in self.sub_statements ] )
		return title + statements

	def execute(self, context):
		context.functions.define_function(self.name, self)

	def run_statements(self, context):
		retval = None
		try:
			for d in self.sub_statements:
				d.execute(context)
		except HaltStackFrame as h:
			retval = h.get_return()

		context.logger.verbose_log("Returning {}".format(retval), context)
		return retval

	def run_as_main(self, context):
		
		child_ctx = ExecutionContext(context, self)

		self.execute(child_ctx)

		for d in self.declarations:
			child_ctx.initialize_variable(d.vn, self)
			vname = d.vn
			result = eval(input("Set {}? ".format(vname)))
			child_ctx.set_variable(vname, result, self)

		ret = self.run_statements(child_ctx)

		print("Returned {}".format(ret))
		return child_ctx


	def apply_function(self, arguments):
		bareCtx = ExecutionContext(None, self)
		self.execute(bareCtx)
		for i, d in enumerate(self.declarations):
			bareCtx.initialize_variable(d.vn, self)
			val = arguments[i]
			bareCtx.set_variable(d.vn, val, self)
	
		return self.run_statements(bareCtx)



ld("FUNC", Algorithm)


class FunctionCall:
	def parse(self, lst):
		self.fname =  lst[1].fname
		self.fargs = [ parse_next(l) for l in lst[1][1] ]
		

	def pretty_print(self, indent=0):
		return i(indent) + "{}({})".format(self.fname, ", ".join([p.pretty_print() for p in self.fargs]))

	def evaluate(self, context, stmnt):
		arguments = [f.evaluate(context, stmnt) for f in self.fargs]
		if not self.fname in standard_lib.standard_library:
			context.logger.verbose_log("Calling: {}({})".format(self.fname, ", ".join([str(a) for a in arguments])) , context)
		func = context.functions.get_function(self.fname)
		rval = func.apply_function(arguments )
		return rval

	def execute(self, context):
		val = self.evaluate(context, self)

		

ld("CALLFUNC", FunctionCall)

class ListAccess:
	def parse(self, list):
		self.lname = list[1].list_name
		self.index_expr = parse_next(list[1].index)
		
	def pretty_print(self, indent=0):
		return "{}[{}]".format(self.lname, self.index_expr.pretty_print())

	def evaluate(self, context, stmnt):
		return context.get_variable(self.lname, stmnt, index = self.index_expr.evaluate(context, stmnt))

ld("LIST", ListAccess)


class VariableAccess:
	def parse(self, list):
		self.varname = list[1]
	def pretty_print(self, indent=0):
		return self.varname
	def evaluate(self, context, containing_statement):
		return context.get_variable(self.varname, containing_statement)

ld("VAR", VariableAccess)

class Literal:
	def parse(self, list):
		self.literal = list[1]
	def pretty_print(self, indent=0):
		return str(self.literal)
	def evaluate(self, context, containing_statement):
		return eval(self.literal) if type(self.literal) == type("") else self.literal

ld("LIT", Literal)



class OpString:
		def __init__(self, st):
			self.st = st.lower()
		def evaluate(self, context, containing_statement):
			return str(self.st)
		def pretty_print(self):
			return str(self.st)

class Expression:

	def parse_set(self, lst):
		self.components = []
		l2 = lst[::-1]
		while l2:
			p = l2.pop()
			if not type(p[0]) == type(""):
				ep = Expression()
				ep.parse([None, [p]])
				self.components += [ep]
			else:
				self.components += [parse_next(p)]
			
			if l2:
				self.components += [OpString(l2.pop())]

	def parse(self, lst):
		expr = lst[1][0]

		if not len(expr) == 2:
			self.is_basic = False
			self.parse_set(expr)
		else:
			self.is_basic = True
			self.direct_eval = parse_next(expr)
	
	def pretty_print(self):
		if self.is_basic:
			return "{}".format(self.direct_eval.pretty_print())
		else:
			return "("+ " ".join([str(p.pretty_print()) for p in self.components]) +")"

	def evaluate(self, context, containing_statement):
		if self.is_basic:
			return self.direct_eval.evaluate(context, self)
		else:
			eval_string = " ".join([str(p.evaluate(context, containing_statement)) for p in self.components])
			return eval(eval_string)
			


ld("EXPR", Expression)


class Display:
	def parse(self, list):
		self.to_parse = parse_next(list[2:])

	def pretty_print(self, indent):
		return i(indent)+"display {}".format(self.to_parse.pretty_print())

	def execute(self, context):
		evald = self.to_parse.evaluate(context, self)
		print(">> {}".format(evald))
ld("DISPLAY", Display)
	


class Assignment:
	def parse(self, lst):
		self.variable = lst.identifier
		self.expr = parse_next(lst.value) 
		

	def pretty_print(self, indent):
		return i(indent)+"{} := {}".format(self.variable, self.expr.pretty_print())

	def execute(self, context):
		# import pdb; pdb.set_verbose()
		if context.verbose:
			context.logger.verbose_log("{} := {} ({})".format(self.variable, self.expr.evaluate(context, self), self.expr.pretty_print()), context)

		context.set_variable(self.variable, self.expr.evaluate(context, self), self)


ld("ASSIGN", Assignment)


class Input:
	def parse(self, list):
		self.var = list[1]
	
	def pretty_print(self, indent):
		return i(indent)+"get {}".format(self.var)

	def execute(self, context):
		vname = self.var
		result = eval(input("Set {}? ".format(vname)))
		context.set_variable(vname, result, self)

ld("INPUT", Input)

class While:
	def parse(self, list):
		rawblocks = list[1][1]
		condition = list[1][0][0]
	
		self.expr = parse_next(condition)
		self.blocks = [parse_next(b) for b in rawblocks]

	

	def pretty_print(self, indent):
		cline = i(indent)+"while {}\n".format(self.expr.pretty_print())
		cline = cline + "\n".join([b.pretty_print(indent + 1) for b in self.blocks])
		cline = cline + "\n"+i(indent)+"endwhile"
		return cline
		

	def execute(self, context):
		def should_go():
			should = self.expr.evaluate(context, self)
			if context.verbose:
				context.logger.verbose_log("Continuing {}".format(self.expr.pretty_print() ) , context)
			return should

		while( should_go() ):
			#if context.verbose:
				#print(i(context.depth())+"~~~~~~~")
			exc = context.child(self)
			for b in self.blocks:
				b.execute(exc)

ld("WHILE", While)

class IfBlock:
	def parse(self, list):
		condition = list[1][0]
		rawblocks = list[1].block
		if list[1].elseblock:
			elseblock = list[1].elseblock[0]
			self.elseblocks = [parse_next(b) for b in elseblock]
		else:
			self.elseblocks = []


		self.expr = parse_next(condition)
		self.blocks = [parse_next(b) for b in rawblocks]

	def pretty_print(self, indent):
		oline = i(indent)+ "if {}\n".format(self.expr.pretty_print())
		oline = oline + "\n".join([b.pretty_print(indent+1) for b in self.blocks])
		oline += "\n" + i(indent)+ "endif"
		return oline

	def execute(self, context):
		if context.verbose:
			context.logger.verbose_log("{} is {}".format(self.expr.pretty_print(), self.expr.evaluate(context, self)), context)

		if(self.expr.evaluate(context, self)):
			exc = context.child(self)
			for b in self.blocks:
				b.execute(exc)
		else:
			exc = context.child(self)
			for b in self.elseblocks:
				b.execute(exc)

ld("IF", IfBlock)

class ListAssign:
	
	def parse(self, list):
		#import pdb; pdb.set_trace()
		self.index_epr = parse_next(list[2].index)
		self.name = list[2].list_name
		self.res = parse_next(list[4:])
	
	def pretty_print(self, indent):
		return i(indent)+"{}[{}] := {}".format(self.name, self.index_epr.pretty_print(), self.res.pretty_print())

	def execute(self, context):
		if(context.verbose):
			context.logger.verbose_log("{}[{}] := {}".format(self.name, self.index_epr.evaluate(context, self), self.res.evaluate(context, self) ), context)
		
		context.set_variable(self.name, self.res.evaluate(context, self), self, index=self.index_epr.evaluate(context, self))
		

ld("LASSIGN", ListAssign)

class Halt:
	def parse(self, list):
		pass
	def pretty_print(self, indent):
		return i(indent)+"halt"
	def execute(self, context):
		print("Halting.")
		raise HaltStackFrame(None)
ld("HALT", Halt)

class Return:
	def parse(self, list):
		self.epr = parse_next(list[1])

	def pretty_print(self, indent):
		return i(indent)+"return {}".format(self.epr.pretty_print())

	def execute(self, context):
		retval = self.epr.evaluate(context, self)
		raise HaltStackFrame(retval)
		#print("Result: {}".format(self.epr.evaluate(context, self)))
ld("RETURN", Return)



