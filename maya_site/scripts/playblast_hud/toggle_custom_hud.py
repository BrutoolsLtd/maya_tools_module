""" Toggle on or off the custom huds.

@author Esteban Ortega <brutools@gmail.com>
"""

import pymel

import hud_names_constants

custom_huds = True

def toggle_custom_huds():
    """ It will display / hid custom huds.
    """

    global custom_huds
    # custom_huds = True

    if custom_huds:
        for hud in hud_names_constants.HUD_CUSTOM_NAMES:

            pymel.core.windows.headsUpDisplay(hud, visible=False, edit=True)
        
        custom_huds = False
    else:
        for hud in hud_names_constants.HUD_CUSTOM_NAMES:

            pymel.core.windows.headsUpDisplay(hud, visible=True, edit=True)
        
        custom_huds = True
    
    return
