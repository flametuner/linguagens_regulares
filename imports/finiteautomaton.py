import pickle
import string


# Representação de Automato Finito
class FiniteAutomata:
    def __init__(self, automata=None, initial=0, accepting=None):
        # Se está recebendo um automato significa que ele já foi carregado
        # Se nao, inicia um novo dict
        if automata is None:
            self.automata = {}
        else:
            self.automata = automata
        self.initial = str(initial)
        if accepting is None:
            self.accepting = set()
        else:
            self.accepting = accepting

    def setInitial(self, state):
        self.initial = str(state)

    def isInitial(self, state):
        return self.initial == str(state)

    def addAccepting(self, state):
        self.accepting.add(str(state))

    def isAccepting(self, state):
        return state in self.accepting

    def removeAccepting(self, state):
        self.accepting.remove(str(state))

    def addState(self, state):
        self.automata[str(state)] = {}

    def hasState(self, state):
        return str(state) in self.automata

    # Para remover o estado, nós tentamos remove-lo das transições para não ocorrer problemas
    # Primeiro tentamos remover o estado do set(), se der erro ele cai no except e remove apenas a string
    def removeState(self, state):
        del self.automata[str(state)]
        for x in self.automata:
            keys = list(self.automata[x].keys())
            while keys:
                c = keys.pop()
                try:
                    if state in self.automata[x][c]:
                        self.automata[x][c].remove(str(state))
                except:
                    if state == self.automata[x][c]:
                        del self.automata[x][c]
        if self.isAccepting(state):
            self.removeAccepting(state)

    def getStates(self):
        return self.automata.keys()

    def getChars(self):
        chars = set()
        for x in self.automata.values():
            for y in x.keys():
                chars.add(y)
        chars = list(chars)
        chars.sort()
        return chars

    def addTransiction(self, state, char, to):
        self.automata[str(state)][char] = str(to)

    def removeTransiction(self, state, char):
        self.automata[str(state)].pop(char)

    def save(self, file):
        with open(file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    # Carrega o automato finito a partir de um filename
    def load(self, file):
        with open(file, 'rb') as pickle_file:
            finiteAutomata = pickle.load(pickle_file)
            self.automata = finiteAutomata.automata
            self.initial = finiteAutomata.initial
            self.accepting = finiteAutomata.accepting

    def union(self, other):
        union_result = NDFiniteAutomata()
        start_state = 'q0'
        union_result.addState(start_state)
        union_result.setInitial(start_state)
        id = 1
        translateTable = {}
        for state in self.getStates():
            translateTable[state] = 'q' + str(id)
            union_result.addState(translateTable[state])
            id += 1
        for state in self.getStates():
            for char in self.getChars():
                if char in self.automata[state].keys():
                    toState = self.automata[state][char]
                    if isinstance(toState, str):
                        union_result.addTransiction(translateTable[state], char, translateTable[toState])
                    else:
                        for s in toState:
                            union_result.addTransiction(translateTable[state], char, translateTable[s])
        for accept in self.accepting:
            union_result.addAccepting(translateTable[accept])
        union_result.addTransiction(start_state, '&', translateTable[self.initial])
        translateTable = {}
        for state in other.getStates():
            translateTable[state] = 'q' + str(id)
            union_result.addState(translateTable[state])
            id += 1
        for state in other.getStates():
            for char in other.getChars():
                if char in other.automata[state].keys():
                    toState = other.automata[state][char]
                    if isinstance(toState, str):
                        union_result.addTransiction(translateTable[state], char, translateTable[toState])
                    else:
                        for s in toState:
                            union_result.addTransiction(translateTable[state], char, translateTable[s])
        for accept in other.accepting:
            union_result.addAccepting(translateTable[accept])
        union_result.addTransiction(start_state, '&', translateTable[other.initial])

        return union_result

    def intersect(self, other):
        self.complement()
        other.complement()
        automata = self.union(other)

        automata.complement()
        if automata.initial in automata.accepting:
            automata.accepting.remove(automata.initial)

        return automata

    def complement(self):
        final_states = [item for item in list(self.getStates()) if item not in self.accepting]
        self.accepting = final_states

    # Função para printar tabela no console
    def printTable(self):
        chars = self.getChars()
        print("      | \'" + "\' | \'".join(chars) + "' |")
        print("------", end='')
        for i in range(len(chars)):
            print("|-----", end='')
        print("|")
        states = list(self.getStates())
        states.sort()
        states.sort(key=len)
        for state in states:
            if state in self.accepting:
                print("*", end='')
            else:
                print(" ", end='')
            if state == self.initial:
                print("->", end='')
            else:
                print("  ", end='')
            print(state + "  |  ", end='')
            for c in chars:
                if c in self.automata[state]:
                    print(str(self.automata[state][c]) + "  |  ", end='')
                else:
                    print("-  |  ", end='')
            print()
        print()


# Automato Finito Não Deterministico filho de FiniteAutomata
class NDFiniteAutomata(FiniteAutomata):
    # Alteramos o addTransiction para suportar transições não deterministicas
    def addTransiction(self, state, char, to):
        if char not in self.automata[str(state)]:
            self.automata[str(state)][char] = set()
        self.automata[str(state)][char].add(str(to))

    # Determinizar
    def determinize(self):
        finite = DFiniteAutomata()
        chars = self.getChars()
        tState = []
        for state in self.getStates():
            tState.append({state})
        finite.setInitial(self.initial)
        while tState:
            stateList = list(tState.pop())
            init = False
            if len(stateList) == 1 and stateList[0] == self.initial:
                init = True
            (state, accept) = self.eClosure(stateList)
            s = getState(state)
            finite.addState(s)
            if init:
                finite.setInitial(s)
            if accept:
                finite.addAccepting(s)
            for char in chars:
                if char == '&':
                    continue
                trans = set()
                for toState in state:
                    if not char in self.automata[toState]:
                        continue
                    trans.update(self.automata[toState][char])
                if len(trans) == 0:
                    continue
                (fecho, accept) = self.eClosure(list(trans))
                newState = getState(fecho)
                if not newState in finite.automata and not newState in tState:
                    tState.append(fecho)
                finite.addTransiction(s, char, newState)
        return finite

    # Função e-fecho que retorna a lista de estados alcançaveis, e um boolean para saber se esse novo estado é de aceitação
    def eClosure(self, efecho):
        state = set()
        accept = False
        while efecho:
            to = efecho.pop()
            state.add(to)
            if to in self.accepting:
                accept = True
            if '&' in self.automata[to]:
                for x in self.automata[to]['&']:
                    if not x in state:
                        efecho.append(x)
        return (state, accept)

    # Implementação de aceitação de string
    # Primeiro crimaos um automato finito Deterministico temporario e retornamos se ele aceita
    def accepts(self, s):
        finite = self.determinize()
        return finite.accepts(s)


# Automato Finito Deterministico filho de FiniteAutomata
class DFiniteAutomata(FiniteAutomata):
    # Roda a String, caracter por caracter por todos os estados
    # Se cair em estado que não existe, retorna False
    # Se cair em estado que não é de aceitação, retorna False
    # Se cair em estado de aceitação, retorna True
    def accepts(self, s):
        state = self.initial
        try:
            for c in s:
                if not c in self.automata[state]:
                    return False
                state = self.automata[state][c]
        except:
            print("Malformed automata")
        return state in self.accepting

    # Converte o AFD para Gramatica Regular
    def convertRG(self):
        grammar = RegularGrammar('S')
        stateNum = 0
        letters = string.ascii_uppercase.replace('S', '')
        conversion = {}
        hasEmptyWord = False
        for x in self.automata:
            if self.isInitial(x):
                conversion[x] = 'S'
            elif not x in conversion:
                conversion[x] = letters[stateNum]
                stateNum += 1
            if self.isInitial(x) and self.isAccepting(x):
                hasEmptyWord = True
            for y in self.automata[x]:
                if not self.automata[x][y] in conversion:
                    conversion[self.automata[x][y]] = letters[stateNum]
                    stateNum += 1
                if self.isAccepting(self.automata[x][y]):
                    grammar.addProduction(conversion[x], y)
                grammar.addProduction(conversion[x], y, conversion[self.automata[x][y]])
        # Se a linguagem tiver palavra vazia (estado inicial é de aceitação)
        # Adiciona Palavra Vazia na Gramática
        if hasEmptyWord:
            grammar.addEmptyWord()
        return grammar

    def minimize(self):
        alcancancaveis = set()
        lista = [self.initial]
        while lista:
            state = lista.pop(0)
            alcancancaveis.add(state)
            for nt in self.getChars():
                if nt in self.automata[state]:
                    if self.automata[state][nt] in alcancancaveis:
                        continue
                    lista.append(self.automata[state][nt])

        inalcancaveis = [item for item in list(self.getStates()) if item not in alcancancaveis]
        for state in inalcancaveis:
            self.removeState(state)
        vivos = set(self.accepting)
        inverseAutomata = {}
        for state in self.getStates():
            for nt in self.getChars():
                if nt in self.automata[state]:
                    toState = self.automata[state][nt]
                    if toState not in inverseAutomata:
                        inverseAutomata[toState] = set()
                    inverseAutomata[toState].add(state)
        lista = list(vivos)
        while lista:
            state = lista.pop(0)
            vivos.add(state)
            if state in inverseAutomata:
                for fromState in inverseAutomata[state]:
                    if fromState not in vivos:
                        lista.append(fromState)
        mortos = [item for item in list(self.getStates()) if item not in vivos]
        for state in mortos:
            self.removeState(state)

        p = [list(self.accepting), [item for item in list(self.getStates()) if item not in self.accepting]]
        consistent = False
        while not consistent:
            consistent = True
            for sets in p:
                for symbol in self.getChars():
                    for sett in p:
                        temp = []
                        for q in sett:
                            if symbol in self.automata[q]:
                                to = self.automata[q][symbol]
                                if to in sets:
                                    if q not in temp:
                                        temp.append(q)
                        if temp and temp != sett:
                            consistent = False
                            p.remove(sett)
                            p.append(temp)
                            temp_t = list(sett)
                            for state in temp:
                                temp_t.remove(state)
                            p.append(temp_t)
        for state in p:
            if self.initial in state:
                self.setInitial(''.join(state))
                break
        final_states = []
        for state in p:
            for final_state in self.accepting:
                if final_state in state and ''.join(state) not in final_states:
                    final_states.append(''.join(state))
        self.accepting = final_states
        new_automata = {}
        for state in p:
            state_name = ''.join(state)
            new_automata[state_name] = {}
            for symbol in self.getChars():
                destiny = ''
                if symbol in self.automata[state[0]]:
                    for state2 in p:
                        if self.automata[state[0]][symbol] in state2:
                            destiny = ''.join(state2)
                if destiny:
                    new_automata[state_name][symbol] = destiny
        self.automata = new_automata

    def rename(self):
        result = DFiniteAutomata()
        start_state = 'q0'
        result.addState(start_state)
        result.setInitial(start_state)
        id = 1
        translateTable = {}
        for state in self.getStates():
            if state == self.initial:
                translateTable[state] = start_state
            else:
                translateTable[state] = 'q' + str(id)
                result.addState(translateTable[state])
                id += 1
        for state in self.getStates():
            for char in self.getChars():
                if char in self.automata[state].keys():
                    toState = self.automata[state][char]
                    if isinstance(toState, str):
                        result.addTransiction(translateTable[state], char, translateTable[toState])
                    else:
                        for s in toState:
                            result.addTransiction(translateTable[state], char, translateTable[s])
        for accept in self.accepting:
            result.addAccepting(translateTable[accept])
        self.initial = result.initial
        self.accepting = result.accepting
        self.automata = result.automata


class Grammar:

    def __init__(self, initial=''):
        self.productions = {}
        self.initial = initial.upper()

    def get_terminals(self, production):
        terminals = set()
        nonterminals = set()
        for c in production:
            if c not in self.productions:
                terminals.add(c)
            else:
                nonterminals.add(c)
        return terminals, nonterminals

    def isInitial(self, nt):
        return nt == self.initial

    def setInitial(self, nt):
        self.initial = nt

    # Adiciona produção
    def addProduction(self, to, prod):
        if not to in self.productions:
            self.productions[to] = []
        if prod in self.productions[to]:
            return -1
        self.productions[to].append(prod)
        return len(self.productions[to]) - 1

    def removeProduction(self, to, prod):
        if to not in self.productions:
            return
        if prod not in self.productions[to]:
            return
        self.productions[to].remove(prod)
        if len(self.productions[to]) == 0:
            del self.productions[to]

    def printGrammar(self):
        for x in self.productions:
            print(str(x) + ": ", end='')
            for prod in self.productions[x]:
                print(' '.join(prod), end=' | ')
            print()
        print()

    def save(self, file):
        with open(file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def load(self, file):
        with open(file, 'rb') as pickle_file:
            gram = pickle.load(pickle_file)
            self.productions = gram.productions
            self.initial = gram.initial

    def convert_chomsky_normal_form(self):
        self.chomsky_start()
        self.chomsky_term()
        self.chomsky_bin()
        self.chomsky_del()
        self.chomsky_unit()

    def chomsky_start(self):
        self.productions['S~'] = [[self.initial]]
        self.initial = 'S~'

    def substitute(self, substituteDict):
        for nt in self.productions:
            for prod in self.productions[nt]:
                for i in range(len(prod)):
                    term = prod[i]
                    if term in substituteDict:
                        prod[i] = substituteDict[term]

    def chomsky_term(self):
        terminals = set()
        nonterminals = set()
        for nt in self.productions:
            for prod in self.productions[nt]:
                t, nt = self.get_terminals(prod)
                nonterminals.update(nt)
                if len(prod) > 1 and len(t) > 0:
                    terminals.update(t)
        substituteDict = {}
        for t in terminals:
            substituteDict[t] = "NT" + t.upper()
        self.substitute(substituteDict)
        for k in substituteDict:
            self.addProduction(substituteDict[k], [k])

    def chomsky_bin(self):
        analyze = list(self.productions.keys())
        while analyze:
            next = analyze.pop(0)
            for prod in self.productions[next]:
                t, nt = self.get_terminals(prod)
                if len(prod) > 2 and len(t) == 0:
                    copyProd = list(prod)
                    del prod[1:len(prod)]
                    prod.append(next + "'")
                    copyProd.pop(0)
                    self.addProduction(next + "'", copyProd)
                    analyze.append(next + "'")

    def chomsky_del(self):
        nullableNonTerminals = set()
        for nt in self.productions:
            for prod in self.productions[nt]:
                for term in prod:
                    if term == '&':
                        nullableNonTerminals.add(nt)
                        break
        indirectNullable = set()
        while nullableNonTerminals:
            for next in self.productions.keys():
                productions = list(self.productions[next])
                while productions:
                    prod = productions.pop(0).copy()
                    for term in prod:
                        if term in nullableNonTerminals:
                            prod.remove(term)
                            if len(prod) == 0:
                                indirectNullable.add(next)
                                prod.append('&')
                            if prod not in self.productions[next]:
                                self.productions[next].append(prod)
                                productions.append(prod)
                            break
            for nt in nullableNonTerminals:
                self.removeProduction(nt, ['&'])
            nullableNonTerminals.clear()
            nullableNonTerminals = indirectNullable

    def chomsky_unit(self):
        analyze = list(self.productions.keys())
        while analyze:
            next = analyze.pop(0)
            productions = list(self.productions[next])
            while productions:
                prod = productions.pop(0)
                t, nt = self.get_terminals(prod)
                if len(prod) == 1 and len(t) == 0:
                    unit = prod[0]
                    for prodUnit in self.productions[unit]:
                        self.addProduction(next, prodUnit)
                    self.removeProduction(next, prod)
                    productions.extend(self.productions[unit])

    def remove_left_recursion(self):
        self.remove_left_recursion_indirect()

    def remove_left_recursion_direct(self):
        dict = list(self.productions.keys())
        while dict:
            nt = dict.pop(0)
            recursive_productions = []
            non_recursive_productions = []
            productions = list(self.productions[nt])
            while productions:
                prod = productions.pop(0)
                if prod[0] == nt:
                    recursive_productions.append(prod)
                else:
                    non_recursive_productions.append(prod)
            if len(recursive_productions) > 0:
                for rp in recursive_productions:
                    self.removeProduction(nt, rp)
                    rp.pop(0)
                    rp.append(nt + '^')
                    self.addProduction(nt + '^', rp)
                self.addProduction(nt + '^', ['&'])
                for nrp in non_recursive_productions:
                    nrp.append(nt + '^')

    def remove_left_recursion_indirect(self):
        nonterminals = list(self.productions.keys())
        for i in range(len(nonterminals)):
            for j in range(i):
                productions = list(self.productions[nonterminals[i]])
                while productions:
                    prod = productions.pop(0)
                    if prod[0] == nonterminals[j]:
                        self.removeProduction(nonterminals[i], prod)
                        alpha = prod[1:len(prod)]
                        for beta in self.productions[nonterminals[j]]:
                            beta = beta.copy()
                            beta.extend(alpha)
                            self.addProduction(nonterminals[i], beta)
        self.remove_left_recursion_direct()

    def factorization(self):
        self.remove_left_recursion_indirect()

    def factorization_direct(self):
        dict = list(self.productions.keys())
        while dict:
            nt = dict.pop(0)
            productions = list(self.productions[nt])
            while productions:
                prod_1 = productions.pop(0)
                alpha = []
                productions_2 = list(productions)
                while productions_2:
                    prod_2 = productions_2.pop(0)
                    for i in range(len(prod_1)):
                        if prod_1[i] == prod_2[i]:
                            alpha.append(prod_1[i])
                            productions_2.clear()
                        else:
                            break

                if len(alpha) > 0:
                    all_prod = list(self.productions[nt])
                    while all_prod:
                        prod = all_prod.pop(0)
                        contains = False
                        for i in range(len(alpha)):
                            if alpha[i] == prod[0]:
                                prod.pop(0)
                                contains = True

                        if contains:
                            self.removeProduction(nt, prod)
                            self.addProduction(nt + '!', prod)
                    alpha.append(nt + '!')
                    self.addProduction(nt, alpha)

    def factorization_indirect(self):
        dict = list(self.productions.keys())
        while dict:
            nt = dict.pop(0)
            productions = list(self.productions[nt])
            while productions:
                prod = productions.pop(0)
                alpha = prod[1:len(prod)]
                first_term = prod[0]
                if first_term in self.productions.keys():
                    self.removeProduction(nt, prod)
                    for beta in self.productions[first_term]:
                        beta = beta.copy()
                        beta.extend(alpha)
                        self.addProduction(nt, beta)
        self.factorization_direct()

    def first(self, term):
        terminals = set()
        nonterminals = set(self.productions.keys())
        for nt in self.productions:
            for prod in self.productions[nt]:
                for curr_term in prod:
                    if curr_term not in nonterminals:
                        terminals.add(curr_term)
        if term in terminals:
            return {term}
        if term not in nonterminals:
            raise Exception("Term not in Grammar")
        first = set()
        for prod in self.productions[term]:
            first_term = prod[0]
            if first_term == '&' or first_term in terminals:
                first.add(first_term)
            else:
                remove = False
                for i in range(len(prod)):
                    if prod[i] == term:
                        break
                    first_next = self.first(prod[i])
                    first.update(first_next)
                    if '&' not in first_next:
                        remove = True
                        break
                if remove and '&' in first:
                    first.remove('&')
        return first

    def first_prod(self, prod):
        first = set()
        remove = False
        for i in range(len(prod)):
            first_next = self.first(prod[i])
            first.update(first_next)
            if '&' not in first_next:
                remove = True
                break
        if remove and '&' in first:
            first.remove('&')
        return first

    def follow(self, term):
        follow = set()
        nonterminals = set(self.productions.keys())
        if term not in nonterminals:
            return follow
        if self.isInitial(term):
            follow.add('$')
        for nt in self.productions:
            for prod in self.productions[nt]:
                for i in range(len(prod)):
                    if prod[i] == term:
                        third_step = False
                        if i + 1 < len(prod):
                            first_next = self.first_prod(prod[i + 1:])
                            follow.update(first_next - {'&'})
                            if '&' in first_next:
                                third_step = True
                        elif i + 1 == len(prod):
                            third_step = True
                        if third_step and nt != term:
                            follow_a = self.follow(nt)
                            follow.update(follow_a)
        return follow

    def generate_ll_1(self):
        self.remove_left_recursion()
        self.factorization()
        nonterminals = set(self.productions.keys())
        for nt in nonterminals:
            if len(self.first(nt).intersection(self.follow(nt))) > 0:
                raise Exception("Gramatica não é LL(1)")
        i = 1
        analysis_table = {}
        production_list = {}
        for nt in self.productions:
            if nt not in analysis_table:
                analysis_table[nt] = {}
            for prod in self.productions[nt]:
                first = self.first_prod(prod)
                if '&' in first:
                    follow = self.follow(nt)
                    for beta in follow:
                        analysis_table[nt][beta] = i
                    first.remove('&')
                for alpha in first:
                    analysis_table[nt][alpha] = i
                production_list[i] = prod
                i += 1
        return analysis_table, production_list

# Gramatica Regular
class RegularGrammar(Grammar):

    def __init__(self, *args, **kwargs):
        super(RegularGrammar, self).__init__(*args, **kwargs)
        self.current = self.initial.upper()

    # Adiciona palavra vazia, criando um novo estado inicial, duplicando os itens e
    def addEmptyWord(self):
        duplicate = False
        for prod in self.productions[self.initial]:
            if len(prod) <= 1:
                continue
            if self.isInitial(prod[1]):
                duplicate = True
                break
        if duplicate:
            self.productions['Z'] = self.productions[self.initial].copy()
            self.initial = 'Z'
        self.productions[self.initial].append('&')
        self.cleanCurrent()

    # Adiciona produção
    # Se o simbolo terminal for &, e o simbolo for inicial roda função addEmptyWord()
    def addProduction(self, to, terminal, nonterminal=""):
        if not to.upper() in self.productions:
            self.productions[to.upper()] = []
        if terminal == '&':
            if len(self.productions) == 1:
                self.setInitial(to)
            if self.isInitial(to):
                self.addEmptyWord()
                return len(self.productions[self.initial]) - 1
            if len(self.productions[to.upper()]) == 0:
                del self.productions[to.upper()]
            return -1
        prod = terminal.lower() + nonterminal.upper()
        return super(RegularGrammar, self).addProduction(to.upper(), prod)

    def removeProduction(self, to, terminal, nonterminal=""):
        prod = terminal.lower() + nonterminal.upper()
        super(RegularGrammar, self).removeProduction(to.upper(), prod)

    # Geração de string com nao terminal e id da produção
    def generate(self, nt, prod):
        try:
            charac = self.productions[nt.upper()][prod]
            if charac == '&':
                charac = ''
            self.current = self.current.replace(nt.upper(), charac)
        except:
            print("Production '" + str(prod) + "' not found for non-terminal: " + str(nt))
        return self.current

    def currentTerminal(self):
        return not any(x.isupper() for x in self.current)

    def cleanCurrent(self):
        self.current = self.initial

    # Converte para AFND
    def convertAFND(self):
        afnd = NDFiniteAutomata()
        afnd.setInitial(self.initial)
        afnd.addState('@')
        afnd.addAccepting('@')
        for x in self.productions:
            afnd.addState(x)
            for prod in self.productions[x]:
                to = '@'
                if len(prod) > 1:
                    to = prod[1]
                afnd.addTransiction(x, prod[0], to)
        return afnd

    def load(self, file):
        super(RegularGrammar, self).load(file)
        self.current = self.initial


# Expressao Regular
class RegularExpression:
    def __init__(self, regex=''):
        self.regex = set()
        if regex:
            self.regex.add(regex)
        self.fecho = False

    def __str__(self):
        return '+'.join(list(self.regex))

    def clear(self):
        self.regex.clear()

    def isValid(self):
        stack = []
        dict = {')': '(', '}': '{', ']': '['}
        for c in str(self):
            if c == '(':
                stack.append(c)
            elif c == ')' and (len(stack) == 0 or not stack.pop() == '('):
                return False
        return len(stack) == 0

    def kleene(self):
        if self.fecho:
            return
        element = str(self)
        if len(element) > 1:
            element = '(' + element + ')'
        elif len(element) == 0:
            return
        element += '*'
        self.fecho = True
        self.clear()
        self.regex.add(element)

    def concatenate(self, regex2):
        if len(self.regex) > 1:
            element = '(' + str(self) + ')' + str(regex2)
            self.clear()
            self.regex.add(element)
        elif len(self.regex) == 1:
            self.regex.add(self.regex.pop() + str(regex2))
        else:
            self.regex.update(regex2.regex)
        self.fecho = False

    def union(self, regex2):
        self.regex.update(regex2.regex)
        self.fecho = False

    def save(self, file):
        with open(file, 'wb') as pickle_file:
            pickle.dump(self, pickle_file)

    def load(self, file):
        with open(file, 'rb') as pickle_file:
            regex = pickle.load(pickle_file)
            self.regex = regex.regex
            self.fecho = regex.fecho


def getState(l):
    if len(l) > 1:
        l = list(l)
        l.sort()
        return ''.join(l)
    else:
        return list(l)[0]
