""" Functionality for window user interface to set user name and 
path for playblast.

@author Esteban Ortega <brutools@gmail.com>
"""

import getpass
import json
import os
import pymel.core
import sys

import hud_names_constants

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

from setting_user_path_UI import SetUserPathUI

class SetUserPathCore(SetUserPathUI):
    """ Funcionality for set user name and path for playblast.
    """

    def __init__(self, parent=None):
        super(SetUserPathCore, self).__init__(parent=parent)

        ## Store the destination path selected.
        # type: str
        self.playblast_directory = None

        ## Store the user settings dictionary.
        # type: {}
        self.user_settings = self.get_user_path_settings()

        ########################################################################
        # Execute at start up.
        ########################################################################
        self.update_path_user_label()

        ########################################################################
        # Connect signals
        ########################################################################
        self.set_user_path_buttonBox.rejected.connect(self.close)
        self.browse_button.clicked.connect(self.on_select_directory)
        self.user_name_lineEdit.textChanged.connect(self.on_text_changed)

        self.set_user_path_buttonBox.accepted.connect(self.on_set_clicked)
    
    def on_text_changed(self, text):
        """ Update current_user text changed.
        """

        if text == '':
            if self.user_settings:
                dir_user = 'Current User: {}'.format(self.user_settings.get('user_name'))

            else:    
                dir_user = 'Current User: {}'.format(getpass.getuser())

            self.current_user.setText(dir_user)

            return
        
        user_text = 'Will set user name: {}'.format(text)
        self.current_user.setText(user_text)

        return
    
    def get_user_path_settings(self):
        """ Gets user name and directory path from json.
        Return:
            Dictionary {'user_name': 'Name', 'playblast_path': '/ADI_project/0010...'}
        """

        if os.path.exists(self.get_full_path_for_json_file()):

            with open(self.get_full_path_for_json_file(), 'r') as settings:

                return json.load(settings)

        return None

    def get_full_path_for_json_file(self):
        """ Creates full path to full path to userSettings.json file.
        Return:
            String representing the full path to json file.
        """

        full_path_name = os.path.expandvars(hud_names_constants.USER_SETTINGS)
        full_path_name_reformatted = full_path_name.replace('\\', '/')

        return full_path_name_reformatted

    def create_userSettings_json_file(self, 
                                      user_name,
                                      dir_path):
        """ Creates userSettings.json file with passed information.
        Args:
            user_name: string representing the name of the user.
            dir_path: selected path to store playblast.
        """

        if self.user_settings:
            current_user_name = self.user_settings.get('user_name')
            current_playblast_path = self.user_settings.get('playblast_path')

            if user_name == '' and current_user_name != '':
                user_name = current_user_name
            
            elif user_name == '' and current_user_name == '':
                user_name = getpass.getuser()
            
            elif dir_path == '' and (current_playblast_path != '' or not current_playblast_path is None):
                dir_path = current_playblast_path
            
            elif dir_path == '' and (current_playblast_path == '' or current_playblast_path is None):
                dir_path = self.get_current_path()

            user_settings_dir = {'user_name': user_name,
                                'playblast_path': dir_path
                                }
        else:

            if user_name == '':
                msg = 'User name is missing!'
                self.show_info_dialog_box(msg)

                return
            
            if dir_path == '' or dir_path is None:
                msg = 'Directory missing for playblast!'
                self.show_info_dialog_box(msg)

                return
            
            user_settings_dir = {'user_name': user_name,
                                 'playblast_path': dir_path
                                }


        json_file = self.get_full_path_for_json_file()
        json_file_dir = os.path.dirname(json_file)

        if not os.path.exists(json_file_dir):
            os.makedirs(json_file_dir)

        with open(json_file, 'w') as settings:
            json.dump(user_settings_dir, settings)

        return True
    
    def update_path_user_label(self):
        """ Updates current path and current user labels.
        """

        # settings = self.get_user_path_settings()

        if self.user_settings is None:
            dir_label = 'Current Directory: {}'.format(self.get_current_path())
            dir_user = 'Current User: {}'.format(getpass.getuser())
        
        else:
            dir_label = 'Current Directory: {}'.format(self.user_settings.get('playblast_path'))
            dir_user = 'Current User: {}'.format(self.user_settings.get('user_name'))

            self.playblast_directory = self.user_settings.get('playblast_path')
            self.user_name = self.user_settings.get('user_name')
            self.user_name_lineEdit.setText(self.user_name)
        
        self.current_path.setText(dir_label)
        self.current_user.setText(dir_user)

        return

    def get_current_path(self):
        """ Get current path for playblast.
        (just for information purposes).
        """
 
        full_path_name = pymel.core.system.sceneName()
        dir_name = os.path.dirname(full_path_name)

        return os.path.join(dir_name, 'playblast')

    def on_set_clicked(self):
        """ Execute when set button is clicked.
        """

        user_name = self.user_name_lineEdit.text()

        if self.create_userSettings_json_file(user_name, self.playblast_directory) is None:

            return

        self.show_info_dialog_box('Playblast directory and user name set!')
    
        self.close()

        return

    def on_select_directory(self):
        """ Executes when select directory button clicked.
        """

        dialog_directory_widget = QtWidgets.QFileDialog()
        selected_path = dialog_directory_widget.getExistingDirectory(self, 
                                                                     "Select directory", 
                                                                     "", 
                                                                     QtWidgets.QFileDialog.Option.ShowDirsOnly)

        self.playblast_directory = selected_path.replace('\\', '/')

        if self.playblast_directory == '':
            self.playblast_diretory = self.get_current_path()
            dir_label = 'Current Directory: {}'.format(self.get_current_path())
            self.current_path.setText(dir_label)

            return
        
        self.current_path.setText('Will set Directory: {}'.format(self.playblast_directory))

        return

    def show_confirmation_message_box(self, msg):
        """ Creates a generic msg box with cancel, ok buttons.
        Args:
            msg: String representing the msg for the user.
        Returns:
            None value.
        """

        return QtWidgets.QMessageBox.information(self, 
                                                 'Confirm settings',
                                                 msg, 
                                                 QtWidgets.QMessageBox.Ok |
                                                 QtWidgets.QMessageBox.Cancel)
    
    def show_info_dialog_box(self, message):
        """ Shows dialog to confirm action with passed message.
        Args:
            message: String representing the message for dialog box.
        Return:
            None value.
        """

        updated_message_box = QtWidgets.QMessageBox(self)
        updated_message_box.setWindowTitle('Information')
        updated_message_box.setText(message)
        updated_message_box.show()

        return

def launch_set_user_path():
    """ Launch export to alembic UI.
    """
    from maya import OpenMayaUI as omui
    from shiboken2 import wrapInstance

    mayaMainWindowPtr = omui.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QWidget)

    w = SetUserPathCore(parent=mayaMainWindow)
    w.setWindowFlags(QtCore.Qt.Window)
    w.show()
    
    return

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = SetUserPathCore()
    w.show()
    app.exec_()
