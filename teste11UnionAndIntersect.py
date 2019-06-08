from imports.finiteautomaton import *

automata1 = NDFiniteAutomata()
automata1.load("automatons/termina com 3 a.afnd")
automata1.printTable()

automata2 = DFiniteAutomata()
automata2.load("automatons/a multiplo de 3.afd")
automata2.printTable()

result2 = automata1.intersect(automata2)
result2.printTable()