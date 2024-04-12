################################################################################
# TME FX Trishul Media Entertainment [Aug 2021]
################################################################################ 
""" Add funcitonality to user interface to automatically assign materials 
to meshes in current file.

@author Esteban Ortega <brutools@gmail.com>
"""

import os
import re
import sys

import pymel

from PySide2 import QtWidgets, QtCore

from assign_material_central_library_UI import AssignMaterialCentralLibraryUI

class AssignMaterialCentralLibraryCore(AssignMaterialCentralLibraryUI):
    """ Adds functionality to ui to assign automatically materials from 
    central library.
    """

    ## Stores the pattern to look for in geometry.
    # type: regex
    _MAT_NAME_PATTERN = re.compile(r'_ID(\w*)_GEO')

    ## Store the pattern for the asset name place holder.
    # type: str
    _ASSET_NAME = 'ASSETNAME'

    def __init__(self, parent=None):
        super(AssignMaterialCentralLibraryCore, self).__init__(parent=parent)

        self.library_directory_path = self.get_material_library_path()

        self.update_info_labels()
        self.update_sourceimages_label()
        ########################################################################
        # Connect signals
        ########################################################################
        self.assign_button_box.clicked.connect(self.on_button_clicked)
        self.change_library_button.clicked.connect(self.on_change_library_directory)

    def update_sourceimages_label(self):
        """ Updates sourceimages label based on current project directory.
        """

        sourceimages_dir = os.path.join(str(pymel.core.workspace.getPath()), 'sourceimages')
        sourceimages_dir = sourceimages_dir.replace('\\', '/')

        if not os.path.exists(sourceimages_dir):
            msg = 'NO sourceimages folder in current project directory\n{}'.format(str(pymel.core.workspace.getPath()))
            self.sourceimages_info_label.setText(msg)
            self.sourceimages_info_label.setStyleSheet('color: red')
        else:
            msg = 'Will target images from project directory sourceimages:\n{}'.format(sourceimages_dir)
            self.sourceimages_info_label.setText(msg)
        
        return

    def update_info_labels(self, color=None):
        """ Update info label based on library path.
        """

        if self.library_directory_path is None:
            self.info_label.setText('There is not material library:')
            self.info_label.setStyleSheet('color:red')
            self.assign_material_button.setEnabled(False)
            return

        self.info_label.setText('This tool will fetch materials from:')
        self.info_label.setStyleSheet('')
        self.info_label_path.setText(self.library_directory_path)
        self.info_label_path.setStyleSheet("font-weight:bold")
        if color:
            self.info_label_path.setStyleSheet("color:{}".format(color))
        self.info_label_help.setText('Based on geometry "IDName" part of the name and assign automatically a material if exists in library.')
        self.assign_material_button.setEnabled(True)

        return

    def on_change_library_directory(self):
        """ Executes when select directory button clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     "Select materials library directory", 
                                                                     "", 
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.library_directory_path = selected_path.replace('\\', '/')

        if self.library_directory_path == '':
            self.library_directory_path = self.get_material_library_path()

            self.update_info_labels()

            return
        
        self.update_info_labels(color='orange')

        return

    def on_button_clicked(self, signal):
        """ Executes when a button is clicked in the interface.
        """

        if signal.text() == 'Cancel':
            
            self.close()
        
            return
        
        new_char_name = self.char_LineEdit.text()
        
        if not new_char_name:

            answer = self.show_decision_msg(
                'Without an asset name, it will assign materials\nbut it will not re-target maps!.\n\nDo you want to continue?')

            if answer == QtWidgets.QMessageBox.Cancel:
                return

        for mesh in pymel.core.ls(type='mesh'):
            
            match = self._MAT_NAME_PATTERN.search(mesh.name())

            if match:
                # Select current mesh
                base_name = match.group(1)
                pymel.core.select(mesh.name())
                material_name = self.create_material_name(base_name)
                
                try:
                    print('Trying to assign material "{}"'.format(material_name))
                    pymel.core.select(material_name)
                    
                    node = pymel.core.ls(sl=True)
                    file_nodes = self.get_related_file_nodes(node[0])

                    pymel.core.select(mesh.name())
                    pymel.core.hyperShade(assign=material_name)

                    # Here will re-target the maps related to material if any.
                    self.retarget_map_files(file_nodes)
                
                except:
                    print('"{}" material no present, trying to import from library'.format(material_name))

                    if self.import_material_file(material_name):
                        print('"{}" material imported!'.format(material_name))
                    
                    else:
                        print('"{}" material does not exists in library'.format(material_name))
                        continue

                    try:
                        pymel.core.select(material_name)

                        node = pymel.core.ls(sl=True)
                        file_nodes = self.get_related_file_nodes(node[0])

                        pymel.core.select(mesh.name())
                        print('Trying to assign material 2nd TRY"{}"'.format(material_name))
                        pymel.core.hyperShade(assign=material_name)

                        # Here will re-target the maps related to material if any.
                        self.retarget_map_files(file_nodes)
                    
                    except:
                        print('No shader material named "{}"'.format(material_name))
        
                        continue       
        
        self.close()

        return
    
    def retarget_map_files(self, file_nodes_list):
        """ Will check every passed file node and retarget file node map to 
        the passed assetTypeName.
        """

        if not file_nodes_list:
            return
        
        for file_node in file_nodes_list:

            map_path = file_node.getAttr('fileTextureName')

            if map_path == '':
                continue

            new_full_path = self.create_new_full_path(map_path)

            if new_full_path is None:
                                
                continue

            file_node.setAttr('fileTextureName', new_full_path)

        return
    
    def create_new_full_path(self, current_image_path):
        """ Creates the new full path for image, and using the passed name.
        Return:
            None value.
        """

        new_asset_name = self.char_LineEdit.text()

        if not new_asset_name:
            return

        file_name = os.path.basename(current_image_path)
        file_name_no_padding = file_name.split('.')[0]
        
        new_file_name = re.sub(self._ASSET_NAME, str(new_asset_name), file_name_no_padding)

        if new_file_name == file_name_no_padding:
            return
                
        sourceimages_dir = os.path.join(str(pymel.core.workspace.getPath()), 'sourceimages')
        sourceimages_dir = sourceimages_dir.replace('\\', '/')

        if not os.path.exists(sourceimages_dir):
            return
        
        for path, dirs, files in os.walk(sourceimages_dir):

            for element in files:
                
                if new_file_name in element:
                    new_full_path = os.path.join(path, element)
                    new_full_path = new_full_path.replace('\\', '/')
                    
                    return new_full_path
        
        return

    def get_current_project_dir(self):
        """ Get the current maya project directory.
        """

        project_dir = pymel.core.workspace.getPath()

        return str(project_dir)

    def get_related_file_nodes(self, material_node):
        """ Get all file name nodes related to the passed material.
        Args:
            material_node: pymel.core.nodetypes
        Return:
            List of strings representing the File nodes. 
        """

        file_node_list = []
        up_stream_nodes = pymel.core.hyperShade(listUpstreamNodes=material_node)

        for node_name in up_stream_nodes:
            node = pymel.core.PyNode(str(node_name))
            
            if isinstance(node, pymel.core.nodetypes.File):
                file_node_list.append(node)     
        
        return file_node_list

    def create_material_name(self, base_string):
        """ Creates the material name based on passed string.
        Args:
            base_string: String representing the base string for material,
            usually a  word.
        """

        return '{}_mat'.format(base_string)

    def import_material_file(self, material_name):
        """ Imports material based on passed material_name.
        Args:
            material_name: String representing the material name.
        Return:
            True if any material was imported, False otherwise.
        """

        for element in os.listdir(self.library_directory_path):

            file_path = os.path.join(self.library_directory_path, element)

            if os.path.isdir(file_path):
                continue
            
            if element == '{}.ma'.format(material_name) or element == '{}.mb'.format(material_name):
                
                pymel.core.importFile(file_path)

                return True
        
        return False
            
    def get_material_library_path(self):
        """ Gets the material library path.
        """

        library_relative_path = 'assets/material_library'

        project_path = os.path.expandvars('%ADI_ROOT_FOLDER%')
        library_path = os.path.join(project_path, library_relative_path)
        library_path = library_path.replace('\\', '/')

        if os.path.exists(library_path):
            return library_path
        
        return
    
    def show_decision_msg(self, msg):
        """ Creates a generic msg box with ok button and cancel button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Confirm action',
            msg, QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)

def launch_assign_materials():
    """ Launches assign materials from central library tool.
    """

    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = AssignMaterialCentralLibraryCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)
    w.exec_()
    # w.show() change to show if any problem.
    
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = AssignMaterialCentralLibraryCore()
    w.show()
    app.exec_()
