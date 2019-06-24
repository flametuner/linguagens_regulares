from imports.finiteautomaton import *

gtable = Grammar()
gtable.addProduction('E', ['T', "E'"])
gtable.addProduction("E'", ['∨', 'T', "E'"])
gtable.addProduction("E'", ['&'])
gtable.addProduction('T', ['F', "T'"])
gtable.addProduction("T'", ['∧', 'F', "T'"])
gtable.addProduction("T'", ['&'])
gtable.addProduction('F', ['¬', 'F'])
gtable.addProduction('F', ['id'])
gtable.setInitial('E')
gtable.printGrammar()
print(gtable.generate_ll_1())