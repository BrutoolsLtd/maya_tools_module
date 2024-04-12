import os
import logging
import maya.cmds as cmds
import pymel

def on_reload_image_callback(path):
    """ Executes when reaload button is pressed when Reload button is 
    pressed in file node.
    """
    # Setting logging, basics
    setting_logging()

    logging.debug('Starting callback')
    selected_file_node = pymel.core.general.selected()

    # Process path
    new_path_with_var = reformat_path(path)
    logging.debug('{} new path to be set.')
    # Set the variable
    logging.debug('Setting the variable...')
    selected_node = pymel.core.general.selected()
    selected_node[0].setAttr('fileTextureName', new_path_with_var)
    logging.debug('Setting the variable...finished')

    return

def reformat_path(path):
    """ Takes the provided path and reformat the path with
    addin ADI_ROOT_FOLDER variable to the name.
    """
    var_name = '%ADI_ROOT_FOLDER%'
    root_folder = os.path.expandvars(var_name)
    root_folder_reformat = root_folder.replace('\\', '/')
    size = len(root_folder_reformat)
    root_folder_selected_file = path[:size]

    logging.debug('{} this is the root folder.'.format(root_folder_reformat))
    logging.debug('{} this is file path of selected file.'.format(root_folder_selected_file))

    if root_folder_reformat != root_folder_selected_file:
        logging.debug('Not doing anything as the file is not in ADI_ROOT_FOLDER')

        return path

    path_under_root = path[size:]
    path_with_variable = '{}{}'.format(var_name, path_under_root)

    return path_with_variable

def setting_logging():
    """ Setting logging to show information as required.
    """

    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s'
    date_string = "%d/%m/%Y %I:%M %p"
    # logging.basicConfig(level=logging.DEBUG,
    #                     format=fmtstr,
    #                     datefmt=date_string)

    logger = logging.getLogger('TMEFX_Logger')
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(fmt=fmtstr, datefmt=date_string)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    # Prevent logging from building up to maya's logger.
    logger.propagate=0

    return
