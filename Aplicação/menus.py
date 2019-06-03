# -*- coding: latin-1 -*-
from tkinter import Label, Button, LEFT, Frame
from tkinter.filedialog import askopenfilename

from automata_gui import Automata
from grammar_gui import Grammar
from imports.finiteautomaton import *
from imports.guiutils import Hideble
from regex_gui import Regex


# Classes utilizadas para todos os Menus

# Menu principal
class Menu(Hideble):
    # Construtor
    def __init__(self, master=None):
        super(Menu, self).__init__(master)

        self.title = Label(self.frame, text="Menu")
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()
        self.famenu = None
        self.rgmenu = None
        self.regexmenu = None
        self.automaton = Button(self.frame)
        self.automaton["text"] = "Autômato Finito"
        self.automaton["font"] = ("Roboto", "10")
        self.automaton["width"] = 20
        self.automaton.bind("<ButtonRelease-1>", self.openFaMenu)
        self.automaton.pack(side=LEFT)

        self.grammar = Button(self.frame)
        self.grammar["text"] = "Gramática Regular"
        self.grammar["font"] = ("Roboto", "10")
        self.grammar["width"] = 20
        self.grammar.bind("<ButtonRelease-1>", self.openRgMenu)
        self.grammar.pack(side=LEFT)

        self.regex = Button(self.frame)
        self.regex["text"] = "Expressão Regular"
        self.regex["font"] = ("Roboto", "10")
        self.regex["width"] = 20
        self.regex.bind("<ButtonRelease-1>", self.openRegexMenu)
        self.regex.pack(side=LEFT)

    def setFaMenu(self, menu):
        self.famenu = menu

    # Função para abrir Menu de Automato finito
    def openFaMenu(self, event):
        if not self.famenu is None:
            self.hide()
            self.famenu.show()

    def setRgMenu(self, menu):
        self.rgmenu = menu

    # Função para abrir Menu de Gramatica Regular
    def openRgMenu(self, event):
        if not self.rgmenu is None:
            self.hide()
            self.rgmenu.show()

    def setRegexMenu(self, menu):
        self.regexmenu = menu

    # Função para abrir Menu de Expressões Regulares
    def openRegexMenu(self, event):
        if not self.regexmenu is None:
            self.hide()
            self.regexmenu.show()


# Menu de Automato Finito
class FAMenu(Hideble):
    # Construtor
    def __init__(self, master=None, topLevel=None):
        super(FAMenu, self).__init__(master)

        self.master = master

        self.topLevel = topLevel
        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.container4 = Frame(self.frame)
        self.container4.pack()
        self.title = Label(self.container1, text="Autômatos Finitos")
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()
        self.createafd = Button(self.container2)
        self.createafd["text"] = "Criar novo AFD"
        self.createafd["font"] = ("Roboto", "10")
        self.createafd["width"] = 20
        self.createafd.bind("<ButtonRelease-1>", self.createAFD)
        self.createafd.pack(side=LEFT)

        self.createafnd = Button(self.container2)
        self.createafnd["text"] = "Criar novo AFND"
        self.createafnd["font"] = ("Roboto", "10")
        self.createafnd["width"] = 20
        self.createafnd.bind("<ButtonRelease-1>", self.createAFND)
        self.createafnd.pack(side=LEFT)

        self.loadafd = Button(self.container3)
        self.loadafd["text"] = "Carregar AFD"
        self.loadafd["font"] = ("Roboto", "10")
        self.loadafd["width"] = 20
        self.loadafd.config(state="active")
        self.loadafd.bind("<ButtonRelease-1>", self.selectAFD)
        self.loadafd.pack(side=LEFT)

        self.loadafnd = Button(self.container3)
        self.loadafnd["text"] = "Carregar AFND"
        self.loadafnd["font"] = ("Roboto", "10")
        self.loadafnd["width"] = 20
        self.loadafnd.bind("<ButtonRelease-1>", self.selectAFND)
        self.loadafnd.pack(side=LEFT)

        self.back = Button(self.container4)
        self.back["text"] = "Voltar"
        self.back["font"] = ("Roboto", "10")
        self.back["width"] = 20
        self.back.bind("<ButtonRelease-1>", self.returnTop)
        self.back.pack()

    # Criacao do AFD e abrir GUI Automata
    def createAFD(self, event):
        automata = DFiniteAutomata()
        automataFrame = Automata(automata, self.master, self)
        self.hide()
        automataFrame.show()

    # Criacao do AFnD e abrir GUI Automata
    def createAFND(self, event):
        automata = NDFiniteAutomata()
        automataFrame = Automata(automata, self.master, self)
        self.hide()
        automataFrame.show()

    # Abrindo seleção de AFD por nome de arquivo
    def selectAFD(self, event):
        filename = askopenfilename(filetypes=[('Arquivos de AFD', '.afd'), ('Todos os arquivos', '.*')])
        if not filename:
            return
        automata = DFiniteAutomata()
        automata.load(filename)
        automataFrame = Automata(automata, self.master, self, filename.split("/")[-1])
        self.hide()
        automataFrame.show()

    # Abrindo seleção de AFND por nome de arquivo
    def selectAFND(self, event):
        filename = askopenfilename(filetypes=[('Arquivos de AFND', '.afnd'), ('Todos os arquivos', '.*')])
        if not filename:
            return
        automata = NDFiniteAutomata()
        automata.load(filename)
        automataFrame = Automata(automata, self.master, self, filename.split("/")[-1])
        self.hide()
        automataFrame.show()

    # Retornar ao menu principal
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()


# Menu de Gramatica Regular
class RGMenu(Hideble):
    # Construtor
    def __init__(self, master=None, topLevel=None):
        super(RGMenu, self).__init__(master)

        self.master = master

        self.topLevel = topLevel
        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.title = Label(self.container1, text="Gramáticas Regulares")
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()
        self.createafd = Button(self.container2)
        self.createafd["text"] = "Criar nova GR"
        self.createafd["font"] = ("Roboto", "10")
        self.createafd["width"] = 20
        self.createafd.bind("<ButtonRelease-1>", self.createGR)
        self.createafd.pack(side=LEFT)

        self.loadafd = Button(self.container2)
        self.loadafd["text"] = "Carregar GR"
        self.loadafd["font"] = ("Roboto", "10")
        self.loadafd["width"] = 20
        self.loadafd.config(state="active")
        self.loadafd.bind("<ButtonRelease-1>", self.selectGR)
        self.loadafd.pack(side=LEFT)

        self.back = Button(self.container3)
        self.back["text"] = "Voltar"
        self.back["font"] = ("Roboto", "10")
        self.back["width"] = 20
        self.back.bind("<ButtonRelease-1>", self.returnTop)
        self.back.pack()

    # Criação de uma nova GR e abrindo GUI
    def createGR(self, event):
        grammar = RegularGrammar()
        grammarFrame = Grammar(grammar, self.master, self)
        self.hide()
        grammarFrame.show()

    # Seleção de GR por filename
    def selectGR(self, event):
        filename = askopenfilename(filetypes=[('Arquivos de Gramatica Regular', '.gr'), ('Todos os arquivos', '.*')])
        if not filename:
            return
        grammar = RegularGrammar()
        grammar.load(filename)
        grammarFrame = Grammar(grammar, self.master, self, filename.split("/")[-1])
        self.hide()
        grammarFrame.show()

    # Retornar ao menu principal
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()


# Menu de Expressao Regular
class RegexMenu(Hideble):
    # Construtor
    def __init__(self, master=None, topLevel=None):
        super(RegexMenu, self).__init__(master)

        self.master = master

        self.topLevel = topLevel
        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.title = Label(self.container1, text="Expressões Regulares")
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()
        self.createafd = Button(self.container2)
        self.createafd["text"] = "Criar nova ER"
        self.createafd["font"] = ("Roboto", "10")
        self.createafd["width"] = 20
        self.createafd.bind("<ButtonRelease-1>", self.createER)
        self.createafd.pack(side=LEFT)

        self.loadafd = Button(self.container2)
        self.loadafd["text"] = "Carregar ER"
        self.loadafd["font"] = ("Roboto", "10")
        self.loadafd["width"] = 20
        self.loadafd.config(state="active")
        self.loadafd.bind("<ButtonRelease-1>", self.selectER)
        self.loadafd.pack(side=LEFT)

        self.back = Button(self.container3)
        self.back["text"] = "Voltar"
        self.back["font"] = ("Roboto", "10")
        self.back["width"] = 20
        self.back.bind("<ButtonRelease-1>", self.returnTop)
        self.back.pack()

    # Criação de Expressao Regular
    def createER(self, event):
        regex = RegularExpression()
        regexFrame = Regex(regex, self.master, self)
        self.hide()
        regexFrame.show()

    # Seleção de Expressão Regular por filename
    def selectER(self, event):
        filename = askopenfilename(filetypes=[('Arquivos de Expressão Regular', '.er'), ('Todos os arquivos', '.*')])
        if not filename:
            return
        regex = RegularExpression()
        regex.load(filename)
        regexFrame = Regex(regex, self.master, self, filename.split("/")[-1])
        self.hide()
        regexFrame.show()

    # Voltar ao menu principal
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()
