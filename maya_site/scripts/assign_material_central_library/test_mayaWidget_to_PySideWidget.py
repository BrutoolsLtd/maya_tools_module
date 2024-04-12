""" User interface to select materials and assign to geometries.

@author Esteban Ortega <brutools@gmail.com>
"""

import sys

from PySide2 import QtWidgets
from PySide2 import QtCore
from PySide2 import QtGui

class CopyPasteMaterialsUI(QtWidgets.QDialog):
    """ UI to assign material from a referenced file to current geometries.
    """

    def __init__(self, parent=None):
        super(self, CopyPasteMaterialsUI).__init__(parent=parent)




## THE FOLLOWING CRAP WORKS, IT CREATES A DIALOG WITH A MAYA WIDGET IN IT.
# but the problem is when try to launch again, it says the panel "outPanel6"
# already exists and I can not continue, if I try to remove the panel
# it does remove it with cmds.deleteUI('name'), but later it crashes....

# Create the outlines panel which should be unique
panel = cmds.outlinerPanel('outPanel6')
#outliner = cmds.outlinerPanel(panel, query=True,outlinerEditor=True)
outEditor = cmds.outlinerEditor( panel, edit=True, mainListConnection='worldList', selectionConnection='modelList', showShapes=False, showReferenceNodes=False, showReferenceMembers=False, showAttributes=False, showConnected=False, showAnimCurvesOnly=False, autoExpand=False, showDagOnly=True, ignoreDagHierarchy=False, expandConnections=False, showCompounds=True, showNumericAttrsOnly=False, highlightActive=True, autoSelectNewObjects=False, doNotSelectNewObjects=False, transmitFilters=False, showSetMembers=True, setFilter='defaultSetFilter', ignoreHiddenAttribute=False, ignoreOutlinerColor=False )
#cmds.showWindow()

# In order for this to work the panel above needs to exist first.
import maya.OpenMayaUI
from shiboken2 import wrapInstance



mayaWidget = maya.OpenMayaUI.MQtUtil.findControl(panel)
print(mayaWidget)

pySideWidget = wrapInstance(long(mayaWidget), QtWidgets.QWidget)

print(pySideWidget)




window = QtWidgets.QDialog()
window.setWindowTitle('Algo test')

main_layout = QtWidgets.QVBoxLayout()
window.setLayout(main_layout)

main_layout.addWidget(pySideWidget)


window.show()


# This works showing how to add a cmds widget into an interface

import maya.OpenMayaUI
import maya.cmds as cmds
#import sip
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtCore import *

from shiboken2 import wrapInstance

mainWindow = QMainWindow()
centralWidget = QListView()
mainWindow.setCentralWidget(centralWidget)
dockWidget = QDockWidget("DockWidget", mainWindow)
dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

mayaMainWindow = wrapInstance(long(maya.OpenMayaUI.MQtUtil.mainWindow()), QObject)
channelBoxDockWidget = None

widget = cmds.attrColorSliderGrp("__MyWidget__")

dockWidget.setWidget([widget for widget in mayaMainWindow.findChildren(QWidget, "__MyWidget__")][0])

mainWindow.addDockWidget(Qt.DockWidgetArea(Qt.LeftDockWidgetArea), dockWidget)
mainWindow.show()


# HOW TO LOOK FOR MANESPACE TO REMOVE THE FILE AFTER SELECTION.
# WILL REFERNCE UNDER A SPECIFIC NAME SPACE AND THEN WE CAN
# REMOVE IT WITH THE NAME SPACE.
# import pymel

# refFiles = pymel.core.ls(type='reference')

# for rf in refFiles:
#     print(rf, type(rf))
#     print(rf.associatedNamespace(True))



# import pymel
# #THIS PART TO GET ALL OBJECT UNDER THE REFERENCE FILE.
# refs = pymel.core.ls(type='reference')

# for i in refs:
#     nodes = pymel.core.referenceQuery(i, nodes=True)
    
#     for node in nodes:
        
#         node = pymel.core.PyNode(str(node))
#         print(type(node), '+++++++++++++++')
        
#         shadeEng = pymel.core.listConnections(node, type='shadingEngine')
#         print(shadeEng)
#         material = pymel.core.ls(shadeEng, materials=True)
#         print(material)
#         break

# # THIS PART TO GET THE MATERIAL FROM MESH OBJECTS IN REFERENCE.
# obj = pymel.core.ls(sl=True)[0]
# obj =  pymel.core.ls(dag=1,o=1,s=1,sl=1)
# shadeEng = pymel.core.listConnections(obj[0], type='shadingEngine')[0]
# print(shadeEng)
# material = pymel.core.ls(shadeEng, materials=True)
# material = pymel.core.ls(pymel.core.listConnections(shadeEng), materials=True)
# print(material)

# for mat in material:
#     if isinstance(mat, pymel.core.nodetypes.DisplacementShader):
#         print(mat, 'this is a displacement')
#     else:
#         print(mat, 'this is NOT a displacement')
#     #print(mat, type(mat))
    
    
# sg = pymel.core.ls(sl=True)[0]
# print(sg.name(), type(sg))

# for i in dir(sg):
#     print(i)

# pymel.core.select(sg.longName())

# #This works to duplicate shading network.
# b = pymel.core.hyperShade(sg, duplicate=True)
  