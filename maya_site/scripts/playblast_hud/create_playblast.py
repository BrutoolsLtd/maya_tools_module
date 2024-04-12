""" Defines funcitons to create a playblast with custom Hud.

@author Esteban Ortega <brutools@gmail.com>
"""

import json
import os
import pymel

import hud_names_constants


class CreatePlayblast():
    """ Playblast class with methods to gather information for playblast.
    """

    def get_current_file_name_and_dir(self):
        """ Get current file name and directory.
        Return:
            tuple ('file name', 'dir') representing the current file name
            and directory where file resides.
        """

        full_path_name = pymel.core.system.sceneName()
        file_name = os.path.basename(full_path_name)

        settings = self.get_userSettings_settings_json()

        if settings is None:
            dir_name = os.path.dirname(full_path_name)
        else:
            dir_name = settings.get('playblast_path')

        return os.path.splitext(file_name)[0], dir_name

    def get_default_resolution(self):
        """ Gets resolution from render settings.
        Return:
            tuple representing the resolution (2048, 1156)
        """

        widht = pymel.core.getAttr('defaultResolution.width')
        height = pymel.core.getAttr('defaultResolution.height')

        return widht, height

    def playblast_write(self):
        """ Writes the playblast with the options gathered.
        """

        name, path = self.get_current_file_name_and_dir()
        
        if self.exists_userSettings_json():
            reformat_destination_dir = path.replace('\\', '/')

        else:
            destination_dir = os.path.join(path, 'playblast')
            reformat_destination_dir = destination_dir.replace('\\', '/')

        w, h = self.get_default_resolution()

        if not os.path.exists(reformat_destination_dir):
            os.makedirs(reformat_destination_dir)
        
        try:
            file_name = '{}.mov'.format(name)
            full_path = os.path.join(reformat_destination_dir, file_name)
            pymel.core.playblast(filename=full_path, 
                                 width=w, 
                                 height=h, 
                                 percent=100, 
                                 quality=100, 
                                 viewer=True, 
                                 format='qt',
                                 compression='H.264',
                                 forceOverwrite=True)

        except RuntimeError:
            file_name = '{}.avi'.format(name)
            full_path = os.path.join(reformat_destination_dir, file_name)
            pymel.core.playblast(filename=full_path, 
                                 width=w, 
                                 height=h, 
                                 percent=100, 
                                 quality=100, 
                                 viewer=True, 
                                 format='avi', 
                                 forceOverwrite=True)

        return
    
    def exists_userSettings_json(self):
        """ Check if userSettings json exists.
        """

        if os.path.exists(self.get_userSettings_full_path()):
            return True

        return False
    
    def get_userSettings_settings_json(self):
        """ Gets user name and directory path from json.
        Return:
            Dictionary {'user_name': 'Name', 'playblas_path': '/ADI_project/0010...'}
        """

        if self.exists_userSettings_json():

            with open(self.get_userSettings_full_path(), 'r') as settings:

                return json.load(settings)

        return None
    
    def get_userSettings_full_path(self):
        """ Gets user name and playblast from %HOMEPATH% 
        """

        full_path_name = os.path.expandvars(hud_names_constants.USER_SETTINGS)
        full_path_name_reformatted = full_path_name.replace('\\', '/')

        return full_path_name_reformatted

    
def turn_on_custom_hud():
    """ Turn on all custom hud.
    """
    
    for hud in hud_names_constants.HUD_CUSTOM_NAMES:
        pymel.core.windows.headsUpDisplay(hud, visible=True, edit=True)

    return

def launch_playblast_write():
    """ Writes the playblast.
    """

    turn_on_custom_hud()
    pb_object = CreatePlayblast()
    pb_object.playblast_write()

    return
