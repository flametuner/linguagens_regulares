# -*- coding: latin-1 -*-
from tkinter import *
from tkinter.filedialog import asksaveasfilename

from imports.finiteautomaton import RegularExpression
from imports.guiutils import *


# GUI de Expressao Regular
class Regex(Hideble):
    # Construtor
    def __init__(self, regex, master=None, topLevel=None, name="new-regex"):
        super(Regex, self).__init__(master)

        self.topLevel = topLevel
        self.master = master
        self.name = name
        self.regex = regex

        self.container1 = Frame(self.frame)
        self.container1.pack()
        self.container2 = Frame(self.frame)
        self.container2.pack()
        self.container3 = Frame(self.frame)
        self.container3.pack()
        self.container4 = Frame(self.frame)
        self.container4.pack()

        self.title = Label(self.container1, text=self.name)
        self.title["font"] = ("Roboto", "15", "bold")
        self.title.pack()

        self.generation = Label(self.container1, text=str(regex))
        self.generation["font"] = ("Roboto", "15", "bold")
        self.generation.pack()

        self.concat = Button(self.container2)
        self.concat["text"] = "Concatenação"
        self.concat["font"] = ("Roboto", "10")
        self.concat["width"] = 20
        self.concat.bind("<ButtonRelease-1>",
                         lambda event, command=self.concatWord, label="Concatenar": self.createNewRegexFrame(command,
                                                                                                             label,
                                                                                                             "Nova Regex"))
        self.concat.pack(side=LEFT)

        self.union = Button(self.container2)
        self.union["text"] = "União"
        self.union["font"] = ("Roboto", "10")
        self.union["width"] = 20
        self.union.bind("<ButtonRelease-1>",
                        lambda event, command=self.unionWord, label="Unir": self.createNewRegexFrame(command, label,
                                                                                                     "Nova Regex"))

        self.union.pack(side=LEFT)

        self.fecho = Button(self.container2)
        self.fecho["text"] = "Fecho de Kleen"
        self.fecho["font"] = ("Roboto", "10")
        self.fecho["width"] = 20
        self.fecho.bind("<ButtonRelease-1>", self.kleeneWord)
        self.fecho.pack(side=LEFT)

        self.clean = Button(self.container3)
        self.clean["text"] = "Limpar"
        self.clean["font"] = ("Roboto", "10")
        self.clean["width"] = 20
        self.clean.bind("<ButtonRelease-1>", self.cleanWord)
        self.clean.pack()

        self.save = Button(self.container4)
        self.save["text"] = "Salvar"
        self.save["font"] = ("Roboto", "10")
        self.save["width"] = 20
        self.save.bind("<ButtonRelease-1>", self.file_save)
        self.save.pack()

        self.exit = Button(self.container4)
        self.exit["text"] = "Voltar"
        self.exit["font"] = ("Roboto", "10")
        self.exit["width"] = 20
        self.exit.bind("<ButtonRelease-1>", self.returnTop)
        self.exit.pack()

    # Criacao de nova REGEX para uniao ou concatenacao
    def createNewRegexFrame(self, command, labelName, text):
        window = Toplevel(self.master)
        container = Frame(window)
        container.pack()
        container2 = Frame(window)
        container2.pack()
        nomeLabel = Label(container, text=text, font="Roboto")
        nomeLabel.pack(side=LEFT)

        self.newregex = Entry(container)
        self.newregex["width"] = 10
        self.newregex["font"] = "Roboto"
        self.newregex.pack(side=LEFT)

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

    # Uniao de regex
    def unionWord(self, event):
        newRegex = RegularExpression(self.newregex.get())
        if not newRegex.isValid():
            displayBox(self.master, "Expressão regular invalida")
            return
        self.regex.union(newRegex)
        self.updateRegexDisplay()

    # Concatenacao de regex
    def concatWord(self, event):
        newRegex = RegularExpression(self.newregex.get())
        if not newRegex.isValid():
            displayBox(self.master, "Expressão regular invalida")
            return
        self.regex.concatenate(newRegex)
        self.updateRegexDisplay()

    # Atualiza o display de regex
    def updateRegexDisplay(self):
        self.generation["text"] = str(self.regex)

    # Fecho de kleene na regex
    def kleeneWord(self, event):
        self.regex.kleene()
        self.updateRegexDisplay()

    # Limpar regex
    def cleanWord(self, event):
        self.regex.clear()
        self.updateRegexDisplay()

    # Salvar
    def file_save(self, event):
        f = asksaveasfilename(defaultextension=".er",
                              filetypes=[('Arquivos de Expressão Regular', '.er'), ('Todos os arquivos', '.*')])
        if not f:
            return
        self.regex.save(f)
        self.title["text"] = f.split('/')[-1]
        displayBox(self.master, "Salvo com sucesso em " + f)

    # Retornar ao menu anterior
    def returnTop(self, event):
        self.hide()
        self.topLevel.show()
