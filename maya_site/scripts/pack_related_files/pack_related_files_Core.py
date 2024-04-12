################################################################################
# TME FX Trishul Media Entertainment [Jul 2021]
################################################################################ 
""" Window user interface for packing file with referenced files.

@author Esteban Ortega <brutools@gmail.com>
"""

import os
import sys
import math

import pymel
import xgenm

import maya.app.general.fileTexturePathResolver

from PySide2 import QtWidgets, QtCore, QtGui

from pack_related_files_UI import PackRelatedFilesUI

class PackRelatedFilesCore(PackRelatedFilesUI):
    """ Add funtionaly to windows ui, to show gathered data.
    """

    ## Store the different type of nodes with files refenced in scene.
    # type: []
    _HEADER_LABELS = ['Reference_type', 'File_path', 'Size', 'In Folder Structure?']

    ## Color for non existing elements, Redish
    # type: QColor
    _NO_EXISTS = QtGui.QColor( 80 ,
                               11 ,
                               12 )

    ## Color for elements not in folder structure.
    # type: QColor
    _NO_IN_STRUCTURE = QtGui.QColor( 85 ,
                                     52 ,
                                     0 )
    
    ## String for inexisting path in system
    # type: str
    _NO_EXIST_LABEL = 'Path does not exist!'


    def __init__(self, parent=None):
        super(PackRelatedFilesCore, self).__init__(parent=parent)

        self.references_QTreeWidget.setHeaderLabels(self._HEADER_LABELS)

        ########################################################################
        # Get the referenced files at instancing.
        ########################################################################
        self.xgen_palettes = xgenm.palettes()
        self.all_file_nodes = self.get_all_unique_file_nodes()
        self.all_reference_files = self.get_reference_file_path()

        ########################################################################
        self.populate_reference_QtWidget()


        # self.amount_of_paths = len(list(self.get_paths_from_QtWidget('Yes'))) + 
        # # print('++++++++++++++++++++++++++++++++++++++++++++++++, next No')
        # self.get_paths_from_QtWidget('No')

        self.check_if_paths_to_pack()
        ########################################################################
        # Connect signals
        ########################################################################
        self.pack_buttonBox.rejected.connect(self.close)
        self.browse_button.clicked.connect(self.on_browse_clicked)

        self.pack_buttonBox.accepted.connect(self.copy_files_into_pack_folder)

    def get_all_unique_file_nodes(self):
        """ Gets all files nodes without repeating the image loaded in it.
        Return:
            List of file nodes representing the full file path to a texture.
        """

        unique_node_files = []
        unique_paths = []

        for file_node in pymel.core.ls(type='file'):
            path = pymel.core.general.getAttr('{}.fileTextureName'.format(file_node))

            if path not in unique_paths:
                unique_paths.append(path)
                unique_node_files.append(file_node)

        return unique_node_files

    def get_all_unique_full_file_paths(self):
        """ Gets every full file path for images including UDIM related files,
        based on file nodes.
        Return:
            List of string representing full file path.
        """

        for file_node in self.all_file_nodes:
            path = pymel.core.general.getAttr('{}.fileTextureName'.format(file_node))

            if path == '':
                yield None

            uv_tiling_mode = pymel.core.general.getAttr('{}.uvTilingMode'.format(file_node))
            if uv_tiling_mode != 0:
                yield path

            compound_file_name_patter = pymel.core.general.getAttr('{}.computedFileTextureNamePattern'.format(file_node))
            all_files_related_for_pattern = maya.app.general.fileTexturePathResolver.findAllFilesForPattern(compound_file_name_patter, None)

            for full_file_path in all_files_related_for_pattern:
                yield full_file_path

    def check_if_paths_to_pack(self):
        """ Checks if there is any path to pack.
        Return:
            True if there is something to pack, False otherwise.
        """

        if list(self.get_paths_from_QtWidget('Yes')) or list(self.get_paths_from_QtWidget('No')):
            self.browse_button.setEnabled(True)

            return True
        
        self.browse_button.setEnabled(False)

        return False

    def populate_reference_QtWidget(self):
        """ Check if there is files nodes, xgen collections and references in
        current maya file.
        Return:
            List ['Images', 'References', 'xgen'], is there is files associated
        with them, otherwise will return empty list.
        """

        if self.xgen_palettes:
            xgenItem = QtWidgets.QTreeWidgetItem(['Xgen', '', '', ''])
            top_level_item = self.references_QTreeWidget.addTopLevelItem(xgenItem)

            # This part add the main xgen file.
            for main_xgen_file in self.get_xgen_collection_file():

                arguments = self.analyse_full_path(main_xgen_file)
                row_path = arguments[:4]
                row_color_brush = arguments[-1]

                xgen_item = QtWidgets.QTreeWidgetItem(row_path)

                if row_color_brush is not None:
                    for column in range(self.references_QTreeWidget.columnCount()):
                        xgen_item.setBackground(column, row_color_brush)

                xgenItem.addChild(xgen_item)

            # This part add all related xgen files for styling xgen.
            for path in self.get_every_file_full_path_name():
                
                arguments = self.analyse_full_path(path)
                row_path = arguments[:4]
                row_color_brush = arguments[-1]
                
                # Adding all referenced files from xgen thing.
                xgen_item = QtWidgets.QTreeWidgetItem(row_path)

                if row_color_brush is not None:
                    for column in range(self.references_QTreeWidget.columnCount()):
                        xgen_item.setBackground(column, row_color_brush)

                xgenItem.addChild(xgen_item)

        if self.all_file_nodes:
            imagesItem = QtWidgets.QTreeWidgetItem(['Images', '', '', ''])
            self.references_QTreeWidget.addTopLevelItem(imagesItem)

            for path in self.get_all_unique_full_file_paths():

                if path is None:
                    continue

                find_path = self.references_QTreeWidget.findItems(path, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive, column=1)
                
                if find_path:
                    continue
                
                arguments = self.analyse_full_path(path)
                row_path = arguments[:4]
                row_color_brush = arguments[-1]

                # Adding all referenced files from xgen thing.
                image_item = QtWidgets.QTreeWidgetItem(row_path)

                if row_color_brush is not None:
                    for column in range(self.references_QTreeWidget.columnCount()):
                        image_item.setBackground(column, row_color_brush)

                imagesItem.addChild(image_item)
        
        if self.all_reference_files:
            referencesItem = QtWidgets.QTreeWidgetItem(['References', '', '', ''])
            self.references_QTreeWidget.addTopLevelItem(referencesItem)

            for path in self.all_reference_files:
                
                arguments = self.analyse_full_path(path)
                row_path = arguments[:4]
                row_color_brush = arguments[-1]
                
                # Adding all referenced files from xgen thing.
                ref_item = QtWidgets.QTreeWidgetItem(row_path)

                if row_color_brush is not None:
                    for column in range(self.references_QTreeWidget.columnCount()):
                        ref_item.setBackground(column, row_color_brush)

                referencesItem.addChild(ref_item)
        
        current_file_item = QtWidgets.QTreeWidgetItem(['Current_File', '', '', ''])
        self.references_QTreeWidget.addTopLevelItem(current_file_item)
        arguments = self.analyse_full_path(pymel.core.sceneName())
        
        row_path = arguments[:4]
        row_color_brush = arguments[-1]

        currentFile = QtWidgets.QTreeWidgetItem(row_path)

        if row_color_brush is not None:
            for column in range(self.references_QTreeWidget.columnCount()):
                currentFile.setBackground(column, row_color_brush)

        current_file_item.addChild(currentFile)

        return
    
    def on_browse_clicked(self):
        """ Executes when select directory button clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     "Select directory for pack", 
                                                                     "", 
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.pack_directory = selected_path.replace('\\', '/')

        if self.pack_directory == '':
            self.pack_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

            return
        
        self.pack_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

        return
    
    def get_paths_from_QtWidget(self, in_folder_structure):
        """ Get paths from QTreeWidget based on passed argument, in or not in 
        folder structure.
        Args:
            in_folder_structure: String 'Yes' or 'No'
        yield a string representing the path of the referenced file.
        """

        for item in self.references_QTreeWidget.findItems(in_folder_structure, QtCore.Qt.MatchFixedString | QtCore.Qt.MatchRecursive, column=3):
            # print(item.text(1))
            yield item.text(1)

    def get_collection_path(self):
        """ Gets the current collection if there is pallets in file.
        Return:
            List of string representing the path to present collections.
        """

        collection_paths = []

        for palette in self.xgen_palettes:
            for path, dirs, files in os.walk(xgenm.localRepo()):
                if palette in dirs:
                    collection_path = os.path.join(path, palette)
                    collection_path_reformat = collection_path.replace('\\', '/')
                    collection_paths.append(collection_path_reformat)
        
        return collection_paths
    
    def compose_on_root_destination_directory(self, path, root_folder):
        """ Compose destination directory for files within in root folder,
        based on selected directory and current item directory path.
        Args:
            path: Is a string representing the current full path name for 
            referenced files within current maya file.
            root_folder: Is a string representing the name of the root folder
            "ADI_project" expected.
        Return:
            tuple (string source path, string destination path)
        """

        index = path.find(root_folder)
        path_under_root_folder = path[index:]

        # compose destination path
        destination_path = os.path.join(self.pack_directory, path_under_root_folder)
        destination_path_formatted = destination_path.replace('\\', '/')

        return path, destination_path_formatted

    def compose_not_on_root_destination_directory(self, path):
        """ Compose destination directory for files not in root folder,
        based on selected directory and current item directory path.
        Args:
            path: Is a string representing the current full path name for 
            referenced files within current maya file.
        Return:
            tuple (string source path, string destination path)
        """

        # CONSIDER XGEN FOLDER OUTSIDE OF STRUCTURE, SO WE CAN SEARCH FOR xgen
        # folder and that could be the folder to copy.
        path_parts = path.split('/')
        xgen_folder = 'xgen'

        if xgen_folder in path_parts:
            index = path.find(xgen_folder)
            path_under_root_folder = path[index:]

            # compose destination path
            destination_path = os.path.join(self.pack_directory, path_under_root_folder)
            destination_path_formatted = destination_path.replace('\\', '/')

            return path, destination_path_formatted

        # HERE WILL USE THE TOP MOST DIRECTORY OF THE LONGEST FILE
        longest_dir_parts = path.split('/')[1:]
        destination_path = os.path.join(self.pack_directory, *longest_dir_parts)
        destination_path_formatted = destination_path.replace('\\', '/')

        return path, destination_path_formatted

    def get_every_file_full_path_name(self):
        """ Gets full path of every file under collection path.
        Yield:
            Yields every full path name of every file found.
        """

        collection_path_list = self.get_collection_path()

        for collection_path in collection_path_list:
            for path, dirs, files in os.walk(collection_path):
                if not files:
                    continue
                for col_file in files:
                    file_path = os.path.join(path, col_file)
                    file_path_reformat = file_path.replace('\\', '/')
                    yield file_path_reformat
    
    def get_xgen_collection_file(self):
        """ Gets the xgen file related to current maya file. (eg. maya_file__xgenPalettes.xgen)
        """

        current_maya_full_path_name = pymel.core.sceneName()
        maya_file_dir = os.path.dirname(current_maya_full_path_name)
        maya_file_name = os.path.basename(current_maya_full_path_name)
        maya_file_name_no_extension = os.path.splitext(maya_file_name)[0]

        for palette in self.xgen_palettes:
            
            xgen_file_name = '{}__{}.xgen'.format(maya_file_name_no_extension, palette)
            
            xgen_full_path = os.path.join(maya_file_dir, xgen_file_name)

            if os.path.exists(xgen_full_path):
                xgen_full_path_reformat = xgen_full_path.replace('\\', '/')
                yield xgen_full_path_reformat
                
    def copy_files_into_pack_folder(self):
        """ Copies files into pack folder.
        """
        root_path = os.path.expandvars("%ADI_ROOT_FOLDER%")
        root_folder = os.path.basename(root_path)

        # TODO: Create a clean folders in the pack firectory to remove
        # folders not required, walk through folder omiting ADI_project and xgen
        # the other can be analized to remove un used folders.

        total_files = len(list(self.get_paths_from_QtWidget('Yes'))) + len(list(self.get_paths_from_QtWidget('No')))
        self.progress_bar.setMaximum(total_files)
        progress = 0

        # THIS ALREADY WORKS AS EXPECTED MUTTED TO ADD NO Files.
        if list(self.get_paths_from_QtWidget('Yes')):

            for path in self.get_paths_from_QtWidget('Yes'):
                source_full_path_name, destination_path_name = self.compose_on_root_destination_directory(path, root_folder)    
                destination_directory = os.path.dirname(destination_path_name)

                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)
                
                source_full_path_name_reformat = source_full_path_name.replace('/', '\\')
                destination_path_name_reformat = destination_path_name.replace('/', '\\')

                # copy the files
                os.popen('copy {} {}'.format(source_full_path_name_reformat, destination_path_name_reformat))
            
                progress += 1
                self.progress_bar.setValue(progress)

        if list(self.get_paths_from_QtWidget('No')):
        
            list_of_path_not_in_structure = self.get_paths_from_QtWidget('No')
            paths_not_in_structure_dic = {path:len(os.path.dirname(path).split('/')) for path in list_of_path_not_in_structure}
            list_key_value_pairs = paths_not_in_structure_dic.items()        
            list_sorted = sorted(list_key_value_pairs, key=lambda x: x[1], reverse=True)

            for value_pair in list_sorted:
                path, _ = value_pair

                source_full_path_name, destination_path_name = self.compose_not_on_root_destination_directory(path)
                destination_directory = os.path.dirname(destination_path_name)

                if not os.path.exists(destination_directory):
                    os.makedirs(destination_directory)

                source_full_path_name_reformat = source_full_path_name.replace('/', '\\')
                destination_path_name_reformat = destination_path_name.replace('/', '\\')

                os.popen('copy {} {}'.format(source_full_path_name_reformat, destination_path_name_reformat))

                progress += 1
                self.progress_bar.setValue(progress)

        msg = 'Files copied under: \n{}'.format(self.pack_directory)

        self.show_info_msg(msg)

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
        
    def get_image_full_file_path(self, file_node):
        """ Gets the full file path from file node passed.
        Args:
            file_node: It is a maya File node.
        """

        path = pymel.core.general.getAttr("{}.fileTextureName".format(file_node))
        path_reformat = path.replace('\\', '/')

        if path_reformat == '':
            return

        else:
            return path_reformat
    
    def get_reference_file_path(self):
        """ Gets paths from referenced files.
        Return:
            List of string representing the path of references.
        """
        list_reference_paths = []
        refs = pymel.core.listReferences(references=True, loaded=True)

        for ref in refs:
            full_path = ref.path

            if '{' in full_path:
                full_path = full_path[:full_path('{')]

            list_reference_paths.append(full_path)

        return list_reference_paths
    
    def get_file_size(self, full_path):
        """ Get file size based on passed full path.
        Args:
            full_path: It is a string representing the full path to file.
        Return:
            String representing the size of the file.
        """

        size_bytes = os.path.getsize(full_path)

        return self.convert_size(size_bytes)
    
    def analyse_full_path(self, path):
        """ Analizes path for existance, file size.
        Args:
            path: String representing the passed full file path.
        Return:
            tuple ('', full_path, file_size, 'yes/No', "") 
        """

        row_color_brush = None
        in_folder_structure = ''

        if not os.path.exists(path):
            file_size = '0'
            in_folder_structure = self._NO_EXIST_LABEL
            row_color_brush = QtGui.QBrush(self._NO_EXISTS)

        else:
            file_size = self.get_file_size(path)
            in_folder_structure = self.in_folder_structure(path)

            if not in_folder_structure:
                in_folder_structure = 'No'
                row_color_brush = QtGui.QBrush(self._NO_IN_STRUCTURE)

            else:
                in_folder_structure = 'Yes'

        return ('', path, file_size, in_folder_structure, row_color_brush)

    def in_folder_structure(self, full_path):
        """ Check if directory is in current folder structure.
        Args:
            full_path: It is a string representing the full path to a file.
        Return:
            True if directory is part of the folder structure, false otherwise.
        """

        root_directory = os.path.expandvars('%ADI_ROOT_FOLDER%')
        root_full_path = full_path[:len(root_directory)]
        root_full_path_reformat = root_full_path.replace('\\', '/')

        if root_directory == root_full_path_reformat:

            return True
        
        return False

    def convert_size(self, size_bytes):
        """ Convert bytes to human readable format.
        Args:
            size_bytes is an integer representing the file size in bytes.
        Return:
            String representing the size of the file.
        """
        if size_bytes == 0:
            return "0B"

        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return "%s %s" % (s, size_name[i])


def launch_pack_files():
    """ Launch pack related files UI.
    """

    # import pymel
    # import xgenm

    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = PackRelatedFilesCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)
    w.exec_() # Changed to show if a problem.
    #w.show()

    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = PackRelatedFilesCore()
    w.show()
    app.exec_()
