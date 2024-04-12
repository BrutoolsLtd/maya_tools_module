""" Window user interface for packing file with referenced files.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys

from PySide2 import QtWidgets

class PackRelatedFilesUI(QtWidgets.QDialog):
    """ Dialog window to show files refered in current maya file.
    """

    def __init__(self, parent=None):
        super(PackRelatedFilesUI, self).__init__(parent=parent)

        self.setWindowTitle('Pack with referenced files')
        # self.setFixedSize(600, 300)
        self.setMinimumSize(600, 300)
        ########################################################################
        # Main Layout
        ########################################################################
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        ########################################################################
        # Create widgets
        ########################################################################
        self.references_QTreeWidget = QtWidgets.QTreeWidget()

        main_layout.addWidget(self.references_QTreeWidget)

        # Progress bar
        ########################################################################
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setFormat('%p% / %m Files')
        
        main_layout.addWidget(self.progress_bar)
        # Browse destination directory
        ########################################################################
        browse_layout = QtWidgets.QHBoxLayout()

        browse_label = QtWidgets.QLabel('Select destination directory')
        self.browse_button = QtWidgets.QPushButton('Browse')
        self.browse_button.setEnabled(False)

        browse_layout.addWidget(browse_label)
        browse_layout.addWidget(self.browse_button)

        main_layout.addLayout(browse_layout)

        ########################################################################
        # Create buttons for UI
        ########################################################################
        self.pack_buttonBox = QtWidgets.QDialogButtonBox( 
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        
        self.pack_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Pack')
        self.pack_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        main_layout.addWidget(self.pack_buttonBox)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PackRelatedFilesUI()
    w.show()
    app.exec_()
