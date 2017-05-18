# -*- coding: utf-8 -*-
"""
Created on Fri May 13 23:23:20 2016

@author: Tony
"""
import numpy as np
from tkinter import *
from tkinter import ttk
from colour import Color
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfilename


class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height
        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)

        self.scale('all', 0, 0, wscale, hscale)


class ButtonGroup():
    def __init__(self, parent):
        self._parent = parent
        self._label = None
        self._max = None
        self._min = None

    def add_buttons(self, index, extent=None):
        # Make color selection button
        if extent is not None:
            min = extent[0]
            max = extent[1]
        else:
            min = ''
            max = ''

        button = ttk.Button(self._parent, text="Choose Color",
                            command=self.choose_color)
        button.grid(column=0, row=index + 5, sticky=(N, S))
        # Display the selected color on a background label
        # label = ttk.Label(self.parent, textvariable=self.color[index])
        self._label = ttk.Label(self._parent, width=7)
        self._label.grid(column=1, row=index + 5, sticky=(N, S, E, W))
        # Empty label to add space in row
        ttk.Label(self._parent, width=3).grid(column=2, row=index + 4)
        # Create Entry for Min value
        self._min = StringVar(self._parent, value=min)
        min_ent = ttk.Entry(self._parent, width=5, textvariable=self._min)
        min_ent.grid(column=4, row=index + 5)
        # Empty label to add space in row
        # ttk.Label(parent, width=1).grid(column=4, row=index)
        # Create Entry for Max value
        self._max = StringVar(self._parent, value=max)
        max_ent = ttk.Entry(self._parent, width=5, textvariable=self._max)
        max_ent.grid(column=5, row=index + 5)  # , sticky=(N,S))

    @property
    def label(self):
        return self._label

    @property
    def max(self):
        return self._max

    @property
    def min(self):
        return self._min

    def get_color(self, type='str'):
        if type is 'object':
            return Color(str(self.label['background']))
        elif type is 'rgb':
            return Color(str(self.label['background'])).rgb
        else:
            return str(self.label['background'])

    def choose_color(self):
        """Update the color based upon the user input

        """
        #
        result = askcolor(color='red', title="Choose Color")
        self.label.configure(background=result[1])

class ColorScaler(object):
    """Creates an ColorScaler object that creates a gradient between three
        selected colors.
    
    """

    def __init__(self, root, regions):
        """Initializes the ColorScaler object.
        Args:
            root (object): The Tk Toplevel object
            regions(object): The Regions object (list of Region objects added to canvas)
        
        """
        # Setup the TK object and the Tk Frame
        self._root = root
        self._regions = regions
        self._root.title('Create a Color Scale')
        self._parent = ttk.Frame(self._root, padding='5 5 5')
        self._parent.grid(row=0, column=0, sticky=(N, S, E, W))
        # Setup the global variables used throughout the class
        self._help = None
        self._color = []
        self._label_list = []
        self._maxs = []
        self._mins = []
        self._range = []
        self._gradient = []

        self._parent.grid_columnconfigure(0, weight=1)
        self._parent.grid_rowconfigure(0, weight=1)


    def main(self):

        """ Need to add a canvas that shows gradient between
        two selection colors. the default colors will be red and blue.
        Save this scale for use later. Add feature to determine how many 
        colors to add to scale and how many discrete boxes to make. 
        Associate this with a user supplied scale screen that has a 
        color box on the left and a max and min entry for that color bin. 
        Arrange from first color at top with max +inf and link min 
        value with the next lower range's max value. last min is -inf
        """
        self._gradient.append(ttk.Label(self._parent, width=5, background='red'))
        self._gradient[0].grid(column=2, row=0, columnspan=2)
        ttk.Button(self._parent, text='Range from',
                   command=lambda: set_color(
                       self._gradient[0])).grid(column=1, row=0)
        self._gradient.append(ttk.Label(self._parent, width=5,
                                        background=Color('white')))
        self._gradient[1].grid(column=2, row=1, columnspan=2)
        ttk.Button(self._parent, text='to',
                   command=lambda: set_color(self._gradient[1])
                   ).grid(column=1, row=1)
        self._gradient.append(ttk.Label(self._parent, width=5,
                                        background=Color('blue')))
        self._gradient[2].grid(column=2, row=3, columnspan=2)
        ttk.Button(self._parent, text='End with',
                   command=lambda: set_color(self._gradient[2])
                   ).grid(column=1, row=3)

        ttk.Button(self._parent, text='Apply Gradient',
                   command=self.apply_gradient).grid(column=0,
                                                     row=4, sticky=(N, S, E, W))
        ttk.Label(self._parent, text='Min').grid(row=4, column=4, sticky=(E, W))
        ttk.Label(self._parent, text='Max').grid(row=4, column=5, sticky=(E, W))
        ten_pct_scale = [1e20, 1.1, 1.08, 1.06, 1.04, 1.02, 1.01, 0.99, 0.98, 0.96, 0.94, 0.92, 0.9, 1e-20]

        scale_range = set_scale_values(ten_pct_scale)
        for i in range(13):
            bg = ButtonGroup(self._parent)
            bg.add_buttons(i, scale_range[i])
            self._label_list.append(bg)
            del bg
        ttk.Button(self._parent, text='Apply', command=self.get_scale).grid(
            column=0, row=18)
        ttk.Button(self._parent, text='Save to File',
                   command=self.save).grid(column=4,
                                           row=18, columnspan=2, sticky=(E, W))
        ttk.Button(self._parent, text='Cancel',
                   command=self.close_window).grid(column=4,
                                                   row=19, columnspan=2, sticky=(E, W))

        self._root.grid_columnconfigure(0, weight=1)
        self._root.grid_rowconfigure(0, weight=1)
        self._root.resizable(True, True)

    #        canvas = Canvas(self.parent, width=50,height=500)
    #        for i in range(10):
    #            canvas.create_rectangle(0, i*50, 50, (i+1)*50,
    #                                    fill=self.RGB_colors[1][1])
    #        canvas.grid(column=3, row=0, rowspan=10)
    #        canvas.addtag_all('all')


    def close_window(self):
        self._root.destroy()

    def get_scale(self):

        # Get the active data set

        key = self._regions.current_dset
        print(key)
        print(self._regions.minmax)
        extremes = self._regions.minmax[key]
        print(extremes)
        min = extremes[0]
        max = extremes[1]

        for region in self._regions:
            val = region.data[key]
            val = float(val[0])
            print(self._maxs)
            for index, list in enumerate(self._maxs):
                min = list[0]
                max = list[1]
                print(min, max)
                print(val)
                if max > val > min:
                    region.fill_color = self._label_list[index].get_color()
                    break
        print(self._root.winfo_children())
        for widget in self._root.winfo_children():
            print("Im the widget")
            print(widget.winfo_children())
            if isinstance(widget, Canvas):
                for region in self._regions:
                    region.canvas_id = widget.create_polygon(region.figure, fill=region.fill_color,
                                                             activeoutline=region.outline_color,
                                                             width=region.outline_width)

    def get_bgc(self, label):
        if label is not None:
            color = str(label['background'])
        else:
            color = 'red'
        return color

    def save(self):
        # Call filedialog box to select the save file location and name
        filepath = asksaveasfilename(defaultextension='.nvcolors',
                                     filetypes=[("Color file", "*.nvcolors"),
                                                ("All files", "*.*")])
        print("File saved to : " + filepath)
        # open a file object to write data to
        file = open(filepath, 'w')
        file.write("Custom Color Map\n")
        # get the color of the widget and the associated values of the 
        # entry widgets next to it
        # Get current color value for each button and convert from hex to rgb

        for label in self._label_list:
            scaled = []
            rgb = label.get_color(type='rgb')
            for i in range(3):
                # scale rgb value from 0 to 1.0 to 0 to 255
                # append each value in the tuple to a list since tuples can't
                # do math on each element
                scaled.append(rgb[i] * 255.0)
            file.write('{0[0]:.2f}, {0[1]:.2f}, {0[2]:.2f}'.format(scaled) +
                       ' {0}, {1} \n'.format(label.min, label.max))
        # close file
        file.close()

    def make_buttons(self, index):
        # Make color selection button
        button = ttk.Button(self._parent, text="Choose Color",
                            command=lambda: self.choose_color(index))
        button.grid(column=0, row=index + 5, sticky=(N, S))
        # Display the selected color on a background label
        # label = ttk.Label(self.parent, textvariable=self.color[index])
        label = ttk.Label(self._parent, width=7)
        label.grid(column=1, row=index + 5, sticky=(N, S, E, W))
        # Empty label to add space in row
        ttk.Label(self._parent, width=3).grid(column=2, row=index + 4)
        # Create Entry for Min value
        array = []
        array.append(StringVar())
        min_ent = ttk.Entry(self._parent, width=5, textvariable=self._maxs[index][0])
        min_ent.grid(column=4, row=index + 5)
        # Empty label to add space in row
        # ttk.Label(parent, width=1).grid(column=4, row=index)
        # Create Entry for Max value
        array.append(StringVar())
        self._maxs.append(array)
        max_ent = ttk.Entry(self._parent, width=5, textvariable=self._maxs[index][1])
        max_ent.grid(column=5, row=index + 5)  # , sticky=(N,S))

        return button, label, min_ent, max_ent

    def apply_gradient(self):

        # color range is a list of colors to make a gradient with
        # ordered as [top, middle, bottom]. Gradient is top to middle and 
        # middle to bottom
        # TODO: Add three checkboxes to select the three colors to make a
        # a gradient, use red,white,blue as default values at first.
        print(len(self._label_list))
        print(self._label_list)
        num_butons = len(self._label_list)
        color_range = []
        for label in self._gradient:
            color_range.append(Color(self.get_bgc(label)))
        # The middle index is the total number of buttons minus the top,
        # bottom and middle button itself
        flag = False
        middle = None
        if num_butons > 3:
            flag = True
            middle = (num_butons - 3) / 2

        if flag:
            # TODO: add flag to only apply defaults if the bg hasn't been set yet
            self._label_list[0].label.configure(background=Color('magenta'))
            self._label_list[-1].label.configure(background=Color('purple'))
            if middle.is_integer():
                middle = int(middle)
                c_tops = list(color_range[0].range_to(color_range[1],
                                                      middle + 1))
                c_bots = list(color_range[1].range_to(color_range[2],
                                                      middle + 1))

                for i in range(middle):
                    self._label_list[i + 1].label.configure(background=c_tops[i])
                    self._label_list[middle + 1].label.configure(
                        background=color_range[1])

                    self._label_list[middle + i + 2].label.configure(
                        background=c_bots[i + 1])
            else:
                print("Error number of colors in gradient can't be divided evenly")
                sys.exit()

def set_color(label):
    result = askcolor('red', title='Choose Color')
    label.configure(background=result[1])

def set_scale_values(array):
    """ This method sets the values used by the scale

    """

    def_low = array[1::]
    def_high = array[0:-1]
    new_range = []
    for low, high in zip(def_low, def_high):

        new_range.append([low, high])
    return new_range

def main():
     root = Tk()

     ColorScaler(root).main()

     root.mainloop()


if __name__ == '__main__':
     main()
