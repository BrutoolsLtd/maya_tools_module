################################################################################
# TME FX Trishul Media Entertainment [Jul 2021]
################################################################################ 
""" Window user interface to export selected objs to alembics.

@author Esteban Ortega <brutools@gmail.com>
"""
import sys
import subprocess

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class CustomMsgBoxUI(QtWidgets.QDialog):
    """ Custom msg box with option to open destination directory.
    """

    def __init__(self, path, parent=None):
        super(CustomMsgBoxUI, self).__init__(parent=parent)

        self.path = path

        self.setWindowTitle('Information')
        self.setFixedHeight(100)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        msg = 'Alembics exported into:\n{}'.format(self.path)
        self.msg_label = QtWidgets.QLabel(msg)

        main_layout.addWidget(self.msg_label)

        # Create button box
        ########################################################################
        self.show_in_folder_button = QtWidgets.QPushButton('Show in Folder')
        self.ok_button = QtWidgets.QPushButton('OK')

        self.msg_button_box = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.msg_button_box.ButtonLayout(QtWidgets.QDialogButtonBox.WinLayout)

        self.msg_button_box.addButton(self.show_in_folder_button,
                                      QtWidgets.QDialogButtonBox.AcceptRole)
        self.msg_button_box.addButton(self.ok_button,
                                      QtWidgets.QDialogButtonBox.AcceptRole)

        main_layout.addWidget(self.msg_button_box)

        self.show()
        # Connect signals
        ########################################################################
        self.msg_button_box.clicked.connect(self.on_buttonBox_clicked)

    def on_buttonBox_clicked(self, signal):
        
        if signal.text() == 'Show in Folder':

            path_reformat = self.path.replace('/', '\\')
            
            subprocess.Popen(r'explorer "{}"'.format(path_reformat))

            self.close()

        else:
            self.close()

        return                         


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = CustomMsgBoxUI('')
    app.exec_()
