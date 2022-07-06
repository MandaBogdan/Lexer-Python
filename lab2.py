#!/usr/bin/python
from typing import Dict, List
from collections import defaultdict

class DFA:
	def __init__(self, alfa, name, q0, qfs, d):
		self.alphabet = alfa
		self.delta = d
		self.initial = q0
		self.finals = qfs
		self.token = name
		self.states = find_states(d)
		self.sinkstates = find_sink(q0, qfs, d, self.states)

	def __str__(self):
		string = ""
		string += "ALFABET: " + str(self.alphabet) + "\n"
		string += ("Name: " + self.token) + "\n"
		string += ("Q0: " + self.initial + " Qf: " + str(self.finals)) + "\n"
		string += str(self.delta) + "\n"
		return string

	def next_config(self, point):
		state, word = point
		c = word[0]
		new_state = None
		new_word = word[1:]
		state = str(state)
		if state in list(self.delta.keys()):
			if c in self.delta[state]:
				new_state = self.delta[state][c]
				return (new_state, new_word)
		return -1

	def accepted(self, word):
		state = self.initial
		config = (state, word)
		nr = 0
		while 1:
			new_config = self.next_config(config)
			if new_config is not -1:
				nr += 1
				(new_state, new_word) = new_config
				new_state = str(new_state) 
			else:
				new_state = "x"
			if new_state in self.sinkstates:
				return nr
			if new_config is -1:
				return False
			if new_config[1] == "":
				if new_config[0] in self.finals:
					return True
				return False
			config = new_config

def find_states(d):
	states = set()
	for state in list(d.keys()):
		states.add(state)
		for c in d[state]:
			state2 = d[state][c]
			states.add(state2)
	return states

def find_sink(q0, qfs, d, states):
	rd = defaultdict(dict)
	for state in list(d.keys()):
		for c in d[state]:
			state2 = d[state][c]
			if c not in rd[state2]:
				rd[state2][c] = [state]
			else:
				rd[state2][c].append(state)
	queue = [] + qfs
	visited =  set()
	while len(queue) > 0:
		state = queue.pop(0)
		visited.add(state)
		for c in rd[state]:
			for state2 in rd[state][c]:
				if state2 not in visited:
					visited.add(state2)
					queue.append(state2)
	return list(set(states) - set(visited))