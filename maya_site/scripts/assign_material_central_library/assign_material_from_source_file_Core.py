""" User interface to select materials and assign to geometries.

@author Esteban Ortega <brutools@gmail.com>
"""

import os
import re
import sys

import pymel

from maya import OpenMaya

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from assign_material_from_source_file_UI import AssignMaterialFromSourceFileUI

class AssignMaterialFromSourceFileCore(AssignMaterialFromSourceFileUI):
    """ UI to assign material from a referenced file to current geometries.
    """

    ## Stores the namespace for reference file
    # type: str
    _MATFILE = 'MATFILE'


    def __init__(self, parent=None):
        super(AssignMaterialFromSourceFileCore, self).__init__(parent=parent)
    
        ########################################################################
        # Defining some variables, which will be set accordingly.
        ########################################################################
        # Stores the current selection.
        self.active_selection = pymel.core.ls(sl=True)

        # Stores the selected file
        self.selected_file = None

        # File referenced in current maya file
        self.ref_selected_file = None

        ########################################################################
        self.update_sourceimages_label()

        ########################################################################
        # Connect a function to SelectionChange callback
        ########################################################################
        self.selection_changed_callback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.on_selection_change)

        ########################################################################
        # Connect signals
        ########################################################################
        self.cancel_button.clicked.connect(self.on_cancel)
        self.select_material_file.clicked.connect(self.on_choose_file)

        self.assign_material_button.clicked.connect(self.on_assign_material_clicked)

        self.materials_table.itemSelectionChanged.connect(self.on_selection_change)
    

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

    def on_selection_change(self, *args, **kwargs):
        """ Triggers when selection change during the use of the tool.
        """

        self.active_selection = pymel.core.ls(selection=True)
        mat_selected = self.materials_table.selectedItems()


        if not self.active_selection or not mat_selected:
            self.assign_material_button.setEnabled(False)

        else:
            self.assign_material_button.setEnabled(True)

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

    def on_assign_material_clicked(self):
        """ Executes when assign material button is clicked.
        """
        
        new_asset_name = self.destination_name.text()
        current_asset_name = self.source_name.text()

        if not new_asset_name or not current_asset_name:
            msg=(
"""Without a source asset name or destination asset name,
it will assign materials but it will not re-target maps!.

Do you want to continue?""")

            answer = self.show_decision_msg(msg)

            if answer == QtWidgets.QMessageBox.Cancel:
                return

        # Disable callback to avoid changes in selection during the process.
        try:
            OpenMaya.MMessage.removeCallback(self.selection_changed_callback)
        except RuntimeError:
            pass

        sel_item = self.materials_table.selectedItems()
        mat_name = sel_item[0].text()

        for item in sel_item:

            # Try to assign existing material if current maya file if any, 
            # otherwise run the complete process.
            if ':' in mat_name:
                mat_name_only = mat_name.split(':')[1]

            else:
                mat_name_only = mat_name
            
            # print(mat_name_only, 'This is the material name to select ++++++++++++++++++++++++')

            try:
                pymel.core.select(mat_name_only, add=True)
                pymel.core.hyperShade(assign=mat_name_only)
                # print('Material name assigned ++++++++++++++++++++++++')
                pymel.core.select(clear=True)

            except:
                sg_name = item.data(5)
                # print(sg_name, 'this is the shadingEngine name +++++++++++++++++++')

                PyNode_mat = pymel.core.PyNode(mat_name)
                # print(PyNode_mat, 'material node ++++++++++++++++++++++++++')

                shading_engine = pymel.core.listConnections(PyNode_mat, type='shadingEngine')

                if not shading_engine:
                    return

                shading_engine[0].select(noExpand=True)

                upstream_nodes = pymel.core.hyperShade(listUpstreamNodes=shading_engine[0])

                for node in upstream_nodes:
                    pynode = pymel.core.PyNode(node)
                    if isinstance(pynode, pymel.core.nodetypes.Mesh):
                        continue
                    pymel.core.select(node, add=True)
                
                pymel.core.mel.eval('cutCopyPaste "copy"')
                pymel.core.mel.eval('cutCopyPaste "paste"')

                # print('message after copying material network +++++++++++++++++++++++')

                # Find nodes under new Namespace MATFILE1
                new_namespace = '{}1'.format(self._MATFILE)
                pattern = '{}::*'.format(new_namespace)
                nodes_under_ns = pymel.core.ls(pattern)
                
                # Find the material and assign to selected geometries.
                new_shadingEngine_node = None
                file_nodes = []

                for node in nodes_under_ns:
                    if isinstance(node, pymel.core.nodetypes.ShadingEngine):
                        new_shadingEngine_node = node
                    
                    elif isinstance(node, pymel.core.nodetypes.File):
                        file_nodes.append(node)
                
                # print(new_shadingEngine_node, 'This is the shadingEngine node found +++++++++++++++++++++++')
                # print(file_nodes, 'This are the File nodes cound +++++++++++++++++++++++++++++++++++++')
                # Assign material to selected geometries
                pymel.core.select(clear=True)
                if new_shadingEngine_node:
                    for sel in self.active_selection:
                        if isinstance(sel, pymel.core.nodetypes.Transform):
                            pymel.core.select(sel, add=True)
                
                    pymel.core.hyperShade(assign=new_shadingEngine_node)

                pymel.core.select(clear=True)
                
                # Repath file nodes.
                self.retarget_map_files(file_nodes)       
                # print('after retargeting file nodes ++++++++++++++++++++++++++++++')
                # Remove new namespace.
                pymel.core.namespace(removeNamespace=new_namespace, mergeNamespaceWithRoot=True)
                # print('after removing MATFILE1 namespace ++++++++++++++++++++++++++++++')
                        
        # Enable callback to help during selecion of elements and changes in UI
        self.selection_changed_callback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.on_selection_change)

        msg='Material {} assigned to selection!!!'.format(mat_name)
        self.show_info_msg(msg)

        return

    def retarget_map_files(self, file_nodes_list):
        """ Will check every passed file node and retarget file node map to 
        the passed assetTypeName.
        Args:
            file_nodes_list: List of pymel.core.nodetypes.File
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
        Args:
            current_image_path: String representing the full path for map / image.
        Return:
            None value.
        """

        new_asset_name = self.destination_name.text()
        current_asset_name = self.source_name.text()

        if not new_asset_name:
            return

        file_name = os.path.basename(current_image_path)
        file_name_no_padding = file_name.split('.')[0]
        
        new_file_name = re.sub(current_asset_name, str(new_asset_name), file_name_no_padding, re.IGNORECASE)

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
    
    def show_info_msg(self, msg):
        """ Creates a generic msg box with ok button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Information',
            msg, QtWidgets.QMessageBox.Ok)

    def on_cancel(self):
        """ Executes when cancel button is clicked.
        """

        if self.ref_selected_file is not None:
            self.ref_selected_file.remove()

        try:
            OpenMaya.MMessage.removeCallback(self.selection_changed_callback)
            self.close()

        except RuntimeError:
            self.close()

        return

    def on_choose_file(self):
        """ Excecutes when button choose file with materials button is clicked.
        """

        current_dir = str(pymel.core.workspace.getPath())
        
        if self.ref_selected_file is not None:
            self.ref_selected_file.remove()

        self.selected_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                       "Select Maya file", 
                                                                       current_dir, 
                                                                       "Maya File(*.ma *.mb)")

        if self.selected_file == '' or self.selected_file is None:
            self.assign_material_button.setEnabled(False)

            return
        
        self.populate_materials_table()

        return
    
    def populate_materials_table(self):
        """ Add materials from selected file table
        """

        # Reference the selected file.
        refFile = self.reference_selected_file() 

        # Clean table and get all node from reference and list in table.
        self.materials_table.clear()

        for sg_node, mat_node in self.get_shading_engine_and_material_nodes(refFile):
            
            self.add_mat_data_to_table(mat_node, sg_node)
        
        return

    def add_mat_data_to_table(self, mat_node, sg_node):
        """ Add material name to table.
        Args:
            mat_node: pymel.core.nodetype.XXXX
            sg_node: pymel.core.nodetype.XXXX
        """

        node_name = mat_node.name()
        item = QtWidgets.QListWidgetItem()
        item.setText(node_name)
        item.setData(5, sg_node.longName())

        self.materials_table.addItem(item)
    
        return

    def get_shading_engine_and_material_nodes(self, refFile):
        """ Gets all present shading engines present in referenced file.
        Args:
            refFile: pymel.core.system.FileReference
        Yields:
            pymel.core.nodetypes.XXXXXXX        
        """

        for node in refFile.nodes():
            
            if isinstance(node, pymel.core.nodetypes.ShadingEngine):
                
                materials = pymel.core.ls(pymel.core.listConnections(node), materials=True)

                if not materials:
                    continue

                for material in materials:
                
                    if not isinstance(material, pymel.core.nodetypes.DisplacementShader):
                        yield node, material
    
    def reference_selected_file(self):
        """ Reference the selected file under specific namespace "MATFILE"
        """

        self.ref_selected_file = pymel.core.system.createReference(self.selected_file, namespace=self._MATFILE)

        return self.ref_selected_file

def launch_assign_material_from_source():
    """ Launches assign materials from source file UI.
    """

    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = AssignMaterialFromSourceFileCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)
    #w.exec_()
    w.show() #change to show if any problem.
    
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = AssignMaterialFromSourceFileCore()
    w.show()
    app.exec_()
