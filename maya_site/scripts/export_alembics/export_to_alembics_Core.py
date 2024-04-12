""" Functionality for window user interface to export selected objs to alembics.

@author Esteban Ortega <brutools@gmail.com>
"""

import os
import re
import sys
import time
import uuid
import pymel.core

from datetime import datetime
from maya import OpenMaya

from PySide2 import QtWidgets
from PySide2 import QtCore

from export_to_alembics_UI import ExportToAlembicUI
from custom_message_UI import CustomMsgBoxUI

class ExportToAlembicCore(ExportToAlembicUI):
    """ Class with functionality to export to alembics, using UI.
    """
    
    ## List of all asset types available.
    # tpe: []
    _ASSETTYPES = ['char',
                   'env',
                   'props',
                   'crowd',
                   'fx',
                   'masterCamera',
                   'subAsset' ]

    ## List of all steps available.
    # type: []
    _STEPS = ['mdl',
              'mcp',
              'rig',
              'grm',
              'tex',
              'ldv',
              'trk',
              'lyt',
              'anm',
              'cfx',
              'lgt',
              'crw',
              'sfx',
              'mtp'
             ]

    ## This is the pattern for version folders.
    # type: regex
    _VERSION_PATTERN = re.compile(r'^[0-9]{3}$')

    ## This is the pattern for shot.
    # type: regex
    _SHOT_PATTERN = re.compile(r'^([0-9]{4}[A-Z])$|^([0-9]{4})$')

    # # This part is to create a singleton. DOES NOT WORK
    # ############################################################################
    # _instancce = None

    # def __new__(self, parent=None):
    #     if not self._instancce:
    #         self._instancce = super(ExportToAlembicCore, self).__new__(self, parent=parent)
        
    #     return self._instancce
    # ############################################################################


    def __init__(self, parent=None):
        super(ExportToAlembicCore, self).__init__(parent=parent)

        ########################################################################
        # Defining some variables, which will be set accordingly.
        ########################################################################
        # Stores the current selection.
        self.selection = pymel.core.ls(selection=True)

        # Creates a path based on file name and sets 
        # self.destination_path variable
        self.create_path_from_file_name()

        # Set label based on self.destination_path variable.
        self.set_label_with_path()

        # Gets and sets variables start_time and end_time.
        self.get_start_end_from_time_slider()

        ########################################################################
        self.at_launch_tool()

        ########################################################################
        # Connect a function to SelectionChange callback
        ########################################################################
        self.selection_changed_callback = OpenMaya.MEventMessage.addEventCallback("SelectionChanged", self.on_selection_change)

        ########################################################################
        # Connect signals
        ########################################################################
        self.time_slider_radioButton.toggled.connect(self.on_time_slider_toggled)
        self.end_lineEdit.textChanged.connect(self.on_end_text_change)
        self.start_lineEdit.textChanged.connect(self.on_start_text_change)
        self.browse_button.clicked.connect(self.on_browse_clicked)
        
        self.exportToAlembic_buttonBox.clicked.connect(self.on_button_clicked)

        self.alembic_per_selection_checkBox.stateChanged.connect(self.on_checkBox_change)
    
    def load_AbcExport_plugin(self):
        """ Load AbcExport Alembics, if it is not loaded yet.
        """

        if not pymel.core.pluginInfo('AbcExport.mll', query = True, loaded = True):
            try:
                pymel.core.loadPlugin('AbcExport.mll')
            except RuntimeError:
                raise RuntimeError("There is no plugin AbcExport to load")
        
        return

    def on_checkBox_change(self, signal):
        """ Excecutes when checkBox change.
        """

        if signal == 0:
            self.alembic_per_selection_checkBox.setText('Create one Alembic for selected / if names do not clash')
        else:
            self.alembic_per_selection_checkBox.setText('Create Alembic file per selection')
        
        return

    def at_launch_tool(self):
        """ Executes when tool is launched!.
        """

        if self.check_variables_settings():
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        
            if self.check_adi_root_folder():
                self.publish_button.setEnabled(True)

        return

    def on_cancel(self):
        """ Executes when cancel button is pressed.
        """
        # Remove callback
        try:
            OpenMaya.MMessage.removeCallback(self.selection_changed_callback)
            self.close()
        except RuntimeError:
            self.close()

        return

    def on_selection_change(self, *args, **kwargs):
        """ Triggers when selection change during the use of the tool.
        """

        self.selection = pymel.core.ls(selection=True)

        if not self.selection:
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            self.publish_button.setEnabled(False)

        if self.check_variables_settings():
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
            
            if self.check_adi_root_folder():
                self.publish_button.setEnabled(True)

        return

    def get_current_file_name(self):
        """ Get current file name.
        Return:
            String representing the current file name.
        """

        full_path_name = pymel.core.system.sceneName()
        # full_path_name = 'D:/TheCompleteStuff/TMEFX_Docs/Work_Done/Folder_Structure/tmefx_test/0011/0030/lyt/workFile/000_005/0011_0030_lyt_wf_000_005.ma'
        file_name = os.path.basename(full_path_name)

        return os.path.splitext(file_name)[0]

    def check_variables_settings(self):
        """ Checks if there is a selection, start and end frame, and destination
        path to enabled or disabled the OK button.
        Return:
            True if all variables are set False otherwise.
        """

        if self.selection and self.start_time and self.end_time and self.destination_path:
            return True

        return False

    def on_time_slider_toggled(self, signal):
        """ Executes when radio button is toggled.
        """

        if not signal:
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            self.start_lineEdit.setEnabled(True)
            self.end_lineEdit.setEnabled(True)

            self.publish_button.setEnabled(False)

            return
        
        self.get_start_end_from_time_slider()

        self.start_lineEdit.clear()
        self.end_lineEdit.clear()

        self.start_lineEdit.setEnabled(False)
        self.end_lineEdit.setEnabled(False)

        if self.check_variables_settings:
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

            if self.check_adi_root_folder():
                self.publish_button.setEnabled(True)

        return

    def on_end_text_change(self, end_time):
        """ Execute when text change in QLineEdit.
        Args:
            end_time: String representing the end time.
        """

        start_time = self.start_lineEdit.text()

        if end_time == '' or start_time == '':
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            self.publish_button.setEnabled(False)

            return

        if int(end_time) >= int(start_time) and self.check_variables_settings():
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        
            if self.check_adi_root_folder(): 
                self.publish_button.setEnabled(True)

            return
        
        self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.publish_button.setEnabled(False)

        return

    def on_start_text_change(self, start_time):
        """ Execute when text change in QLineEdit.
        Args:
            start_time: String representing the start_time.
        """

        end_time = self.end_lineEdit.text()

        if end_time == '' or start_time == '':
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
            self.publish_button.setEnabled(False)
            
            return

        if int(start_time) <= int(end_time) and self.check_variables_settings():
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

            if self.check_adi_root_folder():
                self.publish_button.setEnabled(True)

            return
        
        self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.publish_button.setEnabled(False)

        return

    def create_path_from_file_name(self):
        """ Create path from file name.
        """

        file_name = self.get_current_file_name()
        file_name_parts = file_name.split('_')

        root_folder = os.path.expandvars('%ADI_ROOT_FOLDER%')

        if len(file_name_parts) < 4:
            self.destination_path = None
            self.publish_path = None

            return None
        
        elif len(file_name_parts) == 5:
            # Check parts to make sure it is the context.
            seq, shot, step, wf, version = file_name_parts

            valid_sq = self._SHOT_PATTERN.search(seq)
            valid_shot = self._SHOT_PATTERN.search(shot)
            valid_step = step in self._STEPS
            valid_wf = wf == 'wf'
            valid_version = self._VERSION_PATTERN.search(version)

            if valid_sq and valid_shot and valid_version and wf=='wf' and valid_step:
                
                path_created = os.path.join(root_folder, 
                                            seq, 
                                            shot, 
                                            step, 
                                            'workFile', 
                                            version, 
                                            'alembics')
                
                self.destination_path = path_created.replace('\\', '/')

                if not os.path.exists(self.destination_path):
                    os.makedirs(self.destination_path)
                
                publish_path = os.path.join(root_folder, 
                                            seq, 
                                            shot, 
                                            step,  
                                            'published',
                                            version)
                
                self.publish_path = publish_path.replace('\\', '/')

                if not os.path.exists(self.publish_path):
                    os.makedirs(self.publish_path)

                return None

        elif len(file_name_parts) == 6:
             # Check parts to make sure it is the context.
             assets, assetType, assetName, step, wf, version = file_name_parts

             valid_assets = assets == 'assets'
             valid_assetType = assetType in self._ASSETTYPES
             valid_step = step in self._STEPS
             valid_wf = wf == 'wf'
             valid_version = self._VERSION_PATTERN.search(version)

             if valid_assets and valid_assetType and valid_step and valid_wf and valid_version:

                path_created = os.path.join(root_folder, 
                                            assetType,
                                            assetName,
                                            step,
                                            'workFile',
                                            version,
                                            'alembics')
                
                self.destination_path = path_created.replace('\\', '/')
                
                if not os.path.exists(self.destination_path):
                    os.makedirs(self.destination_path)
                
                publish_path = os.path.join(root_folder, 
                                            assetType,
                                            assetName,
                                            step,
                                            'published',
                                            version)
                
                self.publish_path = publish_path.replace('\\', '/')
                
                if not os.path.exists(self.publish_path):
                    os.makedirs(self.publish_path)

                return None

        self.destination_path = None
        self.publish_path = None

        return None

    def on_browse_clicked(self):
        """ Executes when browse button is clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     "Select directory", 
                                                                     "", 
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.destination_path = selected_path.replace('\\', '/')
        
        if self.destination_path == '':
            
            # If cancel set again the original path, which sets self.destination_path
            self.create_path_from_file_name()
            self.set_label_with_path()

            if self.check_variables_settings():
                self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

                if self.check_adi_root_folder():
                    self.publish_button.setEnabled(True)

            else:
                self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
                self.publish_button.setEnabled(False)

            return

        self.set_label_with_path()

        if self.check_variables_settings:
            self.exportToAlembic_buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

            if self.check_adi_root_folder():
                self.publish_button.setEnabled(True)

        return

    def set_label_with_path(self):
        """ Set in label the destination path.
        """

        root_folder = os.path.expandvars('%ADI_ROOT_FOLDER%')

        if self.destination_path is None:
            
            msg = 'No context found in file name!.\nSelect a destination folder!'
            self.message_label.setText(msg)
        
            return
        
        if self.check_adi_root_folder():
            msg = 'Root destination directory:\n{}'.format(self.destination_path[len(root_folder):])        
            self.message_label.setText(msg)

            return
        
        msg = 'NOT Root destination directory:\n{}'.format(self.destination_path)        
        self.message_label.setText(msg)

        return

    def check_adi_root_folder(self):
        """ Checks if self.destination_path is part of the root folder. 
        """

        root_folder = os.path.expandvars('%ADI_ROOT_FOLDER%')
        root_folder_reformat = root_folder.replace('\\', '/')
        
        destination_root_folder = self.destination_path[:len(root_folder)]

        if root_folder_reformat == destination_root_folder:
            return True
        
        return False

    def get_start_end_from_time_slider(self):
        """ Gets the start time and end time from current time slider, and set
        its corresponding variables.
        Return:
            tuple containg start and end time (1001, 1015).
        """

        self.start_time = pymel.core.playbackOptions(q=True, minTime=True)
        self.end_time = pymel.core.playbackOptions(q=True, maxTime=True)

        return self.start_time, self.end_time

    def get_start_end_time_from_ui(self):
        """ Gets start and end time from UI.
        Return:
            tuple containg start and end time (1001, 1015). 
        """

        self.start_time = int(self.start_lineEdit.text())
        self.end_time = int(self.end_lineEdit.text())

        return self.start_time, self.end_time
    
    def on_button_clicked(self, signal):
        """ Creates the root part of the export command using the 
        selected objects.
        Return:
            String representing the root part of the command.
            (eg. -root |pCube1 -root |pSphere1 -root |pSphere2)
        
        "AbcExport -j "-frameRange 1 1 -dataFormat ogawa -root |pCube1 -root |pSphere1 -root |pSphere2 -file C:/Users/bru_n/OneDrive/Escritorio/Alembics/Test_export.abc";"
        """

        if signal.text() == 'Cancel':
            self.on_cancel()
            
            return

        self.create_and_publish = False
        
        if signal.text() == 'Export and Publish':
            self.create_and_publish = True

        # Load AbcExport plugin.
        self.load_AbcExport_plugin()

        # Suspend refresh
        pymel.core.general.refresh(suspend=True)

        files_per_selection = self.alembic_per_selection_checkBox.isChecked()

        if not self.check_duplicate_object_names(self.selection):

            if files_per_selection:
                self.export_file_per_selection()

            else:
                self.export_one_file_for_all_selected()
        
        else:
            self.export_file_per_selection()
        
        # Enable refresh
        time.sleep(2)
        pymel.core.general.refresh(suspend=False)
                
        # Remove callback
        OpenMaya.MMessage.removeCallback(self.selection_changed_callback)

        CustomMsgBoxUI(self.destination_path, parent=self)

        self.close()

        return

    def export_command(self, name_from_namespace, root_string, camera=None):
        """ Exceutes the actual export based on passed data.
        Args:
            name_from_namespace: String representing the selected object.
            root_string: String representing the -root part of command.
            camera: String representing the name of the folder for cameras.
        """

        alembic_options = '-frameRange {} {} -stripNamespaces -uvWrite -worldSpace -writeUVSets -step 1 -dataFormat ogawa {} -file {}'

        output_file_name = '{}.abc'.format(name_from_namespace)
        if camera is None:
            full_path_destination_dir = '{}/{}'.format(self.destination_path, output_file_name)
        else:
            full_path_destination_dir = '{}/{}/{}'.format(self.destination_path, camera, output_file_name)
            if not os.path.exists(os.path.dirname(full_path_destination_dir)):
                os.makedirs(os.path.dirname(full_path_destination_dir))

        command_formatted = alembic_options.format(self.start_time,
                                                    self.end_time,
                                                    root_string,
                                                    full_path_destination_dir)

        pymel.core.AbcExport(j=command_formatted)  

        # If Export and Publish is clicked.
        if self.create_and_publish:
            self.copy_into_publish_path(full_path_destination_dir, camera)
 
        return

    def copy_into_publish_path(self, full_file_path, camera):
        """ Copies created alembic file into published path.
        Args:
            full_file_path: String representing the full file path name.
            camera: String 'camera' if full_file_path is a camera, None otherwise
        """

        file_name = os.path.basename(full_file_path)

        if camera is None:
            destination_path = os.path.join(self.publish_path, file_name)
        
        else:
            destination_path = os.path.join(self.publish_path, camera, file_name)
            destination_path_dir = os.path.dirname(destination_path)

            if not os.path.exists(destination_path_dir):
                os.makedirs(destination_path_dir)

        destination_path_reformat = destination_path.replace('/', '\\')
        full_file_path_reformat = full_file_path.replace('/', '\\')

        os.popen('copy {} {}'.format(full_file_path_reformat, destination_path_reformat))

        return
    
    def export_one_file_for_all_selected(self):
        """ Exports all selected files under one alembic file.
        """
        
        root_string = ''
        name_from_namespace = ''

        for name in self.selection:
            root_string += ' -root {}'.format(name.name())
            name_from_namespace = self.get_name_for_alembic_file(name)

        self.export_command(name_from_namespace, root_string)

        return

    def export_file_per_selection(self):
        """ Export one alembic per selection.
        """
                
        root_string = ''
        name_from_namespace = ''

        for name in self.selection:
            camera_folder = None

            if isinstance(name.getShape(), pymel.core.nodetypes.Camera):
                camera_folder = 'camera'

            root_string = ' -root {}'.format(name.name())
            name_from_namespace = self.get_name_for_alembic_file(name)

            self.export_command(name_from_namespace, root_string, camera=camera_folder)
        
        return
    
    def get_name_for_alembic_file(self, selection):
        """ Gets the namespace from selection.
        Args:
            selection: Is an object pymel.core.nodetypes.Transform.
        
        Return:
            String representing the selected object.
        """

        file_name = ''
        if ':' in selection.name():
            file_name = selection.name().split(':')[0]

            return file_name

        elif '|' in selection.name():
            file_name = ''.join(selection.name().split('|'))

            return file_name
        
        else:
            return selection.name()
        
        return

    def check_duplicate_object_names(self, selection):
        """ Checks if there is duplicate names in passed selection.

        Return:
            True if there are duplicates, False otherwiese.
        """

        names = []

        for object in selection:
            
            if ':' in object:
                names.append(object.split(':')[-1])
            
            elif '|' in selection:
                names.append(object.split('|')[-1])

            else:
                names.append(object)
        
        for name in names:
            if names.count(name) > 1:
                return True

        return False
    
    def show_info_msg(self, msg):
        """ Creates a generic msg box with ok button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 
                                                 'Information',
                                                 msg, 
                                                 QtWidgets.QMessageBox.Ok)

    def get_date_time_str(self):
        """ Creates a string representing date time in a more readable way.
        Returns:
            String representing date time formated as month-day-year hours:minutes
            (eg. 06Jun_h1245)
        """

        today = datetime.today()

        return today.strftime("%d%b_h%H%M")
    
    def show_decision_msg(self, msg):
        """ Creates a generic msg box with ok button and cancel button.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Confirm action',
            msg, QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)


def launch_export_to_alembic():
    """ Launch export to alembic UI.
    """
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = ExportToAlembicCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)
    # w.exec_()
    w.show()
    
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = ExportToAlembicCore()
    w.show()
    app.exec_()
