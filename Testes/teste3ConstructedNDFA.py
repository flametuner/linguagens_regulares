from imports.finiteautomaton import *

ndfaconstructed = NDFiniteAutomata()
ndfaconstructed.addState('p')
ndfaconstructed.addState('q')
ndfaconstructed.addState('r')
ndfaconstructed.addState('s')

ndfaconstructed.setInitial('p')
ndfaconstructed.addAccepting('s')

ndfaconstructed.addTransiction('p', '0', 'p')
ndfaconstructed.addTransiction('p', '0', 'q')
ndfaconstructed.addTransiction('p', '1', 'p')
ndfaconstructed.addTransiction('q', '0', 'r')
ndfaconstructed.addTransiction('q', '1', 'r')
ndfaconstructed.addTransiction('r', '0', 's')
ndfaconstructed.addTransiction('s', '0', 's')
ndfaconstructed.addTransiction('s', '1', 's')

ndfaconstructed.save("automatons/ndfa.afnd")

ndfaconstructed.printTable()