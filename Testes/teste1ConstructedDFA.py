from imports.finiteautomaton import *

dfaconstructed = DFiniteAutomata()
dfaconstructed.addState(0)
dfaconstructed.addState(1)
dfaconstructed.addState(2)
dfaconstructed.addTransiction(0, '0', 0)
dfaconstructed.addTransiction(0, '1', 1)
dfaconstructed.addTransiction(1, '0', 2)
dfaconstructed.addTransiction(1, '1', 0)
dfaconstructed.addTransiction(2, '0', 1)
dfaconstructed.addTransiction(2, '1', 2)
dfaconstructed.setInitial(0)
dfaconstructed.addAccepting(0)

dfaconstructed.save("automatons/dfa.afd")

dfaconstructed.printTable()