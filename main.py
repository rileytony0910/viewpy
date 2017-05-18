import sys
from tkinter import *
from tkinter import ttk

import h5py
from region import Regions
from display import Display


# class MenuBar(Frame):
#    def __init(self, parent):
#        Frame.__init__(self,parent)
#        
#        self.parent = parent
#        self.initUI()
#        
#    def initUI(self):
#        self.parent.title("Simple Menu")
#        
#        menubar = Menu(self.parent)
#        self.parent.config(menu=menubar)
#        
#        fileMenu = Menu(menubar)
#        fileMenu.add_command(label="Exit", command=self.onExit)
#        menubar.add_cascade(label='File', menu=fileMenu)
#        
#    def onExit(self):
#        self.quit()

REGION_LIST = Regions()
REGION_LIST.current_dset = 'fission'

def main():

    read_geometry_file('boxes.cfig')
    read_datafile('data.txt')
    #sys.exit()
    # For Debug
    #print_region_list()

    Display(REGION_LIST).setup()


def print_region_list():
    """
    Print all Region objects
    :param list: List of Region objects
    """
    for region in REGION_LIST:
        print(region)
    print ("The number of regions: {}".format(len(REGION_LIST)))
    #print (REGION_LIST['RX61'])
    #print (REGION_LIST[30])

def read_geometry_file(filename):
    """
    Create display regions from the definitions provided in the .cfig file
    :str filename: path to cfig
    :return: list of Region objects
    """
    scale_factor = 10
    file = open(filename).readlines()
    flag = False
    total_region_pts = 0
    # read each line in the cfig file
    prev = 0
    for line in file:
        splits = line.split()
        # For each part not named OBOUND create a new region object
        if len(splits) == 2 and not splits[0].startswith('OBO'):
            flag = True
            name = splits[0]
            REGION_LIST.add_region(name)
            total_region_pts = int(splits[1])
            prev = 0
            pt_list = []
            continue
        if flag:
            for i in range(len(splits)):
                pt_list.append(float(splits[i]) * scale_factor)
            prev = prev + len(splits)
            # If the total point read in is less than the total points defined for the region, then continue reading
            # the next line until the total points for the region is reached.
            if total_region_pts > len(splits):
                continue
            else:
                # extract the x and y values from list of total points
                if len(pt_list[::2]) is not len(pt_list[1::2]):
                    print('ERROR: Incompatible number of x ({}) and y ({}) values read'.format(len(pt_list[::2]),
                                                                                               len(pt_list[1::2])))
                # Assign X and Y coordinates to the region object
                REGION_LIST[name].coords_x = pt_list[::2]
                REGION_LIST[name].coords_y = pt_list[1::2]
                flag = False
                continue

def read_datafile(filename, ftype='ascii'):
    if ftype is 'hdf5':
        read_h5_data(filename)
    elif ftype is 'ascii':
        read_ascii_data(filename)
    else:
        print('Unsupported file type: ' + ftype)

def read_h5_data(filename):
    h5f = h5py.File(filename , 'r')
    regions = h5f['region_names']
    for dset in h5f['datasets'].keys():
        data = h5f['datasets/' + dset].value
        for index, region in enumerate(regions):
            REGION_LIST[region].add_dataset(dset, data[index])
    h5f.close()

def read_ascii_data(filename):

    file = open(filename, 'r').readlines()
    flag = False
    data = {}
    for line in file:
        if line.startswith('#'):
            continue

        if '<Dataset>' in line:
            flag = True
            dset_name = line.split()[1]
            regions = {}
            values = []
            continue
        splits = line.split()
        size = len(splits)
        if flag and size > 1:

            if splits[0] in regions.keys():
                print("Warning: Region repeated in data assignment")
                print(splits[0] + " already in region list")
            else:
                values = []
                for i in range(1, size):
                    values.append(splits[i])
                regions[(splits[0])] = values

        if '<End>' in line:
            data[dset_name] = regions
            flag = False
    REGION_LIST.add_dataset(data)

    return

if __name__ == '__main__':
    main()
