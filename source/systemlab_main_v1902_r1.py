'''
    SystemLab-Design Version 19.02
    Primary author: Marc Verreault
    E-mail: marc.verreault@systemlabdesign.com
    Copyright (C) 2019 SystemLab Inc. All rights reserved.
    
    NOTICE================================================================================   
    This file is part of SystemLab-Design 19.02.
    
    SystemLab-Design 19.02 is free software: you can redistribute it 
    and/or modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation, either version 3 of the License,
    or (at your option) any later version.

    SystemLab-Design 19.02 is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with SystemLab-Design 19.02.  If not, see <https://www.gnu.org/licenses/>.    
    ======================================================================================

    ABOUT THIS MODULE
    SystemLab primary interface (GUI) for managing and running system
    designs (create, load, save, run simulations and analyze results)
    Name: systemlab_main_v1902_rc1
    Note: Release designation is as follows: 19 (major - year); 02 (minor - month);
    a1 (alpha), b1 (beta), rc1 (release candidate), r1 (release)
    Build numbers are added for tracking purposes: e.g. 210301 (month-day-sequence)
    
    SW Architecture:
        High level classes:
            - SystemLabMainApp
            Main application interface (QtWidgets.QApplication)
            - DesignLayoutScene
            Container class for all QT graphics items
            - DesignLayoutView
            Framework for viewing design components
        QtWidgets.QGraphicsItem classes:
            - FunctionaBlockDesignView/PortsDesignView
            QGraphicsItems for functional blocks & ports. Used to build components, 
            sub-systems or any abstract element within a systems model, interconnections
            between functional blocks are enabled with ports and links, the former are
            captured as instances of PortsDesignView and are integrated into the functional
            block object.        
            - DataBoxDesignView
            QGraphicsItem for data panels. Used for displaying simulation data during and
            after simulation iterations    
            - DescriptionBoxDesignView
            QGraphicsItem for data boxes. Used for highlighting design functions or groups
            or providing text descriptions with a background
            - TextBoxDesignView
            QGraphicsItem for data boxes. Used for labeling regions or providing
            text/paragraphs in the design scene
            - LineArrowDesignView/Anchor
            QGraphicsItem for lines w/wo arrows. Used with labels to direct attention or
            annotate items/results in the design
        Data model classes
            Python-specific classes for managing the data models for system components
            See systemlab_scene_models.py for further information
        Signal classes
            Python-specific classes for managing the signal models for transitioning data
            See
        UI classes:
            FunctionalBlockGUI: Properties dialog for FunctionaBlockDesignView
            (includes links to AddPortDialog, EditPortDialog, DeletePortDialog)
            DescriptionBoxGUI: Properties dialog for DescriptionBoxDesignView
            DataBoxGUI: Properties dialog for DataBoxDesignView
            LineArrowGUI: Properties dialog for LineArrowDesignView
            TextBoxGUI: Properties dialog for TextBoxDesignView
            ProjectListGUI: Properties dialog for DesignLayoutView
            AboutGUI: About this software dialog (SystemLabMainApp)
            FunctionalBlockListGUI: Table view of functional blocks (DesignLayoutView)
            SimulationStatusGUI: Status dialog when running simulations (SystemLabMainApp)
            SimulationDataGUI: Data presentation/output dialog when running simulations

    Notes on installation environment:
    Python 3.7.1, Spyder 3.3.2 (with PyQt 5.9.2), NumPy (1.15.4), Matplotlib (3.0.2),
    SciPy (1.1.0)

Import statements======================================================================
'''
import os
import sys
import numpy as np
import pickle
import hashlib
import traceback
import importlib
import time as time_data
import webbrowser
from PyQt5 import QtCore, QtGui, uic, QtWidgets

#Import SystemLab specific Python modules
import config
import systemlab_set_link as set_link
import systemlab_signals as signls
import systemlab_scene_models as models
import port_viewer_digital as port_digital
import port_viewer_electrical as port_electrical
import port_viewer_optical as port_optical
import port_viewer_analog as port_analog

fb_lib_path = str('syslab_config_files.config_fb_library')
try:
    config_lib = importlib.import_module(fb_lib_path)
except:
    e0 = sys.exc_info() [0]
    e1 = sys.exc_info() [1]
    msg = QtWidgets.QMessageBox()
    msg.setIcon(QtWidgets.QMessageBox.Warning)
    msg.setText('Error processing functional block library config module')
    msg.setInformativeText(str(e0) + ' ' + str(e1))
    msg.setInformativeText(str(traceback.format_exc()))
    msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
    msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
    msg.setWindowTitle("Processing error: Functional block library config file")
    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
    rtnval = msg.exec()
    if rtnval == QtWidgets.QMessageBox.Ok:
        msg.close()
        
# Import config_data_panel module
data_panels_path = str('syslab_config_files.config_data_panels')
config_data_panel = importlib.import_module(data_panels_path)

#Import modules to be used in scripts (for pyinstaller build)
from scipy import constants, signal, special 

'''Load SystemLab main GUI templates created in QT Creator================================
'''
#Retrieve system path for gui file directory
root_path = os.getcwd()
full_path = os.path.dirname(os.path.abspath(__file__))

local_dir = 'syslab_gui_files'
qtCreatorFile = os.path.join(root_path, local_dir, 'SystemLabApplication.ui')
qtPropertiesFile = os.path.join(root_path, local_dir, 'FunctionalBlockProperties.ui')
qtFunctionalBlockDim = os.path.join(root_path, local_dir, 'FunctionalBlockDimensionProperties.ui')
qtDescBoxFile = os.path.join(root_path, local_dir, 'DescBoxProperties.ui')
qtLineFile = os.path.join(root_path, local_dir, 'LineArrowProperties.ui')
qtDataBoxFile = os.path.join(root_path, local_dir, 'DataBoxProperties.ui')
qtTextBoxFile = os.path.join(root_path, local_dir, 'TextBoxProperties.ui')
qtAddPortFile = os.path.join(root_path, local_dir, 'AddPortDialog.ui')
qtEditPortFile = os.path.join(root_path, local_dir, 'EditPortDialog.ui')
qtDeletePortFile = os.path.join(root_path, local_dir, 'DeletePortDialog.ui')
qtProjectSettingsFile = os.path.join(root_path, local_dir, 'ProjectSettings.ui')
qtSimulationStatusFile = os.path.join(root_path, local_dir, 'SimulationStatus.ui')
qtSimDataViewFile = os.path.join(root_path, local_dir, 'DataView.ui')
qtFunctionalBlockListFile = os.path.join(root_path, local_dir, 'FunctionalBlockTable.ui')
qtLinkListFile = os.path.join(root_path, local_dir, 'LinkTable.ui')
qtProjectsList = os.path.join(root_path, local_dir, 'ProjectList.ui')
qtAboutSystemLabDesign = os.path.join(root_path, local_dir, 'AboutSystemLabDesign.ui')

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
Ui_FBWindow, QtBaseClass = uic.loadUiType(qtPropertiesFile)
Ui_FBDimWindow, QtBaseClass = uic.loadUiType(qtFunctionalBlockDim)
Ui_DescWindow, QtBaseClass = uic.loadUiType(qtDescBoxFile)
Ui_LineWindow, QtBaseClass = uic.loadUiType(qtLineFile)
Ui_DataWindow, QtBaseClass = uic.loadUiType(qtDataBoxFile)
Ui_TextWindow, QtBaseClass = uic.loadUiType(qtTextBoxFile)
Ui_AddPort, QtBaseClass = uic.loadUiType(qtAddPortFile)
Ui_EditPort, QtBaseClass = uic.loadUiType(qtEditPortFile)
Ui_DeletePort, QtBaseClass = uic.loadUiType(qtDeletePortFile)
Ui_ProjectWindow, QtBaseClass = uic.loadUiType(qtProjectSettingsFile)
Ui_SimStatus, QtBaseClass = uic.loadUiType(qtSimulationStatusFile)
Ui_SimData, QtBaseClass = uic.loadUiType(qtSimDataViewFile)
Ui_FunctionalBlockList, QtBaseClass = uic.loadUiType(qtFunctionalBlockListFile)
Ui_LinkList, QtBaseClass = uic.loadUiType(qtLinkListFile)
Ui_ProjectList, QtBaseClass = uic.loadUiType(qtProjectsList)
Ui_About, QtBaseClass = uic.loadUiType(qtAboutSystemLabDesign)

'''Set styles and fonts for main interface and dialogs====================================
'''
#Font for QDialog interfaces
app_font_default = 'font-size: 8pt; font-family: Segoe UI;'
#Fonts and styles for menubar and statusbar information boxes
font = QtGui.QFont("Arial", 8)
font_normal = QtGui.QFont("Arial", 8)
font.setWeight(QtGui.QFont.Light)
font_normal.setWeight(QtGui.QFont.Light)
font_small = QtGui.QFont("Arial", 7)
font_small.setWeight(QtGui.QFont.Light)
font_value = QtGui.QFont("Arial", 8)
style = ("""QLineEdit {background-color: rgb(245, 245, 245); color: rgb(50, 50, 50) }""")

'''SystemLab-Design primary application interface (initialization)========================
'''
class SystemLabMainApp(QtWidgets.QMainWindow, Ui_MainWindow):
    '''Initialize the SystemLab application space and load design space
    '''
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        #Perform setup of main SystemLab view (designed via QT Designer)
        self.setupUi(self)     
        #Add icon image to main application view
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        #Set default connector type to "line"
        self.lineConnectionMode = True
        self.action_LineConnector.setChecked(1)
        self.action_AngledConnector.setChecked(0)
        # Flag for application quit (initialized to True)
        self.app_quit = True
        
        '''Initialize dictionaries for project space/scene management=====================
        '''
        #Dictionary to manage list of all open projects
        self.project_names_list = {} 
        #Dictionary for tab/project layout objects
        #(QtWidgets.QHBoxLayout)       
        self.project_layouts_list = {}
        #Dictionary for project scene objects
        #(DesignLayoutScene - QtWidgets.QGraphicsScene)
        self.project_scenes_list = {} 
        #Dictionary for project view objects
        #(DesignLayoutView - QtWidgets.QGraphicsView)
        self.project_views_list = {}      
        #Dictionaries for storing binary images of each project
        #(used for file comparisons)
        self.hash_list_open = {}
        self.hash_list_close = {}
        #Dictionary for tracking project file paths 
        self.project_file_paths_list = {}
        #Dictionary for data boxes (all projects)
        self.projects_data_box_ID_list = []       
        
        '''MENUBAR SETTINGS===============================================================
        '''
        #File menu========================================================================
        #Project new
        action_new_icon = QtGui.QIcon()
        icon_path_new = os.path.join(root_path, 'syslab_gui_icons', 'folder.png')
        icon_path_new = os.path.normpath (icon_path_new)
        action_new_icon.addFile(icon_path_new)
        self.action_NewProject.setIcon(action_new_icon)
        self.action_NewProject.triggered.connect(self.project_new)
        #Project open
        action_open_icon = QtGui.QIcon()
        icon_path_open = os.path.join(root_path, 'syslab_gui_icons', 'folder-open.png')
        icon_path_open = os.path.normpath (icon_path_open)
        action_open_icon.addFile(icon_path_open)
        self.action_OpenProject.setIcon(action_open_icon)
        self.action_OpenProject.triggered.connect(self.project_open)
        #Project save
        action_save_icon = QtGui.QIcon()
        icon_path_save = os.path.join(root_path, 'syslab_gui_icons', 'disk.png')
        icon_path_save = os.path.normpath (icon_path_save)
        action_save_icon.addFile(icon_path_save)
        self.action_SaveProject.setIcon(action_save_icon)
        self.action_SaveProject.triggered.connect(self.project_save)
        #Save project as
        action_save_as_icon = QtGui.QIcon()
        icon_path_save_as = os.path.join(root_path, 'syslab_gui_icons', 'disk-rename.png')
        icon_path_save_as = os.path.normpath (icon_path_save_as)
        action_save_as_icon.addFile(icon_path_save_as)
        self.action_SaveProjectAs.setIcon(action_save_as_icon)
        self.action_SaveProjectAs.triggered.connect(self.project_save_as)
        #Close project
        self.action_CloseProject.triggered.connect(self.project_close)  
        action_close_icon = QtGui.QIcon()
        icon_path_close = os.path.join(root_path, 'syslab_gui_icons', 'folder--minus.png')
        icon_path_close = os.path.normpath (icon_path_close)
        action_close_icon.addFile(icon_path_close)
        self.action_CloseProject.setIcon(action_close_icon)
        #Quit application
        self.action_QuitApplication.triggered.connect(self.application_close)
        action_quit_icon = QtGui.QIcon()
        icon_path_quit = os.path.join(root_path, 'syslab_gui_icons', 'cross.png')
        icon_path_quit = os.path.normpath (icon_path_quit)
        action_quit_icon.addFile(icon_path_quit)
        self.action_QuitApplication.setIcon(action_quit_icon)
        
        #Edit menu========================================================================
        self.action_CopyPaste.triggered.connect(self.copy_paste_selected_items)
        self.action_copy_paste_icon = QtGui.QIcon()
        icon_path_copy_paste = os.path.join(root_path, 'syslab_gui_icons', 'block--plus.png')
        icon_path_copy_paste = os.path.normpath (icon_path_copy_paste)
        self.action_copy_paste_icon.addFile(icon_path_copy_paste)
        self.action_CopyPaste.setIcon(self.action_copy_paste_icon)
        
        self.action_CopyPasteToAnotherProj.triggered.connect(self.copy_paste_selected_items_to_another_proj)
        self.action_copy_paste_proj_icon = QtGui.QIcon()
        icon_path_copy_paste_proj = os.path.join(root_path, 'syslab_gui_icons', 'block--arrow.png')
        icon_path_copy_paste_proj = os.path.normpath (icon_path_copy_paste_proj)
        self.action_copy_paste_proj_icon.addFile(icon_path_copy_paste_proj)
        self.action_CopyPasteToAnotherProj.setIcon(self.action_copy_paste_proj_icon)
        
        self.action_Delete.triggered.connect(self.delete_selected_items)
        self.action_delete_icon = QtGui.QIcon()
        icon_path_delete = os.path.join(root_path, 'syslab_gui_icons', 'block--minus.png')
        icon_path_delete = os.path.normpath (icon_path_delete)
        self.action_delete_icon.addFile(icon_path_delete)
        self.action_Delete.setIcon(self.action_delete_icon)
        
        self.action_Delete.setEnabled(False)
        self.action_CopyPaste.setEnabled(False)
        self.action_CopyPasteToAnotherProj.setEnabled(False)
        
        self.action_OpenScriptEditor.triggered.connect(self.open_script_editor)
        action_editor_icon = QtGui.QIcon()
        icon_path_editor = os.path.join(root_path, 'syslab_gui_icons', 'iconfinder_application-x-python_8974.png')
        icon_path_editor = os.path.normpath (icon_path_editor)
        action_editor_icon.addFile(icon_path_editor)
        self.action_OpenScriptEditor.setIcon(action_editor_icon)
        
        #Project menu=====================================================================
        self.action_AddFunctionalBlock.triggered.connect(self.add_functional_block)
        self.action_add_fb_icon = QtGui.QIcon()
        icon_path_add_fb = os.path.join(root_path, 'syslab_gui_icons', 'fb.png')
        icon_path_add_fb = os.path.normpath (icon_path_add_fb)
        self.action_add_fb_icon.addFile(icon_path_add_fb)
        self.action_AddFunctionalBlock.setIcon(self.action_add_fb_icon)
        
        self.action_AddDescriptionBox.triggered.connect(self.add_description_box)
        self.action_add_desc_icon = QtGui.QIcon()
        icon_path_add_desc = os.path.join(root_path, 'syslab_gui_icons', 'ui-text-area.png')
        icon_path_add_desc = os.path.normpath (icon_path_add_desc)
        self.action_add_desc_icon.addFile(icon_path_add_desc)
        self.action_AddDescriptionBox.setIcon(self.action_add_desc_icon)
        
        self.action_AddDataBox.triggered.connect(self.add_data_box)
        self.action_add_data_icon = QtGui.QIcon()
        icon_path_add_data = os.path.join(root_path, 'syslab_gui_icons', 'ui-list-box.png')
        icon_path_add_data = os.path.normpath (icon_path_add_data)
        self.action_add_data_icon.addFile(icon_path_add_data)
        self.action_AddDataBox.setIcon(self.action_add_data_icon)
        
        self.action_AddTextBox.triggered.connect(self.add_text_box)
        self.action_add_text_icon = QtGui.QIcon()
        icon_path_add_text = os.path.join(root_path, 'syslab_gui_icons', 'ui-text-field.png')
        icon_path_add_text = os.path.normpath (icon_path_add_text)
        self.action_add_text_icon.addFile(icon_path_add_text)
        self.action_AddTextBox.setIcon(self.action_add_text_icon)        
        
        self.action_AddLineArrow.triggered.connect(self.add_line_arrow)
        self.action_add_line_arrow_icon = QtGui.QIcon()
        icon_path_add_line_arrow = os.path.join(root_path, 'syslab_gui_icons', 'line-arrow.png')
        icon_path_add_line_arrow = os.path.normpath (icon_path_add_line_arrow)
        self.action_add_line_arrow_icon.addFile(icon_path_add_line_arrow)
        self.action_AddLineArrow.setIcon(self.action_add_line_arrow_icon) 
        
        self.action_ProjectLayoutSettings.triggered.connect(self.project_settings_open)
        self.project_settings_icon = QtGui.QIcon()
        icon_path_project_settings = os.path.join(root_path, 'syslab_gui_icons',
                                                  'ProjectSettings_16.png')
        icon_path_project_settings = os.path.normpath (icon_path_project_settings)
        self.project_settings_icon.addFile(icon_path_project_settings)
        self.action_ProjectLayoutSettings.setIcon(self.project_settings_icon) 
        
        self.action_ViewFunctionalBlocks.triggered.connect(self.view_fb_blocks_list)
        self.action_fblist_icon = QtGui.QIcon()
        icon_path_fblist = os.path.join(root_path, 'syslab_gui_icons', 'edit-list.png')
        icon_path_fblist = os.path.normpath (icon_path_fblist)
        self.action_fblist_icon.addFile(icon_path_fblist)
        self.action_ViewFunctionalBlocks.setIcon(self.action_fblist_icon)
        
        self.action_SceneBackgroundColor.triggered.connect(self.scene_background_color)
        self.action_scene_color_icon = QtGui.QIcon()
        icon_path_scene_color = os.path.join(root_path, 'syslab_gui_icons', 'spectrum.png')
        icon_path_scene_color = os.path.normpath (icon_path_scene_color)
        self.action_scene_color_icon.addFile(icon_path_scene_color)
        self.action_SceneBackgroundColor.setIcon(self.action_scene_color_icon)
        
        self.action_SaveImageScene.triggered.connect(self.scene_image)
        self.action_save_scene_icon = QtGui.QIcon()
        icon_path_save_scene = os.path.join(root_path, 'syslab_gui_icons', 'image-select.png')
        icon_path_save_scene = os.path.normpath(icon_path_save_scene)
        self.action_save_scene_icon.addFile(icon_path_save_scene)
        self.action_SaveImageScene.setIcon(self.action_save_scene_icon)
        
        #Simulation menu =================================================================
        #Start
        action_start_sim_icon = QtGui.QIcon()
        icon_path_start_sim = os.path.join(root_path, 'syslab_gui_icons', 'control.png')
        icon_path_start_sim = os.path.normpath (icon_path_start_sim)
        action_start_sim_icon.addFile(icon_path_start_sim)
        self.actionStart.setIcon(action_start_sim_icon)
        self.actionStart.setEnabled(True)
        self.actionStart.triggered.connect(self.start_simulation)
        #Pause
        action_pause_sim_icon = QtGui.QIcon()
        icon_path_pause_sim = os.path.join(root_path, 'syslab_gui_icons', 'control-pause.png')
        icon_path_pause_sim = os.path.normpath (icon_path_pause_sim)
        action_pause_sim_icon.addFile(icon_path_pause_sim)
        self.actionPause.setIcon(action_pause_sim_icon)
        self.actionPause.setEnabled(False)
        self.actionPause.triggered.connect(self.pause_simulation)
        #End
        action_stop_sim_icon = QtGui.QIcon()
        icon_path_stop_sim = os.path.join(root_path, 'syslab_gui_icons', 'control-stop-square.png')
        icon_path_stop_sim = os.path.normpath (icon_path_stop_sim)
        action_stop_sim_icon.addFile(icon_path_stop_sim)
        self.actionEnd.setIcon(action_stop_sim_icon) 
        self.actionEnd.setEnabled(False)
        self.actionEnd.triggered.connect(self.stop_simulation) 
        
        #Help menu =======================================================================
        #Help
        self.actionHelp.triggered.connect(self.open_doc_html)
        help_icon = QtGui.QIcon()
        icon_path_help = os.path.join(root_path, 'syslab_gui_icons', 'question.png')
        icon_path_help = os.path.normpath (icon_path_help)
        help_icon.addFile(icon_path_help)
        self.actionHelp.setIcon(help_icon)
        
        self.actionAbout.triggered.connect(self.open_about)
        help_about_icon = QtGui.QIcon()
        icon_path_about = os.path.join(root_path, 'syslab_gui_icons', 'information.png')
        icon_path_about = os.path.normpath (icon_path_about)
        help_about_icon.addFile(icon_path_about)
        self.actionAbout.setIcon(help_about_icon)       
        
        '''TAB SETTINGS===================================================================
        '''
        self.tabWidget.tabCloseRequested.connect(self.project_close)
        
        '''STATUSBAR SETTINGS=============================================================
        '''
        border = ("QLabel{border-width: 1px; border-style: solid;"
                  + "border-color: rgb(240,240,240) rgb(240,240,240) rgb(240,240,240) grey;}" )
        
        #Information/status box (for simulations)
        status_label = QtWidgets.QLabel()
        status_label.setText(' Info/Status:')
        status_label.setFont(font)
        status_label.setFixedWidth(58)
               
        config.status = QtWidgets.QLineEdit()
        config.status.setFixedWidth(400)
        self.statusbar.addPermanentWidget(status_label)
        self.statusbar.addPermanentWidget(config.status)
        config.status.setReadOnly(1)
        config.status.setFont(font_value)
        config.status.setStyleSheet(style)
        
        #File path of current project 
        path_label = QtWidgets.QLabel()
        path_label.setText(' Project file path:')
        path_label.setFont(font)
        path_label.setFixedWidth(85)
        path_label.setStyleSheet(border)
        self.file_path = QtWidgets.QLineEdit()
        self.file_path.setFixedWidth(450)
        self.statusbar.addPermanentWidget(path_label)
        self.statusbar.addPermanentWidget(self.file_path)
        self.file_path.setReadOnly(1)
        self.file_path.setFont(font_value)
        self.file_path.setStyleSheet(style)
        
        #Scene zoom setting
        zoom_label = QtWidgets.QLabel()
        zoom_label.setText('Zoom (%):')
        zoom_label.setFont(font)
        zoom_label.setFixedWidth(55)
        zoom_label.setStyleSheet(border)
        self.zoom_value = QtWidgets.QLineEdit()
        self.zoom_value.setFixedWidth(35)
        self.statusbar.addPermanentWidget(zoom_label)
        self.statusbar.addPermanentWidget(self.zoom_value)
        self.zoom_value.setReadOnly(1)
        self.zoom_value.setFont(font_value)
        
        '''TOOLBAR SETTINGS===============================================================
        '''
        #Setup icons for file management, simulation, connectors, project settings========
        action_new_icon = QtGui.QIcon()
        icon_path_action_new = os.path.join(root_path, 'syslab_gui_icons', 'folder-24.png')
        icon_path_action_new = os.path.normpath (icon_path_action_new)
        action_new_icon.addFile(icon_path_action_new)
        self.actionNew.setIcon(action_new_icon)
        
        action_open_icon = QtGui.QIcon()
        icon_path_action_open = os.path.join(root_path, 'syslab_gui_icons', 'folder-open-24.png')
        icon_path_action_open = os.path.normpath (icon_path_action_open)
        action_open_icon.addFile(icon_path_action_open)     
        self.actionOpen.setIcon(action_open_icon)
        
        action_save_icon = QtGui.QIcon()
        icon_path_action_save = os.path.join(root_path, 'syslab_gui_icons', 'disk-24.png')
        icon_path_action_save = os.path.normpath (icon_path_action_save)
        action_save_icon.addFile(icon_path_action_save)
        self.actionSave.setIcon(action_save_icon)

        action_start_icon = QtGui.QIcon()
        icon_path_action_start = os.path.join(root_path, 'syslab_gui_icons', 'Start-64.png')
        icon_path_action_start = os.path.normpath (icon_path_action_start)
        action_start_icon.addFile(icon_path_action_start)
        self.action_StartSimulation.setIcon(action_start_icon)
        
        action_pause_icon = QtGui.QIcon()
        icon_path_action_pause = os.path.join(root_path, 'syslab_gui_icons', 'Pause-64.png')
        icon_path_action_pause = os.path.normpath (icon_path_action_pause)
        action_pause_icon.addFile(icon_path_action_pause)
        self.action_PauseSimulation.setIcon(action_pause_icon)

        action_stop_icon = QtGui.QIcon()
        icon_path_action_stop = os.path.join(root_path, 'syslab_gui_icons', 'Stop-64.png')
        icon_path_action_stop = os.path.normpath (icon_path_action_stop)
        action_stop_icon.addFile(icon_path_action_stop)
        self.action_StopSimulation.setIcon(action_stop_icon)
        
        line_conn_icon = QtGui.QIcon()
        icon_path_line_conn = os.path.join(root_path, 'syslab_gui_icons',
                                           'LineConnector-24.png')
        icon_path_line_conn = os.path.normpath (icon_path_line_conn)
        line_conn_icon.addFile(icon_path_line_conn)
        self.action_LineConnector.setIcon(line_conn_icon) 
        angle_conn_icon = QtGui.QIcon()
        icon_path_angle_conn = os.path.join(root_path, 'syslab_gui_icons',
                                            'AngleConnector-24.png')
        icon_path_angle_conn = os.path.normpath (icon_path_angle_conn)
        angle_conn_icon.addFile(icon_path_angle_conn)
        self.action_AngledConnector.setIcon(angle_conn_icon) 
        
        action_project_settings = QtGui.QIcon()
        icon_path_project_settings = os.path.join(root_path, 'syslab_gui_icons', 
                                                  'ProjectSettings-24.png')
        icon_path_project_settings = os.path.normpath (icon_path_project_settings)
        action_project_settings.addFile(icon_path_project_settings)
        self.actionProjectSettings.setIcon(action_project_settings)        
        
        #Set simulation pause/stop to disabled
        self.action_PauseSimulation.setEnabled(False)
        self.action_StopSimulation.setEnabled(False)
        
        #Project/design settings (save port data/activate data window)====================
        self.port_settings_bar = QtWidgets.QToolBar()
        self.port_settings_bar.setWindowTitle('Port data settings')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.port_settings_bar)       
        list_check_boxes = QtWidgets.QListWidget()
        list_check_boxes.setFixedSize(140, 50)
        list_check_boxes.setAutoFillBackground(True)
        list_check_boxes.setStyleSheet("""QListWidget {border: 0px ;
                                       background-color: rgb(245, 245, 245)}""")
        item1 = QtWidgets.QListWidgetItem(list_check_boxes) 
        item2 = QtWidgets.QListWidgetItem(list_check_boxes)
        item3 = QtWidgets.QListWidgetItem(list_check_boxes)
        self.check_box_port_data = QtWidgets.QCheckBox()
        self.check_box_port_data.setText('Save port data')
        self.check_box_port_data.setFont(font_normal)
        self.check_box_port_data.setCheckState(2)
        list_check_boxes.setItemWidget(item1, self.check_box_port_data)
        self.check_box_sim_data = QtWidgets.QCheckBox()
        self.check_box_sim_data.setText('Activate data window')
        self.check_box_sim_data.setFont(font_normal)
        self.check_box_sim_data.setCheckState(0)
        list_check_boxes.setItemWidget(item2, self.check_box_sim_data)
        self.check_box_sim_status = QtWidgets.QCheckBox()
        self.check_box_sim_status.setText('Display simulation status')
        self.check_box_sim_status.setFont(font_normal)
        self.check_box_sim_status.setCheckState(2)
        list_check_boxes.setItemWidget(item3, self.check_box_sim_status)
        self.port_settings_bar.addWidget(list_check_boxes)
        
        #Project/design settings (sample rate/time window/samples)========================
        self.sim_settings_bar = QtWidgets.QToolBar()
        self.sim_settings_bar.setWindowTitle('Simulation settings')
        self.addToolBar(QtCore.Qt.TopToolBarArea , self.sim_settings_bar)
        
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setRowCount(3)
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setItem(0, 0, QtWidgets.QTableWidgetItem("Sample rate (Hz)"))
        self.tableWidget.setItem(1, 0, QtWidgets.QTableWidgetItem("Time window (sec)"))
        self.tableWidget.setItem(2, 0, QtWidgets.QTableWidgetItem("Samples (n)"))
        self.tableWidget.setItem(0, 1, QtWidgets.QTableWidgetItem(" "))
        self.tableWidget.setItem(1, 1, QtWidgets.QTableWidgetItem(" "))
        self.tableWidget.setItem(2, 1, QtWidgets.QTableWidgetItem(" "))
        
        font_table = QtGui.QFont("Arial", 8)
        font_table.setWeight(QtGui.QFont.Light)
        
        for row in range(0, self.tableWidget.rowCount()):
            self.tableWidget.item(row, 0).setFont(font_table)
            self.tableWidget.item(row, 1).setFont(font_table)
            self.tableWidget.item(row, 0).setForeground(QtGui.QColor(50,50,50))
            self.tableWidget.item(row, 1).setForeground(QtGui.QColor(50,50,50))
            self.tableWidget.item(row, 0).setBackground(QtGui.QColor(240,240,240))
            self.tableWidget.setRowHeight(row, 16)
            
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setVisible(False)       
        self.tableWidget.resizeColumnsToContents()       
        self.tableWidget.setMaximumWidth(160)
        self.tableWidget.setMaximumHeight(50)
        self.tableWidget.setMinimumWidth(160)
        self.tableWidget.setMinimumHeight(50)
        self.tableWidget.setAutoFillBackground(True)
        self.tableWidget.setStyleSheet("""QTableWidget {border: 2px ;
                                       background-color: rgb(245, 245, 245)}""")   
        self.sim_settings_bar.addWidget(self.tableWidget)
        
        #Simulation data (iteration #, etc.)==============================================
        self.sim_data_bar = QtWidgets.QToolBar()
        self.sim_data_bar.setWindowTitle('Simulation data')
        self.addToolBar(QtCore.Qt.TopToolBarArea , self.sim_data_bar)
        
        self.tableWidget2 = QtWidgets.QTableWidget()
        self.tableWidget2.setRowCount(2)
        self.tableWidget2.setColumnCount(2)
        self.tableWidget2.setItem(0, 0, QtWidgets.QTableWidgetItem("Iteration(s) (Tot)"))
        self.tableWidget2.setItem(1, 0, QtWidgets.QTableWidgetItem("Segment(s) (Tot)"))
        self.tableWidget2.setItem(0, 1, QtWidgets.QTableWidgetItem(" "))
        self.tableWidget2.setItem(1, 1, QtWidgets.QTableWidgetItem(" "))
        
        self.tableWidget3 = QtWidgets.QTableWidget()
        self.tableWidget3.setRowCount(3)
        self.tableWidget3.setColumnCount(2)
        self.tableWidget3.setItem(0, 0, QtWidgets.QTableWidgetItem("Iteration (Cur)"))
        self.tableWidget3.setItem(1, 0, QtWidgets.QTableWidgetItem("Segment (Cur)"))
        self.tableWidget3.setItem(2, 0, QtWidgets.QTableWidgetItem("Sim progress (%)"))
        self.tableWidget3.setItem(0, 1, QtWidgets.QTableWidgetItem(" "))
        self.tableWidget3.setItem(1, 1, QtWidgets.QTableWidgetItem(" "))
        self.tableWidget3.setItem(2, 1, QtWidgets.QTableWidgetItem(" "))
    
        font_table = QtGui.QFont("Arial", 8)
        font_table.setWeight(QtGui.QFont.Light)
        
        for row in range(0, self.tableWidget2.rowCount()):
            self.tableWidget2.item(row, 0).setFont(font_table)
            self.tableWidget2.item(row, 1).setFont(font_table)
            self.tableWidget2.item(row, 0).setForeground(QtGui.QColor(50,50,50))
            self.tableWidget2.item(row, 0).setBackground(QtGui.QColor(240,240,240))                   
            self.tableWidget2.item(row, 1).setForeground(QtGui.QColor(100,100,100))
            self.tableWidget2.setRowHeight(row, 16)
            
        self.tableWidget2.item(0,1).setForeground(QtGui.QColor(50,50,50))
        self.tableWidget2.item(0,1).setBackground(QtGui.QColor(240,240,240))
        self.tableWidget2.item(1,1).setForeground(QtGui.QColor(50,50,50))
        self.tableWidget2.item(1,1).setBackground(QtGui.QColor(240,240,240))
            
        for row in range(0, self.tableWidget3.rowCount()):
            self.tableWidget3.item(row, 0).setFont(font_table)
            self.tableWidget3.item(row, 1).setFont(font_table)         
            self.tableWidget3.item(row, 0).setForeground(QtGui.QColor(50,50,50))
            self.tableWidget3.item(row, 0).setBackground(QtGui.QColor(240,240,240))             
            self.tableWidget3.setRowHeight(row, 16)
            
        self.tableWidget3.item(0,1).setForeground(QtGui.QColor(150,0,0))
        self.tableWidget3.item(0,1).setBackground(QtGui.QColor(255,255,255))
        self.tableWidget3.item(1,1).setForeground(QtGui.QColor(150,0,0))
        self.tableWidget3.item(1,1).setBackground(QtGui.QColor(255,255,255))
        self.tableWidget3.item(2,1).setForeground(QtGui.QColor(0,0,127))
        self.tableWidget3.item(2,1).setBackground(QtGui.QColor(255,255,255))
            
        self.tableWidget2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget2.horizontalHeader().setVisible(False)
        self.tableWidget2.verticalHeader().setVisible(False)       
        self.tableWidget2.setMaximumWidth(130)
        self.tableWidget2.resizeColumnsToContents()       
        self.tableWidget2.setMaximumHeight(50)        
        self.tableWidget2.setAutoFillBackground(True)
        self.tableWidget2.setStyleSheet("""QTableWidget {border: 2px ;
                                       background-color: rgb(245, 245, 245)}""") 
        self.sim_data_bar.addWidget(self.tableWidget2)
        
        self.tableWidget3.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget3.horizontalHeader().setVisible(False)
        self.tableWidget3.verticalHeader().setVisible(False)       
        self.tableWidget3.setMaximumWidth(130)
        self.tableWidget3.resizeColumnsToContents()       
        self.tableWidget3.setMaximumHeight(50)        
        self.tableWidget3.setAutoFillBackground(True)
        self.tableWidget3.setStyleSheet("""QTableWidget {border: 2px ;
                                       background-color: rgb(245, 245, 245)}""") 
        self.sim_data_bar.addWidget(self.tableWidget3) 

        #Iterations data and spinbox =====================================================
        self.iterations_bar = QtWidgets.QToolBar()
        self.iterations_bar.setWindowTitle('Iterations settings')
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.iterations_bar)
        #Iteration spin box
        self.iterationsSelector = QtWidgets.QSpinBox()
        font_iteration = QtGui.QFont("Arial", 8)
        font_iteration.setWeight(QtGui.QFont.Light)
        self.iterationsSelector.setFont(font_iteration)
        self.iterationsSelector.setMinimumWidth(50)
        self.iterationsSelector.setMinimumHeight(24)
        self.iterationsSelector.lineEdit().setReadOnly(True)
        self.iterationsSelector.lineEdit().setStyleSheet("""QLineEdit {color: darkRed; 
                                        background-color: rgb(170, 0, 0, 20)}""") 
        self.iterations_bar.addWidget(self.iterationsSelector)
        #Iteration spin box label
        self.iterations_label = QtWidgets.QLabel()
        self.iterations_label.setText(' Iteration')
        self.iterations_label.setFont(font)
        self.iterations_bar.addWidget(self.iterations_label)  
        
        #Functional block menu tree=======================================================
        self.fb_tree_panel_1 = QtWidgets.QToolBar()
        self.fb_tree_panel_1.setWindowTitle('Functional block library')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.fb_tree_panel_1)
        
        self.fb_tree_panel_2 = QtWidgets.QToolBar()
        self.fb_tree_panel_2.setWindowTitle('Functional block library (2)')
        self.addToolBar(QtCore.Qt.LeftToolBarArea, self.fb_tree_panel_2)        

        fb_library_tree_1 = FunctionalBlockTreeList1(self)
        self.fb_tree_panel_1.addWidget(fb_library_tree_1) 
        
        if len(config_lib.fb_sections_2) > 0:
            fb_library_tree_2 = FunctionalBlockTreeList2(self) 
            self.fb_tree_panel_2.addWidget(fb_library_tree_2) 
        
        # Project actions=================================================================
        self.actionNew.triggered.connect(self.project_new)
        self.actionSave.triggered.connect(self.project_save)
        self.actionOpen.triggered.connect(self.project_open)
        self.actionProjectSettings.triggered.connect(self.project_settings_open)
        
        # Simulation actions==============================================================
        self.action_StartSimulation.triggered.connect(self.start_simulation)
        self.action_PauseSimulation.triggered.connect(self.pause_simulation)
        self.action_StopSimulation.triggered.connect(self.stop_simulation)
        
        #Link connection actions
        self.action_LineConnector.triggered.connect(self.set_line_status_true)
        self.action_AngledConnector.triggered.connect(self.set_line_status_false)
        
        #Load new GraphicsScene and GraphicssView for first tab (default)=================
        self.project_names_list['Project_1'] = 1
        self.project_layouts_list[1] = 'layout_Project_1'
        self.project_scenes_list[1] = DesignLayoutScene('Project_1')
        back_color = self.project_scenes_list[1].design_settings['back_color']
        self.project_scenes_list[1].setBackgroundBrush(QtGui.QBrush(QtGui.QColor(back_color)))
        self.project_views_list[1] = DesignLayoutView(self.project_scenes_list[1], self)
        self.designLayout_1.addWidget(self.project_views_list[1])
        self.designLayout_1.setContentsMargins(2, 2, 2, 2)
        self.tabWidget.setTabText(0, 'Project_1')
        self.file_path.setText(str(root_path))
        self.project_file_paths_list[1] = str(root_path)
        self.iterationsSelector.setValue(1)
        
        self.tableWidget2.item(0, 1).setText(format(1, 'n'))
        self.tableWidget2.item(1, 1).setText(format(100, 'n'))
        self.tableWidget2.resizeColumnsToContents()
        
        self.iterationsSelector.setMinimum(1)
        self.iterationsSelector.setMaximum(1) 
        self.iterationsSelector.valueChanged.connect(self.value_change_iteration)
        
        self.tableWidget.item(0, 1).setText(format(config.sampling_rate_default, '0.3E'))
        self.tableWidget.item(1, 1).setText(format(config.simulation_time_default, '0.3E'))
        self.tableWidget.item(2, 1).setText(format(config.num_samples_default, '0.3E'))  
        self.tableWidget.resizeColumnsToContents()
        
        #Re-sets method for dynamic connection of links within design scenes
        self.startedLink = None    
        
        #Actions to take if a project tab is changed
        self.tabWidget.currentChanged.connect(self.change_project_tab_event)      

    def value_change_iteration(self):
        new_iteration = int(self.iterationsSelector.value())
        self.tableWidget3.item(0, 1).setText(format(new_iteration, 'n'))
        tab_index, key_index = retrieve_current_project_key_index()
        if key_index is not None:
            self.project_scenes_list[key_index].design_settings['current_iteration'] = new_iteration
            self.update_data_boxes()
        
    def set_line_status_true(self):
        self.lineConnectionMode = True
        self.action_AngledConnector.setChecked(0)
        
    def set_line_status_false(self):
        self.lineConnectionMode = False
        self.action_LineConnector.setChecked(0)
        
    def project_settings_open(self):
        tab_index, key_index = retrieve_current_project_key_index()
        self.project_scenes_list[key_index].open_project_settings(tab_index, key_index)
        
    def view_fb_blocks_list(self):
        tab_index, key_index = retrieve_current_project_key_index()  
        proj_sc = self.project_scenes_list[key_index]
        proj_sc.build_fb_list()
        
    def scene_background_color(self):
        tab_index, key_index = retrieve_current_project_key_index() 
        proj_sc = self.project_scenes_list[key_index]
        proj_sc.update_background_color()
        
    def pause_simulation(self):
        if self.action_PauseSimulation.isChecked():
            config.sim_pause_flag = True
        else:
            config.sim_pause_flag = False
            
    def stop_simulation(self):
        config.stop_sim_flag = True
        
    def project_new(self):
        i = set_new_key(self.project_layouts_list)  
        self.project_names_list['Project_' + str(i)] = i
        self.project_layouts_list[i] = 'layout_Project_' + str(i)
        
        self.project_scenes_list[i] = DesignLayoutScene('Project_' + str(i))
        back_color = self.project_scenes_list[i].design_settings['back_color']
        self.project_scenes_list[i].setBackgroundBrush(QtGui.QBrush(QtGui.QColor(back_color)))
        self.project_views_list[i] = DesignLayoutView(self.project_scenes_list[i], self)
      
        self.project_layouts_list[i] = QtWidgets.QHBoxLayout()
        newtab = QtWidgets.QWidget()
        newtab.setLayout(self.project_layouts_list[i])
        self.tabWidget.addTab(newtab, 'Project_' + str(i))  

        self.project_layouts_list[i].addWidget(self.project_views_list[i])
        self.project_layouts_list[i].setContentsMargins(2, 2, 2, 2)
        self.tabWidget.setCurrentWidget(newtab)
        
        self.file_path.setText(str(root_path))
        self.project_file_paths_list[i] = str(root_path)
        self.tableWidget2.resizeColumnsToContents()
        
        #Create hash digest of new project file (to track if it's been modified)
        tab_index, key_index = retrieve_current_project_key_index()
        dict_list_image = self.project_scenes_list[key_index].prepare_project_data_and_items()
        self.hash_list_open[key_index] = hashlib.sha256(str(dict_list_image).encode()).hexdigest()
         
    def project_open(self):
        #Determine which project scene/layout is the current one
        path = str(root_path)
        tab_index, key_index = retrieve_current_project_key_index()
        if key_index is not None:
            proj = self.project_scenes_list[key_index]       
            proj_path = proj.design_settings['file_path_1']
            if not proj_path: #File path is empty
                path = str(root_path)
            else:
                path = proj_path
        
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', path,
                                                      filter = '*.slb')
        if fname[0]:
            dict_list = pickle.load(open(fname[0], 'rb'))
            truncated_file_path = fname[0].rsplit("/", 1) 
            self.file_path.setText(truncated_file_path[0])
            # Load new project
            i = set_new_key(self.project_layouts_list)  
            self.project_file_paths_list[i] = truncated_file_path[0]
            # Set the project name to the file name (in case it was changed)
            base_file_name = truncated_file_path[1].rsplit(".", 1)
            project_name = base_file_name[0]
            #Verify if file/project name already exists
            is_project_duplicate = False
            if project_name in self.project_names_list:
                is_project_duplicate = True
                project_name = project_name + '_' + str(i)
            
            self.project_names_list[project_name] = i
            self.project_layouts_list[i] = 'layout_' + project_name    
            self.project_scenes_list[i] = DesignLayoutScene(project_name)
            self.project_views_list[i] = DesignLayoutView(self.project_scenes_list[i], self)
      
            self.project_layouts_list[i] = QtWidgets.QHBoxLayout()
            newtab = QtWidgets.QWidget()
            newtab.setLayout(self.project_layouts_list[i])
            self.tabWidget.addTab(newtab, project_name)    
            self.project_layouts_list[i].addWidget(self.project_views_list[i])
            self.project_layouts_list[i].setContentsMargins(2, 2, 2, 2)
            self.tabWidget.setCurrentWidget(newtab)
        
            #Setup project settings
            self.project_scenes_list[i].design_settings = dict_list[0]  
            proj_settings = self.project_scenes_list[i].design_settings
            # Check for presence of edit_script_path
            if not 'edit_script_path' in proj_settings.keys():
                execute_path = 'start .\wscite\SciTE -open:'
                proj_settings['edit_script_path'] = execute_path
            
            self.project_scenes_list[i].design_settings['project_name'] = project_name
            color = self.project_scenes_list[i].design_settings['back_color']
            self.project_views_list[i].setBackgroundBrush(QtGui.QBrush(QtGui.QColor(color)))
            
            w = self.project_scenes_list[i].design_settings['scene_width']
            h = self.project_scenes_list[i].design_settings['scene_height']
            self.project_scenes_list[i].setSceneRect(QtCore.QRectF(0,0,w,h))
        
            if self.project_scenes_list[i].design_settings['grid_enabled'] == 2:
                line_opacity = self.project_scenes_list[i].design_settings['grid_opacity']
                g_color = self.project_scenes_list[i].design_settings['grid_color']
                g_width = self.project_scenes_list[i].design_settings['grid_line_width']
                g_style = self.project_scenes_list[i].design_settings['grid_line_style']       
                line_style = set_line_type(g_style)
                self.project_scenes_list[i].lines = []
                pen_grid = QtGui.QPen(QtGui.QColor(g_color), g_width, line_style)
                self.project_scenes_list[i].draw_grid(pen_grid)
                self.project_scenes_list[i].set_opacity(line_opacity) 
                     
            if window.project_scenes_list[i].design_settings['border_enabled'] == 2:
                b_opacity = self.project_scenes_list[i].design_settings['border_opacity'] 
                b_width = self.project_scenes_list[i].design_settings['border_width']
                b_color = self.project_scenes_list[i].design_settings['border_color']
                self.project_scenes_list[i].border = []
                pen_border = QtGui.QPen(QtGui.QColor(b_color), b_width, QtCore.Qt.SolidLine)
                self.project_scenes_list[i].draw_border(pen_border)
                self.project_scenes_list[i].set_opacity_border(b_opacity)   

            self.project_views_list[i].ensureVisible(0, 0, w/2, h/2)               
    
            proj = self.project_scenes_list[i] #Local reference to current project
            #Setup functional blocks
            counter = 0
            while counter < len(dict_list[1]):
                keys = list(dict_list[1].keys())
                fb_key = keys[counter]
                self.project_scenes_list[i].fb_list[fb_key] = dict_list[1][fb_key].fb_name 
                
                self.fb_view = self.project_scenes_list[i].fb_design_view_list
                self.fb_view[fb_key] = dict_list[1][fb_key].fb_name
                        
                #Instantiate new FB and FB design view objects
                name = dict_list[1][fb_key].fb_name
                display_name = dict_list[1][fb_key].display_name
                display_port_name = dict_list[1][fb_key].display_port_name
                geometry = dict_list[1][fb_key].fb_geometry
                dim = dict_list[1][fb_key].fb_dim
                position = dict_list[1][fb_key].fb_position
                ports = dict_list[1][fb_key].fb_ports_list
                script = dict_list[1][fb_key].fb_script_module
                icon_display = dict_list[1][fb_key].fb_icon_display         
                icon = dict_list[1][fb_key].fb_icon
                icon_x = dict_list[1][fb_key].fb_icon_x
                icon_y = dict_list[1][fb_key].fb_icon_y
                parameters = dict_list[1][fb_key].fb_parameters_list
                results = dict_list[1][fb_key].fb_results_list
                text_size = dict_list[1][fb_key].text_size
                text_length = dict_list[1][fb_key].text_length
                text_color = dict_list[1][fb_key].text_color
                text_bold = dict_list[1][fb_key].text_bold
                text_italic = dict_list[1][fb_key].text_italic
                color = dict_list[1][fb_key].fb_color
                color2 = dict_list[1][fb_key].fb_color_2
                grad = dict_list[1][fb_key].fb_gradient
                border_color = dict_list[1][fb_key].fb_border_color
                border_style = dict_list[1][fb_key].fb_border_style
                text_pos_x = dict_list[1][fb_key].text_pos_x
                text_pos_y = dict_list[1][fb_key].text_pos_y
                
                port_label_size = dict_list[1][fb_key].port_label_size
                port_label_bold = dict_list[1][fb_key].port_label_bold
                port_label_italic = dict_list[1][fb_key].port_label_italic
                port_label_color = dict_list[1][fb_key].port_label_color
                
                #Re-build functional blocks (data model and design view)
                self.project_scenes_list[i].fb_list[fb_key] = models.FunctionalBlock(fb_key,
                                    name, display_name, display_port_name, geometry, dim,
                                    position, script, icon_display, icon, icon_x, icon_y,
                                    parameters, results, text_size, text_length, text_color, 
                                    text_bold, text_italic, color, color2, grad,
                                    border_color, border_style, text_pos_x, text_pos_y,
                                    port_label_size, port_label_bold, port_label_italic,
                                    port_label_color)
                self.project_scenes_list[i].fb_list[fb_key].fb_ports_list = ports
                self.fb_view[fb_key] = FunctionalBlockDesignView(fb_key,
                                    name, display_name, display_port_name, geometry, 
                                    dim[0], dim[1], script, icon_display, icon, icon_x, icon_y,
                                    text_size, text_length, text_color, text_bold, text_italic,
                                    color, color2, grad, border_color, border_style,
                                    text_pos_x, text_pos_y, port_label_size, port_label_bold,
                                    port_label_italic, port_label_color) 
                self.fb_view[fb_key].update_ports(fb_key)
                  
                #Add new objects to graphics view space
                self.fb_view[fb_key].setPos(position)           
                self.project_scenes_list[i].addItem(self.fb_view[fb_key])
                counter += 1
                
            #Instantiate saved signal links===============================================
            counter = 0
            while counter < len(dict_list[2]):
                keys = list(dict_list[2].keys())
                l = keys[counter]   
                link_key = dict_list[2][l].link_key
                link_name = dict_list[2][l].link_name
                fb_start_key = dict_list[2][l].fb_start_key
                fb_start = dict_list[2][l].fb_start
                start_port = dict_list[2][l].start_port
                start_port_ID = dict_list[2][l].start_port_ID
                fb_end_key = dict_list[2][l].fb_end_key
                fb_end = dict_list[2][l].fb_end
                end_port = dict_list[2][l].end_port
                end_port_ID = dict_list[2][l].end_port_ID
                line_mode = dict_list[2][l].line_mode
                
                #Setup saved links      
                end_port_pos = self.fb_view[fb_end_key].ports[end_port_ID].scenePos()  
                port_start = self.fb_view[fb_start_key].ports[start_port_ID]
                window.startedLink = set_link.SetLink(port_start, None, line_mode, proj)
                window.startedLink.setEndPos(end_port_pos)
                window.startedLink.endConnectState = True
                window.startedLink.setToPort(self.fb_view[fb_end_key].ports[end_port_ID])      
                window.startedLink.setEndPos(end_port_pos)
                         
                window.startedLink.portlink.fromPort_portID = start_port_ID
                window.startedLink.portlink.fromPort_fb_key = fb_start_key
                window.startedLink.portlink.toPort_portID = end_port_ID
                window.startedLink.portlink.toPort_fb_key = fb_end_key
                window.startedLink.portlink.link_key = link_key
                window.startedLink.portlink.setZValue(-50)
                
                sig = window.startedLink.portlink.signal
                window.startedLink.portlink.set_line_color(sig, True)
                            
                window.startedLink.portlink.setToolTip('Link type: '+ str(sig) + '\n'
                                            + 'From port: ' + str(fb_start) + '/' 
                                            + str(start_port) + '\n' + 'To port: ' 
                                            + str(fb_end) + '/' + str(end_port))
                window.startedLink = None
                
                #Re-populate signal links list dictionary
                window.project_scenes_list[i].signal_links_list[link_key] = (
                        models.SignalLink(link_key, link_name, fb_start_key, fb_start, 
                                          start_port, start_port_ID, fb_end_key, fb_end, 
                                          end_port, end_port_ID, line_mode) )
                #Update associated ports
                self.fb_view[fb_start_key].ports[start_port_ID].link_key = link_key
                self.fb_view[fb_start_key].ports[start_port_ID].link_name = link_name
                self.fb_view[fb_start_key].ports[start_port_ID].connected = True
                self.fb_view[fb_end_key].ports[end_port_ID].link_key = link_key
                self.fb_view[fb_end_key].ports[end_port_ID].link_name = link_name
                self.fb_view[fb_end_key].ports[end_port_ID].connected = True      
                proj.fb_list[fb_start_key].fb_ports_list[start_port_ID-1][5] = True
                proj.fb_list[fb_end_key].fb_ports_list[end_port_ID-1][5] = True
                counter += 1
                
            #Setup saved description boxes================================================
            counter = 0
            while counter < len(dict_list[3]):
                keys = list(dict_list[3].keys())
                box = keys[counter]   
                desc_key = dict_list[3][box].desc_key
                geometry = dict_list[3][box].box_geometry
                dim = dict_list[3][box].box_dim
                position = dict_list[3][box].box_position
                w_text = dict_list[3][box].text_width
                d_text = dict_list[3][box].desc_text
                color = dict_list[3][box].fill_color
                color2 = dict_list[3][box].fill_color_2
                op = dict_list[3][box].opacity
                grad = dict_list[3][box].gradient
                b_color = dict_list[3][box].border_color
                text_size = dict_list[3][box].text_size
                text_color = dict_list[3][box].text_color
                text_bold = dict_list[3][box].text_bold
                text_italic = dict_list[3][box].text_italic
                border_style = dict_list[3][box].border_style
                border_width = dict_list[3][box].border_width
                text_pos_x = dict_list[3][box].text_pos_x
                text_pos_y = dict_list[3][box].text_pos_y
        
                proj.desc_box_list[desc_key] = models.DescriptionBox(desc_key, d_text,
                                   position, dim, geometry, w_text, color, color2, op, grad,
                                   b_color, text_size, text_color, text_bold, text_italic,
                                   border_style, border_width, text_pos_x, text_pos_y)       
                proj.desc_box_design_view_list[desc_key] = DescriptionBoxDesignView(desc_key,
                                   d_text, geometry, dim[0], dim[1], color, color2, op, grad,
                                   b_color, w_text, text_size, text_color, text_bold,
                                   text_italic, border_style, border_width, text_pos_x,
                                   text_pos_y)
                
                proj.desc_box_design_view_list[desc_key].setPos(position)           
                proj.addItem(proj.desc_box_design_view_list[desc_key])
                counter += 1
                
            #Setup saved data boxes
            counter = 0
            while counter < len(dict_list[4]):
                keys = list(dict_list[4].keys())
                d = keys[counter]
                data_key = dict_list[4][d].data_key
                t_text = dict_list[4][d].title_text
                t_geometry = dict_list[4][d].title_geometry
                t_position = dict_list[4][d].title_position
                t_text_width = dict_list[4][d].title_text_width
                t_width = dict_list[4][d].title_width        
                t_height = dict_list[4][d].title_height
                t_color = dict_list[4][d].title_box_color
                t_opacity = dict_list[4][d].title_box_opacity
                t_border_color = dict_list[4][d].title_border_color
                t_text_size = dict_list[4][d].title_text_size
                t_text_color = dict_list[4][d].title_text_color
                t_text_bold = dict_list[4][d].title_text_bold     
                t_text_italic= dict_list[4][d].title_text_italic        
                t_border_style = dict_list[4][d].title_border_style       
                t_border_width = dict_list[4][d].title_border_width      
                t_text_pos_x = dict_list[4][d].title_text_pos_x
                t_text_pos_y = dict_list[4][d].title_text_pos_y
                
                d_box_geometry = dict_list[4][d].data_box_geometry 
                d_box_position = dict_list[4][d].data_box_position
                d_box_width = dict_list[4][d].data_box_width
                d_box_height = dict_list[4][d].data_box_height    
                d_box_color = dict_list[4][d].data_box_color
                d_box_opacity = dict_list[4][d].data_box_opacity
                d_box_gradient = dict_list[4][d].data_box_gradient
                d_border_color = dict_list[4][d].data_border_color
                d_box_border_style = dict_list[4][d].data_box_border_style
                d_box_border_width = dict_list[4][d].data_box_border_width
                d_text_size = dict_list[4][d].data_text_size
                d_width = dict_list[4][d].data_width
                d_width_2 = dict_list[4][d].value_width
                d_text_pos_x = dict_list[4][d].data_text_pos_x
                d_text_pos_y = dict_list[4][d].data_text_pos_y
                data_source_file = dict_list[4][d].data_source_file
                
                proj.data_box_list[data_key] = models.DataBox(data_key, t_text, t_geometry,
                                   t_position, t_width, t_height, t_color, t_opacity,
                                   t_border_color, t_text_width, t_text_size, t_text_color,
                                   t_text_bold, t_text_italic, t_border_style,
                                   t_border_width, t_text_pos_x, t_text_pos_y, d_box_geometry,
                                   d_box_position, d_box_width, d_box_height, d_box_color, 
                                   d_box_opacity, d_box_gradient, d_border_color,
                                   d_box_border_style, d_box_border_width, d_text_size,
                                   d_width, d_width_2, d_text_pos_x, d_text_pos_y, 
                                   data_source_file)
                
                proj.data_box_design_view_list[data_key] = DataBoxDesignView(data_key,
                                   t_text, t_geometry, t_width, t_height, t_color, t_opacity,
                                   t_border_color, t_text_width, t_text_size, t_text_color,
                                   t_text_bold, t_text_italic, t_border_style, t_border_width,
                                   t_text_pos_x, t_text_pos_y, d_box_geometry, d_box_width, 
                                   d_box_height, d_box_color, d_box_opacity, d_box_gradient,
                                   d_border_color, d_box_border_style, d_box_border_width,
                                   d_text_size, d_width, d_width_2, d_text_pos_x,
                                   d_text_pos_y, data_source_file)
                
                proj.data_box_design_view_list[data_key].setPos(d_box_position)           
                proj.addItem(proj.data_box_design_view_list[data_key])
                counter += 1
                
            #Setup saved text boxes
            counter = 0
            while counter < len(dict_list[5]):
                keys = list(dict_list[5].keys())
                t = keys[counter]
                text_key = dict_list[5][t].text_key
                geometry = dict_list[5][t].text_geometry
                position = dict_list[5][t].text_position
                w_text = dict_list[5][t].text_width
                text = dict_list[5][t].text
                color = dict_list[5][t].text_color
                text_size = dict_list[5][t].text_size
                text_bold = dict_list[5][t].text_bold
                text_italic = dict_list[5][t].text_italic
        
                proj.text_list[text_key] = models.TextBox(text_key, text, position, geometry,
                                           w_text, color, text_size, text_bold, text_italic)      
                proj.text_design_view_list[text_key] = TextBoxDesignView(text_key, geometry,
                                           text, w_text, color, text_size, text_bold,
                                           text_italic)
                proj.text_design_view_list[text_key].setPos(position)           
                proj.addItem(proj.text_design_view_list[text_key])
                counter += 1
                
            #Setup saved line-arrows
            counter = 0
            while counter < len(dict_list[6]):
                keys = list(dict_list[6].keys())
                link = keys[counter]
                key = dict_list[6][link].key
                geometry = dict_list[6][link].geometry
                position = dict_list[6][link].position
                line_width = dict_list[6][link].line_width
                line_style = dict_list[6][link].line_style
                arrow = dict_list[6][link].arrow
                color = dict_list[6][link].color
    
                proj.line_arrow_list[key] = models.LineArrow(key, position, geometry, color,
                                     line_width, line_style, arrow)       
                proj.line_arrow_design_view_list[key] = LineArrowDesignView(key, geometry,
                                     color, line_width, line_style, arrow)
                proj.line_arrow_design_view_list[key].setPos(position)           
                proj.addItem(proj.line_arrow_design_view_list[key])
                counter += 1
    
            if is_project_duplicate == True:
                msg = QtWidgets.QMessageBox()
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Project file has been renamed to: ' + project_name)
                msg.setWindowTitle("Project open dialog")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()     
    
            #Setup design settings data views (toolbar)
            max_iterations = self.project_scenes_list[i].design_settings['iterations']
            max_segments = self.project_scenes_list[i].design_settings['feedback_segments']
            self.iterationsSelector.setMaximum(max_iterations)
            self.tableWidget2.item(0, 1).setText(format(max_iterations, 'n'))
            self.tableWidget2.item(1, 1).setText(format(max_segments, 'n'))
            self.tableWidget2.resizeColumnsToContents()
            
            sample_rate = self.project_scenes_list[i].design_settings['sampling_rate']
            time = self.project_scenes_list[i].design_settings['time_window']
            samples = self.project_scenes_list[i].design_settings['num_samples']
            
            self.tableWidget.item(0, 1).setText(format(sample_rate, '0.3E'))
            self.tableWidget.item(1, 1).setText(format(time, '0.3E'))
            self.tableWidget.item(2, 1).setText(format(samples, '0.3E'))        
            self.tableWidget.resizeColumnsToContents()
            
            if self.project_scenes_list[i].design_settings['feedback_enabled'] == 2:
                self.tableWidget3.item(1, 1).setText('')
            else:
                self.tableWidget3.item(1, 1).setText('N/A')
            
            #Create hash digest of opened project (to track for modifications)
            tab_index, key_index = retrieve_current_project_key_index()
            dict_list_image = self.project_scenes_list[key_index].prepare_project_data_and_items()
            self.hash_list_open[key_index] = hashlib.sha256(str(dict_list_image).encode()).hexdigest()
        
    def project_save(self):
        #Determine which project scene/layout is the current one
        tab_index, key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[key_index]
        project_name = self.tabWidget.tabText(tab_index)
        
        #Save project data (fb_list and simulation settings)
        items = proj.items()
        for item in items:
            if type(item) is FunctionalBlockDesignView:
                key = item.fb_key
                proj.fb_list[key].fb_results_list = []
        dict_list_save = proj.prepare_project_data_and_items()
        
        try:
            proj_path = proj.design_settings['file_path_1']
            # Python object structure is serialized into a byte stream (non human readable)
            # Default protocol is used (Version 3). Can only be converted back using Python
            # Suffix used for SystemLab-Design file is .slb (systemlab binary)
            # Ref: https://docs.python.org/3/library/pickle.html
            pickle.dump(dict_list_save, open(proj_path + project_name + '.slb', 'wb'))
            #Update hash digest of saved project
            dict_list_image = proj.prepare_project_data_and_items()
            self.hash_list_open[key_index] = hashlib.sha256(str(dict_list_image).encode()).hexdigest()
            # Send update to Info/Status (StatusBar)
            if not proj_path:
                config.status.setText('File saved to: '+ str(root_path))
            else:
                config.status.setText('File saved to: '+ str(proj_path))
        except:
            msg = QtWidgets.QMessageBox()
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            main = 'Project file could not be saved (file path does not exist)'
            msg.setText(main)
            info = 'Please verify the file path defined in the project settings dialog'
            msg.setInformativeText(info)
            msg.setStyleSheet("QLabel{height: 70px; min-height: 70px; max-height: 70px;}")
            msg.setStyleSheet("QLabel{width: 350px; min-width: 350px; max-width: 350px;}")
            msg.setWindowTitle("Project file save error")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close() 
    
    def project_save_as(self):  
        #Determine which project scene/layout is the current one
        tab_index, key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[key_index]       
        path = proj.design_settings['file_path_1']

        fileName = QtWidgets.QFileDialog.getSaveFileName(self, 'Save project as...',
                                                         path, filter = '*.slb')
        if fileName[0]:              
            #Retrieve project name from file path (C:\filepath\projectname.slb)
            truncated_file_str_1 = fileName[0].rsplit("/")
            last_element = truncated_file_str_1[-1]
            final_text_str = last_element.split('.')
            saved_project_name = final_text_str[0]
            
            truncated_file_str_2 = fileName[0].rsplit("/", 1)
            self.file_path.setText(truncated_file_str_2[0])
            self.project_file_paths_list[key_index] = truncated_file_str_2[0]
            
            # Remove current name from project_names_list
            for name in self.project_names_list:
                if self.project_names_list[name] == key_index:
                    break
            del self.project_names_list[name]   
            #Make sure name is not already being used in another tab
            name_duplicate = False
            for name in self.project_names_list:
                if name == saved_project_name:
                    name_duplicate = True
                    break
            
            if name_duplicate:
                i = set_new_key(self.project_layouts_list)  
                msg = QtWidgets.QMessageBox()
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText('Project name ' + saved_project_name
                            + ' is already being used in the application')
                msg.setInformativeText('The project name will be renamed as '
                                       + saved_project_name + '_'+str(i-1))
                msg.setStyleSheet("QLabel{height: 70px; min-height: 70px; max-height: 70px;}")
                msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
                msg.setWindowTitle("Project save as dialog")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                saved_project_name = saved_project_name + '_' + str(i-1)
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                    
            #Update associated project dictionaries (before pickling)
            self.project_names_list[saved_project_name] = key_index
            window.project_layouts_list[key_index] = saved_project_name
            window.project_scenes_list[key_index].scene_name = saved_project_name
            window.project_scenes_list[key_index].design_settings['project_name'] = saved_project_name
            window.project_views_list[key_index].scene = saved_project_name
            
            #Update title of project tab to reflect updated project name
            window.tabWidget.setTabText(tab_index, saved_project_name)
            
            #Save binary file and update hash digest of saved project
            dict_list_save = self.project_scenes_list[key_index].prepare_project_data_and_items()
            # Python object structure is serialized into a byte stream (non human readable)
            # Default protocol is used (Version 3). Can only be converted back using Python
            # Suffix used for SystemLab-Design file is .slb (systemlab binary)
            # Ref: https://docs.python.org/3/library/pickle.html
            pickle.dump(dict_list_save, open(str(fileName[0]), 'wb'))       
            self.hash_list_open[key_index] = hashlib.sha256(str(dict_list_save).encode()).hexdigest()
           
    def project_close(self):
        tab_index, key_index = retrieve_current_project_key_index()   
        project_name = self.tabWidget.tabText(tab_index)
        dict_list_close = self.project_scenes_list[key_index].prepare_project_data_and_items()
        self.hash_list_close[key_index] = hashlib.sha256(str(dict_list_close).encode()).hexdigest()
        
        if self.hash_list_close[key_index] != self.hash_list_open[key_index]:  
            msg = QtWidgets.QMessageBox()
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setIcon(QtWidgets.QMessageBox.Question)
            msg.setText(project_name + ' has been modified')
            msg.setInformativeText('Do you want to save the changes?')
            msg.setWindowTitle("Project close dialog")
            msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No | 
                                   QtWidgets.QMessageBox.Cancel)
            rtnval = msg.exec()        
            if rtnval == QtWidgets.QMessageBox.Yes: #Overwrite the file with updated design/settings
                items = self.project_scenes_list[key_index].items()
                for item in items:
                    if type(item) is DataBoxDesignView:
                        ID = item.data_source_file
                        config_data_panel.data_box_dict[ID] = {}
                    if type(item) is FunctionalBlockDesignView:
                        key = item.fb_key
                        self.project_scenes_list[key_index].fb_list[key].fb_results_list = []
                self.project_save()
                #Close any data port dialogs that are still open
                counter = 0
                l_data_views = len(self.project_scenes_list[key_index].data_port_view_list)
                while counter < l_data_views:
                    keys = list(window.project_scenes_list[key_index].data_port_view_list.keys())
                    k = keys[counter]
                    self.project_scenes_list[key_index].data_port_view_list[k].close()
                    counter += 1
                #Check if previous sim status/data windows are open & close
                if config.sim_status_win is not None:
                    config.sim_status_win.close()
                if config.sim_data_view is not None:
                    config.sim_data_view.close()
                #Delete all dictionaries linked to the project
                del self.project_names_list[project_name]
                del self.project_views_list[key_index]
                del self.project_scenes_list[key_index]
                del self.project_layouts_list[key_index]
                del self.project_file_paths_list[key_index]
                self.tabWidget.removeTab(tab_index)
                msg.close()               
            elif rtnval == QtWidgets.QMessageBox.No: #Do not save changes and close the file
                items = self.project_scenes_list[key_index].items()
                for item in items:
                    if type(item) is DataBoxDesignView:
                        ID = item.data_source_file
                        config_data_panel.data_box_dict[ID] = {}
                    if type(item) is FunctionalBlockDesignView:
                        key = item.fb_key
                        self.project_scenes_list[key_index].fb_list[key].fb_results_list = []
                #Close any data port dialogs that are still open
                counter = 0
                l_data_views = len(self.project_scenes_list[key_index].data_port_view_list)
                while counter < l_data_views:
                    keys = list(window.project_scenes_list[key_index].data_port_view_list.keys())
                    k = keys[counter]
                    self.project_scenes_list[key_index].data_port_view_list[k].close()
                    counter += 1
                #Check if previous sim status/data windows are open & close
                if config.sim_status_win is not None:
                    config.sim_status_win.close()
                if config.sim_data_view is not None:
                    config.sim_data_view.close()
                #Delete all dictionaries linked to the project
                del self.project_names_list[project_name]
                del self.project_views_list[key_index]
                del self.project_scenes_list[key_index]
                del self.project_layouts_list[key_index]
                del self.project_file_paths_list[key_index]
                self.tabWidget.removeTab(tab_index)
                msg.close()             
            else:
                self.app_quit = False
                msg.close()
            #Do nothing (tab and project stay in place)
        else: #As there are no changes the project/tab is simply closed
            items = self.project_scenes_list[key_index].items()
            for item in items:
                if type(item) is DataBoxDesignView:
                    ID = item.data_source_file
                    config_data_panel.data_box_dict[ID] = {}
                if type(item) is FunctionalBlockDesignView:
                    key = item.fb_key
                    self.project_scenes_list[key_index].fb_list[key].fb_results_list = []
            #Close any data port dialogs that are still open
            counter = 0
            l_data_views = len(self.project_scenes_list[key_index].data_port_view_list)
            while counter < l_data_views:
                keys = list(window.project_scenes_list[key_index].data_port_view_list.keys())
                k = keys[counter]
                self.project_scenes_list[key_index].data_port_view_list[k].close()
                counter += 1
            #Check if previous sim status/data windows are open & close
            if config.sim_status_win is not None:
                config.sim_status_win.close()
            if config.sim_data_view is not None:
                config.sim_data_view.close()
            #Delete all dictionaries linked to the project
            del self.project_names_list[project_name]
            del self.project_views_list[key_index]
            del self.project_scenes_list[key_index]
            del self.project_layouts_list[key_index]
            del self.project_file_paths_list[key_index]
            self.tabWidget.removeTab(tab_index)
        return self.app_quit
    
    def delete_selected_items(self):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        for item in items:
            if type(item) is FunctionalBlockDesignView:                      
                i = item.fb_key
                item.deleteLinks(i)                       
                del proj.fb_list[i]
                del proj.fb_design_view_list[i]
                window.tableWidget2.resizeColumnsToContents()                                                   
            if type(item) is DataBoxDesignView:                                            
                i = item.data_key
                del proj.data_box_list[i]
                del proj.data_box_design_view_list[i]                                            
            if type(item) is DescriptionBoxDesignView:                                            
                i = item.desc_key
                del proj.desc_box_list[i]
                del proj.desc_box_design_view_list[i]                                              
            if type(item) is TextBoxDesignView:                      
                i = item.text_key                       
                del proj.text_list[i]
                del proj.text_design_view_list[i]                                              
            if type(item) is LineArrowDesignView:
                i = item.key
                del proj.line_arrow_list[i]
                del proj.line_arrow_design_view_list[i]                                              
            proj.removeItem(item) 
            del item
        self.action_Delete.setEnabled(False)
        self.action_CopyPaste.setEnabled(False)
        self.action_CopyPasteToAnotherProj.setEnabled(False)
        
    def copy_paste_selected_items(self):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[key_index]
        items = proj.selectedItems()       
        for item in items:
            if type(item) is FunctionalBlockDesignView:                      
                item.copy_paste_fb(item, key_index, key_index)                                                
            if type(item) is DataBoxDesignView:                                            
                item.copy_paste_data_box(item, key_index, key_index)                                            
            if type(item) is DescriptionBoxDesignView:                                            
                item.copy_paste_desc_box(item, key_index, key_index)                                            
            if type(item) is TextBoxDesignView:                      
                item.copy_paste_text_box(item, key_index, key_index)                                              
            if type(item) is LineArrowDesignView:
                item.copy_paste_line_arrow(item, key_index, key_index)                                       
        self.action_CopyPaste.setEnabled(False)
        self.action_CopyPasteToAnotherProj.setEnabled(False)
        
    def copy_paste_selected_items_to_another_proj(self):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        #Load all open projects into the dialog
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()                       
                for item in items:
                    if type(item) is FunctionalBlockDesignView:
                        item.copy_paste_fb(item, key_index, new_index)
                        window.tableWidget2.resizeColumnsToContents()                          
                    if type(item) is DataBoxDesignView:                                            
                        item.copy_paste_data_box(item, key_index, new_index)                                      
                    if type(item) is DescriptionBoxDesignView:                                            
                        item.copy_paste_desc_box(item, key_index, new_index)                                           
                    if type(item) is TextBoxDesignView:                      
                        item.copy_paste_text_box(item, key_index, new_index)                                            
                    if type(item) is LineArrowDesignView:
                        item.copy_paste_line_arrow(item, key_index, new_index)                                      
                self.action_CopyPaste.setEnabled(False)
                self.action_CopyPasteToAnotherProj.setEnabled(False)
                
    def open_script_editor(self):
        tab_index, key_index = retrieve_current_project_key_index()
        script = window.project_scenes_list[key_index].design_settings['edit_script_path']
        try:
            os.system(script)
        except:
            self.error_message_script_editor()  
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('The script editor application could not be successfully loaded.')
            msg.setInformativeText('Please verify the Code/script editor execute path' 
                                   + ' under Project Settings/Advanced settings.')
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
            msg.setWindowTitle("Loading error: Code/script editor application")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
            
    def change_project_tab_event(self):
        tab_index, key_index = retrieve_current_project_key_index()
        if key_index is not None:
            proj_settings = self.project_scenes_list[key_index].design_settings
            iterations = proj_settings['iterations']
            sample_rate = proj_settings['sampling_rate']
            time = proj_settings['time_window']
            samples = proj_settings['num_samples']
            feedback_segments = proj_settings['feedback_segments']
            curr_iter = proj_settings['current_iteration']
            curr_seg = proj_settings['feedback_current_segment']
            feed_mode = proj_settings['feedback_enabled']
        else:
            iterations = 1
            curr_iter = 1
            sample_rate = config.sampling_rate_default
            time = config.simulation_time_default
            samples = config.num_samples_default
            feedback_segments = config.num_samples_default
            curr_seg = 1
            feed_mode = 0
        
        self.iterationsSelector.setMinimum(1)
        self.iterationsSelector.setMaximum(iterations)
        self.iterationsSelector.setValue(curr_iter)
        
        if key_index in window.project_file_paths_list:
            project_file_path = window.project_file_paths_list[key_index]
            self.file_path.setText(project_file_path)
            
        self.tableWidget2.item(0, 1).setText(format(iterations, 'n'))
        self.tableWidget2.item(1, 1).setText(format(feedback_segments, 'n'))
        window.tableWidget2.resizeColumnsToContents()
        
        self.tableWidget3.item(0, 1).setText(format(curr_iter, 'n'))
        if feed_mode == 2:
            self.tableWidget3.item(1, 1).setText(format(curr_seg, 'n'))
        else:
            self.tableWidget3.item(1, 1).setText('N/A')
        window.tableWidget3.resizeColumnsToContents()
            
        self.tableWidget.item(0, 1).setText(format(sample_rate, '0.3E'))
        self.tableWidget.item(1, 1).setText(format(time, '0.3E'))
        self.tableWidget.item(2, 1).setText(format(samples, '0.3E'))        
        self.tableWidget.resizeColumnsToContents()
        
    def count_fb_items_in_scene(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index() 
        fb_num = 0
        if self.key_index is not None:
            fb_list = self.project_scenes_list[self.key_index].fb_list
            fb_num = len(fb_list)
        return fb_num
          
    def application_close(self):
        self.app_close_message()
        rtnval = self.msg.exec()              
        if rtnval == QtWidgets.QMessageBox.Yes:
            print(self.project_layouts_list)
            if len(self.project_layouts_list) > 0:
                for i in range(1, len(self.project_layouts_list)+1):
                    window.tabWidget.setCurrentIndex(i-1)
                    self.app_quit = self.project_close()
                    if self.app_quit == False:
                        break
            if self.app_quit == True:
                config.app.quit()
        
    def closeEvent(self, event): #QT specific method
        self.app_close_message()
        rtnval = self.msg.exec()
        if rtnval == QtWidgets.QMessageBox.No:
            event.ignore()                     
        if rtnval == QtWidgets.QMessageBox.Yes:
            if len(self.project_layouts_list) > 0:
                for i in range(1, len(self.project_layouts_list)+1):
                    window.tabWidget.setCurrentIndex(i-1)
                    self.app_quit = self.project_close()
                    if self.app_quit == False:
                        break
            if self.app_quit == True:
                event.accept()
            else:
                event.ignore()
    
    def app_close_message(self):
        self.msg = QtWidgets.QMessageBox()
        syslab_icon = set_icon_window()
        self.msg.setWindowIcon(syslab_icon)
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setWindowTitle('Application exit')
        self.msg.setText('Are you sure you want to exit the application?')
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes|QtWidgets.QMessageBox.No)
        
    def add_functional_block(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index()  
        fb_list = self.project_scenes_list[self.key_index].fb_list
        i = set_new_key(fb_list)
        scene = self.project_scenes_list[self.key_index]
        scene.insert_functional_block(i)   
        scene.fb_design_view_list[i].setPos(500,500)
        scene.addItem(scene.fb_design_view_list[i])
    
    def add_description_box(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index()  
        desc_list = self.project_scenes_list[self.key_index].desc_box_list
        i = set_new_key(desc_list)
        scene = self.project_scenes_list[self.key_index]
        scene.insert_desc_box(i) 
        scene.desc_box_design_view_list[i].setPos(500,500)
        scene.addItem(scene.desc_box_design_view_list[i])
        
    def add_data_box(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index()  
        data_list = self.project_scenes_list[self.key_index].data_box_list
        i = set_new_key(data_list)
        scene = self.project_scenes_list[self.key_index]
        scene.insert_data_box(i)        
        scene.data_box_design_view_list[i].setPos(500,500)
        scene.addItem(scene.data_box_design_view_list[i])
        
    def add_text_box(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index()  
        text_list = self.project_scenes_list[self.key_index].text_list
        i = set_new_key(text_list)
        scene = self.project_scenes_list[self.key_index]
        scene.insert_text_box(i) 
        scene.text_design_view_list[i].setPos(500,500)
        scene.addItem(scene.text_design_view_list[i])
        
    def add_line_arrow(self):
        self.tab_index, self.key_index = retrieve_current_project_key_index()  
        line_arrow_list = self.project_scenes_list[self.key_index].line_arrow_list
        i = set_new_key(line_arrow_list)
        scene = self.project_scenes_list[self.key_index]
        scene.insert_line_arrow(i) 
        scene.line_arrow_design_view_list[i].setPos(500,500)
        scene.addItem(scene.line_arrow_design_view_list[i])
        
    def scene_image(self):
        tab_index, key_index = retrieve_current_project_key_index()
        scene = self.project_scenes_list[key_index]
        proj_view = window.project_views_list[key_index]
        scene.save_image_scene(proj_view)
        
    def open_doc_html(self):
#        Ref: stackoverflow.com 
#        https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-
#        browser-from-python?rq=1 (accessed: 28 Feb 2019)
#        url = 'file:///path/to/your/file/testdata.html'
        
        # Version for web site
        url = "https://systemlabdesign.com/syslab_documentation/_build/html/index.html"
        webbrowser.open(url)
        
        # Version local (for testing)
#        doc_root = os.path.join(root_path, 'syslab_documentation/_build/html/index.html') 
#        doc_root = os.path.normpath (doc_root)
#        webbrowser.open(doc_root, new=2)            
        
    def open_about(self):
        global about_dialog
        about_dialog = AboutGUI()
        about_dialog.show()

    '''Methods for creating links between FB ports========================================
    Sections of code design below (start_link, sceneMouseMoveEvent,
    sceneMouseReleaseEvent) based on 'DiagramEditorProto.py' (class connection, 
    diagramEditor, diagramScene)
    Author first name: Windel - many thanks to the author!
    Copy of original code is located at the end of module systemlab_set_link.py - 
    Source - Creating a diagram editor,
    http://www.windel.nl/?section=pyqtdiagrameditor (downloaded 11 Feb 2018) 
    '''    
    def start_link(self, port):
        #Start link requires mouse to be hovering over a port object (port must be OUT) 
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        self.startedLink = set_link.SetLink(port, None, self.lineConnectionMode,
                                            self.project_scenes_list[self.key_index])
    
    def sceneMouseMoveEvent(self, event):
        #Mouse movement rebuilds the link continously from port to mouse scene position
        if self.startedLink:
            pos = event.scenePos()
            self.startedLink.setEndPos(pos)
            signal_startPort = self.startedLink.fromPort.signal_type
            self.startedLink.portlink.set_line_color(signal_startPort, False)
            
    def sceneMouseReleaseEvent(self, event):
        #After releasing the mouse, checks are performed to validate and complete the link.
        #Cond 1: To object MUST be another port and must have direction = IN
        #Cond 2: Signal types must be the same
        #Cond 3: The destination fb must be another fb (connections can't be made within
        #the same fb)
        if self.startedLink:
            pos = event.scenePos()
            self.tab_index, self.key_index = retrieve_current_project_key_index()
            proj = self.project_scenes_list[self.key_index]
            items = proj.items(pos)
            for item in items:
                if type(item) is PortsDesignView:
                    signal_startPort = self.startedLink.fromPort.signal_type
                    signal_endPort = item.signal_type
                    startPort_fb_key = self.startedLink.fromPort.fb_key
                    endPort_fb_key = item.fb_key
                    
                    if ( (item.port_direction == 'In'
                          or item.port_direction == 'In-Feedback')
                        and signal_startPort == signal_endPort
                        and startPort_fb_key != endPort_fb_key):
                        #Downstream port has been verified to be OK, complete the link!
                        self.startedLink.endConnectState = True
                        self.startedLink.setToPort(item) 
                        self.startedLink.setEndPos(item.scenePos())
                        self.startedLink.portlink.set_line_color(signal_endPort, True)
                        
                        #Data for downstream port
                        endPort_ID = item.portID
                        endPort_name = item.port_name
                        endPort_fb_name = item.fb_name
                        endPort_fb_key = item.fb_key                    
                        #Data for upstream port
                        startPort_ID = self.startedLink.fromPort.portID
                        startPort_name = self.startedLink.fromPort.port_name
                        startPort_fb_name = self.startedLink.fromPort.fb_name
                        startPort_fb_key = self.startedLink.fromPort.fb_key
                        
                        self.startedLink.portlink.fromPort_portID = startPort_ID
                        self.startedLink.portlink.fromPort_fb_key = startPort_fb_key
                        self.startedLink.portlink.toPort_portID = endPort_ID
                        self.startedLink.portlink.toPort_fb_key = endPort_fb_key
                        sig = self.startedLink.portlink.signal
                        
                        self.startedLink.portlink.setToolTip('Link type: '+ str(sig)
                                +'\n' + 'From port: ' + str(startPort_fb_name) + '/' 
                                + str(startPort_name) + '\n' + 'To port: ' 
                                + str(endPort_fb_name) + '/' + str(endPort_name))
                    
                        i = 1
                        links = proj.signal_links_list
                        while (i in links):
                            i += 1 #Increment to next i   
                        links[i] = models.SignalLink(i, 'Link_'+str(i), startPort_fb_key,
                             startPort_fb_name, startPort_name, startPort_ID,
                             endPort_fb_key, endPort_fb_name, endPort_name, endPort_ID,
                             self.lineConnectionMode)
                    
                        #Update ports with link data and link key
                        item.link_name = links[i].link_name
                        item.link_key = links[i].link_key
                        self.startedLink.fromPort.link_name = links[i].link_name
                        self.startedLink.fromPort.link_key = links[i].link_key
                        
                        #Update linked ports to connected status (held in fb_ports_list of fb_list)
                        fb = proj.fb_list
                        fb_view = proj.fb_design_view_list
                        fb[startPort_fb_key].fb_ports_list[startPort_ID-1][5] = True
                        fb[endPort_fb_key].fb_ports_list[endPort_ID-1][5] = True
                        fb_view[startPort_fb_key].ports[startPort_ID].connected = True
                        fb_view[endPort_fb_key].ports[endPort_ID].connected = True
                        
                        #Update portlink object with link_key
                        self.startedLink.portlink.link_key = i                   
            if self.startedLink.toPort == None:
                self.startedLink.delete()
        self.startedLink = None
    
    def start_simulation(self):
        # Reset stop simulation flag to False (in case where previous simulation had 
        # resulted in an error condition or was intentionally stopped)
        config.stop_sim_flag = False
          
        #Check if previous sim status window/data views are open & close
        if config.sim_status_win is not None:
            config.sim_status_win.close()            
        if config.sim_data_view is not None:
            config.sim_data_view.close()
        
        # Create instance of simulation status window (if enabled)
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win_enabled == True
            config.sim_status_win = SimulationStatusGUI()
            config.sim_status_win.show()            
        else:
            config.sim_status_win_enabled == False
        
        # Create instance of data output window (if enabled)    
        if self.check_box_sim_data.checkState() == 2:
            config.sim_data_activate = True
            config.sim_data_view = SimulationDataGUI()
            config.sim_data_view.show()
        
        # Upload message to sim status dialog (sim has started)
        if self.check_box_sim_status.checkState() == 2:
            self.font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
            self.font_normal = QtGui.QFont("Arial", 8, QtGui.QFont.Normal)
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
            config.sim_status_win.textEdit.setCurrentFont(self.font_bold)
            config.sim_status_win.text_update('Starting simulation')
            config.sim_status_win.textEdit.setCurrentFont(self.font_normal)             
            localtime = time_data.asctime(time_data.localtime(time_data.time()))
            self.sim_time_start = time_data.time()
            config.sim_status_win.text_update('Date/time start: ' + str(localtime))            
            config.app.processEvents() #Updates sim_status_win
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
            config.sim_status_win.textEdit.setCurrentFont(self.font_normal) 
        config.status.setText('Starting simulation')                                                       
        
        #Retrieve all functional blocks in project scene
        self.fb_calculation_list = {} 
        self.fb_calculation_view_list = {}
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        scene = self.project_scenes_list[self.key_index]
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.totalBlocks.setText(str(0))
            config.sim_status_win.simulatedBlocks.setText(str(0))
            config.sim_status_win.currentIteration.setText(str(0))
            config.sim_status_win.totalIterations.setText(str(0))
        
        # One or more functional blocks have been retrieved - proceed to run
        # calculation orchestrator
        if window.project_scenes_list[self.key_index].fb_list != {}:
            # Initiate simulation algorithm (functional blocks have been detected)
            self.fb_calculation_list = scene.fb_list
            self.fb_num = len(self.fb_calculation_list)
            self.fb_calculation_view_list = scene.fb_design_view_list
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.totalBlocks.setText(str(self.fb_num))
                   
            #Clear any fb error state from previous simulation 
            fb_counter = 0
            fb_keys = list(self.fb_calculation_view_list.keys())
            while fb_counter < len(self.fb_calculation_view_list):       
                fb_key = fb_keys[fb_counter]
                if self.fb_calculation_view_list[fb_key].fb_error_state == True:
                    fb_error = self.fb_calculation_view_list[fb_key]
                    fb_border_style = self.fb_calculation_list[fb_key].fb_border_style
                    style = set_line_type(fb_border_style)
                    b_color = self.fb_calculation_list[fb_key].fb_border_color
                    color = self.fb_calculation_list[fb_key].fb_color
                    fb_error.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(b_color)), 0.5, style))
                    fb_error.setBrush(QtGui.QBrush(QtGui.QColor(color)))
                    fb_error.fb_error_state = False
                    break
                fb_counter += 1
                
            #Launch calculation orchestrator
            self.action_PauseSimulation.setEnabled(True)
            self.action_StopSimulation.setEnabled(True)
            self.action_StartSimulation.setEnabled(False)
            self.actionPause.setEnabled(True)
            self.actionEnd.setEnabled(True)
            self.actionStart.setEnabled(False)
            #Start main algorithm for system simulation
            window.calculation_orchestrator()
        else: #Quit simulation (there are no functional blocks)
            text_quit_1 = 'No functional blocks found in the project layout - stopping simulation'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.text_update(text_quit_1)
            config.status.setText(text_quit_1)
            config.app.processEvents()
                                                                                 
    def calculation_orchestrator(self):
        '''Main calculation algorithm for the system simulation'''
        
        '''ITERATIONS loop================================================================
        '''
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        proj = self.project_scenes_list[self.key_index] #Local instance of current project
        self.iterations_sim = proj.design_settings['iterations']
        self.max_attempts = proj.design_settings['max_calculation_attempts']
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.totalIterations.setText(str(self.iterations_sim))
        self.s_iterations = 0
        
        # Reset Iteration (Cur) and Segment (Cur) fields in top tool bar
        self.tableWidget3.item(0, 1).setText('')
        if proj.design_settings['feedback_enabled'] == 2:
            self.tableWidget3.item(1, 1).setText('')
        else:
            self.tableWidget3.item(1, 1).setText('N/A')
        
        for self.iteration in range(1, self.iterations_sim + 1):
            text_start = 'Starting simulation iteration ' + str(self.iteration) + '...'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
                config.sim_status_win.text_update(text_start)
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
                config.sim_status_win.currentIteration.setText(str(self.iteration))
            config.status.setText(text_start)           
            window.tableWidget3.item(0, 1).setText(format(self.iteration, 'n'))        
            window.tableWidget3.resizeColumnsToContents()            
            config.app.processEvents()
            proj.design_settings['current_iteration'] = self.iteration
            
            #Check if a request has been issued to stop the simulation (before running
            #main loop)
            if config.stop_sim_flag == True:
                self.process_stop_sim_actions() 
                break
            
            '''MAIN simulation loop===================================================='''
            #Check if feedback mode has been set to True
            self.feedback = int(proj.design_settings['feedback_enabled'])
            if self.feedback == 2:
                self.main_simulation_loop_feedback()
            else:
                self.main_simulation_loop()
            '''========================================================================'''
            #Check if a request has been issued to stop the simulation (after running
            #main loop)            
            if config.stop_sim_flag == True:
                self.process_stop_sim_actions() 
                break
            
            text_1 = 'Simulation iteration: ' + str(self.iteration) + ' is complete'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))                                                      
                config.sim_status_win.text_update(text_1)           
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
            config.status.setText(text_1)
            config.app.processEvents()
            #Allocate data tables to dictionary (for iterations)
            for name in self.project_names_list:
                if self.project_names_list[name] == self.key_index:
                    break
            #Update any data tables that are in the design scene
            try:
                config_data_panel.update_data_tables_iteration(self.iteration, name)     
                config_data_panel.update_data_dictionaries(name)
                self.update_data_boxes()
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg_err = 'Error/exception while updating data panel(s)'
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#aa0000')))
                    config.sim_status_win.text_update(msg_err)
                    config.sim_status_win.text_update(str(e0) + ' '+ str(e1))
                    config.sim_status_win.text_update(str(traceback.format_exc()))
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#000000')))
                config.status.setText(msg_err)
                config.stop_sim_flag = True
                self.process_stop_sim_actions()
                break
                    
            if config.sim_pause_flag == True:
                text_2 = 'Simulation has been paused - press the pause simulation button to resume.'
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
                    config.sim_status_win.textEdit.setCurrentFont(self.font_bold)                                                         
                    config.sim_status_win.text_update(text_2)
                    config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
                    config.sim_status_win.textEdit.setCurrentFont(self.font_normal) 
                config.status.setText(text_2)
                config.app.processEvents()
                while True:
                    time_data.sleep(0.5)
                    config.app.processEvents()
                    if config.sim_pause_flag == False:
                        self.iteration = self.iteration - 1
                        break      
        '''End ITERATIONS loop============================================================
        '''        
        if config.stop_sim_flag == True:
            config.app.processEvents()
            self.iterationsSelector.setValue(self.iteration)
            self.reset_simulation_action_buttons()
        else:
            text_3 = 'All iterations complete - end of simulation'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
                config.sim_status_win.textEdit.setCurrentFont(self.font_bold)                                          
                config.sim_status_win.text_update(text_3)
                config.sim_status_win.textEdit.setCurrentFont(self.font_normal) 
                localtime = time_data.asctime(time_data.localtime(time_data.time()))
                config.sim_status_win.text_update('Date/time stopped: ' + localtime)
                time_to_complete = time_data.time() - self.sim_time_start
                time_to_complete = str(np.round(time_to_complete/60, 3))
                config.sim_status_win.text_update('Simulation time (min): ' + time_to_complete)
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#aa0000'))
                config.status.setText(text_3)
                config.app.processEvents()

            if self.s < len(self.fb_calculation_list):
                text_3A = 'NOTE: Calculations for one or more functional block(s) could not be completed.' 
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.text_update(text_3A)
                    config.sim_status_win.textEdit.setCurrentFont(self.font_normal) 
                    localtime = time_data.asctime(time_data.localtime(time_data.time()))
                    config.sim_status_win.text_update('Date/time stopped: ' + localtime)
                    config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
                    config.sim_status_win.textEdit.setCurrentFont(self.font_normal) 
                    config.app.processEvents()
            self.iterationsSelector.setValue(self.iterations_sim)
            self.reset_simulation_action_buttons()
            
    def process_stop_sim_actions(self):
        text_4 = 'Simulation has been stopped'
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
            config.sim_status_win.textEdit.setCurrentFont(self.font_bold)
            config.sim_status_win.text_update(text_4)
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
            config.sim_status_win.textEdit.setCurrentFont(self.font_normal)   
        config.status.setText(text_4)
        config.app.processEvents()                                                    
        self.reset_simulation_action_buttons()
            
    def main_simulation_loop(self):
        '''Main simulation loop - called for each iteration (used when feedback is
           not activated)
        '''
        # Reset all functional blocks in the scene
        self.fb_counter = 0
        self.fb_keys = list(self.fb_calculation_list.keys())
        while self.fb_counter < len(self.fb_calculation_list):       
            fb_key = self.fb_keys[self.fb_counter]
            self.fb_calculation_list[fb_key].fb_calculation_status = 'Not ready'
            self.fb_calculation_list[fb_key].status_counter = 0            
            #Reset all fb port "data ready" attributes to False (with exception of disabled ports)
            port_list = window.project_scenes_list[self.key_index].fb_list[fb_key].fb_ports_list
            length_port_list = len(port_list)
            for port in range(0, length_port_list):
                if port_list[port][4] == 'Disabled' or port_list[port][3] == 'In-Feedback':
                    port_list[port][6] = True
                else:
                    port_list[port][6] = False
                
            if self.iteration == 1: #Reset all iteration dictionaries to empty
                self.fb_calculation_view_list[fb_key].iterations_parameters = {}
                self.fb_calculation_view_list[fb_key].iterations_results = {}
                length_port_list = len(self.fb_calculation_list[fb_key].fb_ports_list)
                for p in range(1, length_port_list+1):
                    self.fb_calculation_view_list[fb_key].ports[p].iterations_input_signals = {}
                    self.fb_calculation_view_list[fb_key].ports[p].iterations_return_signals = {}                   
            self.fb_counter += 1
        
        self.s = 0 #Functional blocks that are in a "completed" state (reset to 0 before starting sim) 
        self.fb_counter = 0
        fb_key = self.fb_keys[0] #Reset to first functional block ID in the list
                
        while True: 
            #Simulation will keep running until all functional blocks are in
            #either "Complete" or "Unable to complete calculation" state
            fb_name = self.fb_calculation_list[fb_key].fb_name
            text_5 = 'Verifying calculation status of ' + fb_name + ' (ID:'+ str(fb_key)+ ')'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.text_update(text_5)
            config.app.processEvents()
            status = self.check_calculation_status(fb_key)
            if status == 'Ready': #Functional block is ready to calculate
                #Call fb_script calculation====================              
                fb_script_ok = self.run_fb_script(fb_key)
                if fb_script_ok == False:
                    config.stop_sim_flag = True                   
                    # Highlight fb which has error in project scene
                    self.fb_error = self.fb_calculation_view_list[fb_key]
                    style = set_line_type('DashLine')
                    self.fb_error.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor('#ff0000')), 1, style))                   
                    self.fb_error.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 50)))
                    self.fb_error.fb_error_state = True
                    break
                #==============================================
                #Check all FBs to see if simulation is complete
                self.fb_calculation_list[fb_key].fb_calculation_status = 'Complete'
                self.s += 1
                self.s_iterations += 1
                prog = self.s_iterations/(self.fb_num*self.iterations_sim)
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.simulatedBlocks.setText(str(self.s))
                    config.sim_status_win.update_progress_bar(100*float(prog))
                window.tableWidget3.item(2, 1).setText(format(np.round(prog*100), 'n'))
                window.tableWidget3.resizeColumnsToContents()
                exit_simulation = self.check_exit_simulation()
                if exit_simulation == True: #All FBs have reported complete
                    text_6 = 'Simulation for iteration ' + str(self.iteration) + ' is complete'
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update(text_6)
                    config.status.setText(text_6)
                    config.app.processEvents()
                    break
                else: #Continue simulation
                    fb_key = self.next_fb(fb_key)
                            
            elif status == 'Complete': #Functional block has already finished its calculation
                #Check if all functional blocks have completed their calculations
                exit_simulation = self.check_exit_simulation()
                if exit_simulation == True:
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update(text_6)
                    break
                else:
                    fb_key = self.next_fb(fb_key)
                    text_7 = 'FB ID set to: ' + str(fb_key)
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update(text_7)
                    config.app.processEvents()
                            
            else: #Functional block is not ready (continue to next one)
                self.fb_calculation_list[fb_key].status_counter += 1
                if self.fb_calculation_list[fb_key].status_counter > int(self.max_attempts):
                    status = 'Unable to complete calculation'
                    self.fb_calculation_list[fb_key].fb_calculation_status = status
                    text_4 = ('Unable to complete calculation after ' 
                              + str(self.max_attempts) +' attempts.')
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update(text_4)
                    text_8 = (self.fb_calculation_list[fb_key].fb_name
                              + ' status set to ' 
                              + self.fb_calculation_list[fb_key].fb_calculation_status)
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update(text_8)
                    config.app.processEvents()
                    exit_simulation = self.check_exit_simulation()
                    if exit_simulation == True:
                        text_9 = 'Exiting main simulation routine...'
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.text_update(text_9)
                        config.status.setText(text_9)
                        config.app.processEvents()
                        break
                    else:
                        fb_key = self.next_fb(fb_key)           
                else:
                    fb_key = self.next_fb(fb_key)
                    
    def main_simulation_loop_feedback(self):
        '''Main simulation loop with feedback - called for each iteration. Used when 
           feedback is enabled
        '''
        self.segments = int(round(window.project_scenes_list[self.key_index].design_settings['feedback_segments']))
        
        for i in range(1, self.segments + 1):
            window.tableWidget3.item(1, 1).setText(format(i, 'n'))
            window.tableWidget3.resizeColumnsToContents()
            config.app.processEvents()
            if config.stop_sim_flag == True:
                break 
            #Set project settings "feedback_current_segment" to current segment
            window.project_scenes_list[self.key_index].design_settings['feedback_current_segment'] = i
            text_1 = 'Starting feedback segment ' + str(i) + '...'
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
                config.sim_status_win.text_update(text_1)
                config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
            #Reset all functional blocks in the scene
            self.fb_counter = 0
            self.fb_keys = list(self.fb_calculation_list.keys())
            while self.fb_counter < len(self.fb_calculation_list):
                fb_key = self.fb_keys[self.fb_counter]
                self.fb_calculation_list[fb_key].fb_calculation_status = 'Not ready'
                self.fb_calculation_list[fb_key].status_counter = 0
                    
                #Reset all fb port "data ready" attributes to False (with exception of disabled ports)
                port_list = window.project_scenes_list[self.key_index].fb_list[fb_key].fb_ports_list
                length_port_list = len(port_list)
                for port in range(0, length_port_list):
                    if port_list[port][4] == 'Disabled' or port_list[port][3] == 'In-Feedback':
                        port_list[port][6] = True
                    else:
                        port_list[port][6] = False
                    
                if self.iteration == 1: #Reset all iteration dictionaries to empty
                    self.fb_calculation_view_list[fb_key].iterations_parameters = {}
                    self.fb_calculation_view_list[fb_key].iterations_results = {}
                    length_port_list = len(self.fb_calculation_list[fb_key].fb_ports_list)
                    for p in range(1, length_port_list+1):
                        self.fb_calculation_view_list[fb_key].ports[p].iterations_input_signals = {}
                        self.fb_calculation_view_list[fb_key].ports[p].iterations_return_signals = {}
                self.fb_counter += 1
        
            self.s = 0 #Functional blocks that are in a "completed" state 
                  #(reset to 0 before starting sim) 
            self.fb_counter = 0
            fb_key = self.fb_keys[0] #Reset to first functional block ID in the list
                    
            while True: 
                #Simulation will keep running until all functional blocks are in
                #either "Complete" or "Unable to complete calculation" state
                fb_name = self.fb_calculation_list[fb_key].fb_name
                text_1 = 'Verifying calculation status of ' + fb_name + ' (ID:'+ str(fb_key)+ ')'
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.text_update(text_1)
                status = self.check_calculation_status(fb_key)
                if status == 'Ready': #Functional block is ready to calculate
                    #Call fb_script calculation===========================================
                    fb_script_ok = self.run_fb_script(fb_key)
                    if fb_script_ok == False:
                        config.stop_sim_flag = True
                        # Highlight fb which has error in project scene
                        self.fb_error = self.fb_calculation_view_list[fb_key]
                        style = set_line_type('DashLine')
                        self.fb_error.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor('#ff0000')), 1, style))                   
                        self.fb_error.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 50)))
                        self.fb_error.fb_error_state = True
                        break
                    #=====================================================================                
                    #Check all FBs to see if simulation is complete
                    self.fb_calculation_list[fb_key].fb_calculation_status = 'Complete'
                    self.s += 1
                    self.s_iterations += 1
                    prog = self.s_iterations/(self.fb_num*self.iterations_sim*self.segments)
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.simulatedBlocks.setText(str(self.s))
                        config.sim_status_win.update_progress_bar(100*float(prog))
                    window.tableWidget3.item(2, 1).setText(format(np.round(prog*100), 'n'))
                    window.tableWidget3.resizeColumnsToContents()
                    
                    exit_simulation = self.check_exit_simulation()
                    if exit_simulation == True: #All FBs have reported complete
                        text_2 = 'Simulation for feedback segment ' + str(i) + ' is complete'
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
                            config.sim_status_win.text_update(text_2)
                            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
                        break
                    else: #Continue simulation
                        fb_key = self.next_fb(fb_key)  
                           
                elif status == 'Complete': #Functional block has finished its calculation
                    #Check if all functional blocks have completed their calculations
                    exit_simulation = self.check_exit_simulation()
                    if exit_simulation == True:
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.text_update(text_2)
                        break
                    else:
                        fb_key = self.next_fb(fb_key)
                        text_3 = 'FB ID set to: ' + str(fb_key)
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.text_update('FB ID set to: ' 
                                                              + str(fb_key))
                            config.sim_status_win.text_update(text_3)
                        config.app.processEvents()
                        
                else: #Functional block is not ready (continue to next one)
                    self.fb_calculation_list[fb_key].status_counter += 1
                    if self.fb_calculation_list[fb_key].status_counter > int(self.max_attempts):
                        status = 'Unable to complete calculation'
                        self.fb_calculation_list[fb_key].fb_calculation_status = status
                        text_4 = ('Unable to complete calculation after ' 
                                  + str(self.max_attempts) +' attempts')
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.text_update(text_4)
                        text_5 = (self.fb_calculation_list[fb_key].fb_name
                                   + ' status set to ' 
                                   + self.fb_calculation_list[fb_key].fb_calculation_status)
                        if self.check_box_sim_status.checkState() == 2:
                            config.sim_status_win.text_update(text_5)
                        exit_simulation = self.check_exit_simulation()
                        if exit_simulation == True:
                            text_6 = 'Exiting main simulation routine...'
                            if self.check_box_sim_status.checkState() == 2:
                                config.sim_status_win.text_update(text_6)
                            config.status.setText(text_6)
                            break
                        else:
                            fb_key = self.next_fb(fb_key)           
                    else:
                        fb_key = self.next_fb(fb_key)
    
    def check_exit_simulation(self):
        exit_simulation = True   
        counter = 0
        self.fb_keys = list(self.fb_calculation_list.keys())
        while counter < len(self.fb_calculation_list):
            fb_key = self.fb_keys[counter]
            text_1 = (self.fb_calculation_list[fb_key].fb_name + ' (ID:'+ str(fb_key) 
                      + ') status: ' + self.fb_calculation_list[fb_key].fb_calculation_status)
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.text_update(text_1)
            if (self.fb_calculation_list[fb_key].fb_calculation_status == 'Ready' or
                self.fb_calculation_list[fb_key].fb_calculation_status == 'Not ready'):
                exit_simulation = False             
            counter += 1
        return exit_simulation
    
    def sim_pause(self):
        msg_sim_paused = 'Simulation has been paused - press pause action to continue'        
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#007900'))
            config.sim_status_win.text_update(msg_sim_paused)
            config.sim_status_win.textEdit.setTextColor(QtGui.QColor('#000000'))
        config.status.setText(msg_sim_paused)
        config.app.processEvents()                                                         
    
    def next_fb(self, key):
        self.fb_counter += 1
        if self.fb_counter > len(self.fb_calculation_list) - 1:
            self.fb_counter = 0
        key = self.fb_keys[self.fb_counter]
        fb_name = self.fb_calculation_list[key].fb_name
        text_1 = 'Proceeding to ' + fb_name + ' (ID:' + str(key) + ')'
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.text_update(text_1)
        return key
    
    def check_calculation_status(self, fb_key):
        if (self.fb_calculation_list[fb_key].fb_calculation_status == 'Complete' 
        or self.fb_calculation_list[fb_key].fb_calculation_status == 'Unable to complete calculation'):
            return(self.fb_calculation_list[fb_key].fb_calculation_status)
        else:
            tab_index, key_index = retrieve_current_project_key_index()
            port_list = window.project_scenes_list[key_index].fb_list[fb_key].fb_ports_list
            length_port_list = len(port_list)    
            self.fb_calculation_list[fb_key].fb_calculation_status = 'Ready'
            for i in range(0, length_port_list):
                direction = port_list[i][3]
                data_ready = port_list[i][6]
                if direction == 'In' and data_ready == False:
                    self.fb_calculation_list[fb_key].fb_calculation_status = 'Not ready'    
            fb_name = self.fb_calculation_list[fb_key].fb_name 
            fb_status = self.fb_calculation_list[fb_key].fb_calculation_status
            text_1 = fb_name + ' (ID:' + str(fb_key) + ') status: ' + fb_status
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.text_update(text_1)
            return(self.fb_calculation_list[fb_key].fb_calculation_status)
        
    def run_fb_script(self, fb_key):
        start_time = time_data.time()
        self.fb_script_state = True
        while True: # Program will break once all routines have been completed or if an
                    # exception is raised (simulation will also be halted for the latter)
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            fb_ports = proj.fb_list[fb_key].fb_ports_list
            length_port_list = len(fb_ports)
            if self.check_box_sim_status.checkState() == 2:
                config.sim_status_win.currentBlockName.setText(self.fb_calculation_list[fb_key].fb_name)
            self.time = proj.design_settings['time_window']
            self.num_samples = int(round(proj.design_settings['num_samples']))
            self.num_sym = 100
            #Prepare input signals data===================================================
            input_signals_data = []
            in_sig = 0
            for i in range(0, length_port_list):
                portID = fb_ports[i][0]
                direction = fb_ports[i][3]
                connected = fb_ports[i][5]
                data_ready = fb_ports[i][6]
                signal_type = fb_ports[i][4]
                port = proj.fb_design_view_list[fb_key].ports[portID]
                port_sig = proj.fb_design_view_list[fb_key].signals[portID]
                #Process input ports that have data available (feedback and non-feedback)
                if ((direction == 'In' or direction == 'In-Feedback')
                      and (connected == True) and (data_ready == True)):
                    #Electrical signal
                    if signal_type == 'Electrical':
                        if port_sig.time_array.size != 0:
                            t = port_sig.time_array
                            a = port_sig.amplitude_array 
                            noise = port_sig.noise_array
                        else:
                            t = np.linspace(0, self.time, self.num_samples)
                            a = np.zeros(self.num_samples)
                            noise = np.zeros(self.num_samples)
                        carrier = port_sig.carrier
                        fs = port_sig.sample_rate                   
                        signal_list = [portID, signal_type, carrier,
                                       fs, t, a, noise, carrier]
                        input_signals_data.append(signal_list)               
                        if (self.check_box_port_data.checkState() == 0
                            and self.iteration == self.iterations_sim):
                            port_sig.time_array = np.array([])
                            port_sig.amplitude_array  = np.array([])
                            port_sig.noise_array = np.array([])  
                    #Optical signal
                    if signal_type == 'Optical':
                        signals_optical = []
                        if port_sig.time_array.size != 0:
                            t = port_sig.time_array
                            a = port_sig.wave_channel_dict[1].envelope_array 
                            noise_time = port_sig.wave_channel_dict[1].noise_array
                            noise_freq = port_sig.wave_channel_dict[1].psd_array  
                        else:
                            t = np.linspace(0, self.time, self.num_samples)
                            a = np.zeros(self.num_samples)
                            noise_time = np.zeros(self.num_samples)
                            noise_freq = np.array([np.zeros(20), np.zeros(20)])
                        wave = port_sig.wave_channel_dict[1].wave_channel
                        wave_key = port_sig.wave_channel_dict[1].wave_key
                        jones = port_sig.wave_channel_dict[1].jones_vector
                        fs  = port_sig.sample_rate
                        signal_optical = [wave_key, wave, jones, a, noise_time, noise_freq]
                        signals_optical.append(signal_optical)
                        signal_list = [portID, signal_type, fs, t, signals_optical]
                        
                        input_signals_data.append(signal_list)           
                        if (self.check_box_port_data.checkState() == 0
                            and self.iteration == self.iterations_sim):
                            port_sig.time_array = np.array([])
                            port_sig.envelope_array  = np.array([])
                            port_sig.psd_array = np.array([])                            
                    #Digital signal
                    if signal_type == 'Digital':
                        if port_sig.time_array.size != 0:
                            t = port_sig.time_array
                            a = port_sig.discrete_array 
                        else:
                            t = np.linspace(0, self.time, self.num_samples)
                            a = np.zeros(self.num_sym)
                        sym_rate = port_sig.symbol_rate
                        b_rate = port_sig.bit_rate
                        N = port_sig.order
                        signal_list = [portID, signal_type, sym_rate, b_rate, N, t, a]
                        input_signals_data.append(signal_list)
                        if (self.check_box_port_data.checkState() == 0
                            and self.iteration == self.iterations_sim):
                            port_sig.time_array = np.array([])
                            port_sig.discrete_array  = np.array([])
                    #Analog signal
                    if (signal_type == 'Analog (1)' or signal_type == 'Analog (2)'
                    or signal_type == 'Analog (3)'):
                        if port_sig.time_array.size != 0:
                            t = port_sig.time_array
                            a = port_sig.amplitude_array 
                        else:
                            t = np.linspace(0, self.time, self.num_samples)
                            a = np.zeros(self.num_samples)
                        fs = port_sig.sample_rate   
                        signal_list = [portID, signal_type, fs, t, a]
                        input_signals_data.append(signal_list)
                        if (self.check_box_port_data.checkState() == 0
                            and self.iteration == self.iterations_sim):
                            port_sig.time_array = np.array([])
                            port_sig.amplitude_array  = np.array([])
                    if self.check_box_port_data.checkState() == 2:
                        port.iterations_input_signals[self.iteration] = input_signals_data[in_sig]               
                    in_sig += 1
                
            '''====FUNCTIONAL BLOCK SCRIPT CALCULATION - START========================='''
            #INPUT: input_signals_data, parameters_input, project settings
            #RETURN: output signals, parameters, results
            sys.path.clear()  
            #Load file paths for default script folders
            for i in range(0, len(config_lib.scripts_path_list)):
                script_path =  str(root_path) + str(config_lib.scripts_path_list[i])
                sys.path.append(script_path)
            #Load file paths for project script folders
            path1 = proj.design_settings['file_path_1']
            path2 = proj.design_settings['file_path_2']
            sys.path.append(path1)
            sys.path.append(path2)
            #Retrieve script name
            script = str(proj.fb_list[fb_key].fb_script_module)
            try: #Import script module. If unsuccessful, issue error message and exit 
                 #fb_script routine (simulation stop status flag will be set to True)
                module = __import__(script)
                importlib.reload(module)
                text_1 = 'Loading ' + str(module)
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.text_update(text_1)
                config.status.setText(text_1)
                config.app.processEvents()
                
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                text_2 = ('The python script module for FB: '
                          + str(self.fb_calculation_list[fb_key].fb_name)
                          + ' could not be successfully loaded' )
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#aa0000')))
                    config.sim_status_win.text_update(text_2)
                    config.sim_status_win.text_update(str(e0) + ' '+ str(e1))
                    config.sim_status_win.text_update(str(traceback.format_exc()))
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#000000')))    
                config.status.setText(text_2)
                config.app.processEvents()
                self.reset_simulation_action_buttons()
                config.stop_sim_flag = True
                self.fb_script_state = False
                break
            
            settings = proj.design_settings
            parameters_input = proj.fb_list[fb_key].fb_parameters_list
            try:#Run fb_script (module.run). If unsuccessful, issue error message and exit 
                #fb_script routine (simulation stop status flag will also be set to True)
                text_3 = 'Initiating module.run...'
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.text_update(text_3)
                config.status.setText(text_3)
                config.app.processEvents()
                font_bold = QtGui.QFont("Arial", 8, QtGui.QFont.Bold)
                config.sim_status_win.textEdit.setCurrentFont(font_bold)
                signals_data, parameters, results = module.run(input_signals_data, 
                                                           parameters_input, settings)  
                config.sim_status_win.textEdit.setCurrentFont(font_normal)
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg_err = ('Error/exception while calculating python script module for FB: '
                           + str(self.fb_calculation_list[fb_key].fb_name))
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setCurrentFont(font_normal)
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#aa0000')))
                    config.sim_status_win.text_update(msg_err)
                    config.sim_status_win.text_update(str(e0) + ' '+ str(e1))
                    config.sim_status_win.text_update(str(traceback.format_exc()))
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#000000')))     
                config.status.setText(msg_err)
                config.app.processEvents()
                self.reset_simulation_action_buttons()
                config.stop_sim_flag = True
                self.fb_script_state = False
                break

            '''====FUNCTIONAL BLOCK SCRIPT CALCULATION-END============================='''       
            #Save returned signals and load into signals object of associated ports
            try:
                if len(signals_data) > 0:
                    if self.check_box_sim_status.checkState() == 2:
                        config.sim_status_win.text_update('Preparing signals for output ports...')
                    self.error_loading_signals_flag = False
                    for i in range(0, len(signals_data)):
                        port_sig = proj.fb_design_view_list[fb_key].signals[signals_data[i][0]]
                        port = proj.fb_design_view_list[fb_key].ports[signals_data[i][0]]
                    
                        if port.port_direction == "In" or port.port_direction == "In-Feedback":
                            # Set error flag to stop simulation (incorrect port type
                            # has been specified)
                            self.error_loading_signals_flag = True        
                        
                        if port.connected == True:
                            link_key = port.link_key
                            link = proj.signal_links_list[link_key]
                            d_port_fb_key = link.fb_end_key
                            d_port_ID = link.end_port_ID
                        
                        #Electrical signal (IF)===========================================
                        if signals_data[i][1] == 'Electrical':
                            port_sig.carrier = signals_data[i][2]
                            port_sig.sample_rate = signals_data[i][3]
                            port_sig.time_array = signals_data[i][4]
                            port_sig.amplitude_array = signals_data[i][5]
                            port_sig.noise_array = signals_data[i][6]
                            #Check if port is linked to another port and copy data to downstream port
                            if port.connected == True:
                                d_port_sig_elec = proj.fb_design_view_list[d_port_fb_key].signals[d_port_ID]
                                d_port_sig_elec.carrier = signals_data[i][2]
                                d_port_sig_elec.sample_rate = signals_data[i][3]
                                d_port_sig_elec.time_array = signals_data[i][4]
                                d_port_sig_elec.amplitude_array = signals_data[i][5]
                                d_port_sig_elec.noise_array = signals_data[i][6]
                                proj.fb_list[d_port_fb_key].fb_ports_list[d_port_ID-1][6] = True 
                            #If final iteration AND save port data is off,
                            #delete data arrays associated with current port
                            if (self.check_box_port_data.checkState() == 0 
                                and self.iteration == self.iterations_sim):
                                port_sig.time_array = np.array([])
                                port_sig.amplitude_array  = np.array([])
                                port_sig.noise_array = np.array([])
                            
                        #Optical signal (IF)==================================================
                        if signals_data[i][1] == 'Optical':
                            
                            port_sig.sample_rate = signals_data[i][2]
                            port_sig.time_array = signals_data[i][3]
                            
                            sig = signals_data[i][4]
                            
                            port_sig.wave_channel_dict[1].wave_key = sig[0][0]
                            port_sig.wave_channel_dict[1].wave_channel = sig[0][1]
                            port_sig.wave_channel_dict[1].jones_vector = sig[0][2]
                            port_sig.wave_channel_dict[1].envelope_array = sig[0][3]
                            port_sig.wave_channel_dict[1].noise_array = sig[0][4]
                            port_sig.wave_channel_dict[1].psd_array = sig[0][5]
                            
                            #Check if port is linked to another port and copy data to downstream port
                            if port.connected == True:   
                                d_port_sig_opt = proj.fb_design_view_list[d_port_fb_key].signals[d_port_ID]
                                d_port_sig_opt.sample_rate = signals_data[i][2]
                                d_port_sig_opt.time_array = signals_data[i][3]
                            
                                sig = signals_data[i][4]
                            
                                d_port_sig_opt.wave_channel_dict[1].wave_key = sig[0][0]
                                d_port_sig_opt.wave_channel_dict[1].wave_channel = sig[0][1]
                                d_port_sig_opt.wave_channel_dict[1].jones_vector = sig[0][2]
                                d_port_sig_opt.wave_channel_dict[1].envelope_array = sig[0][3]
                                d_port_sig_opt.wave_channel_dict[1].noise_array = sig[0][4]
                                d_port_sig_opt.wave_channel_dict[1].psd_array = sig[0][5]
                                proj.fb_list[d_port_fb_key].fb_ports_list[d_port_ID-1][6] = True 
                            #If final iteration AND save port data is off,
                            #delete data arrays associated with current port
                            if (self.check_box_port_data.checkState() == 0
                                and self.iteration == self.iterations_sim):
                                port_sig.time_array = np.array([])
                                port_sig.wave_channel_dict[1].envelope_array  = np.array([])
                                port_sig.wave_channel_dict[1].noise_array = np.array([])
                                port_sig.wave_channel_dict[1].psd_array = np.array([]) 
                            
                        #Digital signal (IF)==================================================
                        if signals_data[i][1] == 'Digital':
                            port_sig.symbol_rate = signals_data[i][2]
                            port_sig.bit_rate = signals_data[i][3]
                            port_sig.order = signals_data[i][4]
                            port_sig.time_array = signals_data[i][5]
                            port_sig.discrete_array = signals_data[i][6]
                            #Check if port is linked to another port and
                            #copy data to downstream port
                            if port.connected == True:
                                d_port_sig_dgt = proj.fb_design_view_list[d_port_fb_key].signals[d_port_ID]
                                d_port_sig_dgt.symbol_rate = signals_data[i][2]
                                d_port_sig_dgt.bit_rate = signals_data[i][3]
                                d_port_sig_dgt.order = signals_data[i][4]
                                d_port_sig_dgt.time_array = signals_data[i][5]
                                d_port_sig_dgt.discrete_array = signals_data[i][6]
                                proj.fb_list[d_port_fb_key].fb_ports_list[d_port_ID-1][6] = True 
                            #If final iteration AND save port data is off, 
                            # delete data arrays associated with current port
                            if (self.check_box_port_data.checkState() == 0
                                and self.iteration == self.iterations_sim):
                                port_sig.time_array = np.array([])
                                port_sig.discrete_array  = np.array([])
                                
                        #Analog signal (IF)===================================================
                        if (signals_data[i][1] == 'Analog (1)' or signals_data[i][1] == 'Analog (2)'
                            or signals_data[i][1] == 'Analog (3)'):
                            port_sig.sample_rate = signals_data[i][2]
                            port_sig.time_array = signals_data[i][3]
                            port_sig.amplitude_array = signals_data[i][4]
                            #Check if port is linked to another port and copy data to downstream port
                            if port.connected == True:
                                d_port_sig_analog = proj.fb_design_view_list[d_port_fb_key].signals[d_port_ID]
                                d_port_sig_analog.sample_rate = signals_data[i][2]
                                d_port_sig_analog.time_array = signals_data[i][3]
                                d_port_sig_analog.amplitude_array = signals_data[i][4]
                                proj.fb_list[d_port_fb_key].fb_ports_list[d_port_ID-1][6] = True 
                            #If final iteration AND save port data is off,
                            #delete data arrays associated with current port
                            if (self.check_box_port_data.checkState() == 0 
                                and self.iteration == self.iterations_sim):
                                port_sig.time_array = np.array([])
                                port_sig.amplitude_array  = np.array([])
                    
                        #Allocate return signals to dictionary (for iterations)
                        if self.check_box_port_data.checkState() == 2:
                            sig_data = proj.fb_design_view_list[fb_key].ports[signals_data[i][0]]
                            sig_data.iterations_return_signals[self.iteration] = signals_data[i]
                    signals_data = []
                    
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg_err = ('Error/exception while loading return signals for FB: '
                           + str(self.fb_calculation_list[fb_key].fb_name))
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#aa0000')))
                    config.sim_status_win.text_update(msg_err)
                    config.sim_status_win.text_update(str(e0) + ' '+ str(e1))
                    config.sim_status_win.text_update(str(traceback.format_exc()))
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#000000')))     
                config.status.setText(msg_err)
                config.app.processEvents()
                self.reset_simulation_action_buttons()
                config.stop_sim_flag = True
                self.fb_script_state = False
                break
            #Check if an error resulted during the loading of the signal data    
            if self.error_loading_signals_flag == True:
                text_5 = ('Error preparing the output signals for FB: '
                          + str(self.fb_calculation_list[fb_key].fb_name))
                text_6 = ( 'Incorrect port ID specified. Attempted to allocate output' +
                           ' signal data to an input port' )
                if self.check_box_sim_status.checkState() == 2:
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#aa0000')))
                    config.sim_status_win.text_update(text_5)
                    config.sim_status_win.text_update(text_6)
                    config.sim_status_win.textEdit.setTextColor((QtGui.QColor('#000000')))                                                                       
                config.status.setText(text_6)
                config.app.processEvents()
                self.reset_simulation_action_buttons()
                config.stop_sim_flag = True
                self.fb_script_state = False
                break
            
            #Save parameters to the fb_parameters_list
            proj.fb_list[fb_key].fb_parameters_list = parameters       
            #Allocate parameters to dictionary 
            #(in case some were changed by script as part of iterations)
            proj.fb_design_view_list[fb_key].iterations_parameters[self.iteration] = parameters                   
            #Save results to the fb_results_list          
            proj.fb_list[fb_key].fb_results_list = results               
            #Allocate results to dictionary (for iterations)
            proj.fb_design_view_list[fb_key].iterations_results[self.iteration] = results
        
            #If save data check box is not selected, then port signal data is deleted
            if (self.check_box_port_data.checkState() == 0 
                and self.iteration == self.iterations_sim):
                input_signals_data = []
                signals_data = []
            break #End of fb_script routines (exit While True)
        end_time = time_data.time()
        time_elapsed = end_time - start_time
        time_elapsed = np.round(time_elapsed, 3)
        if self.check_box_sim_status.checkState() == 2:
            config.sim_status_win.text_update('Time to complete script: ' 
                                              + str(time_elapsed) + ' sec')
        return self.fb_script_state # Return status of fb_script routine (has an exception
                                    # been raised?)
            
    def update_data_boxes(self):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items()
        for item in items:
            if type(item) is DataBoxDesignView:
                key = item.data_key
                t_text = item.title_text
                t_geometry = item.title_geometry
                t_position = None
                t_text_width = item.title_text_width
                t_width = item.title_width        
                t_height = item.title_height
                t_color = item.title_box_color
                t_opacity = item.title_box_opacity
                t_border_color = item.title_border_color
                t_text_size = item.title_text_size
                t_text_color = item.title_text_color
                t_text_bold = item.title_text_bold     
                t_text_italic= item.title_text_italic        
                t_border_style = item.title_border_style       
                t_border_width = item.title_border_width      
                t_text_pos_x = item.title_text_pos_x
                t_text_pos_y = item.title_text_pos_y
                
                d_box_geometry = item.data_box_geometry 
                d_box_position = item.pos()
                d_box_width = item.data_box_width
                d_box_height = item.data_box_height    
                d_box_color = item.data_box_color
                d_box_opacity = item.data_box_opacity
                d_box_gradient = item.data_box_gradient
                d_border_color = item.data_border_color
                d_box_border_style = item.data_box_border_style
                d_box_border_width = item.data_box_border_width
                d_text_size = item.data_text_size
                d_width = item.data_width
                d_width_2 = item.value_width
                d_text_pos_x = item.data_text_pos_x
                d_text_pos_y = item.data_text_pos_y
                data_source_file = item.data_source_file
            
                del proj.data_box_list[key]
                del proj.data_box_design_view_list[key]                                              
                #Remove and delete item form design layout scene container
                proj.removeItem(item)
                del item
                
                #Rebuild data box instance
                proj.data_box_list[key] = models.DataBox(key, t_text, t_geometry,
                                   t_position, t_width, t_height, t_color, t_opacity,
                                   t_border_color, t_text_width, t_text_size,
                                   t_text_color,t_text_bold, t_text_italic,
                                   t_border_style, t_border_width, t_text_pos_x, 
                                   t_text_pos_y, d_box_geometry, d_box_position,
                                   d_box_width, d_box_height, d_box_color, d_box_opacity,
                                   d_box_gradient, d_border_color, d_box_border_style,
                                   d_box_border_width, d_text_size, d_width, d_width_2,
                                   d_text_pos_x, d_text_pos_y, data_source_file)
            
                proj.data_box_design_view_list[key] = DataBoxDesignView(key, t_text,
                                t_geometry, t_width, t_height, t_color,
                                t_opacity, t_border_color, t_text_width, t_text_size,
                                t_text_color, t_text_bold, t_text_italic, t_border_style,
                                t_border_width, t_text_pos_x, t_text_pos_y, 
                                d_box_geometry, d_box_width, d_box_height, d_box_color,
                                d_box_opacity, d_box_gradient, d_border_color,
                                d_box_border_style, d_box_border_width, d_text_size,
                                d_width, d_width_2, d_text_pos_x, d_text_pos_y,
                                data_source_file)
            
                proj.data_box_design_view_list[key].setPos(d_box_position)           
                proj.addItem(proj.data_box_design_view_list[key])
                
    def reset_simulation_action_buttons(self):
        self.action_PauseSimulation.setEnabled(False)
        self.action_StopSimulation.setEnabled(False)
        self.action_StartSimulation.setEnabled(True)
        self.actionPause.setEnabled(False)
        self.actionEnd.setEnabled(False)
        self.actionStart.setEnabled(True)
            
    '''End of method definitions for SystemLabMainApp=================================='''
'''END of class definition for main application window/interface (SystemLabMainApp)===='''
    
class DesignLayoutScene(QtWidgets.QGraphicsScene):
    '''PyQt class for QGraphicsScene - Holds all QtGraphics instances for a project
    '''
    def __init__(self, scene_name, parent=None):
        super(DesignLayoutScene, self).__init__(parent)      
        self.scene_name = scene_name
        self.lines = []
        self.border = []     
        self.selectionChanged.connect(self.check_item_selected)
        self.drag_mode = False
        
        #Dictionaries=====================================================================
        self.fb_list = {} #Functional blocks (FunctionalBlock instances)
        self.fb_design_view_list = {}
        self.signal_links_list = {} #Tracks all signal links placed in the scene
        self.design_settings = {'project_name':scene_name,
                                'file_path_1': '', 'file_path_2': '',
                                'time_window':1.0E-08,'sampling_rate': 1.00E+11,
                                'symbol_rate': 1.00E+10, 'samples_per_sym': 10,
                                'sampling_period':1.00E-11, 'num_samples':1E3,
                                'iterations':1, 'current_iteration':1,
                                'feedback_enabled':0, 'feedback_segments': 100,
                                'feedback_current_segment':1, 'samples_per_segment':10,
                                'max_calculation_attempts': 10,
                                'back_color':'#ffffff', 'scene_width':2000,
                                'scene_height':1000, 'grid_enabled':0, 'grid_size':10,
                                'grid_color':'#000000', 'grid_opacity':0.3, 
                                'grid_line_width':0.5, 'grid_line_style':'SolidLine',
                                'border_enabled':0, 'border_color':'#000000',
                                'border_opacity':0.5, 'border_width': 0.75,
                                'edit_script_path': 'start .\wscite\SciTE -open:'}
        self.text_list = {} #Text field data model
        self.text_design_view_list = {} #Text field (QtGraphicsTextItem instances)
        self.desc_box_list = {} #Description boxes (data model)
        self.desc_box_design_view_list = {} #Decription boxes (QtGraphicsRectItem instances)
        self.data_box_list = {}
        self.data_box_design_view_list = {}
        self.line_arrow_list = {}
        self.line_arrow_design_view_list = {}
        self.data_port_view_list = {}
        #=================================================================================
        
        self.setSceneRect(QtCore.QRectF(0,0,self.design_settings['scene_width'],
                                        self.design_settings['scene_height']))
        
        self.style = self.design_settings['grid_line_style']
        self.line_style = set_line_type(self.style)
        self.line_width = self.design_settings['grid_line_width']
        self.color = self.design_settings['grid_color']
        self.pen_grid = QtGui.QPen(QtGui.QColor(self.color), self.line_width,
                                   self.line_style)
        
        self.border_width = self.design_settings['border_width']
        self.border_color = self.design_settings['border_color']
        self.pen_border = QtGui.QPen(QtGui.QColor(self.border_color), 
                                     self.border_width, QtCore.Qt.SolidLine)
        
        if self.design_settings['grid_enabled'] == 2:
            self.draw_grid(self.pen_grid)
            self.set_opacity(self.design_settings['grid_opacity'])
            
        if self.design_settings['border_enabled'] == 2:
            self.draw_border(self.pen_border)
            self.set_opacity_border(self.design_settings['border_opacity'])
      
    def draw_grid(self, pen):
        self.grid = self.design_settings['grid_size']
        self.w = self.design_settings['scene_width']
        self.h = self.design_settings['scene_height']
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)

        for x in range(0,int(round(self.w/self.grid))):
            xc = x * self.grid
            self.lines.append(self.addLine(xc,0,xc,self.h,pen))

        for y in range(0,int(round(self.h/self.grid))):
            yc = y * self.grid
            self.lines.append(self.addLine(0,yc,self.w,yc,pen))
            
        for line in self.lines:
            line.setZValue(-200)

    def set_visible(self,visible=True):
        for line in self.lines:
            line.setVisible(visible)

    def delete_grid(self):
        for line in self.lines:
            self.removeItem(line)
        del self.lines[:]

    def set_opacity(self,opacity):
        for line in self.lines:
            line.setOpacity(opacity)
            
    def draw_border(self, pen):
        self.w = self.design_settings['scene_width']
        self.h = self.design_settings['scene_height']
        
        self.setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        
        self.border.append(self.addLine(0,0,0,self.h,pen))
        self.border.append(self.addLine(0,0,self.w,0,pen))
        self.border.append(self.addLine(self.w,0,self.w,self.h, pen))
        self.border.append(self.addLine(0, self.h,self.w,self.h,pen))
        
        for line in self.border:
            line.setZValue(-200)
        
    def set_opacity_border(self,opacity):
        for line in self.border:
            line.setOpacity(opacity)
            
    def delete_border(self):
        for line in self.border:
            self.removeItem(line)
        del self.border[:]

#        https://stackoverflow.com/questions/39614777/how-to-draw-a-proper-grid-on-pyqt 
#         class QS(QtWidgets.QGraphicsScene):
               
    def prepare_project_data_and_items(self):
        #This is called before saving a project (creates a registry of 
        #functional blocks, links, project settings, text fields, description boxes)
        tab_index, key_index = retrieve_current_project_key_index()
        #Retrieve all functional blocks and description boxes within the project scene
        
        items = window.project_scenes_list[key_index].items()
        for item in items:
            if type(item) is FunctionalBlockDesignView:
                key = item.fb_key
                #Retrieve object's geometry and location and update model attributes
                self.fb_list[key].fb_geometry = item.rect()
                self.fb_list[key].fb_position = item.pos()
                self.fb_list[key].fb_dim = [float(item.width), float(item.height)]           
            if type(item) is DescriptionBoxDesignView:
                key = item.desc_key
                self.desc_box_list[key].box_geometry = item.rect()
                self.desc_box_list[key].box_position = item.pos()
                self.desc_box_list[key].box_dim = [float(item.width), float(item.height)]              
            if type(item) is DataBoxDesignView:
                key = item.data_key
                self.data_box_list[key].data_box_geometry = item.rect()
                self.data_box_list[key].data_box_position = item.pos()          
            if type(item) is TextBoxDesignView:
                key = item.text_key
                self.text_list[key].text_geometry = item.rect()
                self.text_list[key].text_position = item.pos()             
            if type(item) is LineArrowDesignView:
                key = item.key
                self.line_arrow_list[key].geometry = item.line()
                self.line_arrow_list[key].position = item.pos()
       
        #Save fb and desc box dictionaries
        self.dict_list_save = [self.design_settings, self.fb_list, self.signal_links_list,
                               self.desc_box_list, self.data_box_list, self.text_list,
                               self.line_arrow_list]
        return  self.dict_list_save    
    
    def retrieve_scene_items(self, mouseEvent):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
        return key_index, items
        
    def contextMenuEvent(self, event):
        key_index, items = self.retrieve_scene_items(event)      
        if len(items) != 0: #Access context menu for selected item
            for item in items:
                if (type(item) is FunctionalBlockDesignView
                    or type(item) is DataBoxDesignView
                    or type(item) is TextBoxDesignView
                    or type(item) is DescriptionBoxDesignView
                    or type(item) is LineArrowDesignView):
                    item.setSelected(True)
                    item.access_pull_down_menu(event)
                    break
        else:
            self.access_scene_menu(event)
                
    def access_scene_menu(self, event): 
        menu = QtWidgets.QMenu()    
        add_fb_action = menu.addAction('Add functional block')
        add_fb_action.setIcon(window.action_add_fb_icon)
        add_data_action = menu.addAction('Add data panel')
        add_data_action.setIcon(window.action_add_data_icon)
        add_desc_action = menu.addAction('Add description box')
        add_desc_action.setIcon(window.action_add_desc_icon)
        add_txt_action = menu.addAction('Add text box')
        add_txt_action.setIcon(window.action_add_text_icon)
        add_line_arrow_action = menu.addAction('Add line with arrow')
        add_line_arrow_action.setIcon(window.action_add_line_arrow_icon)
        menu.addSeparator()
        project_settings_action = menu.addAction('Project and layout settings')
        project_settings_action.setIcon(window.project_settings_icon)
        fb_list_action = menu.addAction('View list of functional blocks')
        fb_list_action.setIcon(window.action_fblist_icon)
        menu.addSeparator()
        scene_background_action = menu.addAction('Change scene background color')
        scene_background_action.setIcon(window.action_scene_color_icon)
        scene_save_image_action = menu.addAction('Save image of project scene')
        scene_save_image_action.setIcon(window.action_save_scene_icon)
        menu.addSeparator()
        set_cursor_mode = QtWidgets.QAction('Enable scene scrolling (hand cursor)', 
                                            menu, checkable=True)
        menu.addAction(set_cursor_mode)
        if self.drag_mode == True:
            set_cursor_mode.setChecked(True)
        else:
            set_cursor_mode.setChecked(False)
        action = menu.exec_(event.screenPos())       
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        proj_sc = window.project_scenes_list[self.key_index]
        proj_view = window.project_views_list[self.key_index]
        
        if action == add_fb_action:
            #Action to add new functional block to the design (QtGraphicsScene) space
            i = set_new_key(self.fb_list)
            #Instantiate new FB and FB design view objects
            self.insert_functional_block(i)
            self.fb_design_view_list[i].setPos(event.scenePos())
            proj_sc.addItem(self.fb_design_view_list[i])
            window.tableWidget2.resizeColumnsToContents()
        
        if action == add_txt_action:
            #Add text field to graphics scene
            i = set_new_key(self.text_list)           
            self.insert_text_box(i)
            self.text_design_view_list[i].setPos(event.scenePos())
            self.text_design_view_list[i].setRect(QtCore.QRectF(0,0,80,30))
            proj_sc.addItem(self.text_design_view_list[i])
            
        if action == add_desc_action:
            #Add description box field to graphics scene
            i = set_new_key(self.desc_box_list)            
            self.insert_desc_box(i)
            self.desc_box_design_view_list[i].setPos(event.scenePos())
            proj_sc.addItem(self.desc_box_design_view_list[i])
            
        if action == add_data_action:
            #Add data box to graphics scene
            i = set_new_key(self.data_box_list)              
            self.insert_data_box(i)
            self.data_box_design_view_list[i].setPos(event.scenePos())
            proj_sc.addItem(self.data_box_design_view_list[i])
                    
        if action == add_line_arrow_action:
            #Add line-arrow to graphics scene
            i = set_new_key(self.line_arrow_list)
            self.insert_line_arrow(i)
            self.line_arrow_design_view_list[i].setPos(event.scenePos())
            proj_sc.addItem(self.line_arrow_design_view_list[i])
        
        if action == project_settings_action:
            self.open_project_settings(self.tab_index, self.key_index)
                                                        
        if action == fb_list_action:
            self.build_fb_list()
        
        if action == scene_background_action: 
            self.update_background_color()
        
        if action == scene_save_image_action:
            self.save_image_scene(proj_view)
                
        if action == set_cursor_mode:
            if set_cursor_mode.isChecked():
                set_cursor_mode.setChecked(True)
                self.drag_mode = True     
                proj_view.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            else: 
                set_cursor_mode.setChecked(False)
                self.drag_mode = False   
                proj_view.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            
    def insert_functional_block(self, i):
        self.fb_list[i] = models.FunctionalBlock(i, 'functional_block_' + str(i), 
                    display_name = 2, display_port_name = 0, 
                    fb_geometry = QtCore.QRectF(0,0,50,50), fb_dim =[], fb_position = [],
                    fb_script_module='', fb_icon_display = 0, fb_icon='',
                    fb_icon_x = 0, fb_icon_y = 0, fb_parameters_list = [], 
                    fb_results_list = [], text_size = 7, text_length = 100,
                    text_color ='#000000', text_bold = 2, text_italic = 0,
                    fb_color = '#d3d3d3', fb_color_2 = '#d3d3d3', fb_gradient = 0,
                    fb_border_color = '#6d6d6d', fb_border_style = 'SolidLine',
                    text_pos_x = -2, text_pos_y = -2, port_label_size = 7,
                    port_label_bold = 0, port_label_italic = 0, 
                    port_label_color = '#000000')     
        self.fb_design_view_list[i] = FunctionalBlockDesignView(i, 
                    'functional_block_' + str(i), 2, 0, self.fb_list[i].fb_geometry,
                    50, 50, fb_script='', fb_icon_display = 0, fb_icon='',
                    fb_icon_x = 0, fb_icon_y = 0, text_size = 7, text_length = 100,
                    text_color = '#000000', text_bold = 2, text_italic = 0,
                    fb_color = '#d3d3d3', fb_color_2 = '#d3d3d3',
                    fb_gradient = 0, fb_border_color = '#6d6d6d',
                    fb_border_style = 'SolidLine', text_pos_x = -2,
                    text_pos_y = -2, port_label_size = 7, port_label_bold = 0,
                    port_label_italic = 0, port_label_color = '#000000')  

    def insert_text_box(self, i):
        self.text_list[i] = models.TextBox(i, text = 'New text item', text_width = 80,
                      text_position = [], text_geometry = QtCore.QRectF(0,0,80,30),
                      text_color = '#000000', text_size = 7, text_bold = 0,
                      text_italic = 0)
        self.text_design_view_list[i] = TextBoxDesignView(i, 
                                  text_geometry = self.text_list[i].text_geometry,
                                  text = 'New text item', text_width = 80,
                                  text_color = '#000000', text_size = 7, text_bold = 0,
                                  text_italic = 0)
    def insert_desc_box(self, i):
        self.desc_box_list[i] = models.DescriptionBox(i, 'New desciption box', 
                              box_position = [], box_dim = [], 
                              box_geometry = QtCore.QRectF(0,0,250,200), 
                              text_width = 100, fill_color = '#d3d3d3',
                              fill_color_2 = '#d3d3d3', opacity = 1,
                              gradient = 0, border_color = '#6d6d6d', text_size = 7,
                              text_color ='#000000', text_bold = 0, text_italic = 0,
                              border_style = 'SolidLine', border_width = 0.5, 
                              text_pos_x = -2, text_pos_y = -2 )                            
        self.desc_box_design_view_list[i] = DescriptionBoxDesignView(i, 'New desciption box',
                              self.desc_box_list[i].box_geometry, 250, 200,
                              box_color = '#d3d3d3', box_color_2 = '#d3d3d3', opacity = 1,
                              gradient = 0, box_border_color = '#6d6d6d', 
                              text_width = 100, text_size = 7,
                              text_color = '#000000', text_bold = 0, 
                              text_italic = 0, border_style = 'SolidLine',
                              border_width = 0.5, text_pos_x = -2,
                              text_pos_y = -2)
        
    def insert_data_box(self, i):
        self.data_box_list[i] = models.DataBox(i, 'New data panel',
                title_geometry = QtCore.QRectF(0,0,150,18) , title_position = [],
                title_width = 150, title_height = 18, title_box_color = '#d3d3d3',
                title_box_opacity = 1, title_border_color = '#6d6d6d', 
                title_text_width = 100, title_text_size = 7, title_text_color = '#000000',
                title_text_bold = 2, title_text_italic = 2, 
                title_border_style = 'SolidLine', title_border_width = 1,
                title_text_pos_x = 5, title_text_pos_y = 0,
                data_box_geometry = QtCore.QRectF(0,0,150,150), data_box_position = [],
                data_box_width = 150, data_box_height = 150, 
                data_box_color = '#d3d3d3', data_box_opacity = 1, data_box_gradient = 2,
                data_border_color = '#6d6d6d', data_box_border_style = 'SolidLine', 
                data_box_border_width = 1, data_text_size = 7, data_width = 40,
                value_width = 40, data_text_pos_x = 1, data_text_pos_y = 20,
                data_source_file = '')                             
        self.data_box_design_view_list[i] = DataBoxDesignView(i, 'New data panel', 
                title_geometry = QtCore.QRectF(0,0,150,18), title_width = 150, 
                title_height = 18, title_box_color = '#d3d3d3', title_box_opacity = 1,
                title_border_color = '#6d6d6d', title_text_width = 100, title_text_size = 7,
                title_text_color = '#000000', title_text_bold = 2, title_text_italic = 2, 
                title_border_style = 'SolidLine', title_border_width = 1, 
                title_text_pos_x = 5, title_text_pos_y = 0,
                data_box_geometry = QtCore.QRectF(0,0,150,150), data_box_width = 150,
                data_box_height = 150, data_box_color = '#d3d3d3', data_box_opacity = 1,
                data_box_gradient = 2, data_border_color = '#6d6d6d', 
                data_box_border_style = 'SolidLine', data_box_border_width = 1,
                data_text_size = 7, data_width = 40, value_width = 40,
                data_text_pos_x = 1, data_text_pos_y = 20, data_source_file = '')
        
    def insert_line_arrow(self, i):      
        self.line_arrow_list[i] = models.LineArrow(i, position = [], 
                                geometry = QtCore.QLineF(0,0,100,100), color = '#00007f',
                                line_width = 0.5, line_style = 'SolidLine', arrow = 2)
        self.line_arrow_design_view_list[i] = LineArrowDesignView (i,
                                geometry = QtCore.QLineF(0,0,100,100), color = '#00007f',
                                line_width = 0.5, line_style = 'SolidLine', arrow = 2)        
            
    def open_project_settings(self, tab_index, key_index):
        project_name = window.tabWidget.tabText(tab_index)
        proj_design_settings = window.project_scenes_list[key_index].design_settings
        file_path_1 = proj_design_settings['file_path_1']    
        file_path_2 = proj_design_settings['file_path_2'] 
        samplingRate =  proj_design_settings['sampling_rate']
        timeWindow =  proj_design_settings['time_window']
        samplingPeriod =  proj_design_settings['sampling_period']
        samplesNumber = proj_design_settings['num_samples']
        iterationNumber = proj_design_settings['iterations']
        feedbackMode = proj_design_settings['feedback_enabled']
        feedbackSegments = proj_design_settings['feedback_segments']
        samplesPerSegment = proj_design_settings['samples_per_segment']
        symbolRate = proj_design_settings['symbol_rate']
        samplesPerSym = proj_design_settings['samples_per_sym']
        max_calculation_attempts = proj_design_settings['max_calculation_attempts']
        edit_script_path = proj_design_settings['edit_script_path']
        w = proj_design_settings['scene_width']
        h = proj_design_settings['scene_height']
        grid_enabled = proj_design_settings['grid_enabled']
        grid = proj_design_settings['grid_size']
        line_color = proj_design_settings['grid_color']
        line_opacity = proj_design_settings['grid_opacity']
        line_width = proj_design_settings['grid_line_width']
        line_style = proj_design_settings['grid_line_style']
        border_enabled = proj_design_settings['border_enabled']
        border_color = proj_design_settings['border_color']
        border_opacity = proj_design_settings['border_opacity']
        border_width = proj_design_settings['border_width']
    
        global project_dialog
        project_dialog = ProjectPropertiesGUI()
        
        #Load project name (current) and simulation settings
        project_dialog.projectName.setText(project_name)
        project_dialog.projectFilePath.setText(file_path_1)
        project_dialog.projectFilePath2.setText(file_path_2)
        project_dialog.projectSampleRate.setText(str(format(samplingRate, '0.4E')))
        project_dialog.projectSimulationTime.setText(str(format(timeWindow, '0.4E')))
        project_dialog.projectSamplePeriod.setText(str(format(samplingPeriod, '0.4E')))
        project_dialog.projectNumberSamples.setText(str(format(samplesNumber, '0.4E')))
        project_dialog.iterationSetting.setText(str(iterationNumber))
        project_dialog.projectSegments.setText(str(feedbackSegments))
        project_dialog.samplesPerSegment.setText(str(samplesPerSegment))
        project_dialog.checkBoxFeedback.setCheckState(feedbackMode)
        project_dialog.projectSymbolRate.setText(str(format(symbolRate, '0.4E')))
        project_dialog.projectSamplesSym.setText(str(format(samplesPerSym, '0.4E')))
        project_dialog.maxCalculationAttempts.setText(str(format(max_calculation_attempts, 'n')))
        project_dialog.editScriptPath.setText(str(edit_script_path))
            
        project_dialog.projectWidth.setText(str(w))
        project_dialog.projectHeight.setText(str(h))
        project_dialog.checkBoxGrid.setCheckState(grid_enabled)
        project_dialog.gridSize.setText(str(grid))
        project_dialog.gridLineColor.setText(str(line_color))
        project_dialog.gridLineOpacity.setText(str(line_opacity))
        project_dialog.gridLineWidth.setText(str(line_width))
        project_dialog.titleComboBoxGrid.setCurrentText(str(line_style))
            
        project_dialog.checkShowBorder.setCheckState(border_enabled)
        project_dialog.borderLineColor.setText(str(border_color))
        project_dialog.borderLineOpacity.setText(str(border_opacity))   
        project_dialog.borderLineWidth.setText(str(border_width))
        
        if feedbackMode == 2:
            project_dialog.projectSegments.setEnabled(True)
        else:
            project_dialog.projectSegments.setEnabled(False)
            
        #Display window
        project_dialog.show()
        if project_dialog.exec():           
            #If project name is changed, update projects list dict and tab title
            new_project_name = project_dialog.projectName.text()
            window.tabWidget.setTabText(tab_index, new_project_name) #Tab title
            #Update project names dictionary and project settings dictionary
            del window.project_names_list[project_name]
            window.project_names_list[new_project_name] = key_index
            d_settings = window.project_scenes_list[key_index].design_settings
            d_settings['project_name'] = new_project_name             
            #Update name attribute of object dictionaries
            window.project_layouts_list[key_index]= new_project_name
            window.project_scenes_list[key_index].scene_name = new_project_name
            window.project_views_list[key_index].scene = new_project_name
            #==================================================================
            new_file_path_1 = project_dialog.projectFilePath.text()
            d_settings['file_path_1'] = None
            d_settings['file_path_1'] = new_file_path_1
            new_file_path_2 = project_dialog.projectFilePath2.text()
            d_settings['file_path_2'] = None
            d_settings['file_path_2'] = new_file_path_2           
            
            #Project simulation settings=======================================
            project_dialog.apply() #Ensure all calculations are aligned (on OK)
            fs = float(project_dialog.projectSampleRate.text())
            t_win = float(project_dialog.projectSimulationTime.text())
            T = float(project_dialog.projectSamplePeriod.text())
            n = float(project_dialog.projectNumberSamples.text())
            i = int(project_dialog.iterationSetting.text())
            fsym = float(project_dialog.projectSymbolRate.text())
            samples_sym = float(project_dialog.projectSamplesSym.text())
            segments = int(project_dialog.projectSegments.text())
            samples_seg = float(project_dialog.samplesPerSegment.text())
               
            #Update design scene settings (captures any changes)
            d_settings['time_window'] = t_win
            d_settings['sampling_rate'] = fs
            d_settings['sampling_period'] = T
            d_settings['num_samples'] = n
            d_settings['iterations'] = i
            d_settings['symbol_rate'] = fsym
            d_settings['samples_per_sym'] = samples_sym
            d_settings['feedback_segments'] = segments
            d_settings['samples_per_segment'] = samples_seg
            
            window.iterationsSelector.setMaximum(i)
            window.tableWidget2.item(0, 1).setText(format(i, 'n')) 
            window.tableWidget2.item(1, 1).setText(format(segments, 'n')) 
            window.tableWidget2.resizeColumnsToContents()
            window.tableWidget.item(0, 1).setText(format(fs, '0.3E'))
            window.tableWidget.item(1, 1).setText(format(t_win, '0.3E'))
            window.tableWidget.item(2, 1).setText(format(n, '0.3E'))           
            window.tableWidget.resizeColumnsToContents()
                
            w = float(project_dialog.projectWidth.text())
            h = float(project_dialog.projectHeight.text())
            grid_enabled = project_dialog.checkBoxGrid.checkState()
            grid = float(project_dialog.gridSize.text())
            line_color = project_dialog.gridLineColor.text()
            line_opacity = float(project_dialog.gridLineOpacity.text())
            line_width = float(project_dialog.gridLineWidth.text())
            line_style = project_dialog.titleComboBoxGrid.currentText()
                
            b_enabled = project_dialog.checkShowBorder.checkState()
            b_color = project_dialog.borderLineColor.text()
            b_opacity = float(project_dialog.borderLineOpacity.text())
            b_width = float(project_dialog.borderLineWidth.text())
            
            feedback = project_dialog.checkBoxFeedback.checkState()
            
            max_attempts = project_dialog.maxCalculationAttempts.text()
            edit_script = project_dialog.editScriptPath.text()
                
            d_settings['scene_width'] = w
            d_settings['scene_height'] = h
            d_settings['grid_enabled'] = int(grid_enabled)
            d_settings['grid_size'] = grid
            d_settings['grid_color'] = line_color
            d_settings['grid_opacity'] = line_opacity 
            d_settings['grid_line_width'] = line_width
            d_settings['grid_line_style'] = line_style
                
            d_settings['border_enabled'] = int(b_enabled)
            d_settings['border_color'] = b_color
            d_settings['border_opacity'] = b_opacity
            d_settings['border_width'] = b_width
            
            d_settings['feedback_enabled'] = int(feedback)
            
            d_settings['max_calculation_attempts'] = int(max_attempts)
            d_settings['edit_script_path'] = str(edit_script)
            
            if feedback == 2:
                window.tableWidget3.item(1, 1).setText('')
            else:
                window.tableWidget3.item(1, 1).setText('N/A')
                         
            window.project_scenes_list[key_index].setSceneRect(QtCore.QRectF(0,0,w,h))
                
            style = set_line_type(line_style)
            self.pen_grid = QtGui.QPen(QtGui.QColor(line_color), line_width, style)
            self.pen_border = QtGui.QPen(QtGui.QColor(b_color), 
                                         b_width, QtCore.Qt.SolidLine)               
            if self.lines is not None:
                self.delete_grid()                 
            if self.border is not None:
                self.delete_border()             
            if window.project_scenes_list[key_index].design_settings['grid_enabled'] == 2:
                self.lines = []
                self.draw_grid(self.pen_grid)
                self.set_opacity(line_opacity)          
            if window.project_scenes_list[key_index].design_settings['border_enabled'] == 2:
                self.border = []
                self.draw_border(self.pen_border)
                self.set_opacity_border(b_opacity) 
                
    def build_fb_list(self):           
        global fb_list_view
        fb_list_view = FunctionalBlockListGUI()  
        fb_list_view.functionalBlockListTable.setRowCount(0)          
        items = window.project_scenes_list[self.key_index].items()
        i = 0
        for item in items:
            if type(item) is FunctionalBlockDesignView:
                fb_id = item.fb_key
                fb_name = item.name
                fb_script = item.fb_script
                fb_list_view.functionalBlockListTable.insertRow(i)
                fb_list_view.functionalBlockListTable.setItem(i, 0, 
                                            QtWidgets.QTableWidgetItem(str(fb_name)))
                fb_list_view.functionalBlockListTable.setItem(i, 1,
                                            QtWidgets.QTableWidgetItem(str(fb_id)))
                fb_list_view.functionalBlockListTable.setItem(i, 2,
                                            QtWidgets.QTableWidgetItem(str(fb_script)))
                i += 1
            
        fb_list_view.functionalBlockListTable.sortItems(0, QtCore.Qt.AscendingOrder)
        fb_list_view.functionalBlockListTable.resizeColumnsToContents()
        fb_list_view.show()
        
    def update_background_color(self):
        current_color = QtGui.QColor(window.project_scenes_list[self.key_index].design_settings['back_color'])
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            window.project_scenes_list[self.key_index].setBackgroundBrush(QtGui.QBrush(QtGui.QColor(color)))
            window.project_views_list[self.key_index].setBackgroundBrush(QtGui.QBrush(QtGui.QColor(color)))
            window.project_scenes_list[self.key_index].design_settings['back_color'] = color.name()
                  
    def save_image_scene(self, proj_view):
        view_x = proj_view.viewport().width()
        view_y = proj_view.viewport().height()
        self.pix = QtGui.QPixmap(view_x, view_y)
        painter = QtGui.QPainter(self.pix)
        proj_view.render(painter)
        fileName = QtWidgets.QFileDialog.getSaveFileName(None, 'Save image as...',
                                                         'C:', filter = '*.png')
        if fileName[0]:
            self.pix.save(str(fileName[0]), 'png')
            
    def mouseMoveEvent(self, mouseEvent): #QT specific method
        window.sceneMouseMoveEvent(mouseEvent)
        super(DesignLayoutScene, self).mouseMoveEvent(mouseEvent)  
    
    def mouseReleaseEvent(self, mouseEvent): #QT specific method
        window.sceneMouseReleaseEvent(mouseEvent)
        super(DesignLayoutScene, self).mouseReleaseEvent(mouseEvent)
    
    def check_item_selected(self):
        items = self.selectedItems()
        if items:
            window.action_Delete.setEnabled(True)
            window.action_CopyPaste.setEnabled(True)
            window.action_CopyPasteToAnotherProj.setEnabled(True)
        else:
            window.action_Delete.setEnabled(False)
            window.action_CopyPaste.setEnabled(False)
            window.action_CopyPasteToAnotherProj.setEnabled(False)
           
    def dragEnterEvent(self, event): #QT specific method
        if event.mimeData().hasFormat('application/x-item'):
            event.acceptProposedAction()
        else:
            event.ignore
        
    def dragMoveEvent(self, event): #QT specific method
        if event.mimeData().hasFormat('application/x-item'):
            event.acceptProposedAction()
            event.setDropAction(QtCore.Qt.LinkAction)
        else:
            event.ignore()
        
    def dropEvent(self, event): #QT specific method
        if event.mimeData().hasFormat('application/x-item'):
            event.acceptProposedAction()
            data = event.mimeData().data('application/x-item' )
            stream= QtCore.QDataStream(data, QtCore.QIODevice.ReadOnly)
            fb_text = stream.readQString()
            
            tab_index, key_index = retrieve_current_project_key_index()
            proj_sc = window.project_scenes_list[key_index]
            i = set_new_key(proj_sc.fb_list)
            
            local_dir = 'syslab_fb_library'
            fb_file = os.path.join(root_path, local_dir, str(fb_text) + '.slb')
            
            try:
                dict_list = pickle.load(open(fb_file, 'rb'))
                #Instantiate new FB and FB design view objects
                name = dict_list[1][1].fb_name
                display_name = dict_list[1][1].display_name
                display_port_name = dict_list[1][1].display_port_name
                geometry = dict_list[1][1].fb_geometry
                dim = dict_list[1][1].fb_dim
                position = dict_list[1][1].fb_position
                ports = dict_list[1][1].fb_ports_list
                script = dict_list[1][1].fb_script_module
                icon_display = dict_list[1][1].fb_icon_display         
                icon = dict_list[1][1].fb_icon
                icon_x = dict_list[1][1].fb_icon_x
                icon_y = dict_list[1][1].fb_icon_y
                parameters = dict_list[1][1].fb_parameters_list
                results = dict_list[1][1].fb_results_list
                text_size = dict_list[1][1].text_size
                text_length = dict_list[1][1].text_length
                text_color = dict_list[1][1].text_color
                text_bold = dict_list[1][1].text_bold
                text_italic = dict_list[1][1].text_italic
                color = dict_list[1][1].fb_color
                color2 = dict_list[1][1].fb_color_2
                grad = dict_list[1][1].fb_gradient
                border_color = dict_list[1][1].fb_border_color
                border_style = dict_list[1][1].fb_border_style
                text_pos_x = dict_list[1][1].text_pos_x
                text_pos_y = dict_list[1][1].text_pos_y               
                port_label_size = dict_list[1][1].port_label_size
                port_label_bold = dict_list[1][1].port_label_bold
                port_label_italic = dict_list[1][1].port_label_italic
                port_label_color = dict_list[1][1].port_label_color
    
                proj_sc.fb_list[i] = models.FunctionalBlock(i,
                                        name, display_name, display_port_name, geometry, dim,
                                        position, script, icon_display, icon, icon_x, icon_y,
                                        parameters, results, text_size, text_length, text_color, 
                                        text_bold, text_italic, color, color2, grad,
                                        border_color, border_style, text_pos_x, text_pos_y,
                                        port_label_size, port_label_bold, port_label_italic,
                                        port_label_color)
                proj_sc.fb_list[i].fb_ports_list = ports
                proj_sc.fb_design_view_list[i] = FunctionalBlockDesignView(i,
                                        name, display_name, display_port_name, geometry, 
                                        dim[0], dim[1], script, icon_display, icon, icon_x, icon_y,
                                        text_size, text_length, text_color, text_bold, text_italic,
                                        color, color2, grad, border_color, border_style,
                                        text_pos_x, text_pos_y, port_label_size, port_label_bold,
                                        port_label_italic, port_label_color) 
                proj_sc.fb_design_view_list[i].update_ports(i)
                
                #Add new objects to graphics view space
                proj_sc.fb_design_view_list[i].setPos(event.scenePos())           
                proj_sc.addItem(proj_sc.fb_design_view_list[i])
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error loading functional block from library')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
                msg.setWindowTitle("Loading error: Functional block")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
        else:
            event.ignore()
            
    def keyPressEvent (self, eventQKeyEvent): #QT specific method
        key = eventQKeyEvent.key()
        if self.selectedItems():
            items = self.selectedItems()         
            #Key operations for moving items in the scene
            if key == QtCore.Qt.Key_Left:
                for item in items:
                    item.setPos(item.scenePos().x() - 0.25, item.scenePos().y())
            elif key == QtCore.Qt.Key_Up:
                for item in items:
                    item.setPos(item.scenePos().x(), item.scenePos().y() - 0.25)
            elif key == QtCore.Qt.Key_Right:
                for item in items:
                    item.setPos(item.scenePos().x() + 0.25, item.scenePos().y())
            elif key == QtCore.Qt.Key_Down:
                for item in items:
                    item.setPos(item.scenePos().x(), item.scenePos().y() + 0.25)
            elif key == QtCore.Qt.Key_Delete:
                window.delete_selected_items()
             
                    
class FunctionalBlockTreeList1(QtWidgets.QTreeWidget):    
    def __init__(self, parent = None):
        super(FunctionalBlockTreeList1, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setColumnCount(1)
        
        title = config_lib.library_title
        self.setHeaderLabel(title)
        self.setIndentation(10)        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                       QtWidgets.QSizePolicy.Expanding)      
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(config_lib.library_main_w, config_lib.library_main_h))
        self.setMaximumSize(QtCore.QSize(config_lib.library_main_w, config_lib.library_main_h))
        
        try:
            font = QtGui.QFont()
            for s in range(0, len(config_lib.fb_sections)):
                section = QtWidgets.QTreeWidgetItem([config_lib.fb_sections_properties[s][0]])
                r = config_lib.fb_sections_properties[s][1]
                g = config_lib.fb_sections_properties[s][2]
                b = config_lib.fb_sections_properties[s][3]
                t = config_lib.fb_sections_properties[s][4]
                color = QtGui.QBrush(QtGui.QColor(r, g, b, t))
                font.setItalic(True)
                font.setBold(False)
                # Add groups to section
                for i in range(0, len(config_lib.fb_sections[s])-1):
                    group = QtWidgets.QTreeWidgetItem([config_lib.fb_sections[s][0][i]])
                    group.setFont(0, font)
                    group.setBackground(0, color)
                    section.addChild(group)
                    # Add members to group (functional block names)
                    for j in range(0, len(config_lib.fb_sections[s][i+1])):
                        member = QtWidgets.QTreeWidgetItem([config_lib.fb_sections[s][i+1][j]])
                        group.addChild(member)
                # Prepare font/color format for section title      
                font.setItalic(False)
                font.setBold(True)
                self.addTopLevelItem(section)
                section.setBackground(0, QtGui.QBrush(QtGui.QColor(r, g, b, t)))   
                section.setFont(0, font)
                expanded_flag = config_lib.fb_sections_properties[s][5]
                section.setExpanded(expanded_flag)      
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error while loading functional block library')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
            msg.setWindowTitle("Loading error: Functional block library")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
    def startDrag(self, dropActions):
        item = self.currentItem()
        if item.childCount() == 0:    
            data = QtCore.QByteArray()
            stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
            stream.writeQString(item.text(0))
            mimeData = QtCore.QMimeData()
            mimeData.setData("application/x-item", data)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData) 
            drag.exec()
            
class FunctionalBlockTreeList2(QtWidgets.QTreeWidget): #Only instantiated if 
                                                       #config.sections list is not empty  
    def __init__(self, parent = None):
        super(FunctionalBlockTreeList2, self).__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(False)
        self.setColumnCount(1)
        
        title_2 = config_lib.library_2_title
        self.setHeaderLabel(title_2)
        self.setIndentation(10)        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, 
                                       QtWidgets.QSizePolicy.Expanding)      
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(config_lib.library_2_w, config_lib.library_2_h))
        self.setMaximumSize(QtCore.QSize(config_lib.library_2_w, config_lib.library_2_h))
        
        try:
            font = QtGui.QFont()
            for s in range(0, len(config_lib.fb_sections_2)):
                section = QtWidgets.QTreeWidgetItem([config_lib.fb_sections_properties_2[s][0]])
                r = config_lib.fb_sections_properties_2[s][1]
                g = config_lib.fb_sections_properties_2[s][2]
                b = config_lib.fb_sections_properties_2[s][3]
                t = config_lib.fb_sections_properties_2[s][4]
                color = QtGui.QBrush(QtGui.QColor(r, g, b, t))
                font.setItalic(True)
                font.setBold(False)
                # Add groups to section
                for i in range(0, len(config_lib.fb_sections_2[s])-1):
                    group = QtWidgets.QTreeWidgetItem([config_lib.fb_sections_2[s][0][i]])
                    group.setFont(0, font)
                    group.setBackground(0, color)
                    section.addChild(group)
                    # Add members to group (functional block names)
                    for j in range(0, len(config_lib.fb_sections_2[s][i+1])):
                        member = QtWidgets.QTreeWidgetItem([config_lib.fb_sections_2[s][i+1][j]])
                        group.addChild(member)
                # Prepare font/color format for section title      
                font.setItalic(False)
                font.setBold(True)
                self.addTopLevelItem(section)
                section.setBackground(0, QtGui.QBrush(QtGui.QColor(r, g, b, t)))   
                section.setFont(0, font)
                expanded_flag = config_lib.fb_sections_properties_2[s][5]
                section.setExpanded(expanded_flag)      
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error while loading functional block library')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
            msg.setWindowTitle("Loading error: Functional block library")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
        
    def startDrag(self, dropActions):
        item = self.currentItem()
        if item.childCount() == 0:    
            data = QtCore.QByteArray()
            stream = QtCore.QDataStream(data, QtCore.QIODevice.WriteOnly)
            stream.writeQString(item.text(0))
            mimeData = QtCore.QMimeData()
            mimeData.setData("application/x-item", data)
            drag = QtGui.QDrag(self)
            drag.setMimeData(mimeData) 
            drag.exec()
            
                    
class DesignLayoutView(QtWidgets.QGraphicsView):
    #Framework for viewing all objects in a scene ()
    def __init__(self, scene, parent=None):
        QtWidgets.QGraphicsView.__init__(self, scene, parent)    
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setRenderHint(QtGui.QPainter.TextAntialiasing)
        self.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.setMouseTracking(True)
        self.setAcceptDrops(True)
    
    #=====================================================================================
    #Ability to zoom in/out via mouse wheel
    #Source (accessed 21 Feb 2018):
    #https://github.com/baoboa/pyqt5/blob/master/examples/graphicsview/elasticnodes.py
    def wheelEvent(self, event): #QT specific method
        self.scale_view(np.power(1.2, -event.angleDelta().y() / 240.0))
        
    def scale_view(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()
        window.zoom_value.setText(format(factor*100, '0.1f'))
        if factor < 0.2 or factor > 5: #Zoom factor min/max settings: 20% - 500%
            return
        self.scale(scaleFactor, scaleFactor)
    #=====================================================================================
    
 
class FunctionalBlockDesignView(QtWidgets.QGraphicsRectItem):
    '''The graphical view of the functional building block (pyqt companion class
       of the FunctionalBuildingBlock (data model)). Both are tracked using the
       same dictionary index number.
    ''' 
    def __init__(self, fb_key, name, display_name, display_port_name, fb_geometry,
                 width, height, fb_script, fb_icon_display, fb_icon, fb_icon_x,
                 fb_icon_y, text_size, text_length, text_color, text_bold, text_italic,
                 fb_color, fb_color_2, fb_gradient, fb_border_color, fb_border_style,
                 text_pos_x, text_pos_y, port_label_size, port_label_bold,
                 port_label_italic, port_label_color, parent=None):
        super(FunctionalBlockDesignView, self).__init__(parent)
        
        # Node ID (based on dictionary key)
        self.fb_key = fb_key
        self.name = name
        self.display_name = display_name
        self.display_port_name = display_port_name
        self.fb_geometry = fb_geometry
        self.width = width
        self.height = height    
        self.ports = {}
        self.port_labels = {}
        self.signals = {}
        self.fb_script = fb_script
        self.fb_icon_display = fb_icon_display
        self.fb_icon = fb_icon
        self.fb_icon_x = fb_icon_x
        self.fb_icon_y = fb_icon_y
        self.text_size = text_size
        self.text_length = text_length
        self.text_color = text_color
        self.text_bold = text_bold
        self.text_italic = text_italic
        self.fb_color = fb_color
        self.fb_color_2 = fb_color_2
        self.fb_gradient = fb_gradient
        self.fb_border_color = fb_border_color
        self.fb_border_style = fb_border_style
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        self.port_label_size = port_label_size
        self.port_label_bold = port_label_bold
        self.port_label_italic = port_label_italic
        self.port_label_color = port_label_color       
        self.iterations_parameters = {}
        self.iterations_results = {}
        
        self.fb_error_state = False
        
#        self.gui_instance_key = None
        
        #Version tracking
        self.__version = 1

        if self.fb_gradient == 2:
            start = QtCore.QPointF(int(float(self.width)/2), 0)
            end = QtCore.QPointF(int(float(self.width)/2), int(self.height))
            self.gradient = QtGui.QLinearGradient(start, end)
            self.gradient.setColorAt(0.0, QtGui.QColor(self.fb_color))
            self.gradient.setColorAt(1.0, QtGui.QColor(self.fb_color_2))
            self.setBrush(QtGui.QBrush(self.gradient))
        else:
            self.setBrush(QtGui.QBrush(QtGui.QColor(fb_color)))

        style = set_line_type(self.fb_border_style)
        self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(fb_border_color)), 0.5, style))
        self.setRect(fb_geometry)
        self.setFlags(self.ItemIsSelectable | self.ItemIsMovable)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)

        # Add Label
        self.label = QtWidgets.QGraphicsTextItem(name, self) 
        self.label.setFlag(self.label.ItemIsSelectable, False)

        font = QtGui.QFont('Arial', float(self.text_size))
        if self.text_bold == 2:
            font.setBold(True)
        if self.text_italic == 2:
            font.setItalic(True)
        self.label.setFont(font)        
        self.label.setPos(float(self.text_pos_x), float(self.text_pos_y))
        self.label.setDefaultTextColor(QtGui.QColor(self.text_color))
        self.label.setTextWidth(float(self.text_length))
        if self.display_name == 0:
            self.label.setPlainText('')  
                
        if self.fb_icon_display == 2:
            try:
                icon_name = str('syslab_fb_icons.' + self.fb_icon)
                icon_paint = importlib.import_module(icon_name)
                importlib.reload(icon_paint)
                self.icon_items = icon_paint.run(float(self.fb_icon_x),
                                                     float(self.fb_icon_y)) 
                for i in range(0, len(self.icon_items)):
                    self.icon_items[i].setParentItem(self)
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error loading icon script module for functional block: '
                            + str(self.name))
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
                msg.setWindowTitle("File loading/processing error: Icon image")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                    
    def check_version(self):
        pass #No check needed for version 1
        
    def hoverEnterEvent(self, QMouseEvent):
        pos = self.scenePos()       
#        window.status.setText(str(self.name) + ' (Dimensions(x-y): ' + str(self.width) 
#                              + ' ' + str(self.height) + ' Scene pos(x-y): ' 
#                              + str(format(pos.x(), '0.2f')) + ' ' 
#                              + str(format(pos.y(), '0.2f')) + ')')

        self.setToolTip('FB name: ' + str(self.name) + '\n' 
                        + 'Script: ' + str(self.fb_script) + '\n' 
                        + 'Dimensions(x-y): ' + str(self.width) + '-' + str(self.height) + '\n'
                        + 'Scene pos(x-y): ' + str(format(pos.x(), '0.2f')) + '-' 
                        + str(format(pos.y(), '0.2f')))
        
    def update_ports(self, fb_key):
        #Update positions of port objects. Called when number of ports and/or locations
        #have changed (links are also deleted)
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        #Initialization of parameters for creating ports 
        length_port_list = len(proj.fb_list[fb_key].fb_ports_list)     
        self.ports = {}
        self.port_labels = {}     
        self.n_tot, self.e_tot, self.s_tot, self.w_tot = (
                        self.sum_ports_cardinal_direction(key_index, length_port_list) )
        self.n, self.e, self.s, self.w = 0, 0, 0, 0
        fs = proj.design_settings['sampling_rate']
        
        #Create port object instances (PortsDesignView) and place around
        #contour of functional block view
        for row in range(0, length_port_list):
            #Retrive port data from fb_list (class-FunctionalBlock)           
            port_list = proj.fb_list[fb_key].fb_ports_list
            portID = port_list[row][0]
            portName = port_list[row][1]
            portCardinal = port_list[row][2]
            portDirection = port_list[row][3]
            signalType = port_list[row][4]            
            #Instantiate port object (class-PortsDesignView)
            self.ports[portID] = PortsDesignView(portID, str(portName), portDirection,
                                                 portCardinal, signalType, fb_key,
                                                 self.name, None, ' ', False, self)
            self.ports[portID].setZValue(50)
            
            #Instantiate associated signal object (based on signal type)
            if signalType == 'Electrical':
                self.signals[portID] = signls.SignalAnalogElectrical(portID, signalType,
                                               0, fs, np.array([]), np.array([]),
                                               np.array([]))
            elif signalType == 'Optical': 
                signal_1 = signls.SignalAnalogOptical(1, 193.1, np.array([]), np.array([]),
                                               np.array([]), np.array([]))
                self.signals[portID] = signls.SignalAnalogOpticalCollection(portID, signalType,
                                               fs, np.array([]))
                self.signals[portID].wave_channel_dict[1] = signal_1
                
                #=====================Previous===========================
#                self.signals[portID] = sig.SignalAnalogOptical(portID, signalType,
#                                               1, 193.1, np.array([]), fs, np.array([]),
#                                               np.array([]), np.array([]), np.array([]) )
            elif signalType == 'Digital':
                self.signals[portID] = signls.SignalDigital(portID, signalType, 10e9,
                                               10e9, 1, np.array([]), np.array([]))
                
            elif signalType == 'Analog (1)': #Analog generic (1)
                self.signals[portID] = signls.SignalAnalogGeneric(portID, signalType, fs, 
                                                np.array([]), np.array([]))
                
            elif signalType == 'Analog (2)': #Analog generic (2)
                self.signals[portID] = signls.SignalAnalogGeneric2(portID, signalType, fs, 
                                                np.array([]), np.array([]))   
            else: #Analog generic (3)
                self.signals[portID] = signls.SignalAnalogGeneric3(portID, signalType, fs, 
                                                np.array([]), np.array([]))
                
            #Update position of port object (PortsDesignView)
            if self.display_port_name == 2:
                self.updatePortLabelFont(portID, portName)
            self.set_port_position(portID, portCardinal)
                
    def adjust_ports(self):
        #Port locations and labels (font) are adjusted (links are not deleted)
        tab_index, key_index = retrieve_current_project_key_index()
        current_fb = window.project_scenes_list[key_index].fb_list[self.fb_key]
        length_port_list = len(current_fb.fb_ports_list)
        
        if self.port_labels != {}:
            l = len(self.port_labels)
            for i in range(1, l+1):
                window.project_scenes_list[key_index].removeItem(self.port_labels[i])
                del self.port_labels[i]  
        self.port_labels = {}
        self.n_tot, self.e_tot, self.s_tot, self.w_tot = (
                self.sum_ports_cardinal_direction(key_index, length_port_list) )
        self.n, self.e, self.s, self.w = 0, 0, 0, 0
        for row in range(0, length_port_list):          
            port_list = current_fb.fb_ports_list
            portName = port_list[row][1]
            portCardinal = port_list[row][2]
            portID = port_list[row][0]
            if self.display_port_name == 2:
                self.updatePortLabelFont(portID, portName)
            self.set_port_position(portID, portCardinal)

    def updatePortLabelFont(self, portID, portName):
        self.port_labels[portID] = QtWidgets.QGraphicsTextItem(portName, self) 
        font = QtGui.QFont('Arial', float(self.port_label_size))
        if self.port_label_bold == 2:
            font.setBold(True)
        if self.port_label_italic == 2:
            font.setItalic(True)
        self.port_labels[portID].setFont(font)
        self.port_labels[portID].setDefaultTextColor(QtGui.QColor(self.port_label_color))
        
    def set_port_position(self, portID, portCardinal):
        #Set relative location of port within FB
        if portCardinal == 'North':
            self.n += 1
            x = float(self.width) * (self.n/(self.n_tot+1))
            self.ports[portID].setPos(x,-2.5)
            if self.display_port_name == 2:
                txt_len = self.port_labels[portID].boundingRect().width()
                self.port_labels[portID].setPos(x - (txt_len/2), 0)
        elif portCardinal == 'East':
            self.e += 1
            y = float(self.height) * (self.e/(self.e_tot+1))
            self.ports[portID].setPos(float(self.width)+2.5,y)
            if self.display_port_name == 2:
                txt_len = self.port_labels[portID].boundingRect().width()
                text_height = self.port_labels[portID].boundingRect().height()
                self.port_labels[portID].setPos(float(self.width) - txt_len - 2, y - (float(text_height/2)))
        elif portCardinal == 'South':
            self.s += 1
            x = float(self.width) * (self.s/(self.s_tot+1))
            self.ports[portID].setPos(x,float(self.height)+2.5)
            if self.display_port_name == 2:
                txt_len = self.port_labels[portID].boundingRect().width()
                text_height = self.port_labels[portID].boundingRect().height()
                self.port_labels[portID].setPos(x - (txt_len/2), float(self.height) - float(text_height))
        else:
            self.w += 1
            y = float(self.height) * (self.w/(self.w_tot+1))
            self.ports[portID].setPos(-2.5,y)
            if self.display_port_name == 2:
                text_height = self.port_labels[portID].boundingRect().height()
                self.port_labels[portID].setPos(0, y - (float(text_height/2)))
                
    def sum_ports_cardinal_direction(self, key_index, length_port_list):
        #Calculate total number of ports per cardinal direction (used by set ports method)
        n_tot, e_tot, s_tot, w_tot = 0, 0, 0, 0
        for row in range(0, length_port_list):
            current_fb = window.project_scenes_list[key_index].fb_list[self.fb_key]
            port_list =  current_fb.fb_ports_list
            portCardinal = port_list[row][2]
            
            if portCardinal == 'North':
                n_tot += 1
            elif portCardinal == 'East':
                e_tot += 1
            elif portCardinal == 'South':
                s_tot += 1
            else:
                w_tot += 1
        return n_tot, e_tot, s_tot, w_tot
                
    def access_pull_down_menu(self, mouseEvent): 
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
        
        for item in items:
            if type(item) is FunctionalBlockDesignView:
                break   
                             
        menu = QtWidgets.QMenu()
        txt_action_1 = "Copy/paste this functional block to this project"
        copy_paste_fb_action = menu.addAction(txt_action_1)
        copy_paste_fb_action.setIcon(window.action_copy_paste_icon)
        txt_action_2 = "Copy/paste this functional block to another project"
        copy_export_fb_action = menu.addAction(txt_action_2)
        copy_export_fb_action.setIcon(window.action_copy_paste_proj_icon)
        menu.addSeparator()
        txt_action_3 = "Delete functional block"
        delete_fb_action = menu.addAction(txt_action_3)
        delete_fb_action.setIcon(window.action_delete_icon)
        menu.addSeparator()
        txt_action_4 = "Resize dimensions of functional block"
        update_dim_action = menu.addAction(txt_action_4)
        resize_icon = QtGui.QIcon()
        icon_path_resize = os.path.join(root_path, 'syslab_gui_icons', 'selection-resize.png')
        icon_path_resize = os.path.normpath (icon_path_resize)
        resize_icon.addFile(icon_path_resize)
        update_dim_action.setIcon(resize_icon)      
        action = menu.exec_(mouseEvent.screenPos())
            
        if action == delete_fb_action:                            
            #Delete links that are attached to the functional block
            i = item.fb_key
            self.deleteLinks(i)                       
            #Remove items from fb and fb view dictionaries
            del window.project_scenes_list[key_index].fb_list[i]
            del window.project_scenes_list[key_index].fb_design_view_list[i]                                              
            #Remove and delete item form design layout scene container
            window.project_scenes_list[key_index].removeItem(item)
            del item
            window.tableWidget2.resizeColumnsToContents()
                    
        if action == copy_paste_fb_action:
            self.copy_paste_fb(item, key_index, key_index)
            window.tableWidget2.resizeColumnsToContents()
            
        if action == copy_export_fb_action:
            self.copy_paste_fb_to_another_proj(items, key_index)  
            
        if action == update_dim_action:
            global FB_dim_win
            tab_index, key_index = retrieve_current_project_key_index()      
            items = window.project_scenes_list[key_index].selectedItems()
            FB_dim_win = FunctionalBlockDimensions()
            #Load FB name and dimensions (current)
            fb_width = items[0].width
            fb_height = items[0].height   
            fb_color = items[0].fb_color
            fb_color_2 = items[0].fb_color_2
            
            FB_dim_win.functionalBlock_width.setText(str(fb_width))
            FB_dim_win.functionalBlock_height.setText(str(fb_height))
        
            #Display window
            FB_dim_win.show()
            if FB_dim_win.exec(): #OK selected        
                fb_width = FB_dim_win.functionalBlock_width.text()
                fb_height = FB_dim_win.functionalBlock_height.text()     
                try:
                    items[0].width = float(fb_width)
                    items[0].height = float(fb_height)
                except:
                    e0 = sys.exc_info() [0]
                    e1 = sys.exc_info() [1]
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    syslab_icon = set_icon_window()
                    msg.setWindowIcon(syslab_icon)
                    msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                    msg.setInformativeText(str(e0) + ' ' + str(e1))
                    msg.setInformativeText(str(traceback.format_exc()))
                    msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                    msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                    msg.setWindowTitle("Input field processing error")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                    rtnval = msg.exec()
                    if rtnval == QtWidgets.QMessageBox.Ok:
                        msg.close()
                    #Revert to previous values
                    fb_width = items[0].width
                    fb_height = items[0].height
                
                #Save updated properties to functional block data model     
                fb = window.project_scenes_list[key_index].fb_list[items[0].fb_key]           
                fb.fb_dim.append(float(fb_width))
                fb.fb_dim.append(float(fb_height))                      
                #Update dimensions
                i = items[0].fb_key
                items[0].setRect(0,0,float(fb_width),float(fb_height))
                #Update ports
                window.project_scenes_list[key_index].fb_design_view_list[i].adjust_ports()
                
                #Update fill settings
                if self.fb_gradient == 2:
                    self.gradient = QtGui.QLinearGradient(QtCore.QPointF(int(float(fb_width)/2), 0),
                                                      QtCore.QPointF(int(float(fb_width)/2),
                                                                     int(float(fb_height))))
                    self.gradient.setColorAt(0.0, QtGui.QColor(fb_color))
                    self.gradient.setColorAt(1.0, QtGui.QColor(fb_color_2))
                    self.setBrush(QtGui.QBrush(self.gradient))
                else:
                    self.setBrush(QtGui.QBrush(QtGui.QColor(fb_color)))
            else:
                pass           
                
    def copy_paste_fb_to_another_proj(self, items, start_index):     
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        #Load all open projects into the dialog
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()                       
                for item in items:
                    if type(item) is FunctionalBlockDesignView:
                        self.copy_paste_fb(item, start_index, new_index)
                        
    def copy_paste_fb(self, item, start_index, end_index):        
        j = item.fb_key
        #Set new key for dictionary
        i = 1
        if window.project_scenes_list[end_index].fb_design_view_list:
            while (i in window.project_scenes_list[end_index].fb_design_view_list):
                i += 1               
        #Instantiate new FB data object
        fb_to_copy = window.project_scenes_list[start_index].fb_list[j]
        window.project_scenes_list[end_index].fb_list[i] = models.FunctionalBlock(i,
                                fb_to_copy.fb_name + '_'+ str(i), fb_to_copy.display_name,
                                fb_to_copy.display_port_name, fb_to_copy.fb_geometry,
                                fb_to_copy.fb_dim, fb_to_copy.fb_position, fb_to_copy.fb_script_module,
                                fb_to_copy.fb_icon_display, fb_to_copy.fb_icon, fb_to_copy.fb_icon_x, 
                                fb_to_copy.fb_icon_y, fb_to_copy.fb_parameters_list,
                                fb_to_copy.fb_results_list, fb_to_copy.text_size,
                                fb_to_copy.text_length, fb_to_copy.text_color,
                                fb_to_copy.text_bold, fb_to_copy.text_italic,
                                fb_to_copy.fb_color, fb_to_copy.fb_color_2,
                                fb_to_copy.fb_gradient, fb_to_copy.fb_border_color,
                                fb_to_copy.fb_border_style, fb_to_copy.text_pos_x,
                                fb_to_copy.text_pos_y,  fb_to_copy.port_label_size, 
                                fb_to_copy.port_label_bold, fb_to_copy.port_label_italic,
                                fb_to_copy.port_label_color)
                        
        #Recreate port list
        length_port_list = len(fb_to_copy.fb_ports_list)
        new_port_list = []
        for port in range(0,length_port_list):
            port_val_1 = fb_to_copy.fb_ports_list[port][0]
            port_val_2 = fb_to_copy.fb_ports_list[port][1]
            port_val_3 = fb_to_copy.fb_ports_list[port][2]
            port_val_4 = fb_to_copy.fb_ports_list[port][3]
            port_val_5 = fb_to_copy.fb_ports_list[port][4]
            port_val_6 = fb_to_copy.fb_ports_list[port][5]                          
            port_val_7 = fb_to_copy.fb_ports_list[port][6]
            port_entry = [port_val_1, port_val_2, port_val_3, port_val_4,
                                     port_val_5, port_val_6, port_val_7]
            new_port_list.append(port_entry)              
        window.project_scenes_list[end_index].fb_list[i].fb_ports_list = new_port_list
                        
        # Recreate parameter list=========================================================
        length_parameter_list = len(fb_to_copy.fb_parameters_list)
        new_par_list = []
        for par in range(0, length_parameter_list):
            par_val_1 = fb_to_copy.fb_parameters_list[par][0]
            par_val_2 = fb_to_copy.fb_parameters_list[par][1]
            par_val_3 = fb_to_copy.fb_parameters_list[par][2]
            par_val_4 = fb_to_copy.fb_parameters_list[par][3]
            par_val_5 = fb_to_copy.fb_parameters_list[par][4]
            par_val_6 = fb_to_copy.fb_parameters_list[par][5]
            par_entry = [par_val_1, par_val_2, par_val_3, par_val_4, par_val_5, par_val_6]
            new_par_list.append(par_entry)              
        window.project_scenes_list[end_index].fb_list[i].fb_parameters_list = new_par_list
                        
        #Instantiate new design view object===============================================
        window.project_scenes_list[end_index].fb_design_view_list[i] = (
                        FunctionalBlockDesignView(i, item.name + '_'+ str(i),
                                                  item.display_name, item.display_port_name,
                                                  item.fb_geometry, item.width, item.height,
                                                  item.fb_script, item.fb_icon_display,
                                                  item.fb_icon, item.fb_icon_x,
                                                  item.fb_icon_y, item.text_size,
                                                  item.text_length, item.text_color,
                                                  item.text_bold, item.text_italic,
                                                  item.fb_color, item.fb_color_2,
                                                  item.fb_gradient, item.fb_border_color,
                                                  item.fb_border_style, item.text_pos_x,
                                                  item.text_pos_y, item.port_label_size,
                                                  item.port_label_bold, item.port_label_italic,
                                                  item.port_label_color) )

        #Add new FB design view to QGraphicsScene
        new_fb_view_copy = window.project_scenes_list[end_index].fb_design_view_list[i]
        new_fb_view_copy.update_ports(i)
        if end_index == start_index:
            new_fb_view_copy.setPos(item.scenePos().x() + 20, item.scenePos().y() + 20)
        else:
            new_fb_view_copy.setPos(item.scenePos().x(), item.scenePos().y())
        new_fb_view_copy.setRect(0, 0, float(item.width), float(item.height)) 
        window.project_scenes_list[end_index].addItem(new_fb_view_copy)
        item.setSelected(False)
        new_fb_view_copy.setSelected(True)        

    #Double left mouse click opens the GUI panel for defining and/or modifying
    #the functional block's properties      
    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()      
        items = window.project_scenes_list[key_index].selectedItems()
        
        global FB_win
        FB_win = FunctionalBlockGUI()
        
        #Load FB name and dimensions (current)
        fb_key = items[0].fb_key
        fb_view_name = items[0].name
        fb_display_name = items[0].display_name
        fb_display_port_name = items[0].display_port_name
        fb_width = items[0].width
        fb_height = items[0].height
        fb_script = items[0].fb_script
        fb_icon_display_open = items[0].fb_icon_display
        fb_icon = items[0].fb_icon
        fb_icon_x = items[0].fb_icon_x
        fb_icon_y = items[0].fb_icon_y
        text_size = items[0].text_size
        text_length = items[0].text_length
        text_color = items[0].text_color
        text_bold = items[0].text_bold     
        text_italic= items[0].text_italic
        fb_color = items[0].fb_color
        fb_color_2 = items[0].fb_color_2
        fb_gradient = items[0].fb_gradient
        fb_border_color = items[0].fb_border_color
        fb_border_style = items[0].fb_border_style
        fb_name_pos_x = items[0].text_pos_x
        fb_name_pos_y = items[0].text_pos_y
        fb_port_label_size = items[0].port_label_size
        fb_port_label_bold = items[0].port_label_bold
        fb_port_label_italic = items[0].port_label_italic
        fb_port_label_color = items[0].port_label_color
            
        FB_win.functionalBlockID.setText(str(fb_key))
        FB_win.functionalBlockName.setText(fb_view_name)
        FB_win.checkBoxName.setCheckState(fb_display_name)
        FB_win.portDisplayCheckBox.setCheckState(fb_display_port_name)
        FB_win.functionalBlock_width.setText(str(fb_width))
        FB_win.functionalBlock_height.setText(str(fb_height))
        FB_win.functionalBlockScript.setText(fb_script)
        FB_win.checkBoxIcon.setCheckState(fb_icon_display_open)
        FB_win.functionalBlockIcon.setText(fb_icon)
        FB_win.functionalBlockIconX.setText(str(fb_icon_x))
        FB_win.functionalBlockIconY.setText(str(fb_icon_y))
        FB_win.textFontSize.setText(str(text_size))
        FB_win.nameLength.setText(str(text_length))
        FB_win.fontColor.setText(text_color)
        FB_win.checkBoxBold.setCheckState(text_bold)
        FB_win.checkBoxItalic.setCheckState(text_italic)
        FB_win.fillColor.setText(fb_color)
        FB_win.fillColor2.setText(fb_color_2)
        FB_win.checkBoxGradient.setCheckState(fb_gradient)
        FB_win.borderColor.setText(fb_border_color)
        FB_win.dataComboBoxBorder.setCurrentText(fb_border_style)
        FB_win.namePosX.setText(str(fb_name_pos_x))
        FB_win.namePosY.setText(str(fb_name_pos_y))
        
        FB_win.portLabelFontSize.setText(str(fb_port_label_size))
        FB_win.fontColorPortLabel.setText(fb_port_label_color)
        FB_win.checkBoxBoldPortLabel.setCheckState(fb_port_label_bold)
        FB_win.checkBoxItalicPortLabel.setCheckState(fb_port_label_italic)
        
        #Display window
        FB_win.show()
        if FB_win.exec(): #OK selected       
            #If name/dimensions/scripts are updated, capture/rename associated objects
            fb_view_new_name = FB_win.functionalBlockName.text()
            fb_display_new_name = FB_win.checkBoxName.checkState()
            fb_display_new_port_name = FB_win.portDisplayCheckBox.checkState()
            fb_width = FB_win.functionalBlock_width.text()
            fb_height = FB_win.functionalBlock_height.text()
            fb_script_module = FB_win.functionalBlockScript.text()
            fb_icon_display = FB_win.checkBoxIcon.checkState()
            fb_icon = FB_win.functionalBlockIcon.text()
            fb_icon_x = FB_win.functionalBlockIconX.text()
            fb_icon_y = FB_win.functionalBlockIconY.text()
            text_size = FB_win.textFontSize.text()
            text_length = FB_win.nameLength.text()
            text_color = FB_win.fontColor.text()
            text_bold = FB_win.checkBoxBold.checkState()
            text_italic = FB_win.checkBoxItalic.checkState()
            fb_fill_color = FB_win.fillColor.text()
            fb_fill_color_2 = FB_win.fillColor2.text()
            fb_gradient = FB_win.checkBoxGradient.checkState()
            fb_border_color = FB_win.borderColor.text()
            fb_border_style = FB_win.dataComboBoxBorder.currentText()
            name_pos_x = FB_win.namePosX.text()
            name_pos_y = FB_win.namePosY.text()            
            fb_port_label_size = FB_win.portLabelFontSize.text()
            fb_port_label_color = FB_win.fontColorPortLabel.text()
            fb_port_label_bold = FB_win.checkBoxBoldPortLabel.checkState()
            fb_port_label_italic = FB_win.checkBoxItalicPortLabel.checkState()
            
            rebuild_fb_view = False          
            if FB_win.update_ports_decision == True:
                rebuild_fb_view = True   
            try:
                items[0].name = fb_view_new_name
                items[0].display_name = fb_display_new_name
                items[0].display_port_name = fb_display_new_port_name
                items[0].width = float(fb_width)
                items[0].height = float(fb_height)
                items[0].fb_script = fb_script_module
                items[0].fb_icon_display = fb_icon_display
                items[0].fb_icon = fb_icon
                items[0].fb_icon_x = float(fb_icon_x)
                items[0].fb_icon_y = float(fb_icon_y)
                items[0].text_size = float(text_size)
                items[0].text_length = float(text_length)
                items[0].text_color = text_color
                items[0].text_bold = text_bold   
                items[0].text_italic = text_italic
                items[0].fb_color = fb_fill_color
                items[0].fb_color_2 = fb_fill_color_2
                items[0].fb_gradient = fb_gradient
                items[0].fb_border_color = fb_border_color
                items[0].fb_border_style = fb_border_style
                items[0].text_pos_x = float(name_pos_x)
                items[0].text_pos_y = float(name_pos_y)                
                items[0].port_label_size = float(fb_port_label_size)
                items[0].port_label_bold = fb_port_label_bold
                items[0].port_label_italic = fb_port_label_italic
                items[0].port_label_color = fb_port_label_color
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                msg.setWindowTitle("Input field processing error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                #Revert to previous values
                fb_key = items[0].fb_key
                fb_view_name = items[0].name
                fb_display_name = items[0].display_name
                fb_display_port_name = items[0].display_port_name
                fb_width = items[0].width
                fb_height = items[0].height
                fb_script = items[0].fb_script
                fb_icon_display_open = items[0].fb_icon_display
                fb_icon = items[0].fb_icon
                fb_icon_x = items[0].fb_icon_x
                fb_icon_y = items[0].fb_icon_y
                text_size = items[0].text_size
                text_length = items[0].text_length
                text_color = items[0].text_color
                text_bold = items[0].text_bold     
                text_italic= items[0].text_italic
                fb_color = items[0].fb_color
                fb_color_2 = items[0].fb_color_2
                fb_gradient = items[0].fb_gradient
                fb_border_color = items[0].fb_border_color
                fb_border_style = items[0].fb_border_style
                fb_name_pos_x = items[0].text_pos_x
                fb_name_pos_y = items[0].text_pos_y
                fb_port_label_size = items[0].port_label_size
                fb_port_label_bold = items[0].port_label_bold
                fb_port_label_italic = items[0].port_label_italic
                fb_port_label_color = items[0].port_label_color
            #Save updated properties to functional block data model     
            fb = window.project_scenes_list[key_index].fb_list[items[0].fb_key]           
            fb.fb_name = fb_view_new_name
            fb.display_name = fb_display_new_name
            fb.display_port_name = fb_display_new_port_name
            fb.fb_script_module = fb_script_module
            fb.fb_icon_display = fb_icon_display
            fb.fb_icon = fb_icon
            fb.fb_icon_x = fb_icon_x
            fb.fb_icon_y = fb_icon_y
            fb.text_size = text_size
            fb.text_length = text_length
            fb.text_color = text_color
            fb.text_bold = int(text_bold)
            fb.text_italic = int(text_italic)
            fb.fb_color = fb_fill_color
            fb.fb_color_2 = fb_fill_color_2
            fb.fb_gradient = fb_gradient
            fb.fb_border_color = fb_border_color
            fb.fb_border_style = fb_border_style
            fb.text_pos_x = name_pos_x
            fb.text_pos_y = name_pos_y
            fb.fb_dim.append(float(fb_width))
            fb.fb_dim.append(float(fb_height))           
            fb.port_label_size = fb_port_label_size
            fb.port_label_color = fb_port_label_color
            fb.port_label_bold = int(fb_port_label_bold)
            fb.port_label_italic = int(fb_port_label_italic)            
            #Save position and geometry information
            i = items[0].fb_key
            items[0].setRect(0,0,float(fb_width),float(fb_height))
            geometry = items[0].rect()
            position = items[0].pos()
            
            #Save parameters list
            self.save_parameters_list(fb)
            
            #Update label associated with FB design view
            self.label.setPlainText(fb_view_new_name)
            self.label.setPos(float(name_pos_x), float(name_pos_y))
            self.label.setTextWidth(float(text_length))
            font = QtGui.QFont('Arial', float(text_size))
            if self.text_bold == 2:
                font.setBold(True)
            if self.text_italic == 2:
                font.setItalic(True)
            self.label.setFont(font)        
            self.label.setDefaultTextColor(QtGui.QColor(text_color))
                
            if fb_display_new_name == 0:
                self.label.setPlainText('')
            
            #Update fill settings
            if self.fb_gradient == 2:
                self.gradient = QtGui.QLinearGradient(QtCore.QPointF(int(float(fb_width)/2), 0),
                                                      QtCore.QPointF(int(float(fb_width)/2),
                                                                     int(float(fb_height))))
                self.gradient.setColorAt(0.0, QtGui.QColor(fb_fill_color))
                self.gradient.setColorAt(1.0, QtGui.QColor(fb_fill_color_2))
                self.setBrush(QtGui.QBrush(self.gradient))
            else:
                self.setBrush(QtGui.QBrush(QtGui.QColor(fb_fill_color)))
            
            #Updated border settings
            style = set_line_type(fb_border_style)
            self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(fb_border_color)), 0.5, style))
            
            #Rebuild all ports if changes have been made to port settings
            if rebuild_fb_view == True:
                self.deleteLinks(i)
                #Rebuild instance of GraphicsRectItem (class FunctionalBlockDesignView)
                window.project_scenes_list[key_index].removeItem(items[0])
                del items[0]
                window.project_scenes_list[key_index].fb_design_view_list[i] = (
                        FunctionalBlockDesignView(i, fb_view_new_name, fb_display_new_name, 
                                        fb_display_new_port_name, geometry, fb_width,
                                        fb_height, fb_script_module, fb_icon_display, 
                                        fb_icon, fb_icon_x, fb_icon_y, text_size,
                                        text_length, text_color, text_bold, text_italic,
                                        fb_color, fb_color_2, fb_gradient, fb_border_color,
                                        fb_border_style, name_pos_x, name_pos_y, 
                                        fb_port_label_size, fb_port_label_bold,
                                        fb_port_label_italic, fb_port_label_color) )
    
                window.project_scenes_list[key_index].fb_design_view_list[i].update_ports(i)
                window.project_scenes_list[key_index].fb_design_view_list[i].setPos(position)        
                window.project_scenes_list[key_index].addItem(window.project_scenes_list[key_index].fb_design_view_list[i])
            else:
                window.project_scenes_list[key_index].fb_design_view_list[i].adjust_ports()
            
            #Update icon
            #Check if attribute icon alread exists and delete
            if hasattr(self, 'icon_items'):
                l = len(self.icon_items)
                for i in range(0, l):
                    window.project_scenes_list[key_index].removeItem(self.icon_items[i])
            
            #Create icon
            if self.fb_icon_display == 2:
                try:
                    icon_name = str('syslab_fb_icons.' + self.fb_icon)
                    icon_paint = importlib.import_module(icon_name)
                    importlib.reload(icon_paint)
                    self.icon_items = icon_paint.run(float(self.fb_icon_x),
                                                     float(self.fb_icon_y)) 
                    for i in range(0, len(self.icon_items)):
                        self.icon_items[i].setParentItem(self)
                except:
                    e0 = sys.exc_info() [0]
                    e1 = sys.exc_info() [1]
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    syslab_icon = set_icon_window()
                    msg.setWindowIcon(syslab_icon)
                    msg.setText('Error loading icon script module for functional block: '
                                 + str(self.name))
                    msg.setInformativeText(str(e0) + ' ' + str(e1))
                    msg.setInformativeText(str(traceback.format_exc()))
                    msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                    msg.setStyleSheet("QLabel{width: 500px; min-width: 500px; max-width: 500px;}")
                    msg.setWindowTitle("File loading/processing error: Icon image")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                    rtnval = msg.exec()
                    if rtnval == QtWidgets.QMessageBox.Ok:
                        msg.close()
                        
        else: #Cancel selected
            #Reset colors to original values (before opening GUI)
            fb_color = items[0].fb_color
            fb_color_2 = items[0].fb_color_2
            fb_border_color = items[0].fb_border_color
            text_color = items[0].text_color
            fb_port_label_color = items[0].port_label_color
            fb_gradient = items[0].fb_gradient
            w = items[0].width
            h = items[0].height
            
            if fb_gradient == 2:
                self.gradient = QtGui.QLinearGradient(QtCore.QPointF(int(float(w)/2), 0), 
                                                      QtCore.QPointF(int(float(w)/2), int(h)))
                self.gradient.setColorAt(0.0, QtGui.QColor(fb_color))
                self.gradient.setColorAt(1.0, QtGui.QColor(fb_color_2))
                self.setBrush(QtGui.QBrush(self.gradient))
            else:
                self.setBrush(QtGui.QBrush(QtGui.QColor(fb_color)))
            self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(fb_border_color)), 0.5 ))
            
    def save_parameters_list(self, fb):
        fb.fb_parameters_list.clear()
        row = 0
        while (FB_win.parametersTable.item(row, 0) is not None):
            parType = 'standard'
            parName = FB_win.parametersTable.item(row, 0).text()
            if type(FB_win.parametersTable.cellWidget(row, 1)) is QtWidgets.QCheckBox:
                parValue = str(FB_win.parametersTable.cellWidget(row, 1).checkState())
                parType = 'check_box'
                FB_win.parametersTable.removeCellWidget(row, 1)                   
            elif type(FB_win.parametersTable.cellWidget(row, 1)) is QtWidgets.QComboBox:
                parValue = str(FB_win.parametersTable.cellWidget(row, 1).currentText())
                parType = 'list'
                FB_win.parametersTable.removeCellWidget(row, 1)                                        
            elif FB_win.parametersTable.item(row, 1) is not None:
                parValue = FB_win.parametersTable.item(row, 1).text()
            else: 
                parValue = None
                
            if FB_win.parametersTable.item(row, 2) is not None:
                parUnit = FB_win.parametersTable.item(row, 2).text()
            else: 
                parUnit = None
                
            if FB_win.parametersTable.item(row, 3) is not None:
                parNotes = FB_win.parametersTable.item(row, 3).text()
            else: 
                parNotes = None
                
            if FB_win.parametersTable.columnSpan(row, 0) > 1:
                header = True
            else:
                header = False
                
            parameter_entry = [parName, parValue, parUnit, parNotes, header, parType]
            fb.fb_parameters_list.append(parameter_entry)
            row += 1
                           
    def deleteLinks(self, fb_key):
        tab_index, key_index = retrieve_current_project_key_index()
        items = window.project_scenes_list[key_index].items()  
        #Delete links that are connected into FB
        for l in range(1,len(self.ports)+1):
            if self.ports[l].link_key is not None:
                link_key = self.ports[l].link_key
                
                for line_item in items:
                    if type(line_item) is set_link.LinksDesignPathView:
                        if line_item.link_key == link_key:
                            fb_start_key = line_item.fromPort_fb_key
                            fb_start_portID = line_item.fromPort_portID
                            fb_end_key = line_item.toPort_fb_key
                            fb_end_portID = line_item.toPort_portID
                            fb_start = window.project_scenes_list[key_index].fb_design_view_list[fb_start_key]
                            fb_end = window.project_scenes_list[key_index].fb_design_view_list[fb_end_key]
                            fb_start.ports[fb_start_portID].link_key = None
                            fb_start.ports[fb_start_portID].link_name = None
                            fb_start.ports[fb_start_portID].connected = False
                            fb_end.ports[fb_end_portID].link_key = None
                            fb_end.ports[fb_end_portID].link_name = None
                            fb_end.ports[fb_end_portID].connected = False        
                            window.project_scenes_list[key_index].removeItem(line_item)
                            del line_item
                            del window.project_scenes_list[key_index].signal_links_list[link_key]
                            
    def deleteLink(self, portID): #FOR LATER USE
        tab_index, key_index = retrieve_current_project_key_index()
        items = window.project_scenes_list[key_index].items()  
        #Delete link that is connected to port (if applicable)
        if self.ports[portID].link_key is not None:
                link_key = self.ports[portID].link_key
                
                for line_item in items:
                    if type(line_item) is set_link.LinksDesignPathView:
                        if line_item.link_key == link_key:
                            fb_start_key = line_item.fromPort_fb_key
                            fb_start_portID = line_item.fromPort_portID
                            fb_end_key = line_item.toPort_fb_key
                            fb_end_portID = line_item.toPort_portID
                            fb_start = window.project_scenes_list[key_index].fb_design_view_list[fb_start_key]
                            fb_end = window.project_scenes_list[key_index].fb_design_view_list[fb_end_key]
                            fb_start.ports[fb_start_portID].link_key = None
                            fb_start.ports[fb_start_portID].link_name = None
                            fb_start.ports[fb_start_portID].connected = False
                            fb_end.ports[fb_end_portID].link_key = None
                            fb_end.ports[fb_end_portID].link_name = None
                            fb_end.ports[fb_end_portID].connected = False        
                            window.project_scenes_list[key_index].removeItem(line_item)
                            del line_item
                            del window.project_scenes_list[key_index].signal_links_list[link_key]
                            
        
class PortsDesignView(QtWidgets.QGraphicsRectItem):
    '''Represents a port instance that is attached to a functional block
    
    Sections of code design below (itemChange, mousePressEvent,
    based on 'DiagramEditorProto.py' (class connection, 
    diagramEditor, diagramScene)
    Author first name: Windel - many thanks to the author!
    Copy of original code is located at the end of module systemlab_set_link.py - 
    Source - Creating a diagram editor,
    http://www.windel.nl/?section=pyqtdiagrameditor (downloaded 11 Feb 2018)
    '''
    def __init__(self, portID, port_name, port_direction, port_cardinal, signal_type,
                fb_key, fb_name, link_key, link_name, connected, parent=None):
        QtWidgets.QGraphicsRectItem.__init__(self, QtCore.QRectF(-2.5,-2.5,5.0,5.0), parent)
        self.portID = portID
        self.port_name = port_name
        self.port_direction = port_direction
        self.port_cardinal = port_cardinal
        self.signal_type = signal_type
        self.fb_key = fb_key
        self.fb_name = fb_name
        self.link_key = link_key
        self.link_name = link_name
        self.connected = connected
        self.posCallbacks = []
        self.iterations_input_signals = {}
        self.iterations_return_signals = {}   
        self.setFlag(self.ItemSendsScenePositionChanges, True)
        self.setAcceptHoverEvents(True)
           
        #Version tracking
        self.__version = 1
       
        # Rect(Port) properties:
        self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.pen_width = 0.5
        color_brush = QtCore.Qt.white
        if self.signal_type == 'Electrical':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.blue
            color_pen = QtCore.Qt.blue
            self.set_port_colors(color_brush, color_pen, self.pen_width)
        elif self.signal_type == 'Optical':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.darkRed
            color_pen = QtCore.Qt.darkRed
            self.set_port_colors(color_brush, color_pen, self.pen_width)
        elif self.signal_type == 'Digital':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.darkGray
            color_pen = QtCore.Qt.darkGray
            self.set_port_colors(color_brush, color_pen, self.pen_width)
        elif self.signal_type == 'Analog (1)':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.darkGreen
            color_pen = QtCore.Qt.darkGreen
            self.set_port_colors(color_brush, color_pen, self.pen_width)  
        elif self.signal_type == 'Analog (2)':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.magenta
            color_pen = QtCore.Qt.magenta
            self.set_port_colors(color_brush, color_pen, self.pen_width)
        elif self.signal_type == 'Analog (3)':
            if self.port_direction == 'Out':
                color_brush = QtCore.Qt.cyan
            color_pen = QtCore.Qt.cyan
            self.set_port_colors(color_brush, color_pen, self.pen_width)
        else: #Disabled
            color_brush = QtCore.Qt.white
            color_pen = QtCore.Qt.gray
            self.set_port_colors(color_brush, color_pen, self.pen_width)
           
    def check_version(self):
        pass #No check needed for version 1
       
    def set_port_colors(self, color_brush, color_pen, width):
        self.setBrush(QtGui.QBrush(color_brush))
        self.setPen(QtGui.QPen(QtGui.QBrush(color_pen), width ))
    
    def hoverEnterEvent(self, QMouseEvent):
        pos = self.pos()       
#        window.status.setText('Port ID: ' + str(self.portID) + ' (Pos(x/y): '
#                              + str(format(pos.x(), '0.2f')) + ' ' 
#                              + str(format(pos.y(), '0.2f')) + ')')
        self.setToolTip('Port ID: ' + str(self.portID) + '\n'
                        + 'Port name: ' + str(self.port_name) + '\n'
                        + 'Dir: ' + str(self.port_direction) + '\n'
                        + 'Sig type: ' + str(self.signal_type) + '\n'
                        + 'Pos(x/y): ' + str(format(pos.x(), '0.2f')) + ' '
                        + str(format(pos.y(), '0.2f')))
      
    def itemChange(self, change, value):
        if change == self.ItemScenePositionHasChanged and self.connected == True:
            for cb in self.posCallbacks:
                cb(value)
            return value
        return super(PortsDesignView, self).itemChange(change, value)
   
    #Initiation of connection attempt from a port (left click event over port)
    def mousePressEvent(self, event): #QT specific method
        if self.port_direction == 'Out' and self.connected == False:
            window.start_link(self)
        else:
            pass

    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(QMouseEvent.scenePos())
        sim_settings = proj.design_settings
        for item in items:
            if type(item) is PortsDesignView:
                #Retrieve port attributes & signal data
                portID = item.portID
                port_name = item.port_name
                fb_key = item.fb_key
                fb_name = item.fb_name
                sig = item.signal_type
                direction = item.port_direction
              
                fb = proj.fb_design_view_list[fb_key]
                t = fb.signals[portID].time_array
              
                if t.size > 0: #Port has data to view
                   #Create instance of port data view list
                    i = 1
                    while (i in proj.data_port_view_list):
                        i += 1
                    if sig == 'Electrical':
                        if direction == 'In' or direction == 'In-Feedback':
                            signal_data = fb.ports[portID].iterations_input_signals
                        else:
                            signal_data = fb.ports[portID].iterations_return_signals
                        proj.data_port_view_list[i] = (
                              port_electrical.ElectricalPortDataAnalyzer(signal_data, fb_name,
                                                                         port_name, direction,
                                                                         sim_settings) )
                        proj.data_port_view_list[i].show()
                        
                    elif sig == 'Optical':
                        if direction == 'In' or direction == 'In-Feedback':
                            signal_data = fb.ports[portID].iterations_input_signals
                        else:
                            signal_data = fb.ports[portID].iterations_return_signals       
                        proj.data_port_view_list[i] = (
                              port_optical.OpticalPortDataAnalyzer(signal_data, fb_name,
                                                                   port_name, direction,
                                                                   sim_settings) )
                        proj.data_port_view_list[i].show()
                        
                    elif sig == 'Digital':
                        if direction == 'In' or direction == 'In-Feedback':
                            signal_data = fb.ports[portID].iterations_input_signals
                        else:
                            signal_data = fb.ports[portID].iterations_return_signals
                        proj.data_port_view_list[i] = (
                              port_digital.DigitalPortDataAnalyzer(signal_data, fb_name,
                                                                   port_name, direction,
                                                                   sim_settings) )
                        proj.data_port_view_list[i].show()
                        
                    else:
                        if direction == 'In' or direction == 'In-Feedback':
                            signal_data = fb.ports[portID].iterations_input_signals
                        else:
                            signal_data = fb.ports[portID].iterations_return_signals
                        proj.data_port_view_list[i] = (
                              port_analog.AnalogPortDataAnalyzer(signal_data, fb_name,
                                                                   port_name, direction,
                                                                   sim_settings) )                                         
                        proj.data_port_view_list[i].show()
                else:
                    msg = QtWidgets.QMessageBox()
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setText('No port data is available for viewing')
                    msg.setInformativeText('See help button for further information')
                    msg.setWindowTitle("Port data view dialog")
                    msg.setStyleSheet("QLabel{height: 70px; min-height: 70px; max-height: 70px;}")
                    msg.setStyleSheet("QLabel{width: 200px; min-width: 200px; max-width: 200px;}")
                    msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    rtnval = msg.exec()
                    if rtnval == QtWidgets.QMessageBox.Ok:
                        msg.close()  
                        
         
class DataBoxDesignView(QtWidgets.QGraphicsRectItem):
    #Data attributes
    def __init__(self, data_key, title_text, title_geometry, title_width, title_height, 
                 title_box_color, title_box_opacity, title_border_color, title_text_width,
                 title_text_size, title_text_color, title_text_bold, title_text_italic,
                 title_border_style, title_border_width, title_text_pos_x, title_text_pos_y, 
                 data_box_geometry, data_box_width, data_box_height, data_box_color, 
                 data_box_opacity, data_box_gradient, data_border_color, data_box_border_style,
                 data_box_border_width, data_text_size, data_width, value_width,
                 data_text_pos_x, data_text_pos_y, data_source_file, parent=None):
        super(DataBoxDesignView, self).__init__(parent)
        #Title box settings
        self.data_key = data_key
        self.title_text = title_text
        self.title_geometry = title_geometry
        self.title_width = title_width
        self.title_height = title_height    
        self.title_box_color = title_box_color
        self.title_box_opacity = title_box_opacity
        self.title_border_color = title_border_color
        self.title_text_width = title_text_width
        self.title_text_size = title_text_size
        self.title_text_color = title_text_color
        self.title_text_bold = title_text_bold
        self.title_text_italic = title_text_italic
        self.title_border_style = title_border_style
        self.title_border_width = title_border_width
        self.title_text_pos_x = title_text_pos_x
        self.title_text_pos_y = title_text_pos_y   
        #Data box/field settings
        self.data_box_geometry = data_box_geometry
        self.data_box_width = data_box_width
        self.data_box_height = data_box_height    
        self.data_box_color = data_box_color
        self.data_box_opacity = data_box_opacity
        self.data_box_gradient = data_box_gradient
        self.data_border_color = data_border_color
        self.data_box_border_style = data_box_border_style
        self.data_box_border_width = data_box_border_width
        self.data_text_size = data_text_size
        self.data_width = data_width
        self.value_width = value_width
        self.data_text_pos_x = data_text_pos_x
        self.data_text_pos_y = data_text_pos_y
        #Source file (dictionary for importing data fields)
        self.data_source_file = data_source_file  
        #Version tracking
        self.__version = 1
        #=================================================================================
        
        #Setup title box color, border, etc.
        if self.data_box_gradient == 2:
            self.title_box = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0,0,
                                float(self.title_width),float(self.title_height)),self)
            style = set_line_type(self.title_border_style)
            self.title_box.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(self.title_border_color)),
                                         float(self.title_border_width), style ))
            self.title_box.setPos(0, -float(self.title_height))
            
            #Setup title box text color, font, etc.
            self.text = QtWidgets.QGraphicsTextItem(self.title_text, self.title_box)
            font = QtGui.QFont('Arial', float(self.title_text_size))
            if self.title_text_bold == 2:
                font.setBold(True)
            if self.title_text_italic == 2:
                font.setItalic(True)
            self.text.setFont(font)
            self.text.setPos(float(self.title_text_pos_x), float(self.title_text_pos_y))
            self.text.setTextWidth(float(self.title_text_width))
            self.text.setDefaultTextColor(QtGui.QColor(self.title_text_color))
            self.title_box.setBrush(QtGui.QBrush(QtGui.QColor(self.title_box_color)))

        #Setup data box color, border, etc.       
        self.setBrush(QtGui.QBrush(QtGui.QColor(self.data_box_color)))
        style = set_line_type(self.data_box_border_style)
        self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(self.data_border_color)),
                               float(self.data_box_border_width), style ))
        self.setRect(self.data_box_geometry)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable)
        self.setZValue(50.0)

        #Read in data file and create data fields
        tab_index, key_index = retrieve_current_project_key_index()      
        iteration = window.project_scenes_list[key_index].design_settings['current_iteration']

        #Set data file #
        data_ID = self.data_source_file     
        self.data_dict = {}
        self.data_table_iteration = []
         
        #Load information into data table
        if data_ID != '':
            try:
                data_dict = config_data_panel.data_box_dict[data_ID]
            except:
#                e0 = sys.exc_info() [0]
#                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('The data source file name set for this data panel (' 
                            + str(data_ID) + ') does not match \nany data panel name keys'
                            + ' specified in config_data_panels.py.\n'
                            + 'To access and display data during a simulation, matching'
                            + ' file names\nmust be specified.')
#                msg.setInformativeText(str(e0) + ' ' + str(e1))
#                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 75px; min-height: 75px; max-height: 75px;}")
                msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
                msg.setWindowTitle("Incompatible file name key for data panel: "
                                   + self.title_text)
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                data_dict = {}
               
            if len(data_dict) >= iteration:
                data_table_iteration = data_dict[iteration]
                for data in range(0, len(data_table_iteration)):
                    
                    # Name field==========================================================
                    self.data_name = QtWidgets.QGraphicsTextItem(data_table_iteration[data][0], self)                    
                    color_name = '#000000' #Default black color for name field
                    if len(data_table_iteration[data]) > 4:
                        color_name = data_table_iteration[data][4] #Use defined setting
                    self.data_name.setDefaultTextColor(QtGui.QColor(color_name))                    
                    name_font = QtGui.QFont('Arial', float(self.data_text_size))
                    name_font.setBold(True)
                    self.data_name.setFont(name_font)
                    x = float(self.data_text_pos_x)
                    y = ( float(self.data_text_pos_y) 
                            + (float(self.data_text_size)*data) + data*5 )
                    self.data_name.setPos(x, y)                    
                    
                    # Value field=========================================================
                    data_val = str(format(data_table_iteration[data][1],
                                       str(data_table_iteration[data][2])))
                    self.data_value = QtWidgets.QGraphicsTextItem(data_val, self)
                    value_font = QtGui.QFont('Arial', float(self.data_text_size))
                    
                    color_value = '#aa0000' #Default red color for name and unit fields
                    if len(data_table_iteration[data]) > 5:
                        color_value = data_table_iteration[data][5] #Use defined setting
                    self.data_value.setDefaultTextColor(QtGui.QColor(color_value))                                    
                    self.data_value.setFont(value_font)
                    self.data_value.setPos(x + float(self.data_width) + 15, y)
                    
                    # Units field=========================================================
                    self.data_units = QtWidgets.QGraphicsTextItem(data_table_iteration[data][3], self)
                    unit_font = QtGui.QFont('Arial', float(self.data_text_size))
                    unit_font.setItalic(True)
                    self.data_units.setDefaultTextColor(QtGui.QColor(color_value))
                    self.data_units.setFont(unit_font)
                    self.data_units.setPos(x + (float(self.data_width)
                                       + float(self.value_width) + 15), y)   
                                                
    def check_version(self):
        pass #No check needed for version 1
        
    def access_pull_down_menu(self, mouseEvent):                                 
        menu = QtWidgets.QMenu()
        copy_box_action = menu.addAction("Copy/paste data panel")
        copy_box_action.setIcon(window.action_copy_paste_icon)
        copy_export_box_action = menu.addAction("Copy/paste data panel to another project")
        copy_export_box_action.setIcon(window.action_copy_paste_proj_icon)
        menu.addSeparator()
        delete_box_action = menu.addAction("Delete data panel")
        delete_box_action.setIcon(window.action_delete_icon)
        action = menu.exec_(mouseEvent.screenPos())
        
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
                    
        if action == copy_box_action:   
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())    
            for item in items:
                if type(item) is DataBoxDesignView:
                    self.copy_paste_data_box(item, key_index, key_index)
                    
        if action == copy_export_box_action:   
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())    
            self.copy_paste_data_box_to_another_proj(items, key_index)         
                    
        if action == delete_box_action:
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())                 
            for item in items:
                if type(item) is DataBoxDesignView:                                            
                    #Remove items from data_box and data_box_design_view dictionaries
                    i = item.data_key
                    del proj.data_box_list[i]
                    del proj.data_box_design_view_list[i]                                              
                    #Remove and delete item form design layout scene container
                    proj.removeItem(item)
                    del item
                    break 
                    
    def copy_paste_data_box_to_another_proj(self, items, start_index):     
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()                       
                for item in items:
                    if type(item) is DataBoxDesignView:
                        self.copy_paste_data_box(item, start_index, new_index)
            
    def copy_paste_data_box(self, item, start_index, end_index):
        proj = window.project_scenes_list[end_index]
        i = set_new_key(proj.data_box_design_view_list)                      
        t_text = item.title_text
        t_geometry = item.title_geometry
        t_position = item.pos()
        t_text_width = item.title_text_width
        t_width = item.title_width        
        t_height = item.title_height
        t_color = item.title_box_color
        t_opacity = item.title_box_opacity
        #                t_gradient = item.title_box_gradient
        t_border_color = item.title_border_color
        t_text_size = item.title_text_size
        t_text_color = item.title_text_color
        t_text_bold = item.title_text_bold     
        t_text_italic= item.title_text_italic        
        t_border_style = item.title_border_style       
        t_border_width = item.title_border_width      
        t_text_pos_x = item.title_text_pos_x
        t_text_pos_y = item.title_text_pos_y  
        d_box_geometry = item.data_box_geometry 
        d_box_position = item.pos()
        d_box_width = item.data_box_width
        d_box_height = item.data_box_height    
        d_box_color = item.data_box_color
        d_box_opacity = item.data_box_opacity
        d_box_gradient = item.data_box_gradient
        d_border_color = item.data_border_color
        d_box_border_style = item.data_box_border_style
        d_box_border_width = item.data_box_border_width
        d_text_size = item.data_text_size
        d_width = item.data_width
        d_width_2 = item.value_width
        d_text_pos_x = item.data_text_pos_x
        d_text_pos_y = item.data_text_pos_y
        data_source_file = item.data_source_file
                
        #Create new data box
        proj.data_box_list[i] = ( models.DataBox(i, t_text, t_geometry,
                                t_position, t_width, t_height, t_color, t_opacity,
                                t_border_color, t_text_width, t_text_size,
                                t_text_color, t_text_bold, t_text_italic,
                                t_border_style, t_border_width, t_text_pos_x,
                                t_text_pos_y, d_box_geometry, d_box_position,
                                d_box_width, d_box_height, d_box_color, d_box_opacity,
                                d_box_gradient, d_border_color, d_box_border_style,
                                d_box_border_width, d_text_size, d_width,
                                d_width_2, d_text_pos_x, d_text_pos_y,
                                data_source_file) )
            
        proj.data_box_design_view_list[i] = ( DataBoxDesignView(i,
                                t_text, t_geometry, t_width, t_height, t_color, t_opacity,
                                t_border_color, t_text_width, t_text_size,
                                t_text_color, t_text_bold, t_text_italic,
                                t_border_style, t_border_width, t_text_pos_x,
                                t_text_pos_y, d_box_geometry, d_box_width,
                                d_box_height, d_box_color, d_box_opacity,
                                d_box_gradient, d_border_color, d_box_border_style,
                                d_box_border_width, d_text_size, d_width,
                                d_width_2, d_text_pos_x, d_text_pos_y,
                                data_source_file) )
            
        if end_index == start_index:
            proj.data_box_design_view_list[i].setPos(item.scenePos().x() + 20,
                                                     item.scenePos().y() + 20)
        else:
            proj.data_box_design_view_list[i].setPos(item.scenePos().x(),
                                                     item.scenePos().y())
        proj.addItem(proj.data_box_design_view_list[i])
        item.setSelected(False)
        proj.data_box_design_view_list[i].setSelected(True)

    #Double left mouse click opens the GUI panel for defining and/or modifying
    #the description boxes properties      
    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()  
        proj = window.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        global data_win
        data_win = DataBoxGUI()    
        #Data box/field settings
        t_text = items[0].title_text
        t_text_width = items[0].title_text_width
        t_width = items[0].title_width        
        t_height = items[0].title_height
        t_color = items[0].title_box_color
        t_opacity = items[0].title_box_opacity
        t_border_color = items[0].title_border_color
        t_text_size = items[0].title_text_size
        t_text_color = items[0].title_text_color
        t_text_bold = items[0].title_text_bold     
        t_text_italic= items[0].title_text_italic        
        t_border_style = items[0].title_border_style       
        t_border_width = items[0].title_border_width      
        t_text_pos_x = items[0].title_text_pos_x
        t_text_pos_y = items[0].title_text_pos_y        
        d_box_width = items[0].data_box_width
        d_box_height = items[0].data_box_height    
        d_box_color = items[0].data_box_color
        d_box_opacity = items[0].data_box_opacity
        d_box_gradient = items[0].data_box_gradient
        d_border_color = items[0].data_border_color
        d_box_border_style = items[0].data_box_border_style
        d_box_border_width = items[0].data_box_border_width
        d_text_size = items[0].data_text_size
        d_width = items[0].data_width
        d_width_2 = items[0].value_width
        d_text_pos_x = items[0].data_text_pos_x
        d_text_pos_y = items[0].data_text_pos_y
        data_source_file = items[0].data_source_file
        
        data_win.title_text.setText(t_text)
        data_win.title_text_width.setText(str(t_text_width))
        data_win.title_box_width.setText(str(t_width))
        data_win.title_box_height.setText(str(t_height))
        data_win.title_box_fill_color.setText(t_color)
        data_win.title_border_color.setText(t_border_color)
        data_win.title_font_size.setText(str(t_text_size))
        data_win.title_font_color.setText(t_text_color)
        data_win.titleCheckBoxBold.setCheckState(t_text_bold)
        data_win.titleCheckBoxItalic.setCheckState(t_text_italic)
        data_win.titleComboBoxBorder.setCurrentText(t_border_style)
        data_win.title_border_width.setText(str(t_border_width))
        data_win.title_text_pos_x.setText(str(t_text_pos_x))
        data_win.title_text_pos_y.setText(str(t_text_pos_y))        
        data_win.data_box_width.setText(str(d_box_width))
        data_win.data_box_height.setText(str(d_box_height))
        data_win.data_box_fill_color.setText(d_box_color)
        data_win.dataCheckBoxGradient.setCheckState(d_box_gradient)
        data_win.data_border_color.setText(d_border_color)
        data_win.dataComboBoxBorder.setCurrentText(d_box_border_style)
        data_win.data_border_width.setText(str(d_box_border_width))
        data_win.data_font.setText(str(d_text_size))
        data_win.data_width.setText(str(d_width))
        data_win.value_width.setText(str(d_width_2))
        data_win.data_text_pos_x.setText(str(d_text_pos_x))
        data_win.data_text_pos_y.setText(str(d_text_pos_y))
        data_win.data_source_file.setText(str(data_source_file))
        
        #Display window
        data_win.show()
        if data_win.exec(): #OK selected
            # Title section properties
            t_text = data_win.title_text.text()
            t_text_width = data_win.title_text_width.text()
            t_width = data_win.title_box_width.text()
            t_height = data_win.title_box_height.text()
            t_color = data_win.title_box_fill_color.text()
            t_border_color = data_win.title_border_color.text()
            t_text_size = data_win.title_font_size.text()
            t_text_color = data_win.title_font_color.text()
            t_text_bold = data_win.titleCheckBoxBold.checkState()
            t_text_italic = data_win.titleCheckBoxItalic.checkState()
            t_border_style = data_win.titleComboBoxBorder.currentText()
            t_border_width = data_win.title_border_width.text()
            t_text_pos_x = data_win.title_text_pos_x.text()
            t_text_pos_y = data_win.title_text_pos_y.text()  
            # Data section properties
            d_box_width = data_win.data_box_width.text()
            d_box_height = data_win.data_box_height.text()
            d_box_color = data_win.data_box_fill_color.text()
            d_box_gradient = data_win.dataCheckBoxGradient.checkState()
            d_border_color = data_win.data_border_color.text()
            d_box_border_style = data_win.dataComboBoxBorder.currentText()
            d_box_border_width = data_win.data_border_width.text()
            d_text_size = data_win.data_font.text()
            d_width = data_win.data_width.text()
            d_width_2 = data_win.value_width.text()
            d_text_pos_x = data_win.data_text_pos_x.text()
            d_text_pos_y = data_win.data_text_pos_y.text()
            data_source_file = data_win.data_source_file.text()

            try:
                items[0].title_text = t_text
                items[0].title_text_width = float(t_text_width)
                items[0].title_width = float(t_width)  
                items[0].title_height = float(t_height)
                items[0].title_box_color = t_color
                items[0].title_box_opacity = float(1)
                items[0].title_border_color = t_border_color
                items[0].title_text_size = float(t_text_size)
                items[0].title_text_color = t_text_color
                items[0].title_text_bold = t_text_bold  
                items[0].title_text_italic = t_text_italic
                items[0].title_border_style = t_border_style 
                items[0].title_border_width = t_border_width        
                items[0].title_text_pos_x = float(t_text_pos_x)
                items[0].title_text_pos_y = float(t_text_pos_y)                
                items[0].data_box_width = float(d_box_width )
                items[0].data_box_height = float(d_box_height)
                items[0].data_box_color = d_box_color
                items[0].data_box_opacity = float(1)
                items[0].data_box_gradient = d_box_gradient
                items[0].data_border_color = d_border_color
                items[0].data_box_border_style = d_box_border_style
                items[0].data_box_border_width = float(d_box_border_width)
                items[0].data_text_size = float(d_text_size)
                items[0].data_width = float(d_width)
                items[0].value_width = float(d_width_2)
                items[0].data_text_pos_x = float(d_text_pos_x)
                items[0].data_text_pos_y = float(d_text_pos_y)
                items[0].data_source_file = data_source_file
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                msg.setWindowTitle("Input field processing error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                #Revert to previous values
                t_text = items[0].title_text
                t_text_width = items[0].title_text_width
                t_width = items[0].title_width        
                t_height = items[0].title_height
                t_color = items[0].title_box_color
                t_opacity = items[0].title_box_opacity
                t_border_color = items[0].title_border_color
                t_text_size = items[0].title_text_size
                t_text_color = items[0].title_text_color
                t_text_bold = items[0].title_text_bold     
                t_text_italic= items[0].title_text_italic        
                t_border_style = items[0].title_border_style       
                t_border_width = items[0].title_border_width      
                t_text_pos_x = items[0].title_text_pos_x
                t_text_pos_y = items[0].title_text_pos_y        
                d_box_width = items[0].data_box_width
                d_box_height = items[0].data_box_height    
                d_box_color = items[0].data_box_color
                d_box_opacity = items[0].data_box_opacity
                d_box_gradient = items[0].data_box_gradient
                d_border_color = items[0].data_border_color
                d_box_border_style = items[0].data_box_border_style
                d_box_border_width = items[0].data_box_border_width
                d_text_size = items[0].data_text_size
                d_width = items[0].data_width
                d_width_2 = items[0].value_width
                d_text_pos_x = items[0].data_text_pos_x
                d_text_pos_y = items[0].data_text_pos_y
                data_source_file = items[0].data_source_file
            # Save properties to data box model
            d_box = window.project_scenes_list[key_index].data_box_list[items[0].data_key]
            d_box.title_text = t_text
            d_box.title_text_width = float(t_text_width)
            d_box.title_width = float(t_width) 
            d_box.title_height = float(t_height)
            d_box.title_box_color = t_color
            d_box.title_box_opacity= float(1)
            d_box.title_border_color = t_border_color
            d_box.title_text_size = float(t_text_size)
            d_box.title_text_color = t_text_color
            d_box.title_text_bold = int(t_text_bold)    
            d_box.title_text_italic = int(t_text_italic)
            d_box.title_border_style = t_border_style       
            d_box.title_border_width  = float(t_border_width)      
            d_box.title_text_pos_x = float(t_text_pos_x)
            d_box.title_text_pos_y = float(t_text_pos_y)           
            d_box.data_box_width = float(d_box_width )
            d_box.data_box_height = float(d_box_height)   
            d_box.data_box_color = d_box_color
            d_box.data_box_opacity = float(1)
            d_box.data_box_gradient = int(d_box_gradient)
            d_box.data_border_color = d_border_color
            d_box.data_box_border_style = d_box_border_style
            d_box.data_box_border_width = float(d_box_border_width)
            d_box.data_text_size = float(d_text_size )
            d_box.data_width = float(d_width)
            d_box.value_width = float(d_width_2)
            d_box.data_text_pos_x = float(d_text_pos_x)
            d_box.data_text_pos_y = float(d_text_pos_y)
            d_box.data_source_file = data_source_file            
            #Save position and geometry information
            i = items[0].data_key
            if items[0].data_box_gradient == 2:
                items[0].title_box = QtWidgets.QGraphicsRectItem(QtCore.QRectF(0,0,
                                                         float(t_width),float(t_height)),self)
                items[0].title_box.setRect(0,0,float(t_width),float(t_height))
                t_geometry = items[0].title_box.rect()
                style = set_line_type(items[0].title_border_style)
                items[0].title_box.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(items[0].title_border_color)),
                                         float(items[0].title_border_width), style ))
        
        
                items[0].title_box.setPos(0, -float(items[0].title_height))
            
                #Setup title box text color, font, etc.
                items[0].text = QtWidgets.QGraphicsTextItem(items[0].title_text, items[0].title_box)
                font = QtGui.QFont('Arial', float(items[0].title_text_size))
                if items[0].title_text_bold == 2:
                    font.setBold(True)
                if items[0].title_text_italic == 2:
                    font.setItalic(True)
                items[0].text.setFont(font)
                items[0].text.setPos(float(items[0].title_text_pos_x), float(items[0].title_text_pos_y))
                items[0].text.setTextWidth(float(items[0].title_text_width))
                items[0].text.setDefaultTextColor(QtGui.QColor(items[0].title_text_color))
                items[0].text.setPlainText(t_text)
                items[0].title_box.setBrush(QtGui.QBrush(QtGui.QColor(items[0].title_box_color)))            
            else:
                t_geometry = None           
            items[0].setRect(0,0,float(d_box_width),float(d_box_height))
            d_geometry = items[0].rect()
            d_position = items[0].pos()
            
            #Rebuild instance of GraphicsRectItem (class DataBoxDesignView)
            proj.removeItem(items[0])
            del items[0]
            proj.data_box_design_view_list[i] = ( DataBoxDesignView(i, t_text, t_geometry,
                                t_width, t_height, t_color, t_opacity, t_border_color,
                                t_text_width, t_text_size, t_text_color, t_text_bold,
                                t_text_italic, t_border_style, t_border_width,
                                t_text_pos_x, t_text_pos_y, d_geometry, d_box_width,
                                d_box_height, d_box_color, d_box_opacity, d_box_gradient,
                                d_border_color, d_box_border_style, d_box_border_width,
                                d_text_size, d_width, d_width_2, d_text_pos_x,
                                d_text_pos_y, data_source_file) )

            proj.data_box_design_view_list[i].setPos(d_position)
            proj.addItem(proj.data_box_design_view_list[i])
        else:
            pass#Cancel selected
            #Reset colors to original values (before opening GUI)
#            box_color = items[0].box_color
#            box_border_color = items[0].box_border_color
#            self.setBrush(QtGui.QBrush(QtGui.QColor(box_color)))
#            self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(box_border_color)), 0.5 ))
            
                       
class DescriptionBoxDesignView(QtWidgets.QGraphicsRectItem):
    #Data attributes
    def __init__(self, desc_key, desc_text, box_geometry, width, height, box_color,
                 box_color_2, opacity, gradient, box_border_color, text_width, text_size, 
                 text_color, text_bold, text_italic, border_style, border_width,
                 text_pos_x, text_pos_y, parent=None):
        super(DescriptionBoxDesignView, self).__init__(parent)
        self.desc_key = desc_key
        self.desc_text = desc_text
        self.box_geometry = box_geometry
        self.width = width
        self.height = height    
        self.box_color = box_color
        self.box_color_2 = box_color_2
        self.opacity = opacity
        self.gradient = gradient
        self.box_border_color = box_border_color
        self.text_width = text_width
        self.text_size = text_size
        self.text_color = text_color
        self.text_bold = text_bold
        self.text_italic = text_italic
        self.border_style = border_style
        self.border_width = border_width
        self.text_pos_x = text_pos_x
        self.text_pos_y = text_pos_y
        #Version tracking
        self.__version = 1
        style = set_line_type(self.border_style)
            
        if self.gradient == 2:
            start = QtCore.QPointF(int(float(self.width)/2), 0)
            end = QtCore.QPointF(int(float(self.width)/2), int(float(self.height)))
            self.gradient_text_desc = QtGui.QLinearGradient(start, end)
            self.gradient_text_desc.setColorAt(0.0, QtGui.QColor(self.box_color))
            self.gradient_text_desc.setColorAt(1.0, QtGui.QColor(self.box_color_2))
            self.setBrush(QtGui.QBrush(self.gradient_text_desc))
        else:
            self.setBrush(QtGui.QBrush(QtGui.QColor(self.box_color)))
        self.setOpacity(float(self.opacity))
            
        self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(self.box_border_color)),
                               float(self.border_width), style ))
        self.setRect(self.box_geometry)
        self.setFlags(self.ItemIsSelectable|self.ItemIsMovable)
        self.setZValue(-100.0)
        
        self.text = QtWidgets.QGraphicsTextItem(self.desc_text, self)
        font = QtGui.QFont('Arial', float(self.text_size))
        if self.text_bold == 2:
            font.setBold(True)
        if self.text_italic == 2:
            font.setItalic(True)
        self.text.setFont(font)
        self.text.setPos(float(self.text_pos_x), float(self.text_pos_y))
        self.text.setTextWidth(float(self.text_width))
        self.text.setDefaultTextColor(QtGui.QColor(self.text_color))
        
    def check_version(self):
       pass #No check needed for version 1
       
    def access_pull_down_menu(self, mouseEvent):                                 
        menu = QtWidgets.QMenu()
        copy_box_action = menu.addAction("Copy/paste description box")
        copy_box_action.setIcon(window.action_copy_paste_icon)
        copy_export_box_action = menu.addAction("Copy/paste description box to another project")
        copy_export_box_action.setIcon(window.action_copy_paste_proj_icon)
        menu.addSeparator()
        delete_box_action = menu.addAction("Delete description box")
        delete_box_action.setIcon(window.action_delete_icon)
        action = menu.exec_(mouseEvent.screenPos())
        
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
            
        if action == copy_box_action:              
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos()) 
            for item in items:
                if type(item) is DescriptionBoxDesignView:
                    self.copy_paste_desc_box(item, key_index, key_index)
                    
        if action == copy_export_box_action:              
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos()) 
            self.copy_paste_desc_box_to_another_proj(items, key_index) 

        if action == delete_box_action:
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())                 
            for item in items:
                if type(item) is DescriptionBoxDesignView:                                            
                    #Remove items from desc_box and desc_box_design_view dictionaries
                    i = item.desc_key
                    del proj.desc_box_list[i]
                    del proj.desc_box_design_view_list[i]                                              
                    #Remove and delete item form design layout scene container
                    proj.removeItem(item)
                    del item
                    break                     
                
    def copy_paste_desc_box_to_another_proj(self, items, start_index):     
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        #Load all open projects into the dialog
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()                       
                for item in items:
                    if type(item) is DescriptionBoxDesignView:
                        self.copy_paste_desc_box(item, start_index, new_index)          
                    
    def copy_paste_desc_box(self, item, start_index, end_index):
        proj = window.project_scenes_list[end_index]
        i = set_new_key(proj.desc_box_design_view_list)                            
        desc_text = item.desc_text
        box_geometry = item.box_geometry
        box_width = item.width
        box_height = item.height
        box_position = item.pos()
        box_dim = [float(item.width), float(item.height)]
        text_width = item.text_width
        fill_color = item.box_color
        fill_color_2 = item.box_color_2
        opacity = item.opacity
        gradient = item.gradient
        border_color = item.box_border_color
        text_size = item.text_size
        text_color = item.text_color
        text_bold = item.text_bold
        text_italic = item.text_italic 
        border_style = item.border_style
        border_width = item.border_width
        text_pos_x = item.text_pos_x
        text_pos_y = item.text_pos_y
  
        proj.desc_box_list[i] = models.DescriptionBox(i, desc_text,
                                       box_position, box_dim, box_geometry, text_width,
                                       fill_color, fill_color_2, opacity, gradient, border_color,
                                       text_size, text_color, text_bold, text_italic,
                                       border_style, border_width, text_pos_x, text_pos_y) 
        
        proj.desc_box_design_view_list[i] = DescriptionBoxDesignView(i,
                                       desc_text, box_geometry, box_width, box_height,
                                       fill_color, fill_color_2, opacity, gradient, border_color,
                                       text_width, text_size, text_color, text_bold,
                                       text_italic, border_style, border_width, text_pos_x,
                                       text_pos_y)
        
        if end_index == start_index:
            proj.desc_box_design_view_list[i].setPos(item.scenePos().x() + 20,
                                                     item.scenePos().y() + 20)
        else:
            proj.desc_box_design_view_list[i].setPos(item.scenePos().x(),
                                                     item.scenePos().y())
        proj.addItem(proj.desc_box_design_view_list[i])
        item.setSelected(False)
        proj.desc_box_design_view_list[i].setSelected(True)
        
    #Double left mouse click opens the GUI panel for defining and/or modifying
    #the description boxes properties      
    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        global desc_win
        desc_win = DescriptionBoxGUI()
        box_width = items[0].width
        box_height = items[0].height
        text_width = items[0].text_width
        text = items[0].desc_text
        box_color = items[0].box_color
        box_color_2 = items[0].box_color_2
        opacity = items[0].opacity
        gradient = items[0].gradient
        box_border_color = items[0].box_border_color
        text_size = items[0].text_size
        text_color = items[0].text_color
        text_bold = items[0].text_bold     
        text_italic= items[0].text_italic        
        border_style = items[0].border_style       
        border_width = items[0].border_width       
        text_pos_x = items[0].text_pos_x
        text_pos_y = items[0].text_pos_y
        
        desc_win.box_width.setText(str(box_width))
        desc_win.box_height.setText(str(box_height))
        desc_win.fillColor.setText(box_color)
        desc_win.fillColor2.setText(box_color_2)
        desc_win.checkBoxGradient.setCheckState(gradient)
        desc_win.opacity.setText(str(opacity))
        desc_win.borderColor.setText(box_border_color)
        desc_win.textWidth.setText(str(text_width))
        desc_win.textDesc.setText(text)
        desc_win.textFontSize.setText(str(text_size))
        desc_win.fontColor.setText(text_color)
        desc_win.checkBoxBold.setCheckState(text_bold)
        desc_win.checkBoxItalic.setCheckState(text_italic)
        desc_win.comboBoxBorder.setCurrentText(border_style)
        desc_win.borderWidth.setText(str(border_width))
        desc_win.textPosX.setText(str(text_pos_x))
        desc_win.textPosY.setText(str(text_pos_y))

        #Display window
        desc_win.show()
        if desc_win.exec(): #OK selected
            text_width = desc_win.textWidth.text()
            text = desc_win.textDesc.text()
            box_width = desc_win.box_width.text()
            box_height = desc_win.box_height.text()
            box_fill_color = desc_win.fillColor.text()
            box_fill_color_2 = desc_win.fillColor2.text()
            box_opacity = desc_win.opacity.text()
            box_gradient = desc_win.checkBoxGradient.checkState()
            box_border_color = desc_win.borderColor.text()
            text_size = desc_win.textFontSize.text()
            text_color = desc_win.fontColor.text()
            text_bold = desc_win.checkBoxBold.checkState()
            text_italic = desc_win.checkBoxItalic.checkState()
            border_style = desc_win.comboBoxBorder.currentText()
            border_width = desc_win.borderWidth.text()
            text_pos_x = desc_win.textPosX.text()
            text_pos_y = desc_win.textPosY.text()
            try:
                items[0].text_width = float(text_width)
                items[0].desc_text = text
                items[0].width = float(box_width)
                items[0].height = float(box_height)
                items[0].box_color = box_fill_color
                items[0].box_color_2 = box_fill_color_2
                items[0].gradient = box_gradient
                items[0].opacity = float(box_opacity)
                items[0].box_border_color = box_border_color
                items[0].text_font_size = float(text_size)
                items[0].text_color = text_color
                items[0].text_bold = text_bold   
                items[0].text_italic = text_italic      
                items[0].border_style = border_style     
                items[0].border_width = float(border_width)   
                items[0].text_pos_x = float(text_pos_x)
                items[0].text_pos_y = float(text_pos_y)
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                msg.setWindowTitle("Input field processing error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                #Revert to previous values
                box_width = items[0].width
                box_height = items[0].height
                text_width = items[0].text_width
                text = items[0].desc_text
                box_color = items[0].box_color
                box_color_2 = items[0].box_color_2
                opacity = items[0].opacity
                gradient = items[0].gradient
                box_border_color = items[0].box_border_color
                text_size = items[0].text_size
                text_color = items[0].text_color
                text_bold = items[0].text_bold     
                text_italic= items[0].text_italic        
                border_style = items[0].border_style       
                border_width = items[0].border_width       
                text_pos_x = items[0].text_pos_x
                text_pos_y = items[0].text_pos_y
                
            proj.desc_box_list[items[0].desc_key].fill_color = box_fill_color
            proj.desc_box_list[items[0].desc_key].fill_color_2 = box_fill_color_2
            proj.desc_box_list[items[0].desc_key].gradient = box_gradient
            proj.desc_box_list[items[0].desc_key].opacity = box_opacity
            proj.desc_box_list[items[0].desc_key].border_color = box_border_color
            proj.desc_box_list[items[0].desc_key].text_width = float(text_width)
            proj.desc_box_list[items[0].desc_key].desc_text = text
            proj.desc_box_list[items[0].desc_key].box_dim.append(float(box_width))
            proj.desc_box_list[items[0].desc_key].box_dim.append(float(box_height))
            proj.desc_box_list[items[0].desc_key].text_size = text_size
            proj.desc_box_list[items[0].desc_key].text_color = text_color
            proj.desc_box_list[items[0].desc_key].text_bold = int(text_bold)
            proj.desc_box_list[items[0].desc_key].text_italic = int(text_italic)
            proj.desc_box_list[items[0].desc_key].border_style = border_style
            proj.desc_box_list[items[0].desc_key].border_width = float(border_width)
            proj.desc_box_list[items[0].desc_key].text_pos_x = float(text_pos_x)
            proj.desc_box_list[items[0].desc_key].text_pos_y = float(text_pos_y)
            
            #Save position and geometry information
            i = items[0].desc_key
            items[0].setRect(0,0,float(box_width),float(box_height))
            geometry = items[0].rect()
            position = items[0].pos()
            
            #Update text field associated with description box
            self.text.setPlainText(text)
            
            #Rebuild instance of GraphicsRectItem (class DescriptionBoxDesignView)
            proj.removeItem(items[0])
            del items[0]
            proj.desc_box_design_view_list[i] = DescriptionBoxDesignView(i, text, geometry,
                                           box_width, box_height, box_fill_color,
                                           box_fill_color_2, box_opacity, box_gradient, box_border_color,
                                           text_width, text_size, text_color, text_bold,
                                           text_italic, border_style, border_width,
                                           text_pos_x, text_pos_y)

            proj.desc_box_design_view_list[i].setPos(position)        
            proj.addItem(proj.desc_box_design_view_list[i])
        else: #Cancel selected
            #Reset colors to original values (before opening GUI)
            box_color = items[0].box_color
            box_color_2 = items[0].box_color_2
            grad = items[0].gradient
            box_border_color = items[0].box_border_color
            w = items[0].width
            h = items[0].height
            
            if grad == 2:
                start = QtCore.QPointF(int(float(w)/2), 0)
                end = QtCore.QPointF(int(float(w)/2), int(h))
                self.gradient_text_desc = QtGui.QLinearGradient(start, end)
                self.gradient_text_desc.setColorAt(0.0, QtGui.QColor(box_color))
                self.gradient_text_desc.setColorAt(1.0, QtGui.QColor(box_color_2))
                self.setBrush(QtGui.QBrush(self.gradient_text_desc))
            else:
                self.setBrush(QtGui.QBrush(QtGui.QColor(box_color)))
                self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(box_border_color)), 0.5 ))
            self.setOpacity(float(box_opacity))


class TextBoxDesignView(QtWidgets.QGraphicsRectItem):
    #Data attributes
    def __init__(self, text_key, text_geometry, text, text_width, text_color, text_size,
                 text_bold, text_italic, parent=None):
        super(TextBoxDesignView, self).__init__(parent)
        self.text_key = text_key
        self.text_geometry = text_geometry
        self.text = text
        self.text_width = text_width
        self.text_color = text_color
        self.text_size = text_size
        self.text_bold = text_bold
        self.text_italic = text_italic
        #Version tracking
        self.__version = 1
        
        self.setFlags(QtWidgets.QGraphicsItem.ItemIsMovable |
                QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.setBrush(QtGui.QBrush(QtCore.Qt.NoBrush))
        self.setRect(self.text_geometry)
        self.text_field = QtWidgets.QGraphicsTextItem(self.text, self)
        font = QtGui.QFont('Arial', float(self.text_size))
        
        self.text_field.setDefaultTextColor(QtGui.QColor(self.text_color))
        if self.text_bold == 2:
            font.setBold(True)
        if self.text_italic == 2:
            font.setItalic(True)
        self.text_field.setFont(font)    
        self.text_field.setPos(-2, -2)
        self.text_field.setTextWidth(float(self.text_width))
        
    def check_version(self):
        pass #No check needed for version 1
        
    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()  
        proj = window.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        global text_win
        text_win = TextBoxGUI()
        #Retrieve currently saved properties
        text_width = items[0].text_width
        text = items[0].text
        text_color = items[0].text_color
        text_size = items[0].text_size
        text_bold = items[0].text_bold     
        text_italic= items[0].text_italic                
        #Allocate values to dialog fields and display properties
        text_win.fontColor.setText(text_color)
        text_win.textWidth.setText(str(text_width))
        text_win.textEdit.setPlainText(text)
        text_win.textSize.setText(str(text_size))
        text_win.checkBoxBold.setCheckState(text_bold)
        text_win.checkBoxItalic.setCheckState(text_italic)    
        text_win.show()
        
        if text_win.exec(): #OK selected
            #Retrieve field values
            text = text_win.textEdit.toPlainText()
            text_width = text_win.textWidth.text()
            text_color = text_win.fontColor.text()
            text_size = text_win.textSize.text()
            text_bold = text_win.checkBoxBold.checkState()
            text_italic = text_win.checkBoxItalic.checkState()    
            try: #Check to make sure all formats are good (otherwise revert to defaults)
                items[0].text_width = float(text_width)
                items[0].text = text
                items[0].text_color = text_color
                items[0].text_size = float(text_size)
                items[0].text_bold = text_bold   
                items[0].text_italic = text_italic            
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                msg.setWindowTitle("Input field processing error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                text_width = items[0].text_width
                text = items[0].text
                text_color = items[0].text_color
                text_size = items[0].text_size
                text_bold = items[0].text_bold     
                text_italic= items[0].text_italic
            
            txt_list = proj.text_list[items[0].text_key]                
            txt_list.text_color = text_color
            txt_list.text_width = float(text_width)
            txt_list.text = text
            txt_list.text_size = text_size
            txt_list.text_bold = int(text_bold)
            txt_list.text_italic = int(text_italic)           
            self.setRect(QtCore.QRectF(0, 0, float(text_width), 30))                
            #Save position and geometry information
            i = items[0].text_key
            geometry = items[0].rect()
            position = items[0].pos()                
            #Update text field associated with description box
            self.text_field.setPlainText(text)
                
            #Rebuild instance of GraphicsRectItem (class DescriptionBoxDesignView)
            proj.removeItem(items[0])
            del items[0]
            proj.text_design_view_list[i] = ( TextBoxDesignView(i, geometry, text,
                                              text_width, text_color, text_size,
                                              text_bold, text_italic) )               
            proj.text_design_view_list[i].setPos(position)        
            proj.addItem(proj.text_design_view_list[i])
           
        else: #Cancel selected
            #Reset colors to original values (before opening GUI)
            text_color = items[0].text_color 
                     
    def access_pull_down_menu(self, mouseEvent):                                 
        menu = QtWidgets.QMenu()
        copy_text_action = menu.addAction("Copy/paste text block")
        copy_text_action.setIcon(window.action_copy_paste_icon)
        copy_export_text_action = menu.addAction("Copy/paste text block to another project")
        copy_export_text_action.setIcon(window.action_copy_paste_proj_icon)
        menu.addSeparator()
        delete_text_action = menu.addAction("Delete text block")
        delete_text_action.setIcon(window.action_delete_icon)
        action = menu.exec_(mouseEvent.screenPos())
        
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
            
        if action == copy_text_action:
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            cursor_items = proj.items(mouseEvent.scenePos())                 
            for item in cursor_items:
                if type(item) is TextBoxDesignView:
                    self.copy_paste_text_box(item, key_index, key_index)
                    
        if action == copy_export_text_action:
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())                 
            self.copy_paste_text_box_to_another_proj(items, key_index)            
                    
        if action == delete_text_action:
            tab_index, key_index = retrieve_current_project_key_index()
            proj = window.project_scenes_list[key_index]
            items = proj.items(mouseEvent.scenePos())                 
            for item in items:
                if type(item) is TextBoxDesignView:                      
                     i = item.text_key                       
                     #Remove items from text and text view dictionaries
                     del proj.text_list[i]
                     del proj.text_design_view_list[i]                                              
                     #Remove and delete item from design layout scene container
                     proj.removeItem(item)
                     del item    
                     break
                        
    def copy_paste_text_box_to_another_proj(self, items, start_index):     
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        #Load all open projects into the dialog
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()                       
                for item in items:
                    if type(item) is TextBoxDesignView:
                        self.copy_paste_text_box(item, start_index, new_index)
                        
    def copy_paste_text_box (self, item, start_index, end_index):
        proj = window.project_scenes_list[end_index]
        i = set_new_key(proj.desc_box_design_view_list) 
        text = item.text
        text_position = item.pos()
        text_geometry = item.text_geometry
        text_width = item.text_width
        text_color = item.text_color
        text_size = item.text_size
        text_bold = item.text_bold
        text_italic = item.text_italic
                        
        proj.text_list[i] = models.TextBox(i, text, text_position, 
                                       text_geometry, text_width, text_color, text_size,
                                       text_bold, text_italic)
                        
        proj.text_design_view_list[i] = TextBoxDesignView(i, text_geometry,
                                            text, text_width, text_color, text_size,
                                            text_bold, text_italic)

        if end_index == start_index:
            proj.text_design_view_list[i].setPos(item.scenePos().x() + 20,
                                                     item.scenePos().y() + 20)
        else:
            proj.text_design_view_list[i].setPos(item.scenePos().x(),
                                                     item.scenePos().y())
        proj.addItem(proj.text_design_view_list[i]) 
        item.setSelected(False)
        proj.text_design_view_list[i].setSelected(True)

class LineArrowDesignView(QtWidgets.QGraphicsLineItem):
    '''
    '''  
    #Data attributes
    def __init__(self, key, geometry, color, line_width, line_style, arrow, parent = None):  
        super(LineArrowDesignView, self).__init__(parent)      
        self.key = key
        self.geometry = geometry
        self.color = color
        self.line_width = line_width
        self.line_style = line_style
        self.arrow = arrow
        self.anchors = {} 
        #Version tracking
        self.__version = 1
        
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsMovable, True)
        self.setCursor(QtGui.QCursor(QtCore.Qt.SizeAllCursor))
        
        style = set_line_type(self.line_style)
        self.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(self.color)),
                               float(self.line_width), style ))
        self.setLine(geometry)

        self.anchors[1] = Anchor('p1', self)
        self.anchors[1].setPos(geometry.p1())
        self.anchors[1].posChangeCallbacks.append(self.update_p1)        
        self.anchors[1].setFlag(self.anchors[1].ItemIsSelectable, True)
        self.anchors[1].setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.anchors[1].setBrush(QtGui.QBrush(QtCore.Qt.transparent))
        
        self.anchors[2] = Anchor('p2', self)   
        self.anchors[2].setPos(geometry.p2())
        self.anchors[2].posChangeCallbacks.append(self.update_p2)        
        self.anchors[2].setFlag(self.anchors[2].ItemIsSelectable, True)
        self.anchors[2].setPen(QtGui.QPen(QtCore.Qt.NoPen))
        self.anchors[2].setBrush(QtGui.QBrush(QtCore.Qt.transparent))
        
        if self.arrow == 2:
            self.arrow_length = 10
            self.arrow_path = QtWidgets.QGraphicsPathItem(self)
            self.arrow_path.setPen(QtGui.QPen(QtGui.QColor(self.color),
                                              float(self.line_width)))
            self.update_arrow()
            
    def check_version(self):
        pass #No check needed for version 1
         
    def update_p1(self, p1):
        self.anchors[1].setVisible(True)
        p1 = self.anchors[1].pos()
        p2 = self.anchors[2].pos()
        self.setLine(QtCore.QLineF(p1, p2))
        if self.arrow == 2:
            self.update_arrow()

    def update_p2(self, p2):
        self.anchors[2].setVisible(True)
        p1 = self.anchors[1].pos()
        p2 = self.anchors[2].pos()
        self.setLine(QtCore.QLineF(p1, p2))
        if self.arrow == 2:
            self.update_arrow()
        
    def update_arrow(self):        
        angle = np.arccos(self.line().dx() / self.line().length())
        if self.line().dy() >= 0:
            angle = (np.pi * 2.0) - angle
  
        a1 = QtCore.QPointF(np.sin(angle + np.pi / 2.5) * self.arrow_length,
                            np.cos(angle + np.pi / 2.5) * self.arrow_length)
        a2 = QtCore.QPointF(np.sin(angle + np.pi - np.pi / 2.5) * self.arrow_length,
                            np.cos(angle + np.pi - np.pi / 2.5) * self.arrow_length)
        
        arrowP1 = self.line().p2() - a1
        arrowP2 = self.line().p2() - a2
        
        path = QtGui.QPainterPath() 
        path.addPolygon(QtGui.QPolygonF([self.line().p2(), arrowP1, arrowP2,
                                         self.line().p2()]))
        self.arrow_path.setPath(path)
        self.arrow_path.setBrush(QtGui.QBrush(QtGui.QColor(self.color)))
            
    def access_pull_down_menu(self, mouseEvent):                                 
        menu = QtWidgets.QMenu()
        copy_line_action = menu.addAction("Copy/paste line-arrow")
        copy_line_action.setIcon(window.action_copy_paste_icon)
        copy_export_line_action = menu.addAction("Copy/paste line-arrow to another project")
        copy_export_line_action.setIcon(window.action_copy_paste_proj_icon)
        menu.addSeparator()
        delete_line_action = menu.addAction("Delete line-arrow")
        delete_line_action.setIcon(window.action_delete_icon)
        action = menu.exec_(mouseEvent.screenPos())
        
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
            
        if action == copy_line_action:
            key_index, items = self.select_scene_items(mouseEvent)
            for item in items:
                if type(item) is LineArrowDesignView:
                    self.copy_paste_line_arrow(item, key_index, key_index)   
          
        if action == copy_export_line_action:
            key_index, items = self.select_scene_items(mouseEvent) 
            self.copy_paste_line_arrow_to_another_proj(items, key_index)

        if action == delete_line_action:
            key_index, items = self.select_scene_items(mouseEvent)
            for line_arrow_item in items:
                if type(line_arrow_item) is LineArrowDesignView:
                    #Remove and delete qgraphicslineitem
                    i = line_arrow_item.key
                    del window.project_scenes_list[key_index].line_arrow_list[i]
                    del window.project_scenes_list[key_index].line_arrow_design_view_list[i]                                              
                    #Remove and delete item form design layout scene container
                    window.project_scenes_list[key_index].removeItem(line_arrow_item)
                    del line_arrow_item
                    break
                    
    def select_scene_items(self, mouseEvent):
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.items(mouseEvent.scenePos())
        return key_index, items
                    
    def copy_paste_line_arrow_to_another_proj(self, items, start_index):     
        global projects_list_dialog
        projects_list_dialog = ProjectListGUI()
        projects_list_dialog.show()
        #Load all open projects into the dialog
        counter = 0
        while counter < len(window.project_layouts_list):
            keys = list(window.project_layouts_list.keys())
            project_key = keys[counter]
            project_name = window.project_scenes_list[project_key].scene_name
            projects_list_dialog.projectsBox.addItem(str(project_name))
            counter += 1              
        if projects_list_dialog.exec():
            #Create copy of fb and paste to selected project
            if projects_list_dialog.projectType.text():
                name = projects_list_dialog.projectType.text()
                tabs = window.tabWidget.count()
                tab = 0
                new_tab = 0
                while tab < tabs:
                    project_name = window.tabWidget.tabText(tab)
                    if project_name == name:
                        new_tab = tab
                        break
                    tab += 1
                window.tabWidget.setCurrentIndex(new_tab)
                tab_index, new_index = retrieve_current_project_key_index()               
                for item in items:
                    if type(item) is LineArrowDesignView:
                        self.copy_paste_line_arrow(item, start_index, new_index)
                    
    def copy_paste_line_arrow(self, item, start_index, end_index):
        proj = window.project_scenes_list[end_index]
        i = set_new_key(proj.line_arrow_design_view_list) 
        geometry = item.geometry
        position = item.pos()
        color = item.color
        line_width = item.line_width
        line_style = item.line_style
        arrow = item.arrow
  
        proj.line_arrow_list[i] = models.LineArrow(i, position, geometry, color, 
                            line_width, line_style, arrow) 
                        
        proj.line_arrow_design_view_list[i] = LineArrowDesignView(i, geometry, color, 
                                        line_width, line_style, arrow)
        
        #Add new line arrow design view to QGraphicsScene
        if end_index == start_index:
            proj.line_arrow_design_view_list[i].setPos(item.scenePos().x() + 20,
                                                       item.scenePos().y() + 20)
        else:
            proj.line_arrow_design_view_list[i].setPos(item.scenePos().x(),
                                                       item.scenePos().y())
        proj.addItem(proj.line_arrow_design_view_list[i])
        item.setSelected(False)
        proj.line_arrow_design_view_list[i].setSelected(True)
                    
    def mouseDoubleClickEvent(self, QMouseEvent): #QT specific method
        tab_index, key_index = retrieve_current_project_key_index()
        proj = window.project_scenes_list[key_index]
        items = proj.selectedItems()
        
        global line_win
        line_win = LineArrowGUI()

        line_color = items[0].color
        line_style = items[0].line_style
        line_width = items[0].line_width
        arrow = items[0].arrow
        
        line_win.lineColor.setText(line_color)
        line_win.lineWidth.setText(str(line_width))
        line_win.comboBoxLine.setCurrentText(line_style)
        line_win.checkBoxArrow.setCheckState(arrow)
        
        #Display window
        line_win.show()
        if line_win.exec(): #OK selected
            line_color = line_win.lineColor.text()
            line_style = line_win.comboBoxLine.currentText()
            line_width = line_win.lineWidth.text()
            arrow = line_win.checkBoxArrow.checkState()
            try:
                items[0].color = line_color
                items[0].line_style = line_style
                items[0].line_width = float(line_width)
                items[0].arrow = arrow
            except:
                e0 = sys.exc_info() [0]
                e1 = sys.exc_info() [1]
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setText('Error reading value(s) in properties dialog. Will revert to' 
                            + ' previous values after closing.')
                msg.setInformativeText(str(e0) + ' ' + str(e1))
                msg.setInformativeText(str(traceback.format_exc()))
                msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
                msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
                msg.setWindowTitle("Input field processing error")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
                #Revert to previous values
                line_color = items[0].color
                line_style = items[0].line_style
                line_width = items[0].line_width
                arrow = items[0].arrow
            
            line_arw_list = proj.line_arrow_list[items[0].key]
            line_arw_list.color = line_color
            line_arw_list.line_style = line_style
            line_arw_list.line_width = float(line_width)
            line_arw_list.arrow = arrow
            
            #Save position and geometry information
            i = items[0].key
            geometry = items[0].line()
            position = items[0].pos()
            
            #Rebuild instance of GraphicsRectItem (class DescriptionBoxDesignView)
            proj.removeItem(items[0])
            del items[0]
            proj.line_arrow_design_view_list[i] = LineArrowDesignView(i, geometry,
                                             line_color, line_width, line_style, arrow)

            proj.line_arrow_design_view_list[i].setPos(position)
            proj.addItem(proj.line_arrow_design_view_list[i])
        
        else: #Cancel selected
            #Reset colors to original values (before opening GUI)
            line_color = items[0].line_color  
   
         
class Anchor(QtWidgets.QGraphicsEllipseItem):

   def __init__(self, name, parent=None):
       super(Anchor, self).__init__(QtCore.QRectF(-2.0,-2.0,4.0,4.0), parent)
       self.posChangeCallbacks = []
       self.setFlags(self.ItemIsMovable)
       self.setFlag(self.ItemSendsScenePositionChanges, True)
       self.setCursor(QtGui.QCursor(QtCore.Qt.SizeFDiagCursor))
       self.name = name        

   def itemChange(self, change, value):    
       if change == self.ItemScenePositionHasChanged:
           for cb in self.posChangeCallbacks:
               cb(value)
           return value
       return super(Anchor, self).itemChange(change, value)                        
            
'''GUI classes (aside from main application window)===================================='''
            
class ProjectPropertiesGUI(QtWidgets.QDialog, Ui_ProjectWindow):
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_ProjectWindow.__init__(self)
        #Perform setup of project properties dialog (designed via QT Designer)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)
        self.pushButtonColor.clicked.connect(self.color)
        self.pushButtonColorBorder.clicked.connect(self.color_border)
        self.pushButtonHelpFilePath.clicked.connect(self.help_file_path)
        self.pushButtonHelpAdditionalPath.clicked.connect(self.help_additional_path)
        self.pushButtonHelpScriptEditor.clicked.connect(self.help_script_editor)
        self.checkBoxFeedback.toggled.connect(self.set_segments_status)
        style = """QLineEdit { background-color: rgb(245, 245, 245); color: rgb(50, 50, 50) }"""
        self.projectNumberSamples.setStyleSheet(style)
        self.projectSamplePeriod.setStyleSheet(style)
        self.projectSamplesSym.setStyleSheet(style)
        self.samplesPerSegment.setStyleSheet(style)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
       
    def apply(self):              
        time = float(self.projectSimulationTime.text())
        sample_rate = float(self.projectSampleRate.text())
        symbol_rate = float(self.projectSymbolRate.text())
        
        total_samples = float(np.ceil(time * sample_rate))
        total_samples_string = str(format(total_samples, '0.4E'))
        self.projectNumberSamples.setText(total_samples_string)
        
        sample_period = format(1/sample_rate, '0.4E')
        sample_period_str = str(sample_period)
        self.projectSamplePeriod.setText(sample_period_str)
        
        samples_per_sym = format(float(np.ceil(sample_rate/symbol_rate)), '0.4E')
        samples_per_sym_str = str(samples_per_sym)
        self.projectSamplesSym.setText(samples_per_sym_str)
        
        self.projectSimulationTime.setText(format(time, '0.4E'))
        self.projectSampleRate.setText(format(sample_rate, '0.4E'))
        
        if self.checkBoxFeedback.checkState() == 2:
            segments = float(self.projectSegments.text())
            samples_per_seg = total_samples/segments
            self.samplesPerSegment.setText(format(samples_per_seg, '0.1f'))
            if samples_per_seg < 1 or samples_per_seg % 1 != 0:
                msg = QtWidgets.QMessageBox()
                syslab_icon = set_icon_window()
                msg.setWindowIcon(syslab_icon)
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setWindowTitle("Warning: Samples per segment is not a whole number")
                msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
                msg.setText('The samples per segment variable must be greater than 1 and ' + '\n'
                    + 'should not have a non-zero fractional part. Please choose a different'
                    + '\n' + 'setting for the Feedback segments field.')
                msg.setStyleSheet("QLabel{height: 40px; min-height: 70px; max-height: 40px;}")
                msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
                rtnval = msg.exec()
                if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
        
    def color(self):
        current_color = QtGui.QColor(project_dialog.gridLineColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            project_dialog.gridLineColor.setText(color.name())
            
    def color_border(self):
        current_color = QtGui.QColor(project_dialog.borderLineColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            project_dialog.borderLineColor.setText(color.name())  
            
    def set_segments_status(self):
        if self.checkBoxFeedback.checkState() == 2:
            self.projectSegments.setEnabled(True)
        else:
            self.projectSegments.setEnabled(False)
            
    def help_file_path(self):
        msg = QtWidgets.QMessageBox()
        syslab_icon = set_icon_window()
        msg.setWindowIcon(syslab_icon)
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText('The "File path (project)" edit field is used to define the ' + '\n'
                    + 'location where your design project is saved. If it is empty the'
                    + '\n' + 'current working directory (where Python is installed) is used.'
                    + '\n' + '\n'
                    + 'This path is also used to search for the location of your scripts.'
                    + '\n' + 'If empty, the application searches for the script module(s)'
                    + '\n' + 'within the current working directory.'
                    + '\n' + '\n' 
                    + 'IMPORTANT: When defining the path, make sure to list the full path name'
                    + '\n' + 'and to add a back-slash at the end of the path definition'
                    + '\n' + r'(e.g. C:\User\My Project Folder\)')
        msg.setStyleSheet("QLabel{height: 70px; min-height: 70px; max-height: 70px;}")
        msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
        msg.setWindowTitle("Help dialog for File path (project)")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
        rtnval = msg.exec()
        if rtnval == QtWidgets.QMessageBox.Ok:
            msg.close()
            
    def help_additional_path(self):
        msg = QtWidgets.QMessageBox()
        syslab_icon = set_icon_window()
        msg.setWindowIcon(syslab_icon)
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText('The "File path (additional)" edit field can be used to define an' + '\n'
                    + 'additional file path for locating your project scripts. During a'
                    + '\n' + 'simulation, the script file will be first be searched for'
                    + '\n' 'using "File path (project)". If it cannot be located in'
                    + '\n' + 'this directory, then "File path (additional)" will be used.'
                    + '\n' + '\n' + 'Note 1: If the script file is not found in either location,'
                    + '\n' + 'an error message will be raised during the simulation.'
                    + '\n' + '\n' + 'Note 2: This field is optional and can be left empty.')
        msg.setStyleSheet("QLabel{height: 70px; min-height: 70px; max-height: 70px;}")
        msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
        msg.setWindowTitle("Help dialog for File path (additional)")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
        rtnval = msg.exec()
        if rtnval == QtWidgets.QMessageBox.Ok:
            msg.close()
            
    def help_script_editor(self):
        msg = QtWidgets.QMessageBox()
        syslab_icon = set_icon_window()
        msg.setWindowIcon(syslab_icon)
        msg.setIcon(QtWidgets.QMessageBox.Question)
        msg.setText('The "Code/script editor execute path" field is used to define the'
                    + '\n' + 'command line operation for opening a Python-compatible script editor.'
                    + '\n' + '\n' + 'The default editor, packaged with SystemLab-Design, is SciTE'
                    + '\n' + 'and can be accessed using the following command line path:'
                    + '\n' + '"start .\wscite\SciTE -open:"'
                    + '\n' + '\n' + 'You can change the type of editor used (if already installed on'
                    + '\n' 'your computer) by updating this field.'
                    + '\n' + 'e.g. For Notepad++: "start notepad++"'
                    + '\n' + 'e.g. For Python IDLE: "start python -m idlelib"'
                    + '\n' + '\n' + 'NOTE: If the path which defines the location of a Python script'
                    + '\n' + 'contains empty name spaces the file may not be located. It is'
                    + '\n' + 'recommended to remove any blank spaces in your project path'
                    + '\n' + 'definitions.')
        msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
        msg.setStyleSheet("QLabel{width: 425px; min-width: 425px; max-width: 425px;}")
        msg.setWindowTitle("Help dialog for Code/script editor command line path")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
        rtnval = msg.exec()
        if rtnval == QtWidgets.QMessageBox.Ok:
            msg.close()            

           
class FunctionalBlockListGUI(QtWidgets.QDialog, Ui_FunctionalBlockList):
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_FunctionalBlockList.__init__(self)
        #Perform setup of project properties dialog (designed via QT Designer)
        self.setupUi(self)  
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        #Ports table initial settings
        style = "::section {background-color: lightgray }" #"::section{Background-color:rgb(190,1,1)}"
        self.functionalBlockListTable.horizontalHeader().setVisible(True)
        self.functionalBlockListTable.verticalHeader().setVisible(True)
        self.functionalBlockListTable.horizontalHeader().setStyleSheet(style)
        self.functionalBlockListTable.verticalHeader().setStyleSheet(style)
        self.functionalBlockListTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1

        
class LinkListGUI(QtWidgets.QDialog, Ui_LinkList):
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_LinkList.__init__(self)
        #Perform setup of project properties dialog (designed via QT Designer)
        self.setupUi(self) 
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        #Ports table initial settings
        style = "::section {background-color: lightgray }" #"::section{Background-color:rgb(190,1,1)}"
        self.linkListTable.horizontalHeader().setVisible(True)
        self.linkListTable.verticalHeader().setVisible(True)
        self.linkListTable.horizontalHeader().setStyleSheet(style)
        self.linkListTable.verticalHeader().setStyleSheet(style)
        self.linkListTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)   
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1

             
class FunctionalBlockGUI(QtWidgets.QDialog, Ui_FBWindow):
    '''GUI interface for adding, editing or removing ports, parameters,...
    '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_FBWindow.__init__(self)
        #Perform setup of main SystemLab view (designed via QT Designer)
        self.setupUi(self)    
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.update_ports_decision = False
        self.tab_index, self.key_index = retrieve_current_project_key_index()          
        self.items = window.project_scenes_list[self.key_index].selectedItems()
        self.fb_key = self.items[0].fb_key           
        self.tabWidget.setStyleSheet(app_font_default)
        self.tabFunctionalBlock.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        
#        self.instance_key = None
        
        style = ("""QLineEdit { background-color: rgb(245, 245, 245); 
                color: rgb(50, 50, 50) }""")
        self.functionalBlockID.setStyleSheet(style)
        
        '''User action buttons========================================================='''
        #Edit script
        self.editScriptButton.clicked.connect(self.open_editor)
        #Parameters table
        self.insertRowButton.clicked.connect(self.insert_table_row)
        self.deleteRowButton.clicked.connect(self.delete_table_row)
        self.copyRowButton.clicked.connect(self.copy_table_row)
        self.pasteRowButton.clicked.connect(self.paste_table_row)
        self.insertHeaderButton.clicked.connect(self.insert_table_header)
        self.moveRowUpButton.clicked.connect(self.move_row_up)
        self.moveRowDownButton.clicked.connect(self.move_row_down)
        self.insertCheckBoxButton.clicked.connect(self.insert_check_box)
        self.insertCheckBoxButton.setStyleSheet("background-color: #cdffff")
        self.insertListBoxButton.clicked.connect(self.insert_list_box)
        self.insertListBoxButton.setStyleSheet("background-color: #cdffff")
        self.updateParametersTableButton.clicked.connect(self.update_parameters)
        self.updateParametersTableButton.setStyleSheet("background-color: #c5ffa5")
        self.pasteRowButton.setEnabled(False)
        #Ports table
        self.addPortButton.clicked.connect(self.add_port)
        self.editPortButton.clicked.connect(self.edit_port)
        self.deletePortButton.clicked.connect(self.delete_port)
        self.movePortUpButton.clicked.connect(self.move_port_up)
        self.movePortDownButton.clicked.connect(self.move_port_down)
        #FB dimensions and colors
        self.colorFillButton.clicked.connect(self.select_color)
        self.colorFillButton2.clicked.connect(self.select_color2)
        self.colorBorderButton.clicked.connect(self.select_border_color) 
        #FB text settings
        self.colorFontButton.clicked.connect(self.select_font_color)
        self.colorFontButtonPortLabel.clicked.connect(self.select_port_label_color)
        
        '''Initial table settings======================================================'''
        #Ports table
        self.portsTable.clearContents()
        style = "::section {background-color: lightgray }" #background-color:rgb(190,1,1)
        self.portsTable.horizontalHeader().setVisible(True)
        self.portsTable.verticalHeader().setVisible(True)
        self.portsTable.horizontalHeader().setStyleSheet(style)
        self.portsTable.verticalHeader().setStyleSheet(style)
        self.portsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.portsTable.cellClicked.connect(self.ports_table_cell_was_clicked)
        #Parameters table
        self.parametersTable.horizontalHeader().setVisible(True)
        self.parametersTable.verticalHeader().setVisible(True)
        self.parametersTable.horizontalHeader().setStyleSheet(style)
        self.parametersTable.verticalHeader().setStyleSheet(style)
        self.parametersTable.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        #Data output table
        self.dataTable.horizontalHeader().setVisible(True)
        self.dataTable.verticalHeader().setVisible(True)
        self.dataTable.horizontalHeader().setStyleSheet(style)
        self.dataTable.verticalHeader().setStyleSheet(style)
        self.dataTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  
        #Load tables
        self.project = window.project_scenes_list[self.key_index]
        self.fb = self.project.fb_list[self.fb_key]
        self.fb_view = self.project.fb_design_view_list[self.fb_key]
        self.load_ports_table()
        self.load_parameters_table()
        self.load_results_table()
        #Set tab to parameters table view
        self.tabFunctionalBlock.setCurrentIndex(0)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
        
    def open_editor(self):
        script_found = None
        script = self.project.design_settings['edit_script_path']
        script_name = str(self.functionalBlockScript.text()) + '.py'
        
        # Search for fb script in standard/custom libraries (defined in config_fb_library) 
        for i in range(0, len(config_lib.scripts_path_list)):
            script_path = (str(root_path) + str(config_lib.scripts_path_list[i]) + 
                           str(script_name))
            if os.path.isfile(script_path): #Script name found
                script_found = script_path
        
        if script_found is None:
            # Search for fb script in project paths
            path1 = self.project.design_settings['file_path_1']
            script_path = str(path1) + str(script_name)
            script_path = os.path.abspath(script_path) 
            if os.path.isfile(script_path): #Script name found
                script_found = script_path
            else: #Check 2nd project path
                path2 = self.project.design_settings['file_path_2']
                script_path = str(path2) + str(script_name)
                script_path = os.path.abspath(script_path) 
                if os.path.isfile(script_path): #Script name found
                    script_found = script_path
                
        if script_found is None: #Script path cannot be located
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
            msg.setText('The script name defined in the "Script module name" field does'
                        + '\n' + 'not exist or could not be located within the defined functional'
                        + '\n' + 'block script libraries or project folders.')
            msg.setInformativeText('Select OK to continue to open the script editor or Cancel to'
                                   + '\n' + 'stop this operation.')
            msg.setStyleSheet("QLabel{height: 050px; min-height: 100px; max-height: 100px;}")
            msg.setStyleSheet("QLabel{width: 350px; min-width: 350px; max-width: 350px;}")
            msg.setWindowTitle("Open file error: Script file not found")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)	       
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                msg.close()
                try:
                    os.system(script)
                except:
                    self.error_message_script_editor()
        else:
            script = str(script) + ' ' + str(script_found)
            try:
                 os.system(script)
            except:
                self.error_message_script_editor()
            
    def error_message_script_editor(self):       
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Warning)
        syslab_icon = set_icon_window()
        msg.setWindowIcon(syslab_icon)
        msg.setText('The script editor application could not be successfully loaded.')
        msg.setInformativeText('Please verify the Code/script editor execute path' 
                               + ' under Project Settings/Advanced settings.')
        msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
        msg.setStyleSheet("QLabel{width: 400px; min-width: 400px; max-width: 400px;}")
        msg.setWindowTitle("Loading error: Code/script editor application")
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
        rtnval = msg.exec()
        if rtnval == QtWidgets.QMessageBox.Ok:
            msg.close()
        
    def load_ports_table(self):
        port_list = self.fb.fb_ports_list
        length_port_list = len(port_list)
        
        if length_port_list > self.portsTable.rowCount():
            self.portsTable.setRowCount(length_port_list)

        for row in range(0, length_port_list):
            portID = port_list[row][0]
            portName = port_list[row][1]
            portCardinal = port_list[row][2]
            portDirection = port_list[row][3]
            sig = port_list[row][4]        
            self.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(portID)))
            self.portsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(portName))
            self.portsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(portCardinal))
            self.portsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(portDirection))
            self.portsTable.setItem(row, 4, QtWidgets.QTableWidgetItem(sig))
            
        self.portsTable.resizeColumnsToContents()       
        if length_port_list == 0:
            self.editPortButton.setEnabled(False)
            self.deletePortButton.setEnabled(False)
            self.movePortUpButton.setEnabled(False)
            self.movePortDownButton.setEnabled(False)
            
    def ports_table_cell_was_clicked(self):
        self.reset_table_cells_background_color()
        sel_row = self.portsTable.currentRow()
        if self.portsTable.item(sel_row, 0) is not None:
            font = QtGui.QFont()
            font.setBold(True)
            for j in range(0, 5):
                self.portsTable.item(sel_row, j).setBackground(QtGui.QColor('#ffffdb'))
                self.portsTable.item(sel_row, j).setFont(font)
                
    def reset_table_cells_background_color(self):
        font = QtGui.QFont()
        font.setBold(False)
        i = 0
        while (self.portsTable.item(i, 0) is not None ):
            for j in range(0, 5):
                self.portsTable.item(i, j).setBackground(QtCore.Qt.white)
                self.portsTable.item(i, j).setFont(font)
            i += 1
        
    def load_parameters_table(self):
        parameters_list = self.fb.fb_parameters_list  
        length_parameters_list = len(parameters_list)
        
        if length_parameters_list > self.parametersTable.rowCount():
            self.parametersTable.setRowCount(length_parameters_list)
            
        for row in range(0, length_parameters_list):
            parameterName = parameters_list[row][0]
            if len(parameters_list[row]) > 4: #Temporary 
                if parameters_list[row][4] == False:
                    self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(parameterName))
                    parameterValue = parameters_list[row][1]
                    parameterUnit = parameters_list[row][2]
                    parameterNotes = parameters_list[row][3]
                    if len(parameters_list[row]) > 5:
                        parType = parameters_list[row][5]
                        if parType == 'check_box':       
                            self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                            self.parametersTable.item(row, 1).setBackground(QtGui.QColor(240,240,240,200))
                            self.parametersTable.setCellWidget(row, 1, QtWidgets.QCheckBox())
                            self.parametersTable.cellWidget(row, 1).setCheckState(int(parameterValue))
                            self.parametersTable.cellWidget(row, 1).setContentsMargins(0,0,0,0)
                            self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox::indicator {width:16px; height:16px;}')
                            self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox{margin-right:0%; margin-left:10%}')                            
                        elif parType == 'list': 
                            self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                            self.parametersTable.setCellWidget(row, 1, QtWidgets.QComboBox())
                            self.parametersTable.cellWidget(row, 1).setSizeAdjustPolicy(2)
                            if parameterNotes is not None: 
                                combo_list = parameterNotes.split(', ')
                                text_length_max = len(max(combo_list, key=len))
                                self.parametersTable.cellWidget(row, 1).addItems(combo_list)
                                self.parametersTable.cellWidget(row, 1).setMinimumContentsLength(text_length_max)
                                index = self.parametersTable.cellWidget(row, 1).findText(parameterValue)
                                if index >= 0:
                                    self.parametersTable.cellWidget(row, 1).setCurrentIndex(index)
                                else:
                                    self.parametersTable.cellWidget(row, 1).setCurrentIndex(0)
                            else:
                                combo_list = []
                                self.parametersTable.cellWidget(row, 1).addItems(combo_list)
                        else:
                            self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(parameterValue))
                    else:
                        self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(parameterValue))
                    self.parametersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(parameterUnit))
                    self.parametersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(parameterNotes))
            else:
                parameterValue = parameters_list[row][1]
                parameterUnit = parameters_list[row][2]
                parameterNotes = parameters_list[row][3]
                self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(parameterValue))
                self.parametersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(parameterUnit))
                self.parametersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(parameterNotes))  
        
        self.parametersTable.resizeColumnsToContents()         
        for row in range(0, length_parameters_list):
            if len(parameters_list[row]) > 4: 
                if parameters_list[row][4] == True:
                    parameterName = parameters_list[row][0]
                    self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(parameterName))
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.parametersTable.item(row, 0).setFont(font)
                    self.parametersTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
                    self.parametersTable.setSpan(row, 0, 1, 4)
        if self.parametersTable.columnWidth(3) > 400:
            self.parametersTable.setColumnWidth(3, 400)

    def insert_table_header(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            self.parametersTable.insertRow(row)
            self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem('Header'))
            font = QtGui.QFont()
            font.setBold(True)
            self.parametersTable.item(row, 0).setFont(font)
            self.parametersTable.setSpan(row, 0, 1, 4)
            self.parametersTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
            
    def insert_check_box(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            col = self.parametersTable.currentColumn()
            if col == 1:
                self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                self.parametersTable.item(row, 1).setBackground(QtGui.QColor(240,240,240,200))
                self.parametersTable.setCellWidget(row, 1, QtWidgets.QCheckBox())
                self.parametersTable.cellWidget(row, 1).setCheckState(0)
                self.parametersTable.cellWidget(row, 1).setContentsMargins(0,0,0,0)
                self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox::indicator {width:16px; height:16px;}')
                self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox{margin-right:0%; margin-left:10%}')
                
    def insert_list_box(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            col = self.parametersTable.currentColumn()
            if col == 1:
                self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                if self.parametersTable.item(row, 3) is not None:
                    item_list = self.parametersTable.item(row, 3).text()
                    combo_list = item_list.split(', ')
                    text_length_max = len(max(combo_list, key=len))
                    self.parametersTable.setCellWidget(row, 1, QtWidgets.QComboBox())
                    self.parametersTable.cellWidget(row, 1).addItems(combo_list)
                    self.parametersTable.cellWidget(row, 1).setSizeAdjustPolicy(2)
                    self.parametersTable.cellWidget(row, 1).setMinimumContentsLength(text_length_max)
                    
    def update_parameters(self):
        self.fb_view.save_parameters_list(self.fb)
        self.parametersTable.clearContents()
        self.load_parameters_table()
    
    def insert_table_row(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            self.parametersTable.insertRow(row)
            
    def delete_table_row(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            self.parametersTable.removeRow(row)
    
    def copy_table_row(self):        
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            self.check_box_present = False
            self.list_box_present = False
            self.header_present = False
            if self.parametersTable.columnSpan(row, 0) == 1:
                if self.parametersTable.item(row, 0) is not None:
                    self.parameterName = self.parametersTable.item(row, 0).text()
                else:
                    self.parameterName = None
                if type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QCheckBox:
                    self.parameterValue = str(self.parametersTable.cellWidget(row, 1).checkState())
                    self.check_box_present = True
                elif type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QComboBox:
                    self.parameterValue = self.parametersTable.cellWidget(row, 1).currentText()
                    self.list_box_present = True    
                elif self.parametersTable.item(row, 1) is not None:
                    self.parameterValue = self.parametersTable.item(row, 0).text()
                else:
                    self.parameterValue = None
                if self.parametersTable.item(row, 2) is not None:
                    self.parameterUnit = self.parametersTable.item(row, 2).text()
                else:
                    self.parameterUnit = None
                if self.parametersTable.item(row, 3) is not None:
                    self.parameterNotes = self.parametersTable.item(row, 3).text()
                else:
                    self.parameterNotes = None   
            else:
                self.header_present = True
                if self.parametersTable.item(row, 0) is not None:
                    self.parameterName = self.parametersTable.item(row, 0).text()
                else:
                    self.parameterName = None
            self.pasteRowButton.setEnabled(True)
    
    def paste_table_row(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            if self.header_present == False:
                self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(self.parameterName))
                if self.check_box_present == True:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                    self.parametersTable.item(row, 1).setBackground(QtGui.QColor(240,240,240,200))
                    self.parametersTable.setCellWidget(row, 1, QtWidgets.QCheckBox())
                    self.parametersTable.cellWidget(row, 1).setCheckState(int(self.parameterValue))
                    self.parametersTable.cellWidget(row, 1).setContentsMargins(0,0,0,0)
                    self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox::indicator {width:16px; height:16px;}')
                    self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox{margin-right:0%; margin-left:10%}')
                elif self.list_box_present == True:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                    if self.parameterNotes is not None:
                        combo_list = self.parameterNotes.split(', ')
                    else:
                        combo_list = []
                    text_length_max = len(max(combo_list, key=len))
                    self.parametersTable.setCellWidget(row, 1, QtWidgets.QComboBox())
                    self.parametersTable.cellWidget(row, 1).addItems(combo_list)  
                    self.parametersTable.cellWidget(row, 1).setSizeAdjustPolicy(2)
                    self.parametersTable.cellWidget(row, 1).setMinimumContentsLength(text_length_max)
                    index = self.parametersTable.cellWidget(row, 1).findText(self.parameterValue)
                    if index >= 0:
                        self.parametersTable.cellWidget(row, 1).setCurrentIndex(index)
                    else:
                        self.parametersTable.cellWidget(row, 1).setCurrentIndex(0)
                else:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(self.parameterValue))
                self.parametersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(self.parameterUnit))
                self.parametersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(self.parameterNotes))
            else:
                self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(self.parameterName))
                font = QtGui.QFont()
                font.setBold(True)
                self.parametersTable.item(row, 0).setFont(font)
                self.parametersTable.setSpan(row, 0, 1, 4)
                self.parametersTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
                    
    def move_row_up(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            if row != 0:
                if self.parametersTable.columnSpan(row, 0) == 1:
                    # Parameter name
                    if self.parametersTable.item(row, 0) is not None:
                        par_name = self.parametersTable.item(row, 0).text()
                    else:
                        par_name = None
                    # Parameter value  
                    if type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QCheckBox:
                        par_value = str(self.parametersTable.cellWidget(row, 1).checkState())
                    elif type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QComboBox:
                        par_value = self.parametersTable.cellWidget(row, 1).currentText()     
                    elif self.parametersTable.item(row, 1) is not None:
                        par_value = self.parametersTable.item(row, 1).text()
                    else:
                        par_value = None
                    # Parameter unit    
                    if self.parametersTable.item(row, 2) is not None:
                        par_unit = self.parametersTable.item(row, 2).text()
                    else:
                        par_unit = None
                    # Parameter notes   
                    if self.parametersTable.item(row, 3) is not None:
                        par_notes = self.parametersTable.item(row, 3).text()
                    else:
                        par_notes = None
                else:
                    if self.parametersTable.item(row, 0) is not None:
                        par_name = self.parametersTable.item(row, 0).text()
                    else:
                        par_name = None                  
                #Move up one row and insert row above
                row = row - 1
                self.parametersTable.insertRow(row)
                #Paste row items
                if self.parametersTable.columnSpan(row + 2, 0) == 1: #Regular parameter row
                    self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(par_name))
                    if type(self.parametersTable.cellWidget(row + 2, 1)) is QtWidgets.QCheckBox:
                        self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                        self.parametersTable.item(row, 1).setBackground(QtGui.QColor(240,240,240,200))
                        self.parametersTable.setCellWidget(row, 1, QtWidgets.QCheckBox())
                        self.parametersTable.cellWidget(row, 1).setCheckState(int(par_value))
                        self.parametersTable.cellWidget(row, 1).setContentsMargins(0,0,0,0)
                        self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox::indicator {width:16px; height:16px;}')
                        self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox{margin-right:0%; margin-left:10%}')
                    elif type(self.parametersTable.cellWidget(row + 2, 1)) is QtWidgets.QComboBox:
                        self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                        if par_notes is not None:
                            combo_list = par_notes.split(', ')
                        else:
                            combo_list = []
                        text_length_max = len(max(combo_list, key=len))
                        self.parametersTable.setCellWidget(row, 1, QtWidgets.QComboBox())
                        self.parametersTable.cellWidget(row, 1).addItems(combo_list)
                        self.parametersTable.cellWidget(row, 1).setSizeAdjustPolicy(2)
                        self.parametersTable.cellWidget(row, 1).setMinimumContentsLength(text_length_max)
                        index = self.parametersTable.cellWidget(row, 1).findText(par_value)
                        if index >= 0:
                            self.parametersTable.cellWidget(row, 1).setCurrentIndex(index)
                        else:
                            self.parametersTable.cellWidget(row, 1).setCurrentIndex(0)    
                    else:
                        self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(par_value))
                    self.parametersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(par_unit))
                    self.parametersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(par_notes))
                else: #Setup new header
                    self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(par_name))
                    font = QtGui.QFont()
                    font.setBold(True)
                    self.parametersTable.item(row, 0).setFont(font)
                    self.parametersTable.setSpan(row, 0, 1, 4)
                    self.parametersTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
                #Delete row that was copied
                row = row + 2
                self.parametersTable.removeRow(row)
                self.parametersTable.clearSelection()
                self.parametersTable.setCurrentCell(row-2, 0, QtCore.QItemSelectionModel.SelectCurrent)
                
    def move_row_down(self):
        if self.parametersTable.currentItem():
            row = self.parametersTable.currentRow()
            if row + 2 <= self.parametersTable.rowCount():
                if self.parametersTable.columnSpan(row, 0) == 1:
                    # Parameter name
                    if self.parametersTable.item(row, 0) is not None:
                        par_name = self.parametersTable.item(row, 0).text()
                    else:
                        par_name = None
                    # Parameter value    
                    if type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QCheckBox:
                        par_value = str(self.parametersTable.cellWidget(row, 1).checkState())
                    elif type(self.parametersTable.cellWidget(row, 1)) is QtWidgets.QComboBox:
                        par_value = self.parametersTable.cellWidget(row, 1).currentText()
                    elif self.parametersTable.item(row, 1) is not None:
                        par_value = self.parametersTable.item(row, 1).text()
                    else:
                        par_value = None
                    # Parameter unit
                    if self.parametersTable.item(row, 2) is not None:
                        par_unit = self.parametersTable.item(row, 2).text()
                    else:
                        par_unit = None
                    # Parameter notes
                    if self.parametersTable.item(row, 3) is not None:
                        par_notes = self.parametersTable.item(row, 3).text()
                    else:
                        par_notes = None
                else:
                    if self.parametersTable.item(row, 0) is not None:
                        par_name = self.parametersTable.item(row, 0).text()
                    else:
                        par_name = None                     
            #Move down one row and insert row above
            row = row + 2
            self.parametersTable.insertRow(row)
            #Paste row items
            if self.parametersTable.columnSpan(row - 2, 0) == 1: #Regular parameter row
                self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(par_name))
                if type(self.parametersTable.cellWidget(row - 2, 1)) is QtWidgets.QCheckBox:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                    self.parametersTable.item(row, 1).setBackground(QtGui.QColor(240,240,240,200))
                    self.parametersTable.setCellWidget(row, 1, QtWidgets.QCheckBox())
                    self.parametersTable.cellWidget(row, 1).setCheckState(int(par_value))
                    self.parametersTable.cellWidget(row, 1).setContentsMargins(0,0,0,0)
                    self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox::indicator {width:16px; height:16px;}')
                    self.parametersTable.cellWidget(row, 1).setStyleSheet('QCheckBox{margin-right:0%; margin-left:10%}')
                elif type(self.parametersTable.cellWidget(row - 2, 1)) is QtWidgets.QComboBox:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(''))
                    if par_notes is not None:
                        combo_list = par_notes.split(', ')
                    else:
                        combo_list = []
                    text_length_max = len(max(combo_list, key=len))
                    self.parametersTable.setCellWidget(row, 1, QtWidgets.QComboBox())
                    self.parametersTable.cellWidget(row, 1).addItems(combo_list)
                    self.parametersTable.cellWidget(row, 1).setSizeAdjustPolicy(2)
                    self.parametersTable.cellWidget(row, 1).setMinimumContentsLength(text_length_max)                    
                    index = self.parametersTable.cellWidget(row, 1).findText(par_value)
                    if index >= 0:
                        self.parametersTable.cellWidget(row, 1).setCurrentIndex(index)
                    else:
                        self.parametersTable.cellWidget(row, 1).setCurrentIndex(0)     
                else:
                    self.parametersTable.setItem(row, 1, QtWidgets.QTableWidgetItem(par_value))
                self.parametersTable.setItem(row, 2, QtWidgets.QTableWidgetItem(par_unit))
                self.parametersTable.setItem(row, 3, QtWidgets.QTableWidgetItem(par_notes))
            else: #Setup new header
                self.parametersTable.setItem(row, 0, QtWidgets.QTableWidgetItem(par_name))
                font = QtGui.QFont()
                font.setBold(True)
                self.parametersTable.item(row, 0).setFont(font)
                self.parametersTable.setSpan(row, 0, 1, 4)
                self.parametersTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
            #Delete row that was copied
            row = row - 2
            self.parametersTable.removeRow(row)
            self.parametersTable.clearSelection()
            self.parametersTable.setCurrentCell(row+1, 0, QtCore.QItemSelectionModel.SelectCurrent)
        
    def load_results_table(self):
        results_list = self.fb.fb_results_list
        length_results_list = len(results_list)        

        if length_results_list > self.dataTable.rowCount():
            self.dataTable.setRowCount(length_results_list)
        
        try:
            for row in range(0, length_results_list):
                resultName = results_list[row][0]
                if len(results_list[row]) > 4: #Temporary 
                    if results_list[row][4] == False:
                        self.dataTable.setItem(row, 0, QtWidgets.QTableWidgetItem(resultName))
                        resultValue = results_list[row][1]
                        resultUnit = results_list[row][2]
                        resultNotes = results_list[row][3]
                        resultFormat = '0.4E'   
                        if len(results_list[row]) > 5:
                            resultFormat = results_list[row][5] 
                        if resultValue is not 'NA':
                            resultValue = str(format(float(resultValue), resultFormat))
                        self.dataTable.setItem(row, 1, QtWidgets.QTableWidgetItem(resultValue))
                        self.dataTable.setItem(row, 2, QtWidgets.QTableWidgetItem(resultUnit))
                        self.dataTable.setItem(row, 3, QtWidgets.QTableWidgetItem(resultNotes))
                else:
                    resultValue = results_list[row][1]
                    resultUnit = results_list[row][2]
                    resultNotes = results_list[row][3]
                    self.dataTable.setItem(row, 1, QtWidgets.QTableWidgetItem(str(resultValue)))
                    self.dataTable.setItem(row, 2, QtWidgets.QTableWidgetItem(resultUnit))
                    self.dataTable.setItem(row, 3, QtWidgets.QTableWidgetItem(resultNotes))  
                           
            self.dataTable.resizeColumnsToContents()            
            for row in range(0, length_results_list):
                if len(results_list[row]) > 4:
                    if results_list[row][4] == True:
                        resultName = results_list[row][0]
                        self.dataTable.setItem(row, 0, QtWidgets.QTableWidgetItem(resultName))
                        font = QtGui.QFont()
                        font.setBold(True)
                        self.dataTable.item(row, 0).setFont(font)
                        self.dataTable.setSpan(row, 0, 1, 4)
                        self.dataTable.item(row, 0).setBackground(QtGui.QColor(240,240,240,127))
        except:
            e0 = sys.exc_info() [0]
            e1 = sys.exc_info() [1]
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Warning)
            syslab_icon = set_icon_window()
            msg.setWindowIcon(syslab_icon)
            msg.setText('Error loading output data (results) table')
            msg.setInformativeText(str(e0) + ' ' + str(e1))
            msg.setInformativeText(str(traceback.format_exc()))
            msg.setStyleSheet("QLabel{height: 150px; min-height: 150px; max-height: 150px;}")
            msg.setStyleSheet("QLabel{width: 500px; min-width: 400px; max-width: 500px;}")
            msg.setWindowTitle("Loading error (Output results)")
            msg.setStandardButtons(QtWidgets.QMessageBox.Ok)	
            rtnval = msg.exec()
            if rtnval == QtWidgets.QMessageBox.Ok:
                    msg.close()
            
    def select_font_color(self):
        current_color = QtGui.QColor(self.fontColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.fontColor.setText(color.name())
    
    def select_port_label_color(self):       
        current_color = QtGui.QColor(self.fontColorPortLabel.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.fontColorPortLabel.setText(color.name())            
        
    def select_color(self):
        current_color = QtGui.QColor(self.fillColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.fillColor.setText(color.name())
            self.items[0].setBrush(color)
    
    def select_color2(self):
        current_color = QtGui.QColor(self.fillColor2.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.fillColor2.setText(color.name())       

    def select_border_color(self):
        current_color = QtGui.QColor(self.borderColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(color)), 0.5 ))
            self.borderColor.setText(color.name())
        
    def add_port(self):
        addPort_win = AddPortDialog()
        addPort_win.show()
        if addPort_win.exec(): #Select Save (all port data will be added to the FB data model)
            self.update_ports_decision = True
            self.save_port_table_data() #Save/update port table data to FB ports list   
            self.editPortButton.setEnabled(True)
            self.deletePortButton.setEnabled(True)
            self.movePortUpButton.setEnabled(True)
            self.movePortDownButton.setEnabled(True)
        else: #Cancel (reload original table - prior to opening dialog)
            self.portsTable.clearContents()
            self.load_ports_table()
            
    def save_port_table_data(self):
        ports_list = window.project_scenes_list[self.key_index].fb_list[self.fb_key].fb_ports_list
        ports_list.clear()
        row = 0
        while (self.portsTable.item(row, 0) is not None):
            portName = self.portsTable.item(row, 0).text()
            if self.portsTable.item(row, 1) is not None:
                portName = self.portsTable.item(row, 1).text()
            else: 
                portName = None
            portCardinal =  self.portsTable.item(row, 2).text()
            portDirection =  self.portsTable.item(row, 3).text()
            sig = self.portsTable.item(row, 4).text()
            
            if sig == 'Disabled':
                ports_list_new_entry = [row+1, portName, portCardinal, 
                                        portDirection, sig, False, True]
            else:
                ports_list_new_entry = [row+1, portName, portCardinal, 
                                        portDirection, sig, False, False]
            ports_list.append(ports_list_new_entry)
            row += 1
            
    def edit_port(self):
        editPort_win = EditPortDialog()
        editPort_win.show()         
        row = 0
        while self.portsTable.item(row, 0):
            portID = self.portsTable.item(row, 0).text()
            editPort_win.portID.addItem(portID)
            row += 1    
        if self.portsTable.currentItem():
            sel_row = self.portsTable.currentRow()
            if self.portsTable.item(sel_row, 0) is not None:
                editPort_win.portID.setCurrentIndex(sel_row)
        if editPort_win.exec():
            self.update_ports_decision = True
            self.save_port_table_data() #Save/update port table data to FB ports list           
        else: #Cancel (reload original table - prior to opening dialog)
            self.portsTable.clearContents()
            self.load_ports_table()
            
    def delete_port(self):
        deletePort_win = DeletePortDialog()
        deletePort_win.show()          
        row = 0
        while self.portsTable.item(row, 0):
            portID = self.portsTable.item(row, 0).text()
            deletePort_win.portID.addItem(portID)
            row += 1  
        if self.portsTable.currentItem():
            sel_row = self.portsTable.currentRow()
            if sel_row != 0:
                deletePort_win.portID.setCurrentIndex(sel_row)
        if deletePort_win.exec():
            self.update_ports_decision = True
            self.save_port_table_data() #Save/update port table data to FB ports list           
        else: #Cancel (reload original table - prior to opening dialog)
            self.portsTable.clearContents()
            self.load_ports_table()
            
    def move_port_up(self):
        if self.portsTable.currentItem():
            row = self.portsTable.currentRow()
            if row != 0:
                #Copy row items (with exception of port ID)
                port_name = self.portsTable.item(row, 1).text()
                port_cd = self.portsTable.item(row, 2).text()
                port_dir = self.portsTable.item(row, 3).text()
                port_sig = self.portsTable.item(row, 4).text()
                #Move up one row and insert row above
                row = row - 1
                self.portsTable.insertRow(row)
                self.portsTable.clearSelection()
                #Paste row items
                self.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
                self.portsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(port_name))
                self.portsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(port_cd))
                self.portsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(port_dir))
                self.portsTable.setItem(row, 4, QtWidgets.QTableWidgetItem(port_sig))  
                font = QtGui.QFont()
                font.setBold(True)
                for j in range(0, 5):
                    self.portsTable.item(row, j).setBackground(QtGui.QColor('#ffffdb'))
                    self.portsTable.item(row, j).setFont(font)
                #Update port ID for row that was shifted down
                row = row + 1
                self.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
                #Delete row that was copied
                row = row + 1
                self.portsTable.removeRow(row)
                self.portsTable.clearSelection()
                self.portsTable.setCurrentCell(row-2, 0, QtCore.QItemSelectionModel.Select)
                self.update_ports_decision = True
                self.save_port_table_data()
                
    def move_port_down(self):
        if self.portsTable.currentItem():
            row = self.portsTable.currentRow()
            if self.portsTable.item(row+1, 1):
                #Copy row items (with exception of port ID)
                port_name = self.portsTable.item(row, 1).text()
                port_cd = self.portsTable.item(row, 2).text()
                port_dir = self.portsTable.item(row, 3).text()
                port_sig = self.portsTable.item(row, 4).text()
                #Move down one row and insert row above
                row = row + 2
                self.portsTable.insertRow(row)
                self.portsTable.clearSelection()
                #Paste row items
                self.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row)))
                self.portsTable.setItem(row, 1, QtWidgets.QTableWidgetItem(port_name))
                self.portsTable.setItem(row, 2, QtWidgets.QTableWidgetItem(port_cd))
                self.portsTable.setItem(row, 3, QtWidgets.QTableWidgetItem(port_dir))
                self.portsTable.setItem(row, 4, QtWidgets.QTableWidgetItem(port_sig))
                font = QtGui.QFont()
                font.setBold(True)
                for j in range(0, 5):
                    self.portsTable.item(row, j).setBackground(QtGui.QColor('#ffffdb'))
                    self.portsTable.item(row, j).setFont(font)
                #Update port ID for row that was shifted up
                row = row - 1
                self.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row)))
                #Delete row that was copied
                row = row - 1
                self.portsTable.removeRow(row)
                self.portsTable.clearSelection()
                self.portsTable.setCurrentCell(row+1, 0, QtCore.QItemSelectionModel.Select)
                self.update_ports_decision = True
                self.save_port_table_data()
            
           
class AddPortDialog (QtWidgets.QDialog, Ui_AddPort):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_AddPort.__init__(self)
        self.setupUi(self)  
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)

        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
        
    def apply(self):
        font = QtGui.QFont()
        font.setBold(False)
        i = 0
        while (FB_win.portsTable.item(i, 0) is not None ):
            for j in range(0, 5):
                FB_win.portsTable.item(i, j).setBackground(QtCore.Qt.white)
                FB_win.portsTable.item(i, j).setFont(font)
            i += 1
        
        portName = self.portName.text()         
        portCardinal = self.cardinalBox.currentText()
        portDirection = self.directionBox.currentText()
        sig = self.signalBox.currentText()
        
        i = 0
        while (FB_win.portsTable.item(i, 0) is not None ):
            i += 1 #Increment to next i
        if FB_win.portsTable.rowCount() == i:
            FB_win.portsTable.insertRow(i)
            
        FB_win.portsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i+1)))
        FB_win.portsTable.setItem(i, 1, QtWidgets.QTableWidgetItem(portName))
        FB_win.portsTable.setItem(i, 2, QtWidgets.QTableWidgetItem(portCardinal))
        FB_win.portsTable.setItem(i, 3, QtWidgets.QTableWidgetItem(portDirection))
        FB_win.portsTable.setItem(i, 4, QtWidgets.QTableWidgetItem(sig))  
        
        font.setBold(True)
        for j in range(0, 5):
            FB_win.portsTable.item(i, j).setBackground(QtGui.QColor('#ffffdb'))
            FB_win.portsTable.item(i, j).setFont(font)
    
      
class EditPortDialog (QtWidgets.QDialog, Ui_EditPort):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_EditPort.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        
        self.portID.currentIndexChanged.connect(self.port_id_selection_change)
        self.cardinalBox.currentIndexChanged.connect(self.port_cardinal_selection_change)
        self.directionBox.currentIndexChanged.connect(self.port_direction_selection_change)
        self.signalBox.currentIndexChanged.connect(self.signal_type_selection_change)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
        
    def port_id_selection_change(self): 
        # Reset all background colors to white and fonts to normal
        font = QtGui.QFont()
        font.setBold(False)
        i = 0
        while (FB_win.portsTable.item(i, 0) is not None ):
            for j in range(0, 5):
                FB_win.portsTable.item(i, j).setBackground(QtCore.Qt.white)
                FB_win.portsTable.item(i, j).setFont(font)
            i += 1
        # Retrieve port ID from menu selection
        ID = self.portID.currentText()
        self.row = 0
        while (FB_win.portsTable.item(self.row, 0).text() != ID):
            self.row += 1 #Increment to next i 
        # Set background color of row to yellow (to identiy which row is being edited)
        font.setBold(True)
        for i in range(0, 5):
            FB_win.portsTable.item(self.row, i).setBackground(QtGui.QColor('#ffffdb'))
            FB_win.portsTable.item(self.row, i).setFont(font)
        # Retrieve current port settings for selected work
        if FB_win.portsTable.item(self.row, 1) is not None:
            portName = FB_win.portsTable.item(self.row, 1).text()
        else: 
            portName = None
        portCardinal =  FB_win.portsTable.item(self.row, 2).text()
        portDirection =  FB_win.portsTable.item(self.row, 3).text()
        sig = FB_win.portsTable.item(self.row, 4).text()
        # Retrieve any changes and update the table row
        self.portName.setText(portName)
        self.portCardinal.setText(portCardinal)
        self.portDirection.setText(portDirection)
        self.signalType.setText(sig)
        self.cardinalBox.setCurrentText(portCardinal)
        self.directionBox.setCurrentText(portDirection)
        self.signalBox.setCurrentText(sig)       
    
    def port_cardinal_selection_change(self):
        self.portCardinal.setText(self.cardinalBox.currentText())
            
    def port_direction_selection_change(self):
        self.portDirection.setText(self.directionBox.currentText())  
    
    def signal_type_selection_change(self):
        self.signalType.setText(self.signalBox.currentText())
            
    def apply(self):  
        font = QtGui.QFont()
        font.setBold(True)
        FB_win.portsTable.setItem(self.row, 1, 
                                  QtWidgets.QTableWidgetItem(self.portName.text()))
        FB_win.portsTable.setItem(self.row, 2,
                                  QtWidgets.QTableWidgetItem(self.portCardinal.text()))
        FB_win.portsTable.setItem(self.row, 3,
                                  QtWidgets.QTableWidgetItem(self.portDirection.text()))
        FB_win.portsTable.setItem(self.row, 4,
                                  QtWidgets.QTableWidgetItem(self.signalType.text()))
        for i in range(0, 5):
            FB_win.portsTable.item(self.row, i).setBackground(QtGui.QColor('#ffffdb'))
            FB_win.portsTable.item(self.row, i).setFont(font)
       

class DeletePortDialog (QtWidgets.QDialog, Ui_DeletePort):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_DeletePort.__init__(self)
        self.setupUi(self)  
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.portID.currentIndexChanged.connect(self.port_id_selection_change)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowStaysOnTopHint)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Apply).clicked.connect(self.apply)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
        
    def port_id_selection_change(self): 
        font = QtGui.QFont()
        font.setBold(False)
        i = 0
        while (FB_win.portsTable.item(i, 0) is not None ):
            for j in range(0, 5):
                FB_win.portsTable.item(i, j).setBackground(QtCore.Qt.white)
                FB_win.portsTable.item(i, j).setFont(font)
            i += 1
        ID = self.portID.currentText()
        self.row = 0
        while (FB_win.portsTable.item(self.row, 0).text() != ID):
            self.row += 1 #Increment to next i 
        # Set background color of row to yellow (to identiy which row is being edited)
        font.setBold(True)
        for i in range(0, 5):
            FB_win.portsTable.item(self.row, i).setBackground(QtGui.QColor('#ffffdb'))
            FB_win.portsTable.item(self.row, i).setFont(font)
            
        if FB_win.portsTable.item(self.row, 1) is not None:
            portName = FB_win.portsTable.item(self.row, 1).text()
        else: 
            portName = None  
        self.portName.setText(portName)
        
    def apply(self):
        #Delete row
        FB_win.portsTable.removeRow(self.row)
        
        #Reset port IDs (table)
        row = 0
        while FB_win.portsTable.item(row, 0):
            FB_win.portsTable.setItem(row, 0, QtWidgets.QTableWidgetItem(str(row+1)))
            row += 1 
            
class FunctionalBlockDimensions(QtWidgets.QDialog, Ui_FBDimWindow):
    '''GUI interface for updating functional block dimensions
    '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_FBDimWindow.__init__(self)
        #Perform setup of main SystemLab view (designed via QT Designer)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        
                   
class SimulationStatusGUI(QtWidgets.QDialog, Ui_SimStatus):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_SimStatus.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.setWindowFlags(self.windowFlags()|QtCore.Qt.WindowMinimizeButtonHint)  
        #Version tracking
        self.__version = 1
                
    def check_version(self):
        pass #No check needed for version 1
        
    def text_update(self, text):
        self.textEdit.append(text)
        
    def update_progress_bar(self, progress):
        self.progressBar.setValue(progress)

        
class SimulationDataGUI(QtWidgets.QDialog, Ui_SimData):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_SimData.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        #Version tracking
        self.__version = 1
         
    def check_version(self):
        pass #No check needed for version 1
         
        
class DescriptionBoxGUI(QtWidgets.QDialog, Ui_DescWindow):
    '''
    '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_DescWindow.__init__(self)
        self.setupUi(self)  
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        
        #DIALOG USER ACTIONS
        self.colorFillButton.clicked.connect(self.select_color)
        self.colorFillButton2.clicked.connect(self.select_color2)
        self.colorFontButton.clicked.connect(self.select_font_color)
        self.colorBorderButton.clicked.connect(self.select_border_color)
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        self.items = window.project_scenes_list[self.key_index].selectedItems()
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
    
    def select_color(self):
        current_color = QtGui.QColor(desc_win.fillColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].setBrush(color)
            desc_win.fillColor.setText(color.name())
            
    def select_color2(self):
        current_color = QtGui.QColor(desc_win.fillColor2.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            desc_win.fillColor2.setText(color.name())            
            
    def select_font_color(self):
        current_color = QtGui.QColor(desc_win.fontColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            desc_win.fontColor.setText(color.name())

    def select_border_color(self):
        current_color = QtGui.QColor(desc_win.borderColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(color)), 0.5 ))
            desc_win.borderColor.setText(color.name())
            
            
class LineArrowGUI(QtWidgets.QDialog, Ui_LineWindow):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_LineWindow.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        self.colorButton.clicked.connect(self.select_color)
        tab_index, key_index = retrieve_current_project_key_index()
        self.items = window.project_scenes_list[key_index].selectedItems()
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
    
    def select_color(self):
        current_color = QtGui.QColor(line_win.lineColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            for item in self.items:
                if type(item) is LineArrowDesignView:
                    item.setPen(color)
                    line_win.lineColor.setText(color.name()) 

     
class DataBoxGUI(QtWidgets.QDialog, Ui_DataWindow):
    '''
    '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_DataWindow.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)
        
        #DIALOG USER ACTIONS
        self.titleColorFillButton.clicked.connect(self.select_title_color)
        self.titleColorBorderButton.clicked.connect(self.select_title_border_color)
        self.titleColorFontButton.clicked.connect(self.select_title_font_color)
        self.dataBorderColorButton.clicked.connect(self.select_data_border_color)
        self.dataFillColorButton.clicked.connect(self.select_data_color)
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        self.items = window.project_scenes_list[self.key_index].selectedItems()
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
    
    def select_title_color(self):
        current_color = QtGui.QColor(data_win.title_box_fill_color.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].title_box.setBrush(color)
            data_win.title_box_fill_color.setText(color.name())

    def select_title_font_color(self):
        current_color = QtGui.QColor(data_win.title_font_color.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            data_win.title_font_color.setText(color.name())   
            
    def select_title_border_color(self):
        current_color = QtGui.QColor(data_win.title_border_color.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].title_box.setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(color)),
                                                      0.5 ))
            data_win.title_border_color.setText(color.name())             
            
    def select_data_color(self):
        current_color = QtGui.QColor(data_win.data_box_fill_color.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].setBrush(color)
            data_win.data_box_fill_color.setText(color.name())
            
    def select_data_border_color(self):
        current_color = QtGui.QColor(data_win.data_border_color.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            self.items[0].setPen(QtGui.QPen(QtGui.QBrush(QtGui.QColor(color)), 0.5 ))
            data_win.data_border_color.setText(color.name())
            
class TextBoxGUI(QtWidgets.QDialog, Ui_TextWindow):
    '''
    '''
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_TextWindow.__init__(self)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.setStyleSheet(app_font_default)

        #DIALOG USER ACTIONS
        self.colorFontButton.clicked.connect(self.select_color)
        self.tab_index, self.key_index = retrieve_current_project_key_index()
        self.items = window.project_scenes_list[self.key_index].selectedItems()
        
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
    
    def select_color(self):
        current_color = QtGui.QColor(text_win.fontColor.text())
        color = QtWidgets.QColorDialog.getColor(current_color)
        if color.isValid():
            text_win.fontColor.setText(color.name())
            
class ProjectListGUI(QtWidgets.QDialog, Ui_ProjectList):
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_ProjectList.__init__(self)
        #Perform setup of project properties dialog (designed via QT Designer)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        self.projectsBox.currentIndexChanged.connect(self.project_type_selection_change)
        self.setStyleSheet(app_font_default)
        #Version tracking
        self.__version = 1
        
    def check_version(self):
        pass #No check needed for version 1
        
    def project_type_selection_change(self):
        self.projectType.setText(self.projectsBox.currentText())
        
class AboutGUI(QtWidgets.QDialog, Ui_About):
    
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_About.__init__(self)
        #Perform setup of project properties dialog (designed via QT Designer)
        self.setupUi(self)
        syslab_icon = set_icon_window()
        self.setWindowIcon(syslab_icon)
        #Version tracking
        self.__version = 1
        
        image_path = os.path.join(root_path, 'syslab_gui_files', 'SystemLab_Design_About_Image.png')
        self.textEditImage.setHtml("<img src = \""+ image_path +"\" alt = \"\"/>")
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Base, QtGui.QColor(240, 240, 240))
        self.textEditImage.setPalette(palette)
        self.textEditImage.show()
        
    def check_version(self):
        pass #No check needed for version 1
        
'''FUNCTIONS==========================================================================='''
def retrieve_current_project_key_index():
    tab_index = window.tabWidget.currentIndex()
    project_name = window.tabWidget.tabText(tab_index)
    key_index = window.project_names_list.get(project_name)
    return tab_index, key_index

def set_line_type(line_type):
    if line_type == 'SolidLine':
        style = QtCore.Qt.SolidLine
    elif line_type == 'DashLine':
        style = QtCore.Qt.DashLine
    elif line_type == 'DotLine':
        style = QtCore.Qt.DotLine
    else:
        style = QtCore.Qt.NoPen        
    return style
           
def set_new_key(object_list):
    i = 1 
    while (i in object_list): #Set new key for object dictionary
        i += 1 
    return i

def set_icon_window():
    icon_path = os.path.join(root_path, 'syslab_gui_icons', 'SysLab_64.png')
    icon_path = os.path.normpath(icon_path)
    icon = QtGui.QIcon()
    icon.addFile(icon_path)
    return icon
      
'''MAIN APPLICATION===================================================================='''
if __name__ == '__main__':
#    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_Use96Dpi)    
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    
    # Create instance of class SystemLabMainApp and display
    config.app = QtWidgets.QApplication(sys.argv)
#    print(sys.argv[0])
    config.app.setStyle("fusion")
    
    # Build and display flash screen
    splash_image = os.path.join(root_path, 'SplashScreen_SystemLab.png')
    splash_pix = QtGui.QPixmap(splash_image)
    splash = QtWidgets.QSplashScreen(splash_pix)
    splash.show()
    time_data.sleep(3)
    config.app.processEvents()
    
    # Display main config.application interface (object instance: window)
    config.app.aboutToQuit.connect(config.app.deleteLater)
    global window
    window = SystemLabMainApp()
    window.show()
    
    splash.finish(window)
    
    #Create hash digest of default start project (to track modifications)
    dict_list_image = window.project_scenes_list[1].prepare_project_data_and_items()
    window.hash_list_open[1] = hashlib.sha256(str(dict_list_image).encode()).hexdigest()
    # System exit     
    sys.exit(config.app.exec_())
'''===================================================================================='''