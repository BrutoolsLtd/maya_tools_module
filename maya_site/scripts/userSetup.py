import maya.cmds as cmds
import pymel

# Import tool for reference with environment variable
from env_reference import env_reference_Core

# Import Create/Open folder structure tool.
from jobin_tool import jobin_Core

# Export to alembics
from export_alembics import export_to_alembics_Core

# Import alembics
from import_alembics import import_alembics_Core

# Create custom hud for playblast.
from playblast_hud import create_custom_huds
create_custom_huds.launch_create_huds()

# Toggle custom hud on / off.
from playblast_hud import toggle_custom_hud

# Create / Write playblast.
from playblast_hud import create_playblast
# Set user / path.
from playblast_hud import setting_user_path_Core

#pm.evalDeferred('import bruno_script')

################################################################################
# Here will register/ add the Maya callbacks.
################################################################################
from env_on_reload_image_callback import reload_image_callback

cmds.callbacks(addCallback=lambda path:reload_image_callback.on_reload_image_callback(path), 
               hook='textureReload',
               owner='TMEFX_plugin')

################################################################################
# Creates TMEFX_Tools menu and add commands.
################################################################################
from pack_related_files import pack_related_files_Core

# Assign material from central library
from assign_material_central_library import assign_material_central_library_Core

# Assign material from source file
from assign_material_central_library import assign_material_from_source_file_Core

def create_menu():
    """ Creates the TMEFX_Tools menu in main maya menu, to add commands.
    """
    
    mayaWindow = pymel.core.language.melGlobals['gMainWindow']
    tmefx_menu = pymel.core.menu('TMEFX_Tools', parent=mayaWindow)
    pymel.core.menuItem(label='Pack with referenced files...', command='pack_related_files_Core.launch_pack_files()', parent=tmefx_menu)

    pymel.core.menuItem(divider=True, dividerLabel='Assign materials', parent=tmefx_menu)
    pymel.core.menuItem(label='from library...', command='assign_material_central_library_Core.launch_assign_materials()', parent=tmefx_menu)
    pymel.core.menuItem(label='from file...', command='assign_material_from_source_file_Core.launch_assign_material_from_source()', parent=tmefx_menu)

pymel.core.evalDeferred(create_menu)
