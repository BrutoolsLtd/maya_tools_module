################################################################################
# TME FX Trishul Media Entertainment [Jul 2021]
################################################################################ 
""" It creates custom Huds for playblast.

@author Esteban Ortega <brutools@gmail.com>
"""

import json
import os
import getpass
import pymel

from hud_names_constants import *

from datetime import datetime

class CustomHUD():
    """ Creates custom hud for animation playblast.
    """
    
    def __init__(self):
        """ Initialize the hud.
        """

        ########################################################################
        # Hide, preset HUD, Errors because does not exists yet.
        ########################################################################
        # pymel.core.windows.headsUpDisplay('HUDCameraNames', visible=False, edit=True)
        
        ########################################################################

        self.create_date_time_hud(4)

        self.create_file_name_hud(5)
        self.create_artist_name_hud(5)

        self.create_camera_name_hud(7)
        self.create_frame_count_hud(7)

        self.create_resolution_hud(9)
        self.create_focal_lenght(9)


        return

    def create_date_time_hud(self, target_section):
        """ Creates hud for Date and time.
        Args:
            target_section: Int representing the section in the hud.
        """

        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)
        # date_time = self.get_date_time_str()
        pymel.core.windows.headsUpDisplay(HUD_DATE_TIME.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          label=HUD_DATE_TIME.get('label'),
                                          command=self.get_date_time_str,
                                          attachToRefresh=True)
        
        return
    
    def get_date_time_str(self):
        """ Creates a string representing date time in a more readable way.
        Returns:
            String representing date time formated as month-day-year hours:minutes
            (eg. Jun-6-2021 12:45)
        """

        today = datetime.today()

        return today.strftime("%b-%d-%Y %H:%M")

    
    def create_file_name_hud(self, target_section):
        """ Creates hud for file name.
        Args:
            target_section: Int representing the section in the hud.
        """

        file_name = self.get_current_file_name()
        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)

        pymel.core.windows.headsUpDisplay(HUD_FILE_NAME.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          label=HUD_FILE_NAME.get('label'),
                                          command=self.get_current_file_name,
                                          event='SceneOpened')
        
        return
    
    def get_current_file_name(self):
        """ Get current file name.
        Return:
            String representing the current file name.
        """

        full_path_name = pymel.core.system.sceneName()
        file_name = os.path.basename(full_path_name)

        return os.path.splitext(file_name)[0]

    def create_artist_name_hud(self, target_section):
        """ Creates hud for artist file name.
        Args:
            target_section: Int representing the section in the hud.
        """

        # user_name = self.get_user_name()
        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)
        # compound_label = '{} {}'.format(HUD_ARTIST.get('label'), user_name)

        pymel.core.windows.headsUpDisplay(HUD_ARTIST.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          label=HUD_ARTIST.get('label'),
                                          command=self.get_user_name,
                                          attachToRefresh=True)

        return
    
    def get_user_name(self):
        """ Get user name.
        Return:
            String representing the name of the user.
        """

        user_settings = os.path.expandvars(USER_SETTINGS)
        user_settings_reformated = user_settings.replace('\\', '/')

        if os.path.exists(user_settings_reformated):
            with open(user_settings_reformated, 'r') as settings:
                setttings_dic = json.load(settings)
                return setttings_dic.get('user_name', getpass.getuser())

        else:
            return getpass.getuser()

        return

    def create_frame_count_hud(self, target_section):
        """ Creates hud for frame count hud.
        Args:
            target_section: Int representing the section in the hud.
        """

        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)

        pymel.core.windows.headsUpDisplay(HUD_FRAMES.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          label=HUD_FRAMES.get('label'),
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          command=self.get_current_time,
                                          attachToRefresh=True)

        return
    
    def get_current_time(self):
        """ Gets the current time.
        Return:
            Int representing the current time / frame.
        """
        current_time = pymel.core.currentTime(query=True)
        end_time = pymel.core.playbackOptions(q=True, maxTime=True)

        formated_frame_label = '{}/{}'.format(int(current_time), int(end_time))
        
        return formated_frame_label
    
    def create_camera_name_hud(self, target_section):
        """ Creates hud for camera name.
        Args:
            target_section: Int representing the section in the hud.
        """

        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)

        pymel.core.windows.headsUpDisplay(HUD_CAM_NAME.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          label=HUD_CAM_NAME.get('label'),
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          preset='cameraNames')
        
        return
    
    def create_resolution_hud(self, target_section):
        """ Creates hud for camera name.
        Args:
            target_section: Int representing the section in the hud.
        """

        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)

        pymel.core.windows.headsUpDisplay(HUD_RESOLUTION.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          label=HUD_RESOLUTION.get('label'),
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          command=self.get_default_resolution,
                                          attachToRefresh=True)
    
    def get_default_resolution(self):
        """ Gets resolution from render settings.
        Return:
            String representing the resolution (eg. '2048 x 1156')
        """

        widht = pymel.core.getAttr('defaultResolution.width')
        height = pymel.core.getAttr('defaultResolution.height')

        return str('{} x {}'.format(widht, height))

    def create_focal_lenght(self, target_section):
        """ Creates hud for focal lenght.
        Args:
            target_section: Int representing the section in the hud.
        """

        target_block = pymel.core.windows.headsUpDisplay(nextFreeBlock=target_section)

        pymel.core.windows.headsUpDisplay(HUD_FOCAL_LENGHT.get('name'), 
                                          section=target_section,
                                          block=target_block,
                                          blockSize=HUD_BLOCK_SIZE,
                                          labelFontSize=HUD_LABEL_FONT_SIZE,
                                          preset='focalLength')

        return

def launch_create_huds():
    """ Creates custom huds at launch maya file.
    """

    hud_instance = CustomHUD()

    return
