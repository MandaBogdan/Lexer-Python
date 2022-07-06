#!/usr/bin/python
from typing import Dict, List
from collections import defaultdict
from lab2 import DFA

caracterr = ""
sinkchar = ""

class Lexer:
	_sinkc : str;

	def __init__(self, dfas):
		#dfas.sort(key=lambda a: a[1], reverse=True)
		self.dfas = dfas

	def longest_prefix(self, word):
		global sinkchar
		auto = self.dfas
		idx = 0
		max_length = 0
		max_name = ""
		lexemes = []
		i = len(word)
		accepted = False
		w = ""
		while i >= 0:
			sinked_dfas = 0
			w = word[idx:i]						#delimitez subsirul
			nrx = 0
			accepted = False
			for a in auto:
				dfa, dfa_name = a
				x = dfa.accepted(w)
				nrx = max(nrx, x)
				if not isinstance(x, bool):		# a ajuns in sinkstate
					sinked_dfas += 1
				elif x is False:
					sinked_dfas += 1
				elif x is True:					#subsirul a fost acceptat de un dfa
					accepted = True
					max_name = dfa_name
					max_length = len(w)
					idx = i
					i = len(word) + 1	#prioritatea este data de ordinea din fisier
					break				#deci nu mai continui pentru celelalte DFAuri
			i -= 1
			if sinked_dfas == len(auto):
				sinkchar = str(i + nrx)
			if accepted == True:		#daca am acceptat adaug in lista
				sinkchar = ""
				lexemes.append((max_name, w))
				max_length = 0
				max_name = ""
			if (idx >= i):				#am parcurs toate subsirurile curente fara sa accept
				break
		self._sinkc = sinkchar
		return lexemes

def get_DFAs(input):
	DFAs = []
	file = open(input)
	file_content = file.read()
	contents =  file_content.splitlines()
	cursor = 0
	while True:
	#ALFABET
		alfa = []
		if "\\" not in contents[cursor]:
			alfa = [ch for ch in contents[cursor]]
		else:
			line = contents[cursor]			# exitsa \n in alfabet, trebuie afisat diferit
			i = 0
			while i < len(line):
				ch = line[i]
				if ch is not '\\':
					alfa.append(ch)
				else:
					if (line[i+1] == 'n'):
						ch = '\n'
					i += 1
					alfa.append(ch)
				i += 1
		name = contents[cursor+1]
		q0 = contents[cursor+2]
		d = defaultdict(dict)
		cursor = cursor + 3
		#TRANZITII
		while True:
			trans = contents[cursor];
			[a,b,c] = trans.split(",")
			b = b[1:-1]					#elimin ghilimelele
			if b == "\\n":
				b = '\n'
			d[a][b] = c 				#din starea a ajung in b prin simbolul c
			cursor += 1
			if "," not in contents[cursor]:
				break
		#STARI FINALE
		qf = contents[cursor].split()
		dfa = DFA(alfa, name, q0, qf, d)
		DFAs.append((dfa, name))
		cursor += 2
		if cursor > len(contents):
			break
	return DFAs

def print_DFAs(input):
	automate = [aut for (aut, n) in input]
	for a in automate:
		print(a)

def runlexer(lexpath, inputpath, outpath):
	DFAs = get_DFAs(lexpath)
	file = open(inputpath)
	ww = file.read()
	lexer = Lexer(DFAs)
	lexemes = lexer.longest_prefix(ww)
	open(outpath, 'w').close()
	f = open(outpath, "a")
	if (len(lexemes) == 0):
		f.write("empty")
	else:
		for (token, word) in lexemes[0:-1]:
			if '\n' in word:
				word = word.replace("\n","\\n")
			f.write(token + " " + word + '\n')
		(t,w) = lexemes[-1]
		if '\n' in w:
			w = w.replace("\n","\\n")
		f.write(t + " " + w)
	f.close()