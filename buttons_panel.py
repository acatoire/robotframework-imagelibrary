from __future__ import absolute_import

from ImageLibrary.button import Button
from ImageLibrary import errors, utils

class ButtonsPanel(Button):
    '''You set the region, count of button and have several buttons that can be pressed!
        It is deprecated, use multiple_buttons instead

        yaml:
        buttons_panels:
            cards:
                #position of whole button panel block
                position:   [529, 400, 380, 128]
                #count of buttons in panel
                count:      4
                #optional: distance between buttons (0 by default)
                padding:    13
                #optional: direction (horizontal by default)
                direction:  horizontal
    '''
    def __init__(self, name, config):
        super(ButtonsPanel, self).__init__(name)
        info = config

        self.buttons = []
        if "direction" not in info or info["direction"] == "horizontal":
            direction = 0
        elif info["direction"] == "vertical":
            direction = 1
        elif info["direction"] == "matrix":
            direction = 2
        else:
            raise errors.ConfigError("Unknown direction, only horizontal and vertical are supported, {} recieved".format(info["direction"]))

        padding = info["padding"] if "padding" in info else 0
        position = info["position"]
        assert len(position) == 4, "Position must be in form: [l t w h]"

        if direction == 2:
            assert "rows" in info and "columns" in info, "Both rows and columns must be in config when direction is matrix"

            rows = info["rows"]
            columns = info["columns"]
            width = (position[2] - (rows-1)*padding) / columns
            height = (position[3] - (columns-1)*padding) / rows

            l, t = position[:2]
            for row in xrange(rows):
                for column in xrange(columns):
                    self.buttons.append((l + column*(width+padding), t + row*(height+padding), width, height))

        else:
            if direction == 0:
                count = info["count"]
                width = (info["position"][2] - (count-1)*padding) / count
                height = info["position"][3]
    
            elif direction == 1:
                count = info["count"]
                width = info["position"][2]
                height = (info["position"][3] - (count-1)*padding) / count
    
            x, y = info["position"][:2]
            for index in xrange(count):
                self.buttons.append((x, y, width, height))
                if direction == 0:
                    x += width + padding
                else:
                    y += height + padding

    @utils.add_error_info
    def press_button(self, index, times):
        index = int(index)
        assert index != -1, "Index is not set".format(self.name)
        assert index > 0, "Index must by more that zero"
        assert index <= len(self.buttons), "Index must be less then elements count"
        self.click_center(self.buttons[index-1], times)
