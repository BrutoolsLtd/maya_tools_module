import os
import re
import sys
import logging

import maya.cmds as cmd
import maya.mel

from PySide2 import QtWidgets
from jobin_UI import JobInUI


class JobInCore(JobInUI):
    """ Class with methods to work with jobin information.
    """

    ## Folder under version for tex step.
    # type: []
    _TEX_FOLDERS = ['mari', 
                    'maya', 
                    'substance', 
                    'textures']

    ## Stores steps related to a process. 
    # type: dict
    _STEPS = {'modeling': 'mdl',
             'mocap': 'mcp',
             'rigging': 'rig',
             'groom': 'grm',
             'texturing': 'tex',
             'lookdev': 'ldv',
             'matchmove': 'trk',
             'layout': 'lyt',
             'animation': 'anm',
             'cfx': 'cfx',
             'lighting': 'lgt',
             'crowd': 'crw',
             'simfx': 'sfx',
             'mattepaint': 'mtp'}
    
    ## Store the name of the folder used for set maya project
    # type: str
    _SET_PROJECT_FOLDER = 'set_project'

    ## This is the pattern for version folders.
    # type: regex
    _VERSION_PATTERN = re.compile(r'^[0-9]{3}$')

    ## This is the pattern for shot.
    # type: regex
    _SHOT_PATTERN = re.compile(r'^([0-9]{4}[A-Z])$|^([0-9]{4})$')

    ## Regex to replace version for folder an file name '000' in full path maya file.
    # type: regex
    _REGEX_VERSION = re.compile(r'(?<=[\\_])[0-9]{3}(?=[\\.])')

    def __init__(self):
        super(JobInCore, self).__init__()

        self.populate_shotAsset_ComboBox()
        ########################################################################
        # Connect signals
        ########################################################################
        self.shot_radioButton.clicked.connect(self.on_shot_radioButton_clicked)
        self.asset_radioButton.clicked.connect(self.on_assets_radioButton_clicked)

        self.step_comboBox.currentTextChanged.connect(self.on_step_comboBox_changed)
        self.shotAsset_comboBox.currentTextChanged.connect(self.on_shotAsset_comboBox_changed)
        self.version_comboBox.currentTextChanged.connect(self.on_version_comboBox_changed)
        self.maya_files_comboBox.currentTextChanged.connect(self.on_maya_file_comboBox_changed)
        self.jobin_buttonBox.clicked.connect(self.on_buttonBox_button_clicked)
    
    def on_buttonBox_button_clicked(self, button):
        """ Excutes when a button is clicked.
        """
        button_text = button.text()

        if button_text == 'Create version':
            self.on_create_version()
        
        elif button_text == 'Open version':
            self.on_open_version_clicked()

        return        

    def on_create_version(self):
        """ Execute when create version button is clcked.
        """

        logging.debug('{} this is the path to create'.format(self.current_full_path_to_step))

        selected_version = self.version_comboBox.currentText()
        last_version = self.get_last_version_from_comboBox()

        #TODO: Check if next can be simplified, as first 2 contains same code.
        if selected_version == 'Select version':
            # use last version
            next_version = self.create_next_version_string(last_version)
            new_version_directory = self.create_dir_per_step(self.current_full_path_to_step, next_version, self.step)
            new_maya_file_name = self.create_maya_file_name(next_version)

            # Create maya file.
            self.create_maya_file(new_maya_file_name, new_version_directory.get('maya'))

            self.show_info_msg('Version {} created'.format(next_version))

            self.close()

        elif selected_version == '':
            next_version = '001'
            new_version_directory = self.create_dir_per_step(self.current_full_path_to_step, next_version, self.step)
            new_maya_file_name = self.create_maya_file_name(next_version)

            # Create maya file.
            self.create_maya_file(new_maya_file_name, new_version_directory.get('maya'))

            self.show_info_msg('Version {} created'.format(next_version))

            self.close()

        else:
            # Use selected file to be copied.
            file_name = self.maya_files_comboBox.currentText()

            if file_name == 'Select file':
                self.show_info_msg('Select a maya file to based your next version')
                
                return
            
            next_version = self.create_next_version_string(last_version)
            new_version_directory = self.create_dir_per_step(self.current_full_path_to_step, next_version, self.step)

            source_full_path_name = self.maya_files_comboBox.currentData()
            destination_path_name = self._REGEX_VERSION.sub(next_version, source_full_path_name)
            
            logging.debug('Source directory: {}, Destination directory: {}'.format(source_full_path_name, destination_path_name))
            
            os.popen('copy {} {}'.format(source_full_path_name, destination_path_name))
            
            msg = 'Version {} created based on {}!'.format(next_version, selected_version)
            self.show_info_msg(msg)
            
            cmd.file(destination_path_name, o=True, force=True)

            self.set_maya_project(destination_path_name)

            self.close()

        return

    def create_dir_per_step(self, base_path, version, step):
        """ Creates directories based on step selected.
        Args:
            base_path: String representing the based path where to start,
            self.current_full_path_to_step points to path up to workFile
            version: String representing the version to be created.
            step: String representing the selected step.
        Returns:
            Dictionary with folders as a key and path as value, 
        """

        version_path = os.path.join(base_path,version)

        new_folder = {}

        if not os.path.exists(version_path):
            os.makedirs(version_path)
        
        if step == 'tex':

            for folder in self._TEX_FOLDERS:
                
                additional_path = os.path.join(version_path, folder)

                if not os.path.exists(additional_path):
                    os.makedirs(additional_path)
                
                new_folder[folder] = additional_path

        else:

            if not os.path.exists(version_path):
                os.makedirs(version_path)

            new_folder['maya'] = version_path

        return new_folder

    def create_maya_file(self, fileName, path):
        """ Creates maya file.
        Args:
            fileName: String representing the selected maya file.
            path: String representing the destination for the maya file to reside.
        Returns:
            None value.
        """

        full_path_name = os.path.join(path, fileName)
        reformat_path = full_path_name.replace('\\', '/')

        cmd.file(new=True, force=True)
        cmd.file(rename=reformat_path)
        cmd.file(save=True)

        #Set maya project to here
        self.set_maya_project(reformat_path)

        return

    def set_maya_project(self, full_path):
        """Sets maya project based on full path directory passed. 
        Args:
            full_path: String representing the full path.
        """

        full_path_dir = os.path.dirname(full_path)
        full_path_dir_reformat = full_path_dir.replace('\\', '/')

        if not self.step == 'grm':
            maya.mel.eval('setProject "{}"'.format(full_path_dir_reformat))

            return
        
        workFile_dir = os.path.dirname(full_path_dir_reformat)
        worFile_dir_set_project = os.path.join(workFile_dir, self._SET_PROJECT_FOLDER)
        worFile_dir_set_project = worFile_dir_set_project.replace('\\', '/')

        if not os.path.exists(worFile_dir_set_project):
            os.makedirs(worFile_dir_set_project)
        
        maya.mel.eval('setProject "{}"'.format(worFile_dir_set_project))

        return

    def show_confirm_box(self, msg):
        """ Creates a generic msg box with cancel, ok buttons.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Confirm action',
            msg, QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

    def show_info_msg(self, msg):
        """ Creates a generic msg box with cancel, ok buttons.
        Args:
            msg: String representing the msg for the user.
        Returns:
            PySide Message box.
        """

        return QtWidgets.QMessageBox.information(self, 'Information',
            msg, QtWidgets.QMessageBox.Ok)


    def create_maya_file_name(self, version, file_name=None):
        """ Creates maya file name string with passed version.
        Args:
            file_name: String representing the selected maya file name to based 
            the new version.
            version: String representing the version of the file.
        Return:
            String representing the maya file name formatted.
        """

        if file_name is None:
            # Get all details from UI, then create the name and return.
            logging.debug('context: {}, shotAsset: {}, step: {}'.format(self.context,
                                                                        self.shotAsset,
                                                                        self.step))

            if self.context == 'shot':
                seq, shot = self.shotAsset.split('_')

                file_name = '{}_{}_{}_wf_{}.ma'.format(seq, shot, self.step, version)
                logging.debug('New maya file name: {}'.format(file_name))

            else:
                assetName, assetType = self.shotAsset.split(':')

                file_name = 'assets_{}_{}_{}_wf_{}.ma'.format(assetType, assetName, self.step, version)
                logging.debug('New maya file name: {}'.format(file_name))
            
            return file_name
            
        # Replacing version in maya file name.
        splitted_file_name, ext = file_name.split('.')
        name_parts = splitted_file_name.split('_')
        name_parts[len(name_parts)-1] = version

        new_name_vesion = '{}.{}'.format('_'.join(name_parts), ext)
        logging.debug('New maya file name, with new version: {}'.format(new_name_vesion))

        return new_name_vesion

    def create_next_version_string(self, version):
        """ Creates a new version string based on passed version string.
        Args:
            version: Is a string representing an existing version, (eg. '010').
        Return:
            string: Representing the new version, (eg. '011, 002, 001).
        """

        next_version = '{:0>3d}'.format(int(version) + 1)
        
        return next_version

    def get_last_version_from_comboBox(self):
        """ Gets the last version from version comboBox.
        Return:
            string: Representing the last version in selection.
        """

        last_version = ''

        for index in range(1, self.version_comboBox.count()):

            if self.version_comboBox.itemText(index) > last_version:
                last_version = self.version_comboBox.itemText(index)

        return last_version

    def on_maya_file_comboBox_changed(self, fileName):
        """ Executes when comboBox change.
        """

        if fileName == 'Select file' or fileName == '':
            self.jobin_buttonBox.button(self.openVersion_buttonBox).setEnabled(False)

        else:
            self.jobin_buttonBox.button(self.openVersion_buttonBox).setEnabled(True)

        return

    def on_open_version_clicked(self):
        """ Execute when open version button box clicked.
        """

        full_path = self.maya_files_comboBox.currentData()
        cmd.file(full_path, o=True, force=True)

        self.set_maya_project(full_path)

        self.close()

        return

    def is_maya_file(self, file):
        """ Filters the passed file to only show maya files, mb, ma.
        Args:
            file: string representing the file name to check.
        Return:
            String representing the name of the file if it is a mb, ma. None
            otherwise.
        """

        logging.debug(file)
        
        file_ext = file.split('.')

        logging.debug('{}'.format(file_ext[-1]))

        if file_ext[-1] in ['ma', 'mb']:
            
            logging.debug('{} is of the form ma or mb'.format(file_ext[-1]))
            return file

        logging.debug('{} file name'.format(file))

        return None

    def populate_maya_file_comboBox(self, version):
        """ Populates maya_file_comboBox with maya files under selected version.
        Args:
            version: String representing the selected version.
        """

        self.maya_files_comboBox.clear()
        self.maya_files_comboBox.addItem('Select file')

        if self.step == 'tex':
            current_path_version = os.path.join(self.current_full_path_to_step, version, 'maya')

        else:
            current_path_version = os.path.join(self.current_full_path_to_step, version)

        for file in os.listdir(current_path_version):
            logging.debug('{} file in version folder'.format(file))

            if self.is_maya_file(file) is not None:
                logging.debug('{} is maya file'.format(file))
                full_path_to_file = os.path.join(current_path_version, file)
                self.maya_files_comboBox.addItem(file, full_path_to_file)

        return
    
    def on_version_comboBox_changed(self, version):
        """ Execute when version comboBox changes.
        """

        if version == 'Select version' or version == '':
            # self.openVersion_button.setEnabled(False)
            self.maya_files_comboBox.clear()
            self.maya_files_comboBox.setEnabled(False)

            return

        else:
            self.maya_files_comboBox.setEnabled(True)
            logging.debug('Populating maya file comboBox')
            #TODO: Create another definition for populating combobox with
            # file name and path to maya file.
            self.populate_maya_file_comboBox(version)
            self.path_to_version = os.path.join(self.current_full_path_to_step, version)
            logging.debug('{} path to selected version'.format(self.path_to_version))
            # self.openVersion_button.setEnabled(True) # Only if there is a file under version.

        return
    
    def on_step_comboBox_changed(self, step):
        """ Excutes when step comboBox changes.
        Args:
            step: Represent the selected element in step comboBox.
        """
        context = self.shotAsset_comboBox.currentText()

        self.step = step

        if step == 'Select step':

            self.version_comboBox.clear()
            self.version_comboBox.setEnabled(False)

            self.jobin_buttonBox.button(
                QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

            return
        
        # Enable Create button box.
        self.jobin_buttonBox.button(
            QtWidgets.QDialogButtonBox.Ok).setEnabled(True)
        
        # 2. Create path using data.
        full_path = self.create_path_from_data(context, step)
        logging.debug('{} this is the full path to step'.format(full_path))
        
        version_dirs = []

        if full_path is None: 
            self.version_comboBox.clear()
            self.version_comboBox.setEnabled(False)
        
        elif os.path.exists(full_path):
            for fileDir in os.listdir(full_path):
                search_version_folder = self._VERSION_PATTERN.search(fileDir)                

                if not os.path.isfile(fileDir) and search_version_folder:
                    version_dirs.append(fileDir)

        if version_dirs:
            self.version_comboBox.clear()
            self.version_comboBox.setEnabled(True)
            self.version_comboBox.addItem('Select version')
            self.version_comboBox.addItems(version_dirs)

        else:
            self.version_comboBox.clear()
            self.version_comboBox.setEnabled(False)

        return

    def create_path_from_data(self, context, step):
        """ Creates a path up to workFile folder based on passed data.
        Args:
            context: String representing a seq_shot (eg. 0010_0020) or
            an assetName:assetType (eg. vaaliA:char).
            step: String representing the step selected.
        Return:
            String representing the constructed path.
        """

        if context in ['Select shot', 'Select asset','']:
            
            return

        shotAsset = context.split(':')
        seq = None

        if len(shotAsset) == 1:
            seq, shot = context.split('_')

        else:
            assetName, assetType = shotAsset        
        
        root_dir = os.path.expandvars('%ADI_ROOT_FOLDER%')

        if seq:
            full_path = os.path.join(root_dir, seq, shot, step, 'workFile')
            full_path_norm = os.path.normpath(full_path)
            self.current_full_path_to_step = full_path_norm

        else:
            full_path = os.path.join(root_dir, 'assets', assetType, assetName, step, 'workFile')
            full_path_norm = os.path.normpath(full_path)
            self.current_full_path_to_step = full_path_norm

        return full_path_norm

    def on_shotAsset_comboBox_changed(self, signal):
        """ Executes when shotAsset comboBox changed.
        """

        if self.shot_radioButton.isChecked():           
            self.context = 'shot'

        else:
            self.context = 'asset'
        
        if signal == 'Select {}'.format(self.context):
            self.step_comboBox.clear()
            self.step_comboBox.setEnabled(False)
            
            return
        
        self.shotAsset = signal
        self.step_comboBox.setEnabled(True)
        self.step_comboBox.clear()
        self.populate_stepComboBox()

        return

    def on_shot_radioButton_clicked(self):
        """ Excutes when radio buttons is clicked.
        """

        self.populate_shotAsset_ComboBox()

        return

    def on_assets_radioButton_clicked(self):
        """ Excutes when radio buttons is clicked.
        """

        self.populate_shotAsset_ComboBox()

        return

    def populate_versions_comboBox(self, signal):
        """ Add version of selected shot, asset if any.
        """

        if signal == 'Select step':
            self.version_comboBox.clear()
            self.version_comboBox.setEnabled(False)

            return

        self.version_comboBox.setEnabled(True)
        self.version_comboBox.clear()
        self.version_comboBox.addItem('Select a version')

        version = self.get_versions(signal)

        if version is None:
            return

        return

    def get_versions(self, step):
        """ Gets all versions if any under the passed step.
        Args:
            step: string representing the steps under which we want the 
            versions.
        """

        asset_shot = self.shotAsset_comboBox.currentText()

        if self.shotAsset_comboBox.currentText() == 'Select shot':
            return

        return

    def populate_stepComboBox(self):
        """ Add steps to comboBox.
        """

        self.step_comboBox.clear()
        self.step_comboBox.addItem('Select step')

        steps = self._STEPS.values()
        steps.sort()
        self.step_comboBox.addItems(steps)

        return
    
    def populate_shotAsset_ComboBox(self):
        """ Populate shotAsset comboBox. 
        """

        if self.shot_radioButton.isChecked():

            self.populate_shots_comboBox()
        
            return

        self.populate_assets_comboBox()

        return

    def populate_shots_comboBox(self):
        """ Add seq_shot to comboBox.
        """

        self.shotAsset_comboBox.clear()
        self.shotAsset_comboBox.addItem('Select shot')

        shots_dir = self.get_shots()

        for seq, shots in shots_dir.items():

            if shots:

                for shot in shots:

                    compound_shot = '{}_{}'.format(seq, shot)

                    self.shotAsset_comboBox.addItem(compound_shot)

        return
    
    def get_shots(self):
        """ Populate with shots comboBox.
        """

        root_folder = os.path.expandvars('%ADI_ROOT_FOLDER%')

        shots_directory = {}

        for folder in os.listdir(root_folder):
            search_sq = self._SHOT_PATTERN.search(folder)

            if search_sq is None:

                continue

            seq_dir = os.path.join(root_folder, folder)
            shots_dir = []

            for shot_dir in os.listdir(seq_dir):
                search_shot = self._SHOT_PATTERN.search(shot_dir)

                if search_shot is None:

                    continue
            
                shots_dir.append(shot_dir)
            
            shots_directory[folder] = shots_dir

        return shots_directory

    def populate_assets_comboBox(self):
        """ Populate comboBox with assets.
        """

        self.shotAsset_comboBox.clear()
        self.shotAsset_comboBox.addItem('Select asset')

        assetTypes = self.get_assetTypes()

        for assetType, assetNames in assetTypes.items():

            if assetNames:

                for asset_name in assetNames:

                    compound_name = '{}:{}'.format(asset_name, assetType)

                    self.shotAsset_comboBox.addItem(compound_name)

        return    

    def get_assetTypes(self):
        """ Gets asset types and asset names in a dictionary.
        """

        self.get_asset_types()

        assets = {}

        for asset_type in self.asset_types:     
            current_dir = os.path.join(self.get_assets_directory(), asset_type)
            subdir = []

            for item in os.listdir(current_dir):
                item_path = os.path.join(current_dir, item)

                if os.path.isfile(item_path):
                    continue
                else:
                    subdir.append(item)
            
            assets[asset_type] = subdir

        return assets
    
    def get_asset_types(self):
        """ Gets only asset types present in folder structure.
        """
        asset_dir = self.get_assets_directory()
        self.asset_types = None

        for dirpath, dirnames, files in os.walk(asset_dir):
            self.asset_types = dirnames

            return

    def get_assets_directory(self):
        """ Gets assets directory from project root folder.
        """

        root_dir = os.path.expandvars('%ADI_ROOT_FOLDER%')
        
        return os.path.join(root_dir, 'assets')


def launch_jobinCore():
    """ Launch the jobIn window.
    """
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s'
    date_string = "%d/%m/%Y %I:%M %p"
    logging.basicConfig(level=logging.DEBUG,
                        format=fmtstr,
                        datefmt=date_string)
    w = JobInCore()
    w.exec_()

    return

if __name__ == '__main__':
    
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s'
    date_string = "%d/%m/%Y %I:%M %p"
    logging.basicConfig(level=logging.DEBUG,
                        format=fmtstr,
                        datefmt=date_string)

    app = QtWidgets.QApplication(sys.argv)
    w = JobInCore()
    w.show()
    app.exec_()
