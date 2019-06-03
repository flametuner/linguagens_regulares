from tkinter import *

class Hideble:
	def __init__(self, master=None):
		self.frame = Frame(master)
		
	def show(self):
		self.frame.pack()
	
	def hide(self):
		self.frame.pack_forget()

def createConfimationBox(master, command, text):
	window = Toplevel(master)
	container = Frame(window)
	container.pack()
	container2 = Frame(window)
	container2.pack()
	nomeLabel = Label(container,text=text, font="Roboto")
	nomeLabel.pack()
	
	adicionar = Button(container2)
	adicionar["text"] = "Ok"
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
	
def displayBox(master, string):
	window = Toplevel(master)
	container = Frame(window)
	container.pack()
	nomeLabel = Label(container,text=string, font="Roboto")
	nomeLabel.pack()
	ok = Button(container)
	ok["text"] = "Ok"
	ok["font"] = ("Roboto", "10")
	ok["width"] = 20
	ok["command"] = window.destroy
	ok.pack()

def character_limit(entry_text):
    if len(entry_text.get()) > 0:
        entry_text.set(entry_text.get()[-1])
