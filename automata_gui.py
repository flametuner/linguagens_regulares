# -*- coding: latin-1 -*-
from tkinter.filedialog import asksaveasfilename

import grammar_gui
from imports.finiteautomaton import *
from imports.guiutils import *


# Classe de GUI para display de Automato Finito
class Automata(Hideble):
    # Construtor
    def __init__(self, automata, master=None, topLevel=None, name="new-automata"):
        super(Automata, self).__init__(master)

        self.topLevel = topLevel
        self.master = master
        self.name = name
        self.automata = automata
        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.automataframe = Frame(self.frame)
        self.automataframe.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.container4 = Frame(self.frame)
        self.container4.pack()
        self.container5 = Frame(self.frame)
        self.container5.pack()
        self.convertGram = Frame(self.frame)
        self.convertGram.pack()
        self.container6 = Frame(self.frame)
        self.container6.pack()

        self.title = Label(self.container1, text=self.name)
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack(side=LEFT)
        self.needSave = Label(self.container1, text='')
        self.needSave["font"] = ("Roboto", "15", "bold")
        self.needSave.pack(side=LEFT)

        self.updateAutomataDisplay()

        self.entry_text = StringVar()

        self.entry_text.trace("w", lambda *args: character_limit(self.entry_text))

        self.addState = Button(self.container2)
        self.addState["text"] = "Adicionar estado"
        self.addState["font"] = ("Roboto", "10")
        self.addState["width"] = 20
        self.addState.bind("<ButtonRelease-1>",
                           lambda event, command=self.addNewState, label="Adicionar": self.createStateSelect(command,
                                                                                                             label,
                                                                                                             "Nome do Estado"))
        self.addState.pack(side=LEFT)

        self.removeState = Button(self.container2)
        self.removeState["text"] = "Remover estado"
        self.removeState["font"] = ("Roboto", "10")
        self.removeState["width"] = 20
        self.removeState.bind("<ButtonRelease-1>",
                              lambda event, command=self.removeOldState, label="Remover": self.createStateSelect(
                                  command, label, "Nome do Estado"))
        self.removeState.pack(side=LEFT)

        self.addTransiction = Button(self.container3)
        self.addTransiction["text"] = "Adicionar transicao"
        self.addTransiction["font"] = ("Roboto", "10")
        self.addTransiction["width"] = 20
        self.addTransiction.bind("<ButtonRelease-1>", self.createTransictionAdd)
        self.addTransiction.pack(side=LEFT)

        self.removeTransiction = Button(self.container3)
        self.removeTransiction["text"] = "Remover transicao"
        self.removeTransiction["font"] = ("Roboto", "10")
        self.removeTransiction["width"] = 20
        self.removeTransiction.bind("<ButtonRelease-1>", self.createTransictionRemove)
        self.removeTransiction.pack(side=LEFT)

        self.addFinalState = Button(self.container4)
        self.addFinalState["text"] = "Adicionar estado de aceitacao"
        self.addFinalState["font"] = ("Roboto", "10")
        self.addFinalState["width"] = 25
        self.addFinalState.bind("<ButtonRelease-1>",
                                lambda event, command=self.addAcceptState, label="Adicionar": self.createStateSelect(
                                    command, label, "Nome do Estado"))
        self.addFinalState.pack(side=LEFT)

        self.removeFinalState = Button(self.container4)
        self.removeFinalState["text"] = "Remover estado de aceitacao"
        self.removeFinalState["font"] = ("Roboto", "10")
        self.removeFinalState["width"] = 25
        self.removeFinalState.bind("<ButtonRelease-1>", lambda event, command=self.removeAcceptState,
                                                               label="Remover": self.createStateSelect(command, label,
                                                                                                       "Nome do Estado"))
        self.removeFinalState.pack(side=LEFT)

        self.setInitial = Button(self.container5)
        self.setInitial["text"] = "Alterar estado inicial"
        self.setInitial["font"] = ("Roboto", "10")
        self.setInitial["width"] = 20
        self.setInitial.bind("<ButtonRelease-1>",
                             lambda event, command=self.alterInitialState, label="Alterar": self.createStateSelect(
                                 command, label, "Nome do Estado"))
        self.setInitial.pack(side=LEFT)

        self.check = Button(self.container6)
        self.check["text"] = "Check uma String"
        self.check["font"] = ("Roboto", "10")
        self.check["width"] = 20
        self.check.bind("<ButtonRelease-1>",
                        lambda event, command=self.checkString, label="Checkar": self.createStateSelect(command, label,
                                                                                                        "String"))
        self.check.pack()

        self.determinize = Button(self.convertGram)
        self.determinize["text"] = "Determinizar"
        self.determinize["font"] = ("Roboto", "10")
        self.determinize["width"] = 20
        self.determinize.bind("<ButtonRelease-1>",
                              lambda event, command=self.determinizeAutomata, label="Sim": createConfimationBox(
                                  self.master, command,
                                  "Ao continuar, voce ir transformar o AFND Atual em AFD. Deseja continuar?"))

        self.convertRG = Button(self.convertGram)
        self.convertRG["text"] = "Converter para GR"
        self.convertRG["font"] = ("Roboto", "10")
        self.convertRG["width"] = 20
        self.convertRG.bind("<ButtonRelease-1>",
                            lambda event, command=self.convertToGrammar, label="Sim": createConfimationBox(self.master,
                                                                                                           command,
                                                                                                           "Ao continuar, voce ir transformar o AFD Atual em GR. Deseja continuar?"))
        self.minimize = Button(self.convertGram)
        self.minimize["text"] = "Minimizar"
        self.minimize["font"] = ("Roboto", "10")
        self.minimize["width"] = 20
        self.minimize.bind("<ButtonRelease-1>",
                           lambda event, command=self.minimizeAutomata, label="Sim": createConfimationBox(
                               self.master, command,
                               "Ao continuar, voce ira minimizar o automato. Deseja continuar?"))

        self.rename = Button(self.convertGram)
        self.rename["text"] = "Renomear estados"
        self.rename["font"] = ("Roboto", "10")
        self.rename["width"] = 20
        self.rename.bind("<ButtonRelease-1>",
                         lambda event: self.renameAutomata())

        self.updateButtons()
        self.save = Button(self.container6)
        self.save["text"] = "Salvar"
        self.save["font"] = ("Roboto", "10")
        self.save["width"] = 20
        self.save.bind("<ButtonRelease-1>", self.file_save)
        self.save.pack()

        self.exit = Button(self.container6)
        self.exit["text"] = "Voltar"
        self.exit["font"] = ("Roboto", "10")
        self.exit["width"] = 20
        self.exit.bind("<ButtonRelease-1>", self.returnTop)
        self.exit.pack()

    # Se for AFD: mostrar botao de conversao para Gramatica Regular
    # Se for AFND: mostrar botao de determinizar
    def updateButtons(self):
        if isinstance(self.automata, NDFiniteAutomata):
            self.determinize.pack()
        elif isinstance(self.automata, DFiniteAutomata):
            self.convertRG.pack()
            self.minimize.pack()
            self.rename.pack()

    # Função para atualizar o automato finito na GUI
    def updateAutomataDisplay(self):
        for widget in self.automataframe.winfo_children():
            widget.destroy()
        col = 1
        chars = self.automata.getChars()
        for c in chars:
            l = Label(self.automataframe, text=c, borderwidth=1, width=4, relief="solid")
            l["font"] = ("Roboto", "15", "bold")
            l.grid(row=0, column=col, sticky=W + E + N + S)
            col += 1
        ron = 1
        for state in self.automata.getStates():
            labelStr = ""
            if self.automata.isAccepting(state):
                labelStr += "*"
            if self.automata.isInitial(state):
                labelStr += "->"
            labelStr += state
            l = Label(self.automataframe, text=' ' + labelStr + ' ', borderwidth=1, relief="solid")
            l["font"] = ("Roboto", "15", "bold")
            l.grid(row=ron, column=0, sticky=W + E + N + S)
            self.automataframe.columnconfigure(col, weight=1)
            col = 1
            for c in chars:
                if c in self.automata.automata[state]:
                    if len(self.automata.automata[state][c]) > 0:
                        labelStr = str(self.automata.automata[state][c])
                    else:
                        labelStr = '-'
                else:
                    labelStr = "-"
                l = Label(self.automataframe, text=' ' + labelStr + ' ', borderwidth=1, relief="solid")
                l["font"] = ("Roboto", "15", "bold")
                l.grid(row=ron, column=col, sticky=W + E + N + S)
                col += 1
            ron += 1

    # Criação de nova GUI para seleção de estado
    def createStateSelect(self, command, labelName, text):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        container2 = Frame(window)
        container2.pack()
        nomeLabel = Label(container, text=text, font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.stateName = Entry(container)
        self.stateName["width"] = 10
        self.stateName["font"] = "Roboto"
        self.stateName.pack(side=LEFT)

        adicionar = Button(container2)
        adicionar["text"] = labelName
        adicionar["font"] = ("Roboto", "10")
        adicionar["width"] = 20
        adicionar["command"] = window.destroy
        adicionar.bind("<ButtonRelease-1>", command)
        adicionar.pack(side=LEFT)

        exit = Button(container2)
        exit["text"] = "Cancelar"
        exit["font"] = ("Roboto", "10")
        exit["width"] = 20
        exit["command"] = window.destroy
        exit.pack(side=LEFT)

    # Criação de nova GUI para adicionar transicao
    def createTransictionAdd(self, event):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        container2 = Frame(window)
        container2.pack()
        container3 = Frame(window)
        container3.pack()
        container4 = Frame(window)
        container4.pack()
        nomeLabel = Label(container, text="De qual estado", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.fromState = Entry(container)
        self.fromState["width"] = 10
        self.fromState["font"] = "Roboto"
        self.fromState.pack(side=LEFT)

        nomeLabel = Label(container2, text="Qual caracter", font="Roboto")
        nomeLabel.pack(side=LEFT)
        self.entry_text.set('')
        self.char = Entry(container2, textvariable=self.entry_text)
        self.char["width"] = 10
        self.char["font"] = "Roboto"
        self.char.pack(side=LEFT)

        nomeLabel = Label(container3, text="Para qual estado", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.toState = Entry(container3)
        self.toState["width"] = 10
        self.toState["font"] = "Roboto"
        self.toState.pack(side=LEFT)

        adicionar = Button(container4)
        adicionar["text"] = "Adicionar"
        adicionar["font"] = ("Roboto", "10")
        adicionar["width"] = 20
        adicionar["command"] = window.destroy
        adicionar.bind("<ButtonRelease-1>", self.addTrans)
        adicionar.pack(side=LEFT)

        exit = Button(container4)
        exit["text"] = "Cancelar"
        exit["font"] = ("Roboto", "10")
        exit["width"] = 20
        exit["command"] = window.destroy
        exit.pack(side=LEFT)

    # Criação de nova GUI para remover transicao
    def createTransictionRemove(self, event):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        container2 = Frame(window)
        container2.pack()
        container3 = Frame(window)
        container3.pack()
        nomeLabel = Label(container, text="De qual estado", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.fromState = Entry(container)
        self.fromState["width"] = 10
        self.fromState["font"] = "Roboto"
        self.fromState.pack(side=LEFT)

        nomeLabel = Label(container2, text="Qual caracter", font="Roboto")
        nomeLabel.pack(side=LEFT)
        self.entry_text.set('')
        self.char = Entry(container2, textvariable=self.entry_text)
        self.char["width"] = 10
        self.char["font"] = "Roboto"
        self.char.pack(side=LEFT)

        adicionar = Button(container3)
        adicionar["text"] = "Remover"
        adicionar["font"] = ("Roboto", "10")
        adicionar["width"] = 20
        adicionar["command"] = window.destroy
        adicionar.bind("<ButtonRelease-1>", self.removeTrans)
        adicionar.pack(side=LEFT)

        exit = Button(container3)
        exit["text"] = "Cancelar"
        exit["font"] = ("Roboto", "10")
        exit["width"] = 20
        exit["command"] = window.destroy
        exit.pack(side=LEFT)

    # Funcao chamada para determinizar automato e dar display do novo automato
    def determinizeAutomata(self, event):
        self.determinize.destroy()
        finite = self.automata.determinize()
        self.automata = finite
        self.updateAutomataDisplay()
        self.updateButtons()
        self.convertRG.pack()
        self.needSave["text"] = '*'

    # Funcao chamada para determinizar automato e dar display do novo automato
    def minimizeAutomata(self, event):
        self.automata.minimize()
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Conversao de gramatica e display de gramatica
    def convertToGrammar(self, event):
        grammar = self.automata.convertRG()
        grammarFrame = grammar_gui.GrammarGui(grammar, self.master, self.topLevel)
        self.hide()
        grammarFrame.show()

    # Renomeia e da display
    def renameAutomata(self):
        self.automata.rename()
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Adicionar transicao e atualiza GUI de automato
    def addTrans(self, event):
        if not self.char.get():
            displayBox(self.master, "O caracter nao pode ser nulo!")
            return
        fromStates = self.fromState.get().split(", ")
        for s in fromStates:
            if not self.automata.hasState(s):
                displayBox(self.master, "O estado 'De':" + s + " nao existe!")
                return
        toStates = self.toState.get().split(", ")
        for s in toStates:
            if not self.automata.hasState(s):
                displayBox(self.master, "O estado 'Para':" + s + " nao existe!")
                return
        for s in fromStates:
            for to in toStates:
                self.automata.addTransiction(s, self.char.get()[0], to)
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Remover transicao do automato e atualizar automato
    def removeTrans(self, event):
        if not self.char:
            displayBox(self.master, "O caracter nao pode ser nulo!")
            return
        if not self.automata.hasState(self.fromState.get()):
            displayBox(self.master, "O estado 'Para' nao existe!")
            return
        self.automata.removeTransiction(self.fromState.get(), self.char.get()[0])
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Adiciona um novo estado e atualiza GUI do automato
    def addNewState(self, event):
        if not self.stateName.get():
            return
        if self.automata.hasState(self.stateName.get()):
            displayBox(self.master, "O estado ja existe!")
            return
        self.automata.addState(self.stateName.get())
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Remove um estado e atualiza GUI do automato
    def removeOldState(self, event):
        if not self.automata.hasState(self.stateName.get()):
            displayBox(self.master, "O estado nao existe!")
            return
        self.automata.removeState(self.stateName.get())
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Adiciona um estado de aceitacao e atualiza GUI do automato
    def addAcceptState(self, event):
        if not self.automata.hasState(self.stateName.get()):
            displayBox(self.master, "O estado nao existe!")
            return
        if self.automata.isAccepting(self.stateName.get()):
            displayBox(self.master, "O estado ja e de aceitacao")
            return
        self.automata.addAccepting(self.stateName.get())
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Remove um estado de aceitacao e atualiza GUI do automato
    def removeAcceptState(self, event):
        if not self.automata.hasState(self.stateName.get()):
            displayBox(self.master, "O estado nao existe!")
            return
        if not self.automata.isAccepting(self.stateName.get()):
            displayBox(self.master, "O estado nao e de aceitacao")
            return
        self.automata.removeAccepting(self.stateName.get())
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Altera o estado inicial e atualiza GUI do automato
    def alterInitialState(self, event):
        if not self.automata.hasState(self.stateName.get()):
            displayBox(self.master, "O estado nao existe!")
            return
        self.automata.setInitial(self.stateName.get())
        self.needSave["text"] = '*'
        self.updateAutomataDisplay()

    # Checka uma string e retorna se aceitou ou nao
    def checkString(self, event):
        if self.automata.accepts(self.stateName.get()):
            displayBox(self.master, "String foi aceita pelo automato")
        else:
            displayBox(self.master, "String foi rejeitada pelo automato")

    # Salvar
    def file_save(self, event):
        types = [('Arquivos de AFD', '.afd'), ('Todos os arquivos', '.*')]
        default = '.afd'
        if isinstance(self.automata, NDFiniteAutomata):
            types = [('Arquivos de AFND', '.afnd'), ('Todos os arquivos', '.*')]
            default = '.afnd'
        f = asksaveasfilename(defaultextension=default, filetypes=types)
        if not f:
            return
        self.automata.save(f)
        self.title["text"] = f.split('/')[-1]
        self.needSave["text"] = ''
        displayBox(self.master, "Salvo com sucesso em " + f)

    # Retornar ao menu anterior
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()
