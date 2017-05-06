class Region(object):

    def __init__(self):
        self._coord_x = []
        self._coord_y = []
        self._plane = None
        self._fill_color = None
        self._name = None
        self._canvas_id = None
        self._data = {}
        self._outline_color = "black"
        self._outline_width = 3

    def __str__(self):
        return str(self.__class__) + ":" + str(self.__dict__)

    @property
    def coords_x(self):
        """
        Get the X coordinates of the region
        :return: 
        """
        return self._coord_x

    @coords_x.setter
    def coords_x(self, value):
        """
        X coordinates setter
        :param value: 
        :return: 
        """
        self._coord_x = value

    @property
    def coords_y(self):
        """
        Get the Y coordinates of the region
        :return: 
        """
        return self._coord_y

    @coords_y.setter
    def coords_y(self, value):
        """
        Y coordinate setter
        :param value: 
        :return: 
        """
        self._coord_y = value

    @property
    def plane(self):
        """
        Get the plane id 
        :return: 
        """
        return self._plane

    @plane.setter
    def plane(self, value):
        """
        Plane id setter
        :param value: 
        :return: 
        """
        self._plane = value

    @property
    def fill_color(self):
        """
        Getter for background fill color
        :return: 
        """
        return self._fill_color

    @fill_color.setter
    def fill_color(self, value):
        """
        Setter for background fill color
        :param value: 
        :return: 
        """
        self._fill_color = value

    @property
    def name(self):
        """
        Region name getter
        :return: 
        """
        return self._name

    @name.setter
    def name(self, value):
        """
        Region name setter
        :param value: 
        :return: 
        """
        self._name = value

    @property
    def canvas_id(self):
        """
        Region id getter
        :return: 
        """
        return self._canvas_id

    @canvas_id.setter
    def canvas_id(self, value):
        """
        Region id setter
        :param value: 
        :return: 
        """
        self._canvas_id = value

    @property
    def data(self):
        """
        Data value getter
        :return: 
        """
        return self._data

    def add_dataset(self, key, val):
        """
        
        :param key: str Dataset name
        :param val: float -Value of dataset for the region
        :return: 
        """

        self.data[key] = val

    @property
    def outline_width(self):
        """
        Outline width getter
        :return: 
        """
        return self._outline_width

    @outline_width.setter
    def outline_width(self, value):
        """
        Outline width setter
        :param value: 
        :return: 
        """
        self._outline_width = value

    @property
    def outline_color(self):
        """
        Outline color getter
        :return: 
        """
        return self._outline_color

    @outline_color.setter
    def  outline_color(self, value):
        """
        Outline color setter
        :param value: 
        :return: 
        """
        self._outline_color = value

    @property
    def figure(self):
        """
        Get the x and y values of a region. 
        :return: List of x y pairs that make up the region definition. 
        Point are listed as [x1, y1, x2, y2, ...]
        """
        x = self.coords_x
        y = self.coords_y
        list = []
        for pair in zip(x,y):
            for val in pair:
                list.append(val)
        return list

class Regions(object):
    def __init__(self):
        self._regions = []
        self._region_map = {}
        self._num_regions = None
        self._dsets = []
        self._current_dset = None
        self._minmax = {}

    def __getitem__(self, item):
        index = item
        if isinstance(item, str):
            index = self._region_map[item]
        return self._regions[index]

    def __iter__(self):
        for region in self._regions:
            yield region

    def __len__(self):
        return len(self._regions)

    @property
    def regions(self):
        """
        The list of region objects
        :return: List of Region objects
        """
        return self._regions

    @property
    def minmax(self):
        """
        Get the min/max values for each dataset (not including the region id) organized as {key : [min, max]}
        :return: dict
        """
        return self._minmax

    @property
    def num_regions(self):
        """
        Number of Regions in the Region list
        :return: 
        """
        return len(self._regions)

    @property
    def current_dset(self):
        """
        The current dataset 
        :return: 
        """
        return self._current_dset

    @current_dset.setter
    def current_dset(self, value):
        """
        Setter for current dataset
        :param value: 
        :return: 
        """
        self._current_dset = value

    @property
    def datasets(self):
        """
        List of available datasets
        :return: 
        """
        self._get_all_dsets()
        return self._dsets

    def _get_all_dsets(self):
        """
        Private method to get the current datasets in the regions
        :return: 
        """
        keys = self._regions[-1].data.keys()
        for key in keys:
            if key not in self._dsets:
                self._dsets.append(key)

    def add_region(self, name=None, region=None):
        """
        
        :param region: Region Class object to be added to the list
        :return: 
        """
        # Append the new region data
        if region is not None and name is None:
            reg = region

        elif name is not None and region is None:
            reg = Region()
            reg.name = name
            reg.id = len(self._regions)
            reg.add_dataset('region id', len(self._regions))
        else:
            print("I'm confused you want assign a name to an already created Region? Why would you do this?")

        self._regions.append(reg)
        self._region_map[reg.name] = len(self._regions) - 1

        # As a region is added check if it had datasets not already included
        self._get_all_dsets()

    def add_dataset(self, data, name=None, region=None,):
        """
        Add a dataset to an existing region object
        :param region: Region object to add the dataset to
        :param name: The name of the dataset
        :param value: The value to be added
        :return: 
        """
        print('adding the dataset')
        if region is None:
            # For each dataset included:
            # Loop through each part included in the dataset and
            # index the region list by the region name via the map to list index position
            # Then apply the data value to the region object for each part from the cfig.
            print('Adding the dictionary of data')
            for key in data.keys():
                for part in data[key]:
                    # index region list based on region name in dataset
                    # TODO: How to handle time dependence ability?
                    value = data[key][part]
                    self._regions[self._region_map[part]].add_dataset(key, value)
                    self._check_maxmin_val(key, value)

        else:
            region.add_dataset(name, data)
            self._check_maxmin_val(name, data)

    def _check_maxmin_val(self, name, value):
        """
        Update the global max/min dictionary with value if it is outside the current max/min values
        :param name: str Dataset name
        :param value: float
        :return: 
        """
        # As data is added build a min and max dict for each dset for color mapping later
        if name not in self._minmax.keys():
            # First time key has been added to dict so set max and min both to it. {min, max]
            self._minmax[name] = [value, value]

        else:
            if value > self._minmax[name][1] :
                self._minmax[name][1] = value
            if value < self._minmax[name][0]:
                self._minmax[name][0] = value


