#!/usr/bin/python

class Expr:
	pass

class Symbol(Expr):
	_char: str;

	def __init__(self, c: str):
		self._char = c

	def __str__(self):
		return self._char

class Star(Expr):
	_expr: Expr

	def __init__(self, expr: Expr):
		self._expr = expr

	def __str__(self):
		a = str(self._expr)
		return a + "*"

class Concat(Expr):
	_expr1: Expr
	_expr2: Expr

	def __init__(self, expr1: Expr, expr2: Expr):
		self._expr1 = expr1
		self._expr2 = expr2

	def __str__(self):
		a = str(self._expr1)
		b = str(self._expr2)
		return "( " + a + " . " + b + " )" 

class Union(Expr):
	_expr1: Expr
	_expr2: Expr

	def __init__(self, expr1: Expr, expr2: Expr):
		self._expr1 = expr1
		self._expr2 = expr2

	def __str__(self):
		a = str(self._expr1)
		b = str(self._expr2)
		return "( " + a + " U " + b + " )"

class Plus(Expr):
	_expr: Expr

	def __init__(self, expr: Expr):
		self.expr = expr

ExprStack = []

def unify_stack():
	if len(ExprStack) == 1:
		return

	top = ExprStack.pop()
	op = ExprStack.pop()

	if isinstance(op, Concat):
		if op._expr1 is None:
			op._expr1 = top
		else:
			op._expr2 = top
	if isinstance(op, Union):
		if op._expr1 is None:
			op._expr1 = top
		else:
			op._expr2 = top
	if isinstance(op, Star):
		if op._expr is None:
			op._expr = top
	if isinstance(op, Plus):
		op = Concat(top, Star(top))
	ExprStack.append(op)


def is_complete(node):
	if len(ExprStack) == 0:
		return False
	if isinstance(node, Symbol):
		return True
	if isinstance(node, Concat):
		if node._expr1 is not None and node._expr2 is not None:
			return True
	if isinstance(node, Union):
		if node._expr1 is not None and node._expr2 is not None:
			return True
	if isinstance(node, Star):
		if node._expr is not None:
			return True
	return False

def create_stack(exprs):
	tokens = exprs.split()
	for token in tokens:
		obj = None
		if token == "CONCAT":
			obj = Concat(None, None)
		if token == "STAR":
			obj = Star(None)
		if token == "UNION":
			obj = Union(None, None)
		if token == "PLUS":
			obj = Plus(None)
		if obj is None:
			obj = Symbol(token)
		
		ExprStack.append(obj)

		top = ExprStack.pop()

		while is_complete(top):
#			print("top: " + str(top))
#			print("v-before unif-v")
#			for i in ExprStack:
#				print(i)
			ExprStack.append(top)
			unify_stack()
#			print("v-after unif -v")
#			for i in ExprStack:
#				print(i)
#			print()
			top = ExprStack.pop()

		ExprStack.append(top)

letters = "abcdefghijklmnopqrstuvwxyz"
def a_z(letter):
	if letter is "y":
		return Union("y", "z")
	return Union(letter, a_z(letters[letters.find(letter) + 1]))

numbers = "0123456789"
def zero_9(numr):
	if numr is "8":
		return Union("8", "9")
	return Union(numr, zero_9(numbers[numbers.find(numr) + 1]))

def make_plus(expr):
	return Concat(expr, Star(expr))

def parantezare(expr):
	popen = 0
	idx = 0
	for c in expr:
		if c == "(":
			popen += 1
		if c == ")":
			popen -= 1
		idx += 1
		if popen == 0:
			break
	return expr[1:(idx-1)]

def is_full(node):
	if isinstance(node, Symbol):
		return True
	if isinstance(node, Concat):
		if node._expr1 is not None and node._expr2 is not None:
			return True
	if isinstance(node, Union):
		if node._expr1 is not None and node._expr2 is not None:
			return True
	if isinstance(node, Star):
		if node._expr is not None:
			return True
	return False

# -------#
# ETAPA 3#
# -------#

def unify_regex_stack(RegexStr):
	while len(RegexStr) > 1:
		#print("mai mult de 1 element")
		top = RegexStr.pop()
		#print("top " + str(top))
		top2 = RegexStr.pop()
		#print("top2 " + str(top2))
		if is_full(top) and is_full(top2):
			RegexStr.append(Concat(top2, top))
		elif isinstance(top, Union) and not is_full(top):
			RegexStr.append(top2)
			RegexStr.append(top)
			#print("BREAK")
			break
		elif isinstance(top2, Union) and not is_full(top2):
			top3 = RegexStr.pop()
			RegexStr.append(Union(top3, top))


def create_stack_from_regex(regex):
	RegexStr = []
	idx = 0
	end = len(regex)
	while idx < end:
		c = regex[idx]
		#print("->|" + c + "|")
		C = None
		if c is " ":
			idx += 1
			continue
		if c.isalnum():
			C = Symbol(c)
			idx += 1
		if c is "[":
			if regex[idx:idx+6] == "[a-z]+":
				C = make_plus(a_z("a"))
				idx += 6
			elif regex[idx:idx+6] == "[0-9]+":
				C = make_plus(zero_9("0"))
				idx += 6
		if c is '\'':
			idx2 = regex[(idx+1):].find(c)
			idx2 += idx + 1
			c = regex[idx+1 : idx2]
			C = Symbol(c)
			idx = idx2 + 1
		if c is "(":
			cexpr = parantezare(regex[idx:])
			C = create_stack_from_regex(cexpr)
			idx += 2
			idx += len(cexpr)
		if c is "|":
			C = Union(None, None)
			idx += 1
		if idx < len(regex):
			if regex[idx] is "+":	# daca am situatie: '$'+ / a* etc.
				C = make_plus(C)
				idx += 1
			elif regex[idx] is "*":
				C = Star(C)
				idx += 1
		RegexStr.append(C)
		unify_regex_stack(RegexStr)
		#print("Hello " + str(idx) + " " + str(C))
		#for x in RegexStr:
		#	print("--->" + str(x))
		#print("END")
		#print()
	t = RegexStr.pop()
	return t