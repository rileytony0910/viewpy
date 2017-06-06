"""
Created on Sun May  8 22:09:05 2016

@author: Tony
"""
from tkinter import *

class MenuBar(object):
    def __init__(self, root):
        self.root = root
        self.menubar = Menu(root, tearoff=0)
        self.pop_menu = Menu(root, tearoff=0)

    def add_all_menus(self):
        self.add_file_menu()
        self.add_edit_menu()
        self.add_help_menu()

        self.root.config(menu=self.menubar)
        #return self.root

    def hello(self):
        print("Hello World")

    def popup(self,event):
        self.pop_menu.post(event.x_root, event.y_root)
        
    def add_file_menu(self):
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.hello)
        filemenu.add_command(label='Save', command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.onExit)
        self.menubar.add_cascade(label="File", menu=filemenu)

    def add_edit_menu(self):
        # Build the Edits menu cascade
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=self.hello)
        editmenu.add_command(label="Copy", command=self.hello)
        self.menubar.add_cascade(label="Edit", menu=editmenu)

    def add_help_menu(self):
        # Build the Help menu cascade
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.hello)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        
        
    def build_popupmenu(self, canvas):
        self.pop_menu.add_command(label='Undo', command=self.hello)
        self.pop_menu.add_command(label='Redo', command=self.hello)
        canvas.bind("<Button-3>", self.popup)


    def onExit(self):
        self.quit()
