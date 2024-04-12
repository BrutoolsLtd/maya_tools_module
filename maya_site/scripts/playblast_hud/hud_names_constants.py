################################################################################
# TME FX Trishul Media Entertainment [Jul 2021]
################################################################################ 
""" Defines the names of the huds for playblast.

@author Esteban Ortega <brutools@gmail.com>
"""

## Stores hud name for file name and label.
# type: {}
HUD_FILE_NAME = {'name':'HUD_fileName', 'label':'File_name:'}

## Stores hud name for date and time and label.
# type: {}
# _HUD_DATE_TIME = 'HUD_dateTime'
HUD_DATE_TIME = {'name':'HUD_dateTime', 'label':'Date_time:'}

## Stores hud name for camera name and label
# type: {}
# _HUD_CAM_NAME = 'HUD_camName'
HUD_CAM_NAME = {'name':'HUD_camName', 'label':'Cam_name:'}

## Stores hud name camera focal lenght and label.
# type: {}
# _HUD_FOCAL_LENGHT = 'HUD_focalLenght'
HUD_FOCAL_LENGHT = {'name':'HUD_focalLenght', 'label':'Focal_lenght:'}

## Stores hud name for resolution.
# type: {}
# _HUD_RESOLUTION = 'HUD_rez'
HUD_RESOLUTION = {'name':'HUD_rez', 'label':'Resolution:'}

## Stores hud name for artist name.
# type: {}
# _HUD_ARTIST = 'HUD_artistName'
HUD_ARTIST = {'name':'HUD_artistName', 'label':'Artist_name:'}

## Stores hud name for frames.
# type: {}
# _HUD_FRAMES = 'HUD_frames'
HUD_FRAMES = {'name':'HUD_frames', 'label':'Frames:'}

## Stores hud block size, 'medium', 'small', 'large'
# type: int
HUD_BLOCK_SIZE = 'small'

## Stores hud label font size, 'small', 'large' 
# type: int
HUD_LABEL_FONT_SIZE = 'large'

## Store all custom hud names.
## type: []
HUD_CUSTOM_NAMES = [HUD_FILE_NAME.get('name'),
                    HUD_DATE_TIME.get('name'),
                    HUD_CAM_NAME.get('name'),
                    HUD_FOCAL_LENGHT.get('name'),
                    HUD_RESOLUTION.get('name'),
                    HUD_ARTIST.get('name'),
                    HUD_FRAMES.get('name')]

## Store path to userSettings json
# type: str
USER_SETTINGS = "%HOMEPATH%/userSettings/userSetting.json"
