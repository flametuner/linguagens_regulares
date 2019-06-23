# -*- coding: latin-1 -*-
from tkinter import *
from tkinter.filedialog import asksaveasfilename

import automata_gui
from imports.finiteautomaton import *
from imports.guiutils import *


# GUI de Gramatica Regular
class GrammarGLCGui(Hideble):
    # Construtor
    def __init__(self, grammar, master=None, topLevel=None, name="new-grammar"):
        super(GrammarGLCGui, self).__init__(master)

        self.topLevel = topLevel
        self.master = master
        self.name = name
        self.grammar = grammar

        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.grammarframe = Frame(self.frame)
        self.grammarframe.pack()
        self.displaygrammar = Frame(self.frame)
        self.displaygrammar.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.container4 = Frame(self.frame)
        self.container4.pack()
        self.container5 = Frame(self.frame)
        self.container5.pack()
        self.container6 = Frame(self.frame)
        self.container6.pack()

        self.title = Label(self.container1, text=self.name)
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()


        self.updateProdGenDisplay()
        self.updateGrammarDisplay()

        self.entry_textDe = StringVar()

        self.entry_textDe.trace("w", lambda *args: character_limit(self.entry_textDe))
        self.entry_textDe.trace("w", lambda *args: self.entry_textDe.set(self.entry_textDe.get().upper()))

        self.addProd = Button(self.container2)
        self.addProd["text"] = "Adicionar producao"
        self.addProd["font"] = ("Roboto", "10")
        self.addProd["width"] = 20
        self.addProd.bind("<ButtonRelease-1>", self.createAddProductionFrame)
        self.addProd.pack(side=LEFT)

        self.removeProd = Button(self.container2)
        self.removeProd["text"] = "Remover producao"
        self.removeProd["font"] = ("Roboto", "10")
        self.removeProd["width"] = 20
        self.removeProd.bind("<ButtonRelease-1>", self.createRemoveProductionFrame)
        self.removeProd.pack(side=LEFT)

        self.setInitial = Button(self.container4)
        self.setInitial["text"] = "Alterar estado inicial"
        self.setInitial["font"] = ("Roboto", "10")
        self.setInitial["width"] = 20
        self.setInitial.bind("<ButtonRelease-1>",
                             lambda event, command=self.alterInitialState, label="Alterar": self.createStateSelect(
                                 command, label, "Nao Terminal"))
        self.setInitial.pack()

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

    # Frame de adicionar producao
    def createAddProductionFrame(self, event):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        container2 = Frame(window)
        container2.pack()
        container3 = Frame(window)
        container3.pack()
        container4 = Frame(window)
        container4.pack()

        self.entry_textDe.set('')

        nomeLabel = Label(container, text="De", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.fromState = Entry(container, textvariable=self.entry_textDe)
        self.fromState["width"] = 10
        self.fromState["font"] = "Roboto"
        self.fromState.pack(side=LEFT)

        nomeLabel = Label(container2, text="Producao", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.newprod = Entry(container2)
        self.newprod["width"] = 10
        self.newprod["font"] = "Roboto"
        self.newprod.pack(side=LEFT)

        adicionar = Button(container4)
        adicionar["text"] = "Adicionar"
        adicionar["font"] = ("Roboto", "10")
        adicionar["width"] = 20
        adicionar["command"] = window.destroy
        adicionar.bind("<ButtonRelease-1>", self.addProduct)
        adicionar.pack(side=LEFT)

        exit = Button(container4)
        exit["text"] = "Cancelar"
        exit["font"] = ("Roboto", "10")
        exit["width"] = 20
        exit["command"] = window.destroy
        exit.pack(side=LEFT)

    # Frame de remover producao
    def createRemoveProductionFrame(self, event):
        window = Toplevel(self.master)
        for nt in self.grammar.productions:
            container = Frame(window)
            container.pack()
            l = Label(container, text=str(nt) + ": ")
            l["font"] = ("Roboto", "15", "bold")
            l.pack(side=LEFT)
            id = 0
            for x in self.grammar.productions[nt]:
                b = Button(container)
                b["text"] = x
                b["font"] = ("Roboto", "10")
                b["width"] = 4
                b.bind("<ButtonRelease-1>", lambda event, to=nt, term=x: self.removeProduct(to, term))
                b["command"] = window.destroy
                b.pack(side=LEFT)
                id += 1

    # Selecao de producao
    def createStateSelect(self, command, labelName, text):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        for nt in self.grammar.productions:
            b = Button(container)
            b["text"] = str(nt)
            b["font"] = ("Roboto", "10")
            b["width"] = 5
            b["command"] = window.destroy
            b.bind("<ButtonRelease-1>", lambda event, a=str(nt): self.alterInitialState(a))
            b.pack(side=LEFT)

    # Adicionar producao e update nos Displays
    def addProduct(self, event):
        if not self.fromState.get():
            displayBox(self.master, "Estado de inicio nao pode ser nulo")
            return
        if not self.newprod.get():
            displayBox(self.master, "Producao nao pode ser nulo")
            return
        self.grammar.addProduction(self.fromState.get()[0], self.newprod.get())
        self.updateProdGenDisplay()
        self.updateGrammarDisplay()

    # Remover producao e update nos Displays
    def removeProduct(self, to, prod):
        self.grammar.removeProduction(to, prod)
        self.updateProdGenDisplay()
        self.updateGrammarDisplay()

    # Atualizacao do display de gerador de palavras
    def updateProdGenDisplay(self):
        for widget in self.grammarframe.winfo_children():
            widget.destroy()

    # Atualizacao de display da gramatica
    def updateGrammarDisplay(self):
        for widget in self.displaygrammar.winfo_children():
            widget.destroy()
        for x in self.grammar.productions:
            l = Label(self.displaygrammar, text=str(x) + ": " + str(' | '.join(self.grammar.productions[x])))
            l["font"] = ("Roboto", "15", "bold")
            l.pack()

    # Altera producao inicial
    def alterInitialState(self, id):
        self.grammar.setInitial(id)
        self.updateProdGenDisplay()


    # Salvar
    def file_save(self, event):
        f = asksaveasfilename(defaultextension=".gr",
                              filetypes=[('Arquivos de Gramatica Livre de Context', '.glc'), ('Todos os arquivos', '.*')])
        if not f:
            return
        self.grammar.save(f)
        self.title["text"] = f.split('/')[-1]
        displayBox(self.master, "Salvo com sucesso em " + f)

    # Retornar ao menu anterior
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()
