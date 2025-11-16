"""
Views package for ALA-GUI.

Contains all GUI components including windows, dialogs, and widgets.
"""

from views.auto_annotate_dialog import AutoAnnotateDialog
from views.class_list_widget import ClassListWidget
from views.file_list_widget import FileListWidget
from views.image_canvas import ImageCanvas
from views.main_window import MainWindow
from views.settings_dialog import SettingsDialog

__all__ = [
    "AutoAnnotateDialog",
    "MainWindow",
    "ImageCanvas",
    "FileListWidget",
    "ClassListWidget",
    "SettingsDialog",
]
