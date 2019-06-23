from imports.finiteautomaton import *

loadedAutomata = DFiniteAutomata()
loadedAutomata.load("automatons/minimizacao.afd")
loadedAutomata.printTable()
loadedAutomata.minimize()
loadedAutomata.printTable()