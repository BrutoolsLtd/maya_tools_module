################################################################################
# TME FX Trishul Media Entertainment [Jul 2021]
################################################################################ 
""" Window user interface to set user name and path for playblast.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui


class SetUserPathUI(QtWidgets.QDialog):
    """ UI to set user name and path for playblast.
    """

    def __init__(self, parent=None):
        super(SetUserPathUI, self).__init__(parent=parent)

        self.setWindowTitle('Set user and playblast path')
        self.setFixedSize(425, 170)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ########################################################################
        # Create widgets
        ########################################################################
        self.current_path = QtWidgets.QLabel('Current Directory:')
        self.current_user = QtWidgets.QLabel('Current user:')
        self.browse_button = QtWidgets.QPushButton('Select Directory')
        self.user_name_lineEdit = QtWidgets.QLineEdit()
        self.user_name_lineEdit.setPlaceholderText('Input user name')

        main_layout.addWidget(self.current_path)
        main_layout.addWidget(self.current_user)
        main_layout.addWidget(self.browse_button)
        main_layout.addWidget(self.user_name_lineEdit)
        ########################################################################
        # Create buttons for UI
        ########################################################################
        self.set_user_path_buttonBox = QtWidgets.QDialogButtonBox( 
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        # self.set_user_path_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        
        self.set_user_path_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Set')

        main_layout.addWidget(self.set_user_path_buttonBox)

    #     self.set_user_path_buttonBox.rejected.connect(self.algo)

    # def algo(self):

    #     w = self.frameGeometry().width()
    #     h = self.frameGeometry().height()

    #     print(w, h)

    #     return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SetUserPathUI()
    w.show()
    app.exec_()
