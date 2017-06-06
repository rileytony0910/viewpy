import io
from tkinter import *
from tkinter import ttk
from colour import Color
from menubar import MenuBar
from color_scaler import ColorScaler
from PIL import Image


class Display(object):

    def __init__(self, regions):
        self.regions = regions
        self.root = Tk()
        # FullScreen_Window(self._root)

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

class CanvasDrawing(object):
    def __init__(self, canvas, regions):
        self.canvas = canvas
        self.regions = regions
        self.canvas.pack(side='top', fill='both')
        self.canvas.configure(scrollregion=(-400, -400, 400, 400))

    def setup(self):
        """ Setup the GUI basics
    
        """
        #
        # Default color range

        default_fills = list(Color('red').range_to(Color("blue"), len(self.regions)))
        self.set_fill_color(default_fills)


        # Add the cfig shapes to the canvas
        self.draw(self.canvas)
        # canvas.create_rectangle(-10,-10, 10, 10, fill='black')
        #canvas.grid(column=0, row=0, rowspan=3, sticky=(E, W, N, S))

        # canvas.bind("<Motion>", Follower())

    def draw(self, canvas):
        """
        Draw the shapes to be included in the canvas
        :param canvas: 
        :return: 
        """
        for region in self.regions:
            region.canvas_id = canvas.create_polygon(region.figure, fill=region.fill_color,
                                                     activeoutline=region.outline_color, width=region.outline_width)

    def set_fill_color(self, colors):
        """
        Set the fill color of all regions
        :param colors: List of color names to be applied to all regions
        :return: 
        """
        for region in self.regions:
            region.fill_color = colors[region.id]


class Layout(Display):
    def __init__(self, regions):
        Display.__init__(self, regions)
        self.root.title("ViewPY: A Data Viewing Program")

        self.menubar = MenuBar(self.root)
        self.mainframe = ttk.Frame(self.root, padding='5 5 5 5')
        self.mainframe.pack()
        self.canvas = Canvas(self.mainframe, width=800, height=800, background='white')
        self.draw = CanvasDrawing(self.canvas, self.regions)

    def set_layout(self):
        self.menubar.add_all_menus()
        self.menubar.build_popupmenu(self.canvas)
        self.draw.setup()
        self.canvas.grid(column=0, row=0, rowspan=8, sticky=(E, W, N, S))
        close = ttk.Button(self.mainframe, text='Quit', command=self.close_window)
        scale = ttk.Button(self.mainframe, text='Set color scale', command=self.color_scaler)
        vict = ttk.Label(self.mainframe, text='You did it')
        close.grid(column=1, row=0, sticky=(E,W))
        scale.grid(column=1, row=1, sticky=(E,W))
        vict.grid(column=1, row=2, sticky=(E, W))

        self.root.mainloop()

    def color_scaler(self):
        top = Toplevel(self.root)
        cs = ColorScaler(top, self.regions, self.draw)
        cs.main()

    def close_window(self):
        self.root.destroy()

    def save(self):
        # This is all just untested code at the moment
        ps = self.canvas.postscript(colormode='color')
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