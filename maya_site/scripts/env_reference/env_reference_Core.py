import logging
import os
import maya.cmds as cmd

from env_reference_UI import EnvReferenceUI


class EnvReferenceCore(EnvReferenceUI):
    
    def __init__(self):
        super(EnvReferenceCore, self).__init__()
                
    def set_reference_with_variable(self):
        """ Sets the reformated path as reference with env variable.
        """    

        # Create the namespace
        file_name = os.path.basename(self.reference_file)
        name_space = os.path.splitext(file_name)[0]

        var_name = '%ADI_ROOT_FOLDER%'
        root_folder = os.path.expandvars(var_name)
        root_folder_reformat = root_folder.replace('\\', '/')
        size = len(root_folder_reformat)

        root_folder_selected_file = self.reference_file[:size]

        if root_folder_reformat != root_folder_selected_file:

            cmd.file(self.reference_file, r=True, namespace=name_space)

            logging.debug('Setting reference with no environment variable!')

            return

        path_under_root = self.reference_file[size:]
        path_with_variable = '{}{}'.format(var_name, path_under_root)

        cmd.file(path_with_variable, r=True, namespace=name_space)
        logging.debug('Setting reference with Environment variable!')

        return

def launch_env_reference():
    """ Launch the reference window.
    """
    fmtstr = '%(asctime)s: %(levelname)s: %(funcName)s Line:%(lineno)d %(message)s'
    date_string = "%d/%m/%Y %I:%M %p"
    logging.basicConfig(level=logging.DEBUG,
                        format=fmtstr,
                        datefmt=date_string)
    w = EnvReferenceCore()
    w.choose_dir()
    w.set_reference_with_variable()

    return
