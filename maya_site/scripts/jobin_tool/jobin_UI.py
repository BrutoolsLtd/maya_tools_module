################################################################################
# TME FX Trishul Media Entertainment [Jun 2021]
################################################################################ 
""" Window user interface to set jobIn information in Maya.

@author Esteban Ortega <brutools@gmail.com>
"""
import sys

from PySide2 import QtWidgets, QtGui
from PySide2 import QtCore

class JobInUI(QtWidgets.QDialog):
    """ Job in dialog window to set variables for current job in Maya.
    """

    def __init__(self):
        super(JobInUI, self).__init__()

        self.setWindowTitle('Create/Open Version')
        self.setFixedSize(300, 235)
        # self.setWindowModality(QtCore.Qt.ApplicationModal)

        ########################################################################
        # Create layout for UI
        ########################################################################
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        ########################################################################
        # Create radio buttons
        ########################################################################
        self.groupBox = QtWidgets.QGroupBox('Context')
        self.groupBox.setWhatsThis('Select the main context to work on!')
        
        self.shot_radioButton = QtWidgets.QRadioButton('Shot')
        self.shot_radioButton.setChecked(True)
        self.asset_radioButton = QtWidgets.QRadioButton('Asset')

        groupBox_layout = QtWidgets.QHBoxLayout()
        groupBox_layout.addWidget(self.shot_radioButton)
        groupBox_layout.addWidget(self.asset_radioButton)

        self.groupBox.setLayout(groupBox_layout)
        
        self.mainLayout.addWidget(self.groupBox)

        ########################################################################
        # Combo Boxes
        ########################################################################
        self.shotAsset_comboBox = QtWidgets.QComboBox()
        self.step_comboBox = QtWidgets.QComboBox()
        self.step_comboBox.setEnabled(False)
        
        version_layout = QtWidgets.QHBoxLayout()
        self.version_comboBox = QtWidgets.QComboBox()
        self.version_comboBox.setEnabled(False)

        self.maya_files_comboBox = QtWidgets.QComboBox()
        self.maya_files_comboBox.setEnabled(False)

        self.mainLayout.addWidget(self.shotAsset_comboBox)
        self.mainLayout.addWidget(self.step_comboBox)
        self.mainLayout.addWidget(self.version_comboBox)
        
        self.mainLayout.addWidget(self.maya_files_comboBox)

        ########################################################################
        # Button boxes
        ########################################################################
        self.jobin_buttonBox = QtWidgets.QDialogButtonBox( 
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        
        self.jobin_buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setText('Create version')
        self.jobin_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        help_text = """Creates a maya.ma under the selected hierarchy:

        - If there is no version to selelct it will create 
          version 001.

        - If there are versions and you left "Select version",
          it will create the next version.
          (eg. 3 versions exists it will create the 4th).

        - If you select an specific version it will ask to select 
          your file which will be copied in the next version.
          (eg. selected 2 out of 6, it will create version 7 
          copying version 2).
          """
        self.jobin_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setWhatsThis(help_text)

        # create additional button for open version
        self.openVersion_buttonBox = QtWidgets.QDialogButtonBox.Open
        self.jobin_buttonBox.addButton(self.openVersion_buttonBox)
        self.jobin_buttonBox.button(self.openVersion_buttonBox).setText('Open version')
        self.jobin_buttonBox.button(self.openVersion_buttonBox).setEnabled(False)

        self.mainLayout.addWidget(self.jobin_buttonBox)

        ########################################################################
        # Connect signals
        ########################################################################
        self.jobin_buttonBox.rejected.connect(self.close)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = JobInUI()
    w.show()
    app.exec_()
