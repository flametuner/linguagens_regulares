# -*- coding: latin-1 -*-
from tkinter.filedialog import asksaveasfilename

from imports.guiutils import *
import re

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
        self.container7 = Frame(self.frame)
        self.container7.pack()

        self.title = Label(self.container1, text=self.name)
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()

        self.updateProdGenDisplay()
        self.updateGrammarDisplay()

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

        self.setInitial = Button(self.container3)
        self.setInitial["text"] = "Alterar estado inicial"
        self.setInitial["font"] = ("Roboto", "10")
        self.setInitial["width"] = 20
        self.setInitial.bind("<ButtonRelease-1>",
                             lambda event, command=self.alterInitialState, label="Alterar": self.createStateSelect(
                                 command, label, "Nao Terminal"))
        self.setInitial.pack()

        self.chomsky = Button(self.container4)
        self.chomsky["text"] = "Forma normal de Chomsky"
        self.chomsky["font"] = ("Roboto", "10")
        self.chomsky["width"] = 20
        self.chomsky.bind("<ButtonRelease-1>",
                            lambda event, command=self.convertToChomsky, label="Sim": createConfimationBox(self.master,
                                                                                                           command,
                                                                                                           "Ao continuar, voce converter a gramatica atual para forma normal de chomsky. Deseja continuar?"))
        self.chomsky.pack()

        self.left_recursion_dir = Button(self.container4)
        self.left_recursion_dir["text"] = "Remover Req Esq Dir"
        self.left_recursion_dir["font"] = ("Roboto", "10")
        self.left_recursion_dir["width"] = 20
        self.left_recursion_dir.bind("<ButtonRelease-1>",
                          lambda event, command=self.removeLeftRecursionDir, label="Sim": createConfimationBox(self.master,
                                                                                                         command,
                                                                                                         "Ao continuar, voce ira remover a recursão a esquerda. Deseja continuar?"))
        self.left_recursion_dir.pack(side=LEFT)

        self.left_recursion_indir = Button(self.container4)
        self.left_recursion_indir["text"] = "Remover Req Esq Indir"
        self.left_recursion_indir["font"] = ("Roboto", "10")
        self.left_recursion_indir["width"] = 20
        self.left_recursion_indir.bind("<ButtonRelease-1>",
                                     lambda event, command=self.removeLeftRecursionIndir, label="Sim": createConfimationBox(
                                         self.master,
                                         command,
                                         "Ao continuar, voce ira remover a recursão a esquerda. Deseja continuar?"))
        self.left_recursion_indir.pack()

        self.fatoration_dir = Button(self.container5)
        self.fatoration_dir["text"] = "Fatoração Direta"
        self.fatoration_dir["font"] = ("Roboto", "10")
        self.fatoration_dir["width"] = 20
        self.fatoration_dir.bind("<ButtonRelease-1>",
                                 lambda event, command=self.factorization_direct, label="Sim": createConfimationBox(
                                     self.master,
                                     command,
                                     "Ao continuar, voce ira fatorar a gramatica. Deseja continuar?"))
        self.fatoration_dir.pack(side=LEFT)

        self.fatoration_dir = Button(self.container5)
        self.fatoration_dir["text"] = "Fatoração Indireta"
        self.fatoration_dir["font"] = ("Roboto", "10")
        self.fatoration_dir["width"] = 20
        self.fatoration_dir.bind("<ButtonRelease-1>",
                                 lambda event, command=self.factorization_indirect, label="Sim": createConfimationBox(
                                     self.master,
                                     command,
                                     "Ao continuar, voce ira fatorar a gramatica. Deseja continuar?"))
        self.fatoration_dir.pack()

        self.first = Button(self.container6)
        self.first["text"] = "First"
        self.first["font"] = ("Roboto", "10")
        self.first["width"] = 20
        self.first.bind("<ButtonRelease-1>",
                             lambda event, command=self.first_func, label="First": self.createFirstSelect(
                                 command, label, "First"))
        self.first.pack(side=LEFT)

        self.follow = Button(self.container6)
        self.follow["text"] = "Follow"
        self.follow["font"] = ("Roboto", "10")
        self.follow["width"] = 20
        self.follow.bind("<ButtonRelease-1>",
                             lambda event, command=self.follow_func, label="Follow": self.createFollowSelect(
                                 command, label, "Follow"))
        self.follow.pack()

        self.table = Button(self.container7)
        self.table["text"] = "Tabela de Análise"
        self.table["font"] = ("Roboto", "10")
        self.table["width"] = 20
        self.table.bind("<ButtonRelease-1>", self.show_table)
        self.table.pack()


        self.save = Button(self.container7)
        self.save["text"] = "Salvar"
        self.save["font"] = ("Roboto", "10")
        self.save["width"] = 20
        self.save.bind("<ButtonRelease-1>", self.file_save)
        self.save.pack()

        self.exit = Button(self.container7)
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

        nomeLabel = Label(container, text="De", font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.fromState = Entry(container)
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

    # Selecao de first
    def createFirstSelect(self, command, labelName, text):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        terminals = set()
        nonterminals = set(self.grammar.productions.keys())
        for nt in self.grammar.productions:
            for prod in self.grammar.productions[nt]:
                for curr_term in prod:
                    if curr_term not in nonterminals:
                        terminals.add(curr_term)
        terminals.update(nonterminals)
        for nt in terminals:
            b = Button(container)
            b["text"] = str(nt)
            b["font"] = ("Roboto", "10")
            b["width"] = 5
            b["command"] = window.destroy
            b.bind("<ButtonRelease-1>", lambda event, a=str(nt): self.first_func(a))
            b.pack(side=LEFT)

    # Selecao de follow
    def createFollowSelect(self, command, labelName, text):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        nonterminals = set(self.grammar.productions.keys())
        for nt in nonterminals:
            b = Button(container)
            b["text"] = str(nt)
            b["font"] = ("Roboto", "10")
            b["width"] = 5
            b["command"] = window.destroy
            b.bind("<ButtonRelease-1>", lambda event, a=str(nt): self.follow_func(a))
            b.pack(side=LEFT)

    # Adicionar producao e update nos Displays
    def addProduct(self, event):
        if not self.fromState.get():
            displayBox(self.master, "Estado de inicio nao pode ser nulo")
            return
        if not self.newprod.get():
            displayBox(self.master, "Producao nao pode ser nulo")
            return
        elements = re.findall(r'("(.*?)"|.)', self.newprod.get())
        elements = [tuple(j for j in i if j)[-1] for i in elements]
        self.grammar.addProduction(self.fromState.get(), list(elements))
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
            prod_list = []
            for prod in self.grammar.productions[x]:
                prod_list.append(' '.join(prod))
            l = Label(self.displaygrammar, text=str(x) + ": " + str(' | '.join(prod_list)))
            l["font"] = ("Roboto", "15", "bold")
            l.pack()

    # Altera producao inicial
    def alterInitialState(self, id):
        self.grammar.setInitial(id)
        self.updateProdGenDisplay()

    # Altera producao inicial
    def first_func(self, id):
        first = self.grammar.first(id)
        displayBox(self.master, str(first))

    # Altera producao inicial
    def follow_func(self, id):
        follow = self.grammar.follow(id)
        displayBox(self.master, str(follow))

    # Altera producao inicial
    def convertToChomsky(self, event):
        self.grammar.convert_chomsky_normal_form()
        self.updateGrammarDisplay()

    def removeLeftRecursionDir(self, event):
        self.grammar.remove_left_recursion_direct()
        self.updateGrammarDisplay()

    def removeLeftRecursionIndir(self, event):
        self.grammar.remove_left_recursion_indirect()
        self.updateGrammarDisplay()

    def factorization_direct(self, event):
        self.grammar.factorization_direct()
        self.updateGrammarDisplay()

    def factorization_indirect(self, event):
        self.grammar.factorization_indirect()
        self.updateGrammarDisplay()

    def show_table(self, event):
        # try:
            table, list = self.grammar.generate_ll_1()
            window = Toplevel(self.master)
            container = Frame(window)
            container.pack()
            terminals = set()
            nonterminals = set(self.grammar.productions.keys())
            for nt in self.grammar.productions:
                for prod in self.grammar.productions[nt]:
                    for curr_term in prod:
                        if curr_term not in nonterminals:
                            terminals.add(curr_term)
            terminals.add('$')
            for widget in container.winfo_children():
                widget.destroy()
            col = 1
            chars = terminals
            for c in chars:
                l = Label(container, text=c, borderwidth=1, width=4, relief="solid")
                l["font"] = ("Roboto", "15", "bold")
                l.grid(row=0, column=col, sticky=W + E + N + S)
                col += 1
            ron = 1
            for state in nonterminals:
                labelStr = ""
                if self.grammar.isInitial(state):
                    labelStr += "*"
                labelStr += state
                l = Label(container, text=' ' + labelStr + ' ', borderwidth=1, relief="solid")
                l["font"] = ("Roboto", "15", "bold")
                l.grid(row=ron, column=0, sticky=W + E + N + S)
                container.columnconfigure(col, weight=1)
                col = 1
                for c in chars:
                    if c in table[state]:
                        if table[state][c]:
                            labelStr = str(table[state][c])
                        else:
                            labelStr = '-'
                    else:
                        labelStr = "-"
                    l = Label(container, text=' ' + labelStr + ' ', borderwidth=1, relief="solid")
                    l["font"] = ("Roboto", "15", "bold")
                    l.grid(row=ron, column=col, sticky=W + E + N + S)
                    col += 1
                ron += 1

        #
        # except:
        #     displayBox(self.master, "Linguagem não é LL(1)")

    # Salvar
    def file_save(self, event):
        f = asksaveasfilename(defaultextension=".glc",
                              filetypes=[('Arquivos de Gramatica Livre de Context', '.glc'),
                                         ('Todos os arquivos', '.*')])
        if not f:
            return
        self.grammar.save(f)
        self.title["text"] = f.split('/')[-1]
        displayBox(self.master, "Salvo com sucesso em " + f)

    # Retornar ao menu anterior
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()