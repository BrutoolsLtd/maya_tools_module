""" Window user interface to export selected objs to alembics.

@author Esteban Ortega <brutools@gmail.com>
"""
import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class ExportToAlembicUI(QtWidgets.QDialog):
    """ UI to export to alembics.
    """

    def __init__(self, parent=None):
        super(ExportToAlembicUI, self).__init__(parent=parent)

        self.setWindowTitle('Export selection to Alembics')
        # self.setFixedSize(350, 120)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ########################################################################
        # Add widgets
        ########################################################################
        self.message_label = QtWidgets.QLabel('Place holder')
        main_layout.addWidget(self.message_label)

        ########################################################################
        # Create options widget
        ########################################################################
        self.options_GroupBox = QtWidgets.QGroupBox('Cache Options')
        group_layout = QtWidgets.QVBoxLayout()
        self.options_GroupBox.setLayout(group_layout)

        cache_time_layout = QtWidgets.QHBoxLayout()

        self.time_slider_radioButton = QtWidgets.QRadioButton('Time Slider')
        self.time_slider_radioButton.setChecked(True)

        cache_time_layout.addWidget(self.time_slider_radioButton)
        
        # Create a validator for QLineEdit to accept only int
        self.int_validator = QtGui.QIntValidator()

        self.start_lineEdit = QtWidgets.QLineEdit()
        self.start_lineEdit.setPlaceholderText('Start Frame')
        self.start_lineEdit.setEnabled(False)
        self.start_lineEdit.setValidator(self.int_validator)

        cache_time_layout.addWidget(self.start_lineEdit)
        
        self.end_lineEdit = QtWidgets.QLineEdit()
        self.end_lineEdit.setPlaceholderText('End Frame')
        self.end_lineEdit.setEnabled(False)
        self.end_lineEdit.setValidator(self.int_validator)

        cache_time_layout.addWidget(self.end_lineEdit)

        group_layout.addLayout(cache_time_layout)
        main_layout.addWidget(self.options_GroupBox)

        # Checkbox per selection
        ########################################################################
        self.alembic_per_selection_checkBox = QtWidgets.QCheckBox('Create Alembic file per selection')
        self.alembic_per_selection_checkBox.setChecked(True)
        group_layout.addWidget(self.alembic_per_selection_checkBox)

        # Browse button to redirect the output.
        ########################################################################
        browse_layout = QtWidgets.QHBoxLayout()
        browse_label = QtWidgets.QLabel('Change destination path:')

        self.browse_button = QtWidgets.QPushButton('Browse')
        browse_layout.addWidget(browse_label)
        browse_layout.addWidget(self.browse_button)

        group_layout.addLayout(browse_layout)

        ########################################################################
        # Create buttons for UI
        ########################################################################
        self.exportToAlembic_buttonBox = QtWidgets.QDialogButtonBox( 
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Export')

        self.publish_button = QtWidgets.QPushButton('Export and Publish')
        self.publish_button.setEnabled(False)

        self.exportToAlembic_buttonBox.addButton(self.publish_button, 
                                                 QtWidgets.QDialogButtonBox.AcceptRole)

        main_layout.addWidget(self.exportToAlembic_buttonBox)

        ########################################################################
        # Connect signals
        ########################################################################

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ExportToAlembicUI()
    w.show()
    app.exec_()
