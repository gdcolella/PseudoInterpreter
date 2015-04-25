from pyparsing import *


ParserElement.enablePackrat()

def makePush(cl):
	def push_this(strg, loc, toks):
		if type(toks[0]) == type([]):
			toks[0].insert(0, cl)
		else:
			toks.insert(0, cl)
		return toks
	return push_this


# ###############################################################
ParserElement.setDefaultWhitespaceChars(" \t")

def i(indents):
	return '  '*indents

EOL = Suppress(ZeroOrMore(LineEnd()))

integer = Combine(Optional("-")+Word(nums)).setParseAction(lambda s, l, t: [ int(t[0]) ] ).setName("Integer")
decimal = Combine(Word(nums) + "." + Word(nums)).setName("Decimal")

num = decimal ^ integer


arithOp = oneOf("+ - * / %").setName("MathOp")
condOp =  "==" | ( Combine(oneOf("< >") + Optional("=") ) )  | "!="
boolOp = Keyword("AND") | Keyword("OR")

anyOp = arithOp ^ condOp.setName("Conditional")
anyOp.setDebug()

identifier = Word(alphas+"_", alphanums+"_").setName("identifier")
expression = Forward().setName("expression")
listAccess = Forward().setName("listAccess")



strLiteral = dblQuotedString
baseLiteral = (strLiteral | Keyword("True") | Keyword("False") | num ) 
listLiteral = nestedExpr(opener='[', closer=']', content =baseLiteral+Suppress(Optional(",")), ignoreExpr=",")
literal =  (baseLiteral | listLiteral).setResultsName("literal")
literal.setParseAction(makePush("LIT"))
literal.setName("literal")#.setDebug()

variableIdent = identifier.setResultsName("variable")
variableIdent.setParseAction(makePush("VAR"))

functionCall = Forward()

directEvaluable = (literal ^ listAccess ^ variableIdent ^ functionCall)

#expression <<    Group( directEvaluable + anyOp.setResultsName("operator")  + Group(expression).setResultsName("right_hand") )  ^  Group(directEvaluable)   ^ ( Suppress("(") + expression + Suppress(")"))

expop = Literal('^')
signop = oneOf('+ -')
multop = oneOf('* / %')
plusop = oneOf('+ -')

expression << Group(operatorPrecedence(Group(directEvaluable),
	[ 	  
	  (boolOp, 2, opAssoc.LEFT),
	  (multop, 2, opAssoc.LEFT),
	  (plusop, 2, opAssoc.LEFT),
	  (condOp, 2, opAssoc.LEFT)

	])  )
expression.addParseAction(makePush("EXPR")) 
#expression.setDebug()

listAccess << ( Group(identifier.setResultsName("list_name") + Suppress("[") + expression.setResultsName("index") + Suppress("]") ) )
listAccess.addParseAction(makePush("LIST"))

conditional = Group(expression)#.setDebug()


# Statements start below

functionCall << Group(identifier.setResultsName("fname") + Suppress("(") + Group(ZeroOrMore( Group(expression) + Optional(Suppress(",")) )  + Suppress(")")) )
functionCall.addParseAction(makePush("CALLFUNC"))
#functionCall.setDebug()

assignment = identifier.setResultsName("identifier") + Suppress(":=") + expression.setResultsName("value")
assignment.addParseAction(makePush("ASSIGN"))
listAssignment = listAccess + ":=" + expression
listAssignment.addParseAction(makePush("LASSIGN"))

displayStatement = Keyword("display") + expression
displayStatement.addParseAction(makePush("DISPLAY"))

inputStatement = Suppress(Keyword("get"))+ (listAccess ^ identifier)
inputStatement.addParseAction(makePush("INPUT"))

declaration = Group(Optional(Keyword("list")).setResultsName("list") + ( Keyword("number") | Keyword("string") | Keyword("logical") ).setResultsName("type") + identifier.setResultsName("name") )
declaration.addParseAction(makePush("DECLARE"))

rturn = Group(Keyword("return").suppress() + expression)
rturn.addParseAction(makePush("RETURN"))

line = Forward()
whileLoop = Group(Keyword("while").suppress() + Group(conditional).setResultsName("condition") + Group( OneOrMore(line) ).setResultsName("block") + Keyword("endwhile").suppress() ) 
whileLoop.addParseAction(makePush("WHILE"))#.setDebug()

ifBlock   = Group(Keyword("if").suppress() + conditional.setResultsName("condition") + Group(OneOrMore(line) ).setResultsName("block") + Optional(Keyword("else").suppress()+ Group(OneOrMore(line)) ).setResultsName("elseblock") + Keyword("endif").suppress() )
ifBlock.addParseAction(makePush("IF"))

halt = Group(Keyword("halt").suppress())
halt.addParseAction(makePush("HALT"))

function = Forward()

line <<  EOL + Group ( (declaration | assignment | listAssignment | displayStatement | inputStatement |  whileLoop | ifBlock | halt | rturn | functionCall | function) ) + EOL

line.ignore("#" + SkipTo(LineEnd()))
line.setName("line")

func_decl = Keyword("algorithm") + identifier + Optional(Keyword("takes").suppress() + Group(OneOrMore(Group(declaration) + Optional(Suppress(","))))).setResultsName("decls") + EOL
function << EOL + func_decl + Group(OneOrMore(line)).setResultsName("blocks") + Suppress(Optional(Keyword("endalgorithm")))
function.addParseAction(makePush("FUNC"))
