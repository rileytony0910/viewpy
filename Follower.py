# -*- coding: utf-8 -*-
"""
Created on Fri May  6 20:43:10 2016

@author: Tony
"""
from tkinter import *

class Follower(object):

    def __init__(self, on_color="#fff", off_color='#000'):
        self.on_color = on_color
        self.off_color = off_color
        self.previous_item = None

    def hover(self, canvas, item, x, y):
        x1, y1, x2, y2 = canvas.bbox(item)
        if x1 <= x <= x2 and y1 <= y <= y2:
            return True
        return False

    def __call__(self, event):
        canvas = event.widget
        item = canvas.find_closest(event.x, event.y)
        hovering = self.hover(canvas, item, event.x, event.y)
        if (not hovering or item is not self.previous_item) and self.previous_item is not None:
            canvas.itemconfig(self.previous_item, fill=self.off_color)
        if hovering:
            canvas.itemconfig(item, fill=self.on_color)
        self.previous_item = item
