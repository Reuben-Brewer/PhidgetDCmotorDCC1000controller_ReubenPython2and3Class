# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com
www.reubotics.com

Apache 2 License
Software Revision F, 05/10/2023

Verified working on: Python 2.7, 3.8 for Windows 8.1, 10 64-bit and Raspberry Pi Buster (no Mac testing yet).
'''

__author__ = 'reuben.brewer'

###########################################################
from PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import collections
###########################################################

###########################################################
if sys.version_info[0] < 3:
    from Tkinter import * #Python 2
    import tkFont
    import ttk
else:
    from tkinter import * #Python 3
    import tkinter.font as tkFont #Python 3
    from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

###########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG

    global PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject
    global DC30AmpCurrentSensor_OPEN_FLAG
    global SHOW_IN_GUI_DC30AmpCurrentSensor_FLAG

    global MyPrint_ReubenPython2and3ClassObject
    global MYPRINT_OPEN_FLAG
    global SHOW_IN_GUI_MYPRINT_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            if DC30AmpCurrentSensor_OPEN_FLAG == 1 and SHOW_IN_GUI_DC30AmpCurrentSensor_FLAG == 1:
                PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            #########################################################
            if MYPRINT_OPEN_FLAG == 1 and SHOW_IN_GUI_MYPRINT_FLAG == 1:
                MyPrint_ReubenPython2and3ClassObject.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback():
    global EXIT_PROGRAM_FLAG

    print("ExitProgram_Callback event fired!")

    EXIT_PROGRAM_FLAG = 1
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_Thread():
    global root
    global root_Xpos
    global root_Ypos
    global root_width
    global root_height
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_TABS_IN_GUI_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_DC30AmpCurrentSensor
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_DC30AmpCurrentSensor = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_DC30AmpCurrentSensor, text='   CurrentSensor   ')

        Tab_MainControls = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MainControls, text='   Main Controls   ')

        Tab_MyPrint = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_MyPrint, text='   MyPrint Terminal   ')

        TabControlObject.pack(expand=1, fill="both")  # CANNOT MIX PACK AND GRID IN THE SAME FRAME/TAB, SO ALL .GRID'S MUST BE CONTAINED WITHIN THEIR OWN FRAME/TAB.

        ############# #Set the tab header font
        TabStyle = ttk.Style()
        TabStyle.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'))
        #############
        #################################################
    else:
        #################################################
        Tab_MainControls = root
        Tab_DC30AmpCurrentSensor = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    #################################################
    #################################################
    global my_platform

    if platform.system() == "Linux":

        if "raspberrypi" in platform.uname():  # os.uname() doesn't work in windows
            my_platform = "pi"
        else:
            my_platform = "linux"

    elif platform.system() == "Windows":
        my_platform = "windows"

    elif platform.system() == "Darwin":
        my_platform = "mac"

    else:
        my_platform = "other"

    print("The OS platform is: " + my_platform)
    #################################################
    #################################################

    #################################################
    #################################################
    global USE_GUI_FLAG
    USE_GUI_FLAG = 1

    global USE_TABS_IN_GUI_FLAG
    USE_TABS_IN_GUI_FLAG = 1

    global USE_DC30AmpCurrentSensor_FLAG
    USE_DC30AmpCurrentSensor_FLAG = 1

    global USE_MYPRINT_FLAG
    USE_MYPRINT_FLAG = 1

    global USE_PLOTTER_FLAG
    USE_PLOTTER_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_DC30AmpCurrentSensor_FLAG
    SHOW_IN_GUI_DC30AmpCurrentSensor_FLAG = 1

    global SHOW_IN_GUI_MYPRINT_FLAG
    SHOW_IN_GUI_MYPRINT_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_DC30AmpCurrentSensor
    global GUI_COLUMN_DC30AmpCurrentSensor
    global GUI_PADX_DC30AmpCurrentSensor
    global GUI_PADY_DC30AmpCurrentSensor
    global GUI_ROWSPAN_DC30AmpCurrentSensor
    global GUI_COLUMNSPAN_DC30AmpCurrentSensor
    GUI_ROW_DC30AmpCurrentSensor = 1

    GUI_COLUMN_DC30AmpCurrentSensor = 0
    GUI_PADX_DC30AmpCurrentSensor = 1
    GUI_PADY_DC30AmpCurrentSensor = 1
    GUI_ROWSPAN_DC30AmpCurrentSensor = 1
    GUI_COLUMNSPAN_DC30AmpCurrentSensor = 1

    global GUI_ROW_MYPRINT
    global GUI_COLUMN_MYPRINT
    global GUI_PADX_MYPRINT
    global GUI_PADY_MYPRINT
    global GUI_ROWSPAN_MYPRINT
    global GUI_COLUMNSPAN_MYPRINT
    GUI_ROW_MYPRINT = 2

    GUI_COLUMN_MYPRINT = 0
    GUI_PADX_MYPRINT = 1
    GUI_PADY_MYPRINT = 1
    GUI_ROWSPAN_MYPRINT = 1
    GUI_COLUMNSPAN_MYPRINT = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global EXIT_PROGRAM_FLAG
    EXIT_PROGRAM_FLAG = 0

    global CurrentTime_MainLoopThread
    CurrentTime_MainLoopThread = -11111.0

    global StartingTime_MainLoopThread
    StartingTime_MainLoopThread = -11111.0

    global root

    global root_Xpos
    root_Xpos = 900

    global root_Ypos
    root_Ypos = 0

    global root_width
    root_width = 1920 - root_Xpos

    global root_height
    root_height = 1020 - root_Ypos

    global TabControlObject
    global Tab_MainControls
    global Tab_DC30AmpCurrentSensor
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject

    global DC30AmpCurrentSensor_OPEN_FLAG
    DC30AmpCurrentSensor_OPEN_FLAG = -1

    global DC30AmpCurrentSensor_MostRecentDict
    DC30AmpCurrentSensor_MostRecentDict = dict()

    global DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Raw
    DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Raw = [-11111.0]*1

    global DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Filtered
    DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Filtered = [-11111.0]*1

    global DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_CurrentDerivative_AmpsPerSec
    DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_CurrentDerivative_AmpsPerSec = [-11111.0]*1

    global DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_ErrorCallbackFiredFlag
    DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_ErrorCallbackFiredFlag = [-1]*1

    global DC30AmpCurrentSensor_MostRecentDict_Time
    DC30AmpCurrentSensor_MostRecentDict_Time = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_ReubenPython2and3ClassObject

    global MYPRINT_OPEN_FLAG
    MYPRINT_OPEN_FLAG = -1
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject

    global PLOTTER_OPEN_FLAG
    PLOTTER_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = -1

    global LastTime_MainLoopThread_PLOTTER
    LastTime_MainLoopThread_PLOTTER = -11111.0
    #################################################
    #################################################

    #################################################  KEY GUI LINE
    #################################################
    if USE_GUI_FLAG == 1:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread)
        GUI_Thread_ThreadingObject.setDaemon(True) #Should mean that the GUI thread is destroyed automatically when the main thread is destroyed.
        GUI_Thread_ThreadingObject.start()
        time.sleep(0.5)  #Allow enough time for 'root' to be created that we can then pass it into other classes.
    else:
        root = None
        Tab_MainControls = None
        Tab_DC30AmpCurrentSensor = None
        Tab_MyPrint = None
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_GUIparametersDict
    PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_DC30AmpCurrentSensor_FLAG),
                                    ("root", Tab_DC30AmpCurrentSensor),
                                    ("EnableInternal_MyPrint_Flag", 1),
                                    ("NumberOfPrintLines", 10),
                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                    ("GUI_ROW", GUI_ROW_DC30AmpCurrentSensor),
                                    ("GUI_COLUMN", GUI_COLUMN_DC30AmpCurrentSensor),
                                    ("GUI_PADX", GUI_PADX_DC30AmpCurrentSensor),
                                    ("GUI_PADY", GUI_PADY_DC30AmpCurrentSensor),
                                    ("GUI_ROWSPAN", GUI_ROWSPAN_DC30AmpCurrentSensor),
                                    ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_DC30AmpCurrentSensor)])

    global PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_setup_dict
    PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                ("VINT_DesiredSerialNumber", -1), #-1 MEANS ANY SN, CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                                ("VINT_DesiredPortNumber", 0), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                                ("DesiredDeviceID", 105),
                                                                                ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                                ("NameToDisplay_UserSet", "Reuben's Test VCP1100 Current Sensor Board"),
                                                                                ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                                ("DataCallbackUpdateDeltaT_ms", 20),
                                                                                ("CurrentSensorList_Current_Amps_ExponentialFilterLambda", [0.95]),
                                                                                ("CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda", [0.5])]) #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

    if USE_DC30AmpCurrentSensor_FLAG == 1:
        try:
            PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject = PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class(PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject_setup_dict)
            DC30AmpCurrentSensor_OPEN_FLAG = PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions, 0)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1:

        MyPrint_ReubenPython2and3ClassObject_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MYPRINT_FLAG),
                                                                        ("root", Tab_MyPrint),
                                                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                        ("GUI_ROW", GUI_ROW_MYPRINT),
                                                                        ("GUI_COLUMN", GUI_COLUMN_MYPRINT),
                                                                        ("GUI_PADX", GUI_PADX_MYPRINT),
                                                                        ("GUI_PADY", GUI_PADY_MYPRINT),
                                                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MYPRINT),
                                                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MYPRINT)])

        MyPrint_ReubenPython2and3ClassObject_setup_dict = dict([("NumberOfPrintLines", 10),
                                                                ("WidthOfPrintingLabel", 200),
                                                                ("PrintToConsoleFlag", 1),
                                                                ("LogFileNameFullPath", os.getcwd() + "//TestLog.txt"),
                                                                ("GUIparametersDict", MyPrint_ReubenPython2and3ClassObject_GUIparametersDict)])

        try:
            MyPrint_ReubenPython2and3ClassObject = MyPrint_ReubenPython2and3Class(MyPrint_ReubenPython2and3ClassObject_setup_dict)
            MYPRINT_OPEN_FLAG = MyPrint_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_ReubenPython2and3ClassObject __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                                                ("NumberOfPrintLines", 10),
                                                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                                ("GraphCanvasWidth", 890),
                                                                                                ("GraphCanvasHeight", 700),
                                                                                                ("GraphCanvasWindowStartingX", 0),
                                                                                                ("GraphCanvasWindowStartingY", 0),
                                                                                                ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 20)])

    global MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict
    MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_GUIparametersDict),
                                                                                        ("ParentPID", os.getpid()),
                                                                                        ("WatchdogTimerExpirationDurationSeconds_StandAlonePlottingProcess", 5.0),
                                                                                        ("MarkerSize", 3),
                                                                                        ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Raw", "Filtered", "Derivative"]),("ColorList", ["Red", "Blue", "Green"])])),
                                                                                        ("NumberOfDataPointToPlot", 50),
                                                                                        ("XaxisNumberOfTickMarks", 10),
                                                                                        ("YaxisNumberOfTickMarks", 10),
                                                                                        ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                                                        ("XaxisAutoscaleFlag", 1),
                                                                                        ("YaxisAutoscaleFlag", 1),
                                                                                        ("X_min", 0.0),
                                                                                        ("X_max", 20.0),
                                                                                        ("Y_min", -30.0),
                                                                                        ("Y_max", 30.0),
                                                                                        ("XaxisDrawnAtBottomOfGraph", 0),
                                                                                        ("XaxisLabelString", "Time (sec)"),
                                                                                        ("YaxisLabelString", "Y-units (units)"),
                                                                                        ("ShowLegendFlag", 1)])

    if USE_PLOTTER_FLAG == 1:
        try:
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_setup_dict)
            PLOTTER_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_DC30AmpCurrentSensor_FLAG == 1 and DC30AmpCurrentSensor_OPEN_FLAG != 1:
        print("Failed to open PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MYPRINT_FLAG == 1 and MYPRINT_OPEN_FLAG != 1:
        print("Failed to open MyPrint_ReubenPython2and3ClassObject.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_PLOTTER_FLAG == 1 and PLOTTER_OPEN_FLAG != 1:
        print("Failed to open MyPlotterPureTkinterClass_Object.")
        ExitProgram_Callback()
    #################################################
    #################################################

    #################################################
    #################################################
    #################################################
    print("Starting main loop 'test_program_for_PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        ####################################################
        ####################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        ####################################################
        ####################################################

        #################################################### GET's
        ####################################################
        if DC30AmpCurrentSensor_OPEN_FLAG == 1:

            DC30AmpCurrentSensor_MostRecentDict = PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "Time" in DC30AmpCurrentSensor_MostRecentDict:
                DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Raw = DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_Current_Amps_Raw"]
                DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Filtered = DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_Current_Amps_Filtered"]
                DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_CurrentDerivative_AmpsPerSec = DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_CurrentDerivative_AmpsPerSec"]
                DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_ErrorCallbackFiredFlag = DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_ErrorCallbackFiredFlag"]
                DC30AmpCurrentSensor_MostRecentDict_Time = DC30AmpCurrentSensor_MostRecentDict["Time"]

                #print("DC30AmpCurrentSensor_MostRecentDict_Time: " + str(DC30AmpCurrentSensor_MostRecentDict_Time))
        ####################################################
        ####################################################

        ####################################################
        ####################################################
        if PLOTTER_OPEN_FLAG == 1:

            ####################################################
            MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict:
                MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject_MostRecentDict_StandAlonePlottingProcess_ReadyForWritingFlag == 1:
                    if CurrentTime_MainLoopThread - LastTime_MainLoopThread_PLOTTER >= 0.040:
                        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExternalAddPointOrListOfPointsToPlot(["Raw", "Filtered", "Derivative"], [CurrentTime_MainLoopThread]*3, [DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Raw, DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_Current_Amps_Filtered, DC30AmpCurrentSensor_MostRecentDict_CurrentSensorList_CurrentDerivative_AmpsPerSec])
                        LastTime_MainLoopThread_PLOTTER = CurrentTime_MainLoopThread
            ####################################################

        ####################################################
        ####################################################

        time.sleep(0.002)
    #################################################
    #################################################
    #################################################

    ################################################# THIS IS THE EXIT ROUTINE!
    #################################################
    print("Exiting main program 'test_program_for_PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class.")

    #################################################
    if DC30AmpCurrentSensor_OPEN_FLAG == 1:
        PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if MYPRINT_OPEN_FLAG == 1:
        MyPrint_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    if PLOTTER_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3ClassObject.ExitProgram_Callback()
    #################################################

    #################################################
    #################################################

##########################################################################################################
##########################################################################################################