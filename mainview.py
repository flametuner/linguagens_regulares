# -*- coding: latin-1 -*-
from menus import *


# Menu principal
class MainView:
    def __init__(self, master=None):
        self.master = master
        self.master.winfo_toplevel().title("Linguagens Formais e Compiladores")
        self.mainmenu = Menu(master)
        self.famenu = FAMenu(master, self.mainmenu)
        self.rgmenu = RGMenu(master, self.mainmenu)
        self.regexmenu = RegexMenu(master, self.mainmenu)
        self.mainmenu.setFaMenu(self.famenu)
        self.mainmenu.setRgMenu(self.rgmenu)
        self.mainmenu.setRegexMenu(self.regexmenu)

        self.mainmenu.show()
