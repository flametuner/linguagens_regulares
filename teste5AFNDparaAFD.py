from imports.finiteautomaton import *

loadedAutomata = NDFiniteAutomata()
loadedAutomata.load("automatons/ndfa.fa")
finite = loadedAutomata.determinize()

finite.printTable()