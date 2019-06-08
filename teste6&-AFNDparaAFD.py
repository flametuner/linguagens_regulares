from imports.finiteautomaton import *

endfa = NDFiniteAutomata()
endfa.addState('p')
endfa.addState('q')
endfa.addState('r')

endfa.setInitial('p')
endfa.addAccepting('r')

endfa.addTransiction('p', '0', 'p')
endfa.addTransiction('p', '1', 'r')
endfa.addTransiction('q', '&', 'p')
endfa.addTransiction('q', '0', 'q')
endfa.addTransiction('r', '&', 'q')
endfa.addTransiction('r', '0', 'r')
endfa.addTransiction('r', '1', 'p')

edeterminized = endfa.determinize()

edeterminized.printTable()