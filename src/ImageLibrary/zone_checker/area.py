"""
area library
"""
import yaml


class Area:
    """
    Area
    Define a screen Area which is part of a Masterscreen
    """
    def __init__(self,
                 x: int, y: int, width: int, height: int, name: str):
        """
        Constructor
        :param x: area x coordinate
        :param y:  area x coordinate
        :param width:  area x coordinate
        :param height:  area x coordinate
        :param name:  area name
        """
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._name = name

    def __str__(self):
        return "{0} ({1},{2}) {3}x{4}".format(self.name,
                                              self.x, self.y,
                                              self.width, self.height)

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    @property
    def width(self) -> int:
        return self._width

    @property
    def height(self) -> int:
        return self._height

    @property
    def name(self) -> str:
        return self._name


class MasterScreen:
    """
    MasterScreen
    """

    def __init__(self):
        self._width = None
        self._height = None
        self._table = []

    def load(self, config_file_path):

        with open(config_file_path) as file:
            config = yaml.load(file.read(), Loader=yaml.FullLoader)

        for zone_name in config["main"]["zones"]:
            area = config["main"]["zones"][zone_name]
            self._table.append(Area(area[0], area[1], area[2], area[3],
                               zone_name))

        for zone_name in config["main"]["button_coord"]:
            area = config["main"]["button_coord"][zone_name]["position"]
            self._table.append(Area(area[0], area[1], area[2], area[3],
                                    zone_name))

    def reload(self, config_file_path):

        self._table = []
        self.load(config_file_path)

    @property
    def width(self) -> int:
        if not self._width:
            raise KeyError("Size should be setup first")

        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        if not self._height:
            raise KeyError("Size should be setup first")
        return self._height

    @height.setter
    def height(self, value: int):
        self._width = value

    @property
    def table(self) -> list[Area]:
        return self._table

    def __len__(self):
        return len(self._table)
