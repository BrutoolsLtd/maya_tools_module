""" User interface to automatically assign materials to meshes in current file.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys
import subprocess

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

class AssignMaterialCentralLibraryUI(QtWidgets.QDialog):
    """ UI to assign materials from central library automatically.
    """

    def __init__(self, parent=None):
        super(AssignMaterialCentralLibraryUI, self).__init__(parent=parent)

        self.setWindowTitle('Assign materials v1.0')
        self.setMinimumSize(300, 100)
        main_layout = QtWidgets.QVBoxLayout()

        self.setLayout(main_layout)

        library_info_layout = QtWidgets.QHBoxLayout()
        text_info_layout = QtWidgets.QVBoxLayout()
        self.info_label = QtWidgets.QLabel('')
        self.info_label_path = QtWidgets.QLabel('')
        self.info_label_help = QtWidgets.QLabel('')

        text_info_layout.addWidget(self.info_label)
        text_info_layout.addWidget(self.info_label_path)
        text_info_layout.addWidget(self.info_label_help)

        self.change_library_button = QtWidgets.QPushButton('Change library directory')

        library_info_layout.addLayout(text_info_layout)
        library_info_layout.addWidget(self.change_library_button)

        main_layout.addLayout(library_info_layout)

        self.char_LineEdit = QtWidgets.QLineEdit()
        self.char_LineEdit.setPlaceholderText('New assetTypeName to re-target maps')

        main_layout.addWidget(self.char_LineEdit)

        self.sourceimages_info_label = QtWidgets.QLabel('')

        main_layout.addWidget(self.sourceimages_info_label)

        ########################################################################
        # Create button group.
        ########################################################################
        self.assign_material_button = QtWidgets.QPushButton('Assign Materials')
        self.cancel_button = QtWidgets.QPushButton('Cancel')

        self.assign_button_box = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.assign_button_box.ButtonLayout(QtWidgets.QDialogButtonBox.WinLayout)

        self.assign_button_box.addButton(self.assign_material_button,
                                         QtWidgets.QDialogButtonBox.AcceptRole)
        self.assign_button_box.addButton(self.cancel_button,
                                         QtWidgets.QDialogButtonBox.RejectRole)

        main_layout.addWidget(self.assign_button_box)

        ########################################################################
        # Connect signals
        ########################################################################
        #self.assign_button_box.clicked.connect(self.close)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = AssignMaterialCentralLibraryUI()
    w.exec_()
