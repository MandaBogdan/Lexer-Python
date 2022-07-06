#!/usr/bin/python
import sys
from typing import Dict, List
from collections import defaultdict
from lab3 import *
from lab2 import *
from Lexer import *

epsilon = "ε"
crt_state = -1

def getNewState():
	global crt_state
	crt_state = crt_state + 1
	return crt_state

class NFA:

	def __init__(self, s0, sf):
		self.q0 = s0
		self.qf = sf
		self.delta = defaultdict(dict)
		self.alfa = set()

	def add_transition (self, state0, symbol, state1):
		if symbol not in self.delta[state0]:
			if isinstance(state1, list):
				self.delta[state0][symbol] = state1
			else:
				self.delta[state0][symbol] = [state1]
		else:
			self.delta[state0][symbol].append(state1)
		if symbol != epsilon:
			self.alfa.add(symbol)

	def print_transitions(self):
		for key1 in list(self.delta.keys()):
			for key2 in self.delta[key1]:
				print(str(key1) + " " + key2 + " " + str(self.delta[key1][key2]) )

	def unify(self, x: 'NFA'):
		for key1 in list(x.delta.keys()):
			for key2 in x.delta[key1]:
				self.add_transition(key1, key2, x.delta[key1][key2])

def NFA_from_Stack(s):
	n3 = None
	if isinstance(s, Concat):
		n1 = NFA_from_Stack(s._expr1)
		n2 = NFA_from_Stack(s._expr2)
		q0 = n1.q0
		qf = n2.qf
		n3 = NFA(q0, qf)
		n3.add_transition(n1.qf, epsilon, n2.q0)
		n3.unify(n1)
		n3.unify(n2)
	if isinstance(s, Union):
		n1 = NFA_from_Stack(s._expr1)
		n2 = NFA_from_Stack(s._expr2)
		q0 = getNewState()
		qf = getNewState()
		n3 = NFA(q0, qf)
		n3.add_transition(q0, epsilon ,n1.q0)
		n3.add_transition(q0, epsilon, n2.q0)
		n3.add_transition(n1.qf, epsilon, qf)
		n3.add_transition(n2.qf, epsilon, qf)
		n3.unify(n1)
		n3.unify(n2)
	if isinstance(s, Star):
		n0 = NFA_from_Stack(s._expr)
		q0 = getNewState()
		qf = getNewState()
		n3 = NFA(q0, qf)
		n3.add_transition(q0, epsilon, n0.q0)
		n3.add_transition(q0, epsilon, qf)
		n3.add_transition(n0.qf, epsilon, n0.q0)
		n3.add_transition(n0.qf, epsilon, qf)
		n3.unify(n0)
	if isinstance(s, Symbol):
		c = s._char
		q0 = getNewState()
		qf = getNewState()
		n3 = NFA(q0, qf)
		n3.add_transition(q0, c, qf)
	return n3

visited = set()
new_states = []

def DFS(q, c, delta):
	visited.add(q)
	if c in delta[q]:
		neigh = delta[q][c]
		for state in neigh:
			if c != epsilon:
				symbol_visited.add(state)
			if state not in visited:
				DFS(state, c, delta)

class DFA_from_NFA:
	def __init__(self, n: 'NFA'):
		self.q0 = None
		self.qf = []
		self.delta = defaultdict(dict)
		self.alfa = None
		self.initial_state(n)
		self.create(n)
		self.final_states(n)

	def initial_state(self, n: 'NFA'):
		global visited
		visited = set()
		DFS(n.q0, epsilon, n.delta)
		self.q0 = visited
		self.alfa = n.alfa

	def final_states(self, n:'NFA'):
		qf = n.qf
		for s in new_states[:-1]:
			if qf in s:
				self.qf.append(new_states.index(s))

	def add_transition(self, state0, symbol, state1):
		self.delta[state0][symbol] = state1

	def create(self, n: 'NFA'):
		global new_states
		global visited
		global symbol_visited
		new_states = []
		new_states.append(self.q0)
		for group_state in new_states:
			for c in self.alfa:
				next_state = set()
				for s in group_state:
					visited = set()
					if c in n.delta[s]:
						for state1 in n.delta[s][c]:
							DFS(state1, epsilon, n.delta)
							x = visited
							next_state.update(x)
				if len(next_state) != 0:
					if next_state not in new_states:
						new_states.append(next_state)
					self.add_transition(new_states.index(group_state), c, new_states.index(next_state))
		g = set()
		sink_state = len(new_states)
		g.add(sink_state)
		new_states.append(g)
		for c in self.alfa:
			for i in range(0, len(new_states)):
				if i not in list(self.delta.keys()):
					self.add_transition(i, c, sink_state)
				else:
					if c not in self.delta[i]:
						self.add_transition(i, c, sink_state)

	def print_transitions(self):
		for key1 in list(self.delta.keys()):
			for key2 in self.delta[key1]:
				print(str(key1) + " " + key2 + " " + str(self.delta[key1][key2]) )

def runparser(inp, outp):
	aasd = 2

def runcompletelexer(lexpath, inputpath, outpath):
	global sinkchar
	file1 = open(lexpath, 'r')
	lines = file1.readlines()
	DFA_List = []
	for line in lines:
		space = line.find(" ")
		token = line[0:space]
		regex = line[space+1:]
		regex = regex[:-1]
		regex = regex[:-1]
		Stack = create_stack_from_regex(regex)
		N = NFA_from_Stack(Stack)
		D = DFA_from_NFA(N)
		d = defaultdict(dict)
		for key1 in list(D.delta.keys()):
			for key2 in D.delta[key1]:
				key22 = str(key2)
				if key22 == "\\n":
					key22 = '\n'
				d[str(key1)][key22] = str(D.delta[key1][key2])
		dfa = DFA(sorted(D.alfa), token, "0", list(map(str,D.qf)), d)
		DFA_List.append((dfa, token))
	file1.close()
	file2 = open(inputpath, 'r')
	ww = file2.read()
	wwl = len(ww)
	lexer = Lexer(DFA_List)
	lexemes = lexer.longest_prefix(ww)
	open(outpath, 'w').close()
	f = open(outpath, "a")
	sinkchar = lexer._sinkc;
	if sinkchar != "":
		if int(sinkchar) == wwl:
			f.write("No viable alternative at character EOF, line 0")
		else:
			f.write("No viable alternative at character " + str(sinkchar) + ", line 0")
	else:
		if len(lexemes) > 0:
			for (token, word) in lexemes[0:-1]:
				if '\n' in word:
					word = word.replace("\n","\\n")
				f.write(token + " " + word + '\n')
			(t,w) = lexemes[-1]
			if '\n' in w:
				w = w.replace("\n","\\n")
			f.write(t + " " + w)
	f.close()

