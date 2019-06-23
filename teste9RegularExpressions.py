from imports.finiteautomaton import RegularExpression

regex1 = RegularExpression('ab')
regex2 = RegularExpression('ba')
regex1.union(regex2)
print(regex1)
regex2.kleene()
print(regex2)
regex1.concatenate(regex2)
print(regex1)