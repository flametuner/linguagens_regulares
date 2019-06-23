from imports.finiteautomaton import *

grammar = RegularGrammar('A')

grammar.addProduction('A', 'a', 'B')
grammar.addProduction('A', 'b', 'A')
grammar.addProduction('A', 'a')
grammar.addProduction('B', 'b', 'B')
grammar.addProduction('B', 'a', 'A')
grammar.addProduction('B', 'b')
grammar.addProduction('C', 'a', 'D')
grammar.addProduction('C', 'b', 'C')
grammar.addProduction('C', 'b')
grammar.addProduction('D', 'a', 'C')
grammar.addProduction('D', 'b', 'D')
grammar.addProduction('D', 'a')

grammar.save("automatons/grammar.gr")
grammar.printGrammar()

