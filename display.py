import io
from tkinter import *
from tkinter import ttk
from colour import Color
from menubar import MenuBar
from PIL import Image


class Display(object):

    def __init__(self, regions):
        self._regions = regions
        self._root = Tk()
        # Extract the names of data available for displaying

        # Initialize to show the region id dataset first
        self._current_dset = 'region id'

    @property
    def current_dset(self):
        """
        Return the current dataset value
        :return: 
        """
        return self._current_dset

    @current_dset.setter
    def current_dset(self, value):
        """
        Current dataset setter
        :param value: 
        :return: 
        """
        self._current_dset = value

    def setup(self):
        """ Setup the GUI basics
    
        """
        #
        FullScreen_Window(self._root)
        self._root.title("ViewPY: A Data Viewing Program")
        # The dropdown menu setup
        menu = MenuBar(self._root, self._regions)
        self._root = menu.main()

        mainframe = ttk.Frame(self._root, padding='5 5 5 5')
        mainframe.pack()
        # mainframe.pack(column=0, row=0, sticky=(N,W,E,S))
        # root.grid_columnconfigure(0, weight=1)
        # root.grid_rowconfigure(0,weight=1)
        # Default color range

        default_fills = list(Color('red').range_to(Color("blue"), len(self._regions)))
        self.set_fill_color(default_fills)

        canvas = Canvas(mainframe, width=1500, height=2000, background='white')
        canvas.pack(side='top', fill='both')
        canvas.configure(scrollregion=(-400, -400, 400, 400))
        menu.build_popupmenu(canvas)
        # Add the cfig shapes to the canvas
        self.draw(canvas)
        # canvas.create_rectangle(-10,-10, 10, 10, fill='black')
        qbut = ttk.Button(mainframe, text='Quit', command=self.close_window)
        lbl = ttk.Label(mainframe, text='You did it')
        canvas.grid(column=0, row=0, rowspan=3, sticky=(E, W, N, S))
        qbut.grid(column=1, row=0, sticky=E)
        lbl.grid(column=1, row=1, sticky=W)
        mainframe.grid_columnconfigure(0, weight=1)
        mainframe.grid_rowconfigure(0, weight=1)

        # canvas.bind("<Motion>", Follower())

        self._root.mainloop()

    def draw(self, canvas):
        """
        Draw the shapes to be included in the canvas
        :param canvas: 
        :return: 
        """
        for region in self._regions:
            region.canvas_id = canvas.create_polygon(region.figure, fill=region.fill_color,
                                                     activeoutline=region.outline_color, width=region.outline_width)

    def close_window(self):
        self._root.destroy()

    def set_fill_color(self, colors):
        """
        Set the fill color of all regions
        :param colors: List of color names to be applied to all regions
        :return: 
        """
        for region in self._regions:
            region.fill_color = colors[region.id]

    def save(self, canvas):
        ps = canvas.postscript(colormode='color')
        img = Image.open(io.BytesIO(ps.encode('utf-8')))
        img.save("test.jpg")

class FullScreen_Window(object):
    def __init__(self, master, **kwargs):
        self.master = master
        self.master.state('zoomed')
        self.state = False
        pad = 3
        self._geom = '200x200+0+0'
        master.geometry("{0}x{1}+0+0".format(master.winfo_screenwidth() - pad,
                                             master.winfo_screenheight()- pad))
        master.bind('<F11>', self.toggle_full_screen)
        master.bind('<Escape>', self.end_full_screen)

    def toggle_full_screen(self, event=None):
        self.state = not self.state
        self.master.attributes('-fullscreen', self.state)
        return "break"

    def end_full_screen(self, event=None):
        self.state = False
        self.master.attributes('-fullscreen', False)
        return 'break'