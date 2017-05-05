"""
Created on Sun May  8 22:09:05 2016

@author: Tony
"""
from tkinter import *
from color_scaler import ColorScaler

class MenuBar(object):
    def __init__(self, root, regions):
        self._regions = regions
        self.root = root
        self.menubar = Menu(root, tearoff=0)
        self.pop_menu = Menu(root, tearoff=0)
        # Setup seperate menu popout for color scaler.
        #self.color_scaler = ColorScaler(Toplevel())
        
    def main(self):
        self.build_menubar()
        #self.build_popupmenu()
        self.root.config(menu=self.menubar)
        return self.root

    def hello(self):
        print("Hello World")

    def popup(self,event):
        self.pop_menu.post(event.x_root, event.y_root)
        
    def build_menubar(self):
       # Build the file menu cascade
        filemenu = Menu(self.menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.hello)
        filemenu.add_command(label='Save', command=self.hello)
        filemenu.add_separator()
        filemenu.add_command(label='Exit', command=self.onExit)
        self.menubar.add_cascade(label="File", menu=filemenu)
        
        # Build the Edits menu cascade
        editmenu = Menu(self.menubar, tearoff=0)
        editmenu.add_command(label="Cut", command=self.hello)
        editmenu.add_command(label="Copy", command=self.hello)
        self.menubar.add_cascade(label="Edit", menu=editmenu)
        # Build the Color Menu cascade
        colormenu = Menu(self.menubar, tearoff=0)
        colormenu.add_command(label='Set Color Scale', command=self.color_scale)
        self.menubar.add_cascade(label='Color Menu', menu=colormenu)
        # Build the Help menu cascade
        helpmenu = Menu(self.menubar, tearoff=0)
        helpmenu.add_command(label="About", command=self.hello)
        self.menubar.add_cascade(label="Help", menu=helpmenu)
        
        
    def build_popupmenu(self, canvas):
        self.pop_menu.add_command(label='Undo', command=self.hello)
        self.pop_menu.add_command(label='Redo', command=self.hello)
        canvas.bind("<Button-3>", self.popup)

    def color_scale(self):
        top = Toplevel(self.root)
        cs = ColorScaler(top, self._regions)
        cs.main()

    def onExit(self):
        self.quit()
