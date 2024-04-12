""" Functionality window to import alembics.

@author Esteban Ortega <brutools@gmail.com>
"""

import os
import sys
import pymel

from PySide2 import QtWidgets
from PySide2 import QtCore

class ImportAlembicsCore(QtWidgets.QFileDialog):
    """ Creates a QFileDialog window to import alembic files.
    """

    def __init__(self, parent=None):
        super(ImportAlembicsCore, self).__init__(parent=parent)

        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.setNameFilter("Alembic (*.abc)")
        self.setViewMode(QtWidgets.QFileDialog.Detail)
        self.setWindowTitle('Select alembic files to import')

        self.set_default_directory()
    
    def set_default_directory(self):
        """ Sets the default directory.
        """

        default_dir = os.path.expandvars('%ADI_ROOT_FOLDER%')
        QDirectory = QtCore.QDir(default_dir)

        self.setDirectory(QDirectory)

        return

def import_selected_files(selected, selected_node=None):
    """ Import selected files if any.
    Args:
        selected: String representing the full path of selected alembic file
        to be imported.
        selected_node: String representing the current selected node in maya.
    """

    if not pymel.core.pluginInfo('AbcImport.mll', query = True, loaded = True):
        pymel.core.loadPlugin('AbcImport.mll')
        
    for alembic in selected:
        if selected_node is None:
            pymel.core.AbcImport(str(alembic), mode='import')
        
        else:
            pymel.core.AbcImport(str(alembic), mode='import', connect=selected_node)
        
    return

def show_info_msg(parentWidget, msg):
    """ Creates a generic msg box with ok button.
    Args:
        msg: String representing the msg for the user.
    Returns:
        PySide Message box.
    """

    return QtWidgets.QMessageBox.information(parentWidget, 'Information',
        msg, QtWidgets.QMessageBox.Ok)

def launch_import_alembics():
    """ Launch export to alembic UI.
    """
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = ImportAlembicsCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)

    fileNames = []
    selected_node = pymel.core.ls(sl=True)

    if w.exec_():
        fileNames = w.selectedFiles()
    
    if not fileNames:
        return
    
    if selected_node:
        import_selected_files(fileNames, selected_node=selected_node[0].name())
    else:
        import_selected_files(fileNames)

    msg = 'Files imported:\n'
    for file in fileNames:
        msg += '{}\n'.format(str(file))

    show_info_msg(mayaMainWindow, msg)
    
    return


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ImportAlembicsCore()
    w.show()
    app.exec_()
