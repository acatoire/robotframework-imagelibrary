import inspect
import os.path
import sys
import traceback

from PIL import Image, ImageDraw, ImageFont
from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileSystemModel, QFileDialog

from area import Area, MasterScreen


def excepthook(exc_type, exc_value, exc_tb):
    print("".join(traceback.format_exception(exc_type, exc_value, exc_tb)))
    QtWidgets.QApplication.quit()


class ZoneChecker:
    """
    Class ZoneChecker
    """

    COLORS_LIST = [
        "aqua", "red", "blue", "blueviolet", "brown",
        "chartreuse", "orange", "yellow", "silver", "fuchsia",
        "goldenrod", "green", "palegreen", "peachpuff", "rosybrown",
        "white",
        "aqua", "red", "blue", "blueviolet", "brown",
        "chartreuse", "orange", "yellow", "silver", "fuchsia",
        "goldenrod", "green", "palegreen", "peachpuff", "rosybrown",
        "white",
        "aqua", "red", "blue", "blueviolet", "brown",
        "chartreuse", "orange", "yellow", "silver", "fuchsia",
        "goldenrod", "green", "palegreen", "peachpuff", "rosybrown",
        "white",
                   ]
    RECT_WIDTH = 2
    FONT_SIZE = 12
    CAPTION_ZONE_L = 150

    def __init__(self):
        self._img_path = None
        self._width = None
        self._height = None

        self._masterscreen = MasterScreen()

    @property
    def masterscreen(self):
        return self._masterscreen

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def load_image(self, img_path):
        self._img_path = img_path

        image = Image.open(img_path).convert("RGB")

        self._width = image.size[0]
        self._height = image.size[1]

        return image

    def draw_single_zone(self, zone):
        # Load image
        image = self.load_image(self._img_path)
        result_image = Image.new('RGB', (self.width, self.height), 'white')

        if issubclass(type(zone), Area):
            img_draw = ImageDraw.Draw(image)
            img_draw.rectangle((zone.x, zone.y, zone.x + zone.width, zone.y + zone.height), outline='red')

        result_image.paste(image)
        return result_image

    def draw_multiple_zones(self, zones):
        # Load image
        image = self.load_image(self._img_path)
        result_image = Image.new('RGB', (self.width, self.height), 'white')

        for zone in zones:
            if issubclass(type(zone), Area):
                img_draw = ImageDraw.Draw(image)
                img_draw.rectangle((zone.x, zone.y, zone.x + zone.width, zone.y + zone.height), outline='red')

        result_image.paste(image)
        return result_image

    def draw_all_zones(self):
        # Load image
        image = self.load_image(self._img_path)
        zones = self._masterscreen.table

        if len(zones) == 0:
            return image

        final_pict_l = self.width + self.CAPTION_ZONE_L
        result_image = Image.new('RGB', (final_pict_l, self.height), 'white')
        caption_h = round(self.height / len(zones))
        print(f"Caption high will be {caption_h} because there is {len(zones)} zones")

        for i, area in enumerate(zones):
            img_draw = ImageDraw.Draw(image)
            img_draw.rectangle((area.x, area.y, area.x + area.width, area.y + area.height),
                               outline=self.COLORS_LIST[i],
                               width=self.RECT_WIDTH)

            img_draw = ImageDraw.Draw(result_image)
            img_draw.rectangle((self.width, i * caption_h, final_pict_l, i * caption_h + caption_h),
                               fill=self.COLORS_LIST[i])

            font = ImageFont.truetype("arial.ttf", self.FONT_SIZE)
            img_draw.text((self.width + 10, i * caption_h), f"{i}: {area.name}",
                          fill='black',
                          font=font)

            print(f"Zone {i}({self.COLORS_LIST[i]}): {area}")

        result_image.paste(image)
        return result_image


def refresh_method(func):
    """
    Useful decorator to check mandatory elements before refreshing display
    """
    def wrapped_func(*args, **kwargs):
        """
        Decorated function
        """
        self = args[0]
        if self.checker and self.img_path:
            return func(*args, **kwargs)
        else:
            return None

    # Return the decorated function
    return wrapped_func


class ZoneCheckerGui(QMainWindow):
    """
    Class ZoneCheckerGui
    """

    ALL_ZONES = "All"   # Text displayed in zones list

    def __init__(self):
        """
        Constructor
        """
        super().__init__()

        # Init instance attribute
        self._checker = ZoneChecker()
        self._img_path = None
        self._cfg_path = None

        # Configure UI
        self.model = QFileSystemModel()
        uic.loadUi('./zone_checker.ui', self)
        self.folder = None
        self.setCentralWidget(self.central_widget)
        self.showMaximized()

        # SIGNALS/SLOTS MAPPING
        # Menu bar events
        self.actionOpen.triggered.connect(self.open_image_file_dialog)
        self.actionOpenConfig.triggered.connect(self.open_config_file_dialog)
        self.action_copy_to_clipboard.triggered.connect(self.copy_to_clipboard)
        # Masterscreens / areas events
        self.zones_list_widget.itemSelectionChanged.connect(self.zone_clicked)
        # X/Y mouse position events
        self.output_view.mouseMoveEvent = self.get_mouse_position
        # Draw events
        self.height_spinbox.valueChanged.connect(self.draw_area)
        self.width_spinbox.valueChanged.connect(self.draw_area)
        self.x_spinbox.valueChanged.connect(self.draw_area)
        self.y_spinbox.valueChanged.connect(self.draw_area)

    @property
    def img_path(self):
        return self._img_path

    @property
    def cfg_path(self):
        return self._cfg_path

    @property
    def checker(self):
        return self._checker

    @property
    def selected_zone(self) -> Area or None:
        """
        Methods used to return selected zone
        :return Area instance if an element different from 'All' has been selected otherwise None
        """
        masterscreen = self._checker.masterscreen
        selected_item = self.zones_list_widget.selectedItems()

        if masterscreen and selected_item:
            # A masterscreen and a zone has been selected
            # Get selected zone name
            zone_name = selected_item[0].text()
            if zone_name and zone_name != self.ALL_ZONES:
                # Zone name exist and is different from All element
                # Iterate zones
                for area in masterscreen.table:
                    if area.name == zone_name:
                        # Zone has been found (name is equals to the selected zone)
                        return area

        # No zone selected or All element
        return None

    def open_image_file_dialog(self) -> None:
        """
        Method used to open an image file (it displays a QFileDialog)
        """
        # Display QFileDialog
        self._img_path = QFileDialog.getOpenFileName(
            None, "Select a file...", "", filter="Image Files (*.png *.jpg *.bmp)")[0]

        if self._img_path and os.path.exists(self._img_path) and os.path.isfile(self._img_path):
            # File selected is an image file

            # Update image in zone checker
            self._checker.load_image(self._img_path)
            # Update preview
            self.refresh()

    def open_config_file_dialog(self) -> None:
        """
        Method used to open a config file (it displays a QFileDialog)
        """
        # Display QFileDialog
        self._cfg_path = QFileDialog.getOpenFileName(
            None, "Select a file...", "", filter="Image Files (*.yaml)")[0]

        if self._cfg_path and os.path.exists(self._cfg_path) and os.path.isfile(self._cfg_path):
            # Update
            self._checker.masterscreen.reload(self._cfg_path)
            self.setup_zone_list()

            # Update preview
            self.refresh()

    def copy_to_clipboard(self) -> None:
        """
        Method used to copy output image in clipboard
        """
        # Get image displayed in QLabel
        pixmap = self.output_view.pixmap()
        if pixmap:
            # QLabel doesn't contain image
            QApplication.clipboard().setImage(pixmap.toImage())

    def setup_zone_list(self) -> None:
        """
        Method used to refresh zones list
        """
        # Remove existing elements
        self.zones_list_widget.clear()
        # Add 'All' item
        self.zones_list_widget.addItem(self.ALL_ZONES)

        # Get zones list
        zones = self._checker.masterscreen.table
        # Add all zones in widget
        for zone in zones:
            self.zones_list_widget.addItem(zone.name)

    def zone_clicked(self) -> None:
        """
        Method used to handle click on zones list
        """
        self.refresh()

    def methods_clicked(self) -> None:
        """
        Method used to handle click on zones list
        """
        masterscreen = self._checker.masterscreen
        method_name = self.methods_combobox.currentText()

        if method_name and masterscreen and hasattr(masterscreen, method_name):
            # Get method object
            method = getattr(masterscreen, self.methods_combobox.currentText())

            # Get method parameters signature
            signature = str(inspect.signature(method))
            sig_param = signature[:signature.find(' ->')]

            # Refresh command line text widget
            self.command_line_text.setText(f"{self.methods_combobox.currentText()}{sig_param}")
            self.command_line_text.setToolTip(sig_param)

            # Refresh methods combobox widget
            self.methods_combobox.setToolTip(inspect.getdoc(method))
        else:
            self.methods_combobox.setToolTip("")
            self.command_line_text.setToolTip("")
            self.command_line_text.setText("")

    def get_mouse_position(self, event) -> None:
        """
        Method used to handle mouse move event on the preview image
        """
        # Get mouse position
        x = event.pos().x()
        y = event.pos().y()
        # Display position in status bar
        self.statusbar.showMessage(f"x = {x}, y = {y}")

    @refresh_method
    def refresh_raw_image(self) -> None:
        """
        Method used to refresh raw image display
        """
        pixmap = QPixmap(self._img_path)
        pixmap = pixmap.scaled(self.checker.width, self.checker.height,
                               Qt.KeepAspectRatio, Qt.FastTransformation)
        self.input_view.setPixmap(pixmap)

    @staticmethod
    def pil_to_qt(pil_img) -> QPixmap:
        """
        Method used to convert image from Pillow image to QPixmap
        :param pil_img: Instance of Pillow image
        """
        qt_image = ImageQt(pil_img)
        pixmap = QPixmap.fromImage(qt_image)
        pixmap.detach()
        return pixmap

    @refresh_method
    def refresh(self) -> None:
        """
        Method used to refresh raw image and preview image from selected zone in zone list
        """
        # Update raw image
        self.refresh_raw_image()

        # Get selected element in zone list
        zone = self.selected_zone
        if zone:
            # Zone element has been selected and is different from All
            img = self._checker.draw_single_zone(zone)
            # Update zone spinboxes using zone parameter elements
            self.update_zone_spinboxes(zone)
        else:
            # Zone element has not been selected or All selected
            img = self._checker.draw_all_zones()

        # Update preview image
        self.output_view.setPixmap(self.pil_to_qt(img))

    def update_zone_spinboxes(self, zone: Area) -> None:
        """
        Method used to copy zone values in spinboxes
        :param zone: Zone to copy in spinboxes
        """
        self.x_spinbox.setValue(zone.x)
        self.y_spinbox.setValue(zone.y)
        self.width_spinbox.setValue(zone.width)
        self.height_spinbox.setValue(zone.height)

    @refresh_method
    def draw_area(self, *args, **kwargs) -> None:
        """
        Method used to draw square from spinboxes values
        """
        # Construct Area from spinboxes values
        zone = Area(self.x_spinbox.value(), self.y_spinbox.value(),
                    self.width_spinbox.value(), self.height_spinbox.value(), "Custom area")
        # Draw square and update preview
        img = self._checker.draw_single_zone(zone)
        self.output_view.setPixmap(self.pil_to_qt(img))


def main():
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ZoneCheckerGui()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
