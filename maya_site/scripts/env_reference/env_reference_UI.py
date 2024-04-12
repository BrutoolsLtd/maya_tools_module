import logging
import os
from PySide2 import QtWidgets


class EnvReferenceUI(QtWidgets.QDialog):
    
    def __init__(self):
        super(EnvReferenceUI, self).__init__()
                
    def choose_dir(self):

        initial_dir = os.path.expandvars('%ADI_ROOT_FOLDER%')
        logging.debug('Initial directory: {}'.format(initial_dir))

        self.reference_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, 
                                                                       "Select Maya file", 
                                                                       initial_dir, 
                                                                       "Maya File(*.ma *.mb)")
        
        if self.reference_file == '':
            logging.debug('No Maya file selected!')

            return
