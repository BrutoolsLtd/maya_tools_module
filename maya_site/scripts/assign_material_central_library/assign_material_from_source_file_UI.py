""" User interface to select materials and assign to geometries.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

class AssignMaterialFromSourceFileUI(QtWidgets.QDialog):
    """ UI to assign material from a referenced file to current geometries.
    """

    def __init__(self, parent=None):
        super(AssignMaterialFromSourceFileUI, self).__init__(parent=parent)

        self.setWindowTitle('Assig material from file v1.0')
        self.setMinimumSize(350, 200)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ########################################################################
        # Create button to choose a file for materials.
        ########################################################################
        self.select_material_file = QtWidgets.QPushButton('Choose file with materials')

        main_layout.addWidget(self.select_material_file)

        ########################################################################
        # Create QtTreeWidget
        ########################################################################
        self.materials_table = QtWidgets.QListWidget()
        
        main_layout.addWidget(self.materials_table)

        ########################################################################
        # Source and Destination asset name widgets
        ########################################################################
        self.source_name = QtWidgets.QLineEdit()
        self.source_name.setPlaceholderText('Source asset name "Sugreev"')
        self.source_name.setToolTip(
"""This name is the one used in maps / images 
(eg. SugreevBump.1001.exr) in this example "Sugreev"
is the pattern to be replaced by destination asset name.
""" )

        self.destination_name = QtWidgets.QLineEdit()
        self.destination_name.setPlaceholderText('Destination asset name "Angad"')
        self.destination_name.setToolTip(
"""This name will replace the source asset name
(eg. from SugreevBump.1001.exr to AngadBump.1001.exr)
and will target the sourceimages folder of current project
to look for the destination file name.
""" )

        source_destination_layout = QtWidgets.QHBoxLayout()

        source_destination_layout.addWidget(self.source_name)
        source_destination_layout.addWidget(self.destination_name)

        main_layout.addLayout(source_destination_layout)

        ########################################################################
        # Connect signals
        ########################################################################
        self.sourceimages_info_label = QtWidgets.QLabel('Here will shown the label')
        main_layout.addWidget(self.sourceimages_info_label)

        ########################################################################
        # Create button group.
        ########################################################################
        self.assign_material_button = QtWidgets.QPushButton('Assign Material')
        self.assign_material_button.setEnabled(False)
        self.cancel_button = QtWidgets.QPushButton('Cancel')

        self.assign_button_box = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.assign_button_box.ButtonLayout(QtWidgets.QDialogButtonBox.WinLayout)

        self.assign_button_box.addButton(self.assign_material_button,
                                         QtWidgets.QDialogButtonBox.AcceptRole)
        self.assign_button_box.addButton(self.cancel_button,
                                         QtWidgets.QDialogButtonBox.RejectRole)

        main_layout.addWidget(self.assign_button_box)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = AssignMaterialFromSourceFileUI()
    w.show()
    app.exec_()      
        