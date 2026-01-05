# -*- coding: utf-8 -*-

'''
Reuben Brewer, Ph.D.
reuben.brewer@gmail.com,
www.reubotics.com

Apache 2 License
Software Revision G, 12/31/2025

Verified working on: Python 3.12/13 for Windows 10/11 64-bit and Raspberry Pi Bookworm (no Mac testing yet, but might work while not in GUI-mode).
'''

__author__ = 'reuben.brewer'

##########################################################################################################
##########################################################################################################

###########################################################
import ReubenGithubCodeModulePaths #Replaces the need to have "ReubenGithubCodeModulePaths.pth" within "C:\Anaconda3\Lib\site-packages".
ReubenGithubCodeModulePaths.Enable()
###########################################################

###########################################################
from MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class import *
from MyPrint_ReubenPython2and3Class import *
from PhidgetDCmotorDCC1000controller_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import threading
import math
import traceback
import collections
import keyboard
###########################################################

###########################################################
from tkinter import *
import tkinter.font as tkFont
from tkinter import ttk
###########################################################

###########################################################
import platform
if platform.system() == "Windows":
    import ctypes
    winmm = ctypes.WinDLL('winmm')
    winmm.timeBeginPeriod(1) #Set minimum timer resolution to 1ms so that time.sleep(0.001) behaves properly.
###########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def GetLatestWaveformValue(CurrentTime, MinValue, MaxValue, Period, WaveformTypeString="Sine"):

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            ##########################################################################################################
            OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            WaveformTypeString_ListOfAcceptableValues = ["Sine", "Cosine", "Triangular", "Square"]

            if WaveformTypeString not in WaveformTypeString_ListOfAcceptableValues:
                print("GetLatestWaveformValue: Error, WaveformTypeString must be in " + str(WaveformTypeString_ListOfAcceptableValues))
                return -11111.0
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if WaveformTypeString == "Sine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Cosine":

                TimeGain = math.pi/Period
                OutputValue = (MaxValue + MinValue)/2.0 + 0.5*abs(MaxValue - MinValue)*math.cos(TimeGain*CurrentTime)
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Triangular":
                TriangularInput_TimeGain = 1.0
                TriangularInput_MinValue = -5
                TriangularInput_MaxValue = 5.0
                TriangularInput_PeriodInSeconds = 2.0

                #TriangularInput_Height0toPeak = abs(TriangularInput_MaxValue - TriangularInput_MinValue)
                #TriangularInput_CalculatedValue_1 = abs((TriangularInput_TimeGain*CurrentTime_CalculatedFromMainThread % PeriodicInput_PeriodInSeconds) - TriangularInput_Height0toPeak) + TriangularInput_MinValue

                A = abs(MaxValue - MinValue)
                P = Period

                #https://stackoverflow.com/questions/1073606/is-there-a-one-line-function-that-generates-a-triangle-wave
                OutputValue = (A / (P / 2)) * ((P / 2) - abs(CurrentTime % (2 * (P / 2)) - P / 2)) + MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            elif WaveformTypeString == "Square":

                TimeGain = math.pi/Period
                MeanValue = (MaxValue + MinValue)/2.0
                SinusoidalValue =  MeanValue + 0.5*abs(MaxValue - MinValue)*math.sin(TimeGain*CurrentTime)

                if SinusoidalValue >= MeanValue:
                    OutputValue = MaxValue
                else:
                    OutputValue = MinValue
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            else:
                OutputValue = 0.0
            ##########################################################################################################
            ##########################################################################################################

            return OutputValue

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        except:
            exceptions = sys.exc_info()[0]
            print("GetLatestWaveformValue: Exceptions: %s" % exceptions)
            #return -11111.0
            traceback.print_exc()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def getPreciseSecondsTimeStampString():
    ts = time.time()

    return ts
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

    number_of_decimal_places = max(1, number_of_decimal_places) #Make sure we're above 1

    ListOfStringsToJoin = []

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if isinstance(input, str) == 1:
        ListOfStringsToJoin.append(input)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, int) == 1 or isinstance(input, float) == 1:
        element = float(input)
        prefix_string = "{:." + str(number_of_decimal_places) + "f}"
        element_as_string = prefix_string.format(element)

        ##########################################################################################################
        ##########################################################################################################
        if element >= 0:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1)  # +1 for sign, +1 for decimal place
            element_as_string = "+" + element_as_string  # So that our strings always have either + or - signs to maintain the same string length
        else:
            element_as_string = element_as_string.zfill(number_of_leading_numbers + number_of_decimal_places + 1 + 1 + 1)  # +1 for sign, +1 for decimal place
        ##########################################################################################################
        ##########################################################################################################

        ListOfStringsToJoin.append(element_as_string)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, list) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append(ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, tuple) == 1:

        if len(input) > 0:
            for element in input: #RECURSION
                ListOfStringsToJoin.append("TUPLE" + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a list() or []
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    elif isinstance(input, dict) == 1:

        if len(input) > 0:
            for Key in input: #RECURSION
                ListOfStringsToJoin.append(str(Key) + ": " + ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

        else: #Situation when we get a dict()
            ListOfStringsToJoin.append(str(input))

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    else:
        ListOfStringsToJoin.append(str(input))
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if len(ListOfStringsToJoin) > 1:

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        StringToReturn = ""
        for Index, StringToProcess in enumerate(ListOfStringsToJoin):

            ################################################
            if Index == 0: #The first element
                if StringToProcess.find(":") != -1 and StringToProcess[0] != "{": #meaning that we're processing a dict()
                    StringToReturn = "{"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[0] != "(":  # meaning that we're processing a tuple
                    StringToReturn = "("
                else:
                    StringToReturn = "["

                StringToReturn = StringToReturn + StringToProcess.replace("TUPLE","") + ", "
            ################################################

            ################################################
            elif Index < len(ListOfStringsToJoin) - 1: #The middle elements
                StringToReturn = StringToReturn + StringToProcess + ", "
            ################################################

            ################################################
            else: #The last element
                StringToReturn = StringToReturn + StringToProcess

                if StringToProcess.find(":") != -1 and StringToProcess[-1] != "}":  # meaning that we're processing a dict()
                    StringToReturn = StringToReturn + "}"
                elif StringToProcess.find("TUPLE") != -1 and StringToProcess[-1] != ")":  # meaning that we're processing a tuple
                    StringToReturn = StringToReturn + ")"
                else:
                    StringToReturn = StringToReturn + "]"

            ################################################

        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    elif len(ListOfStringsToJoin) == 1:
        StringToReturn = ListOfStringsToJoin[0]

    else:
        StringToReturn = ListOfStringsToJoin

    return StringToReturn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ConvertDictToProperlyFormattedStringForPrinting(DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

    ProperlyFormattedStringForPrinting = ""
    ItemsPerLineCounter = 0

    for Key in DictToPrint:

        if isinstance(DictToPrint[Key], dict): #RECURSION
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ":\n" + \
                                                 ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                 str(Key) + ": " + \
                                                 ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)

        if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
            ItemsPerLineCounter = ItemsPerLineCounter + 1
        else:
            ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
            ItemsPerLineCounter = 0

    return ProperlyFormattedStringForPrinting
##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def GUI_update_clock():
    global root
    global EXIT_PROGRAM_FLAG
    global GUI_RootAfterCallbackInterval_Milliseconds
    global USE_GUI_FLAG
    global MostRecentDict_Label

    global PhidgetDCmotorDCC1000controller_Object
    global PhidgetDCmotorDCC1000controller_OPEN_FLAG
    global SHOW_IN_GUI_PhidgetDCmotorDCC1000controller_FLAG
    global PhidgetDCmotorDCC1000controller_MostRecentDict

    global MyPrint_Object
    global MyPrint_OPEN_FLAG
    global SHOW_IN_GUI_MyPrint_FLAG

    if USE_GUI_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
        #########################################################
        #########################################################

            #########################################################
            MostRecentDict_Label["text"] = ConvertDictToProperlyFormattedStringForPrinting(PhidgetDCmotorDCC1000controller_MostRecentDict,
                                                                                            NumberOfDecimalsPlaceToUse=3,
                                                                                            NumberOfEntriesPerLine=1,
                                                                                            NumberOfTabsBetweenItems=1)
            #########################################################

            #########################################################
            if PhidgetDCmotorDCC1000controller_OPEN_FLAG == 1 and SHOW_IN_GUI_PhidgetDCmotorDCC1000controller_FLAG == 1:
                PhidgetDCmotorDCC1000controller_Object.GUI_update_clock()
            #########################################################

            #########################################################
            if MyPrint_OPEN_FLAG == 1 and SHOW_IN_GUI_MyPrint_FLAG == 1:
                MyPrint_Object.GUI_update_clock()
            #########################################################

            root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
        #########################################################
        #########################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
def ExitProgram_Callback(OptionalArugment = 0):
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

    global PhidgetDCmotorDCC1000controller_Object
    global PhidgetDCmotorDCC1000controller_OPEN_FLAG

    global MyPrint_Object
    global MyPrint_OPEN_FLAG

    ################################################# KEY GUI LINE
    #################################################
    root = Tk()

    root.protocol("WM_DELETE_WINDOW", ExitProgram_Callback)  # Set the callback function for when the window's closed.
    root.title("test_program_for_PhidgetDCmotorDCC1000controller_ReubenPython2and3Class")
    root.geometry('%dx%d+%d+%d' % (root_width, root_height, root_Xpos, root_Ypos)) # set the dimensions of the screen and where it is placed
    #################################################
    #################################################

    #################################################
    #################################################
    global TabControlObject
    global Tab_MainControls
    global Tab_PhidgetDCmotorDCC1000controller
    global Tab_MyPrint

    if USE_TABS_IN_GUI_FLAG == 1:
        #################################################
        TabControlObject = ttk.Notebook(root)

        Tab_PhidgetDCmotorDCC1000controller = ttk.Frame(TabControlObject)
        TabControlObject.add(Tab_PhidgetDCmotorDCC1000controller, text='   DCmotor   ')

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
        Tab_PhidgetDCmotorDCC1000controller = root
        Tab_MyPrint = root
        #################################################

    #################################################
    #################################################

    #################################################
    #################################################
    global MostRecentDict_Label
    MostRecentDict_Label = Label(Tab_MainControls, text="MostRecentDict_Label", width=120, font=("Helvetica", 10))
    MostRecentDict_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
    #################################################
    #################################################

    #################################################
    #################################################
    if PhidgetDCmotorDCC1000controller_OPEN_FLAG == 1:
        PhidgetDCmotorDCC1000controller_Object.CreateGUIobjects(TkinterParent=Tab_PhidgetDCmotorDCC1000controller)
    #################################################
    #################################################

    #################################################
    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.CreateGUIobjects(TkinterParent=Tab_MyPrint)
    #################################################
    #################################################

    ################################################# THIS BLOCK MUST COME 2ND-TO-LAST IN def GUI_Thread() IF USING TABS.
    #################################################
    root.after(GUI_RootAfterCallbackInterval_Milliseconds, GUI_update_clock)
    root.mainloop()
    #################################################
    #################################################

    #################################################  THIS BLOCK MUST COME LAST IN def GUI_Thread() REGARDLESS OF CODE.
    #################################################
    root.quit() #Stop the GUI thread, MUST BE CALLED FROM GUI_Thread
    root.destroy() #Close down the GUI thread, MUST BE CALLED FROM GUI_Thread
    #################################################
    #################################################

##########################################################################################################
##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################
if __name__ == '__main__':

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

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

    global USE_PhidgetDCmotorDCC1000controller_FLAG
    USE_PhidgetDCmotorDCC1000controller_FLAG = 1

    global USE_MyPrint_FLAG
    USE_MyPrint_FLAG = 1
    
    global USE_MyPlotterPureTkinterStandAloneProcess_FLAG
    USE_MyPlotterPureTkinterStandAloneProcess_FLAG = 1
    
    global USE_KEYBOARD_FLAG
    USE_KEYBOARD_FLAG = 1
    
    global USE_PeriodicInput_FLAG
    USE_PeriodicInput_FLAG = 0

    global USE_PositionControl_FLAG
    USE_PositionControl_FLAG = 0 #SET TO 0 FOR VELOCITY CONTROL
    #################################################
    #################################################

    #################################################
    #################################################
    global SHOW_IN_GUI_PhidgetDCmotorDCC1000controller_FLAG
    SHOW_IN_GUI_PhidgetDCmotorDCC1000controller_FLAG = 1

    global SHOW_IN_GUI_MyPrint_FLAG
    SHOW_IN_GUI_MyPrint_FLAG = 1
    #################################################
    #################################################

    #################################################
    #################################################
    global GUI_ROW_PhidgetDCmotorDCC1000controller
    global GUI_COLUMN_PhidgetDCmotorDCC1000controller
    global GUI_PADX_PhidgetDCmotorDCC1000controller
    global GUI_PADY_PhidgetDCmotorDCC1000controller
    global GUI_ROWSPAN_PhidgetDCmotorDCC1000controller
    global GUI_COLUMNSPAN_PhidgetDCmotorDCC1000controller
    GUI_ROW_PhidgetDCmotorDCC1000controller = 1

    GUI_COLUMN_PhidgetDCmotorDCC1000controller = 0
    GUI_PADX_PhidgetDCmotorDCC1000controller = 1
    GUI_PADY_PhidgetDCmotorDCC1000controller = 10
    GUI_ROWSPAN_PhidgetDCmotorDCC1000controller = 1
    GUI_COLUMNSPAN_PhidgetDCmotorDCC1000controller = 1

    global GUI_ROW_MyPrint
    global GUI_COLUMN_MyPrint
    global GUI_PADX_MyPrint
    global GUI_PADY_MyPrint
    global GUI_ROWSPAN_MyPrint
    global GUI_COLUMNSPAN_MyPrint
    GUI_ROW_MyPrint = 2

    GUI_COLUMN_MyPrint = 0
    GUI_PADX_MyPrint = 1
    GUI_PADY_MyPrint = 10
    GUI_ROWSPAN_MyPrint = 1
    GUI_COLUMNSPAN_MyPrint = 1
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
    
    global LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess
    LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = -11111.0

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
    global Tab_PhidgetDCmotorDCC1000controller
    global Tab_MyPrint

    global GUI_RootAfterCallbackInterval_Milliseconds
    GUI_RootAfterCallbackInterval_Milliseconds = 30


    
    global PeriodicInput_AcceptableValues
    PeriodicInput_AcceptableValues = ["GUI", "Sine", "Cosine", "Triangular", "Square"]

    global PeriodicInput_Type_PositionControl
    PeriodicInput_Type_PositionControl = "Triangular"

    global PeriodicInput_MinValue_PositionControl
    PeriodicInput_MinValue_PositionControl = -50.0

    global PeriodicInput_MaxValue_PositionControl
    PeriodicInput_MaxValue_PositionControl = 50.0

    global PeriodicInput_Period_PositionControl
    PeriodicInput_Period_PositionControl = 1.0

    global PeriodicInput_CalculatedValue_PositionControl
    PeriodicInput_CalculatedValue_PositionControl = 0.0
    
    
    
    global PeriodicInput_Type_VelocityControl
    PeriodicInput_Type_VelocityControl = "Triangular"

    global PeriodicInput_MinValue_VelocityControl
    PeriodicInput_MinValue_VelocityControl = -1.0

    global PeriodicInput_MaxValue_VelocityControl
    PeriodicInput_MaxValue_VelocityControl = 1.0

    global PeriodicInput_Period_VelocityControl
    PeriodicInput_Period_VelocityControl = 1.0

    global PeriodicInput_CalculatedValue_VelocityControl
    PeriodicInput_CalculatedValue_VelocityControl = 0.0
    #################################################
    #################################################

    #################################################
    #################################################
    global PhidgetDCmotorDCC1000controller_Object

    global PhidgetDCmotorDCC1000controller_OPEN_FLAG
    PhidgetDCmotorDCC1000controller_OPEN_FLAG = -1

    global PhidgetDCmotorDCC1000controller_MostRecentDict
    PhidgetDCmotorDCC1000controller_MostRecentDict = dict()

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_TO_BE_SET
    PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_TO_BE_SET = 0.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_TO_BE_SET
    PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_TO_BE_SET = 0.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_FromDevice
    PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_FromDevice = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_FromDevice
    PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_FromDevice = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw
    PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed
    PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice
    PhidgetDCmotorDCC1000controller_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Temperature_DegC_FromDevice
    PhidgetDCmotorDCC1000controller_MostRecentDict_Temperature_DegC_FromDevice = -11111.0

    global PhidgetDCmotorDCC1000controller_MostRecentDict_Time
    PhidgetDCmotorDCC1000controller_MostRecentDict_Time = -11111.0
    #################################################
    #################################################

    #################################################
    #################################################
    global MyPrint_Object

    global MyPrint_OPEN_FLAG
    MyPrint_OPEN_FLAG = -1
    #################################################
    #################################################

    ####################################################
    ####################################################
    global MyPlotterPureTkinterStandAloneProcess_Object

    global MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG
    MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = -1

    global MyPlotterPureTkinter_MostRecentDict
    MyPlotterPureTkinter_MostRecentDict = dict()

    global MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag
    MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = -1
    ####################################################
    ####################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global PhidgetDCmotorDCC1000controller_GUIparametersDict
    PhidgetDCmotorDCC1000controller_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_PhidgetDCmotorDCC1000controller_FLAG),
                                                                ("EnableInternal_MyPrint_Flag", 0),
                                                                ("NumberOfPrintLines", 10),
                                                                ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                ("GUI_ROW", GUI_ROW_PhidgetDCmotorDCC1000controller),
                                                                ("GUI_COLUMN", GUI_COLUMN_PhidgetDCmotorDCC1000controller),
                                                                ("GUI_PADX", GUI_PADX_PhidgetDCmotorDCC1000controller),
                                                                ("GUI_PADY", GUI_PADY_PhidgetDCmotorDCC1000controller),
                                                                ("GUI_ROWSPAN", GUI_ROWSPAN_PhidgetDCmotorDCC1000controller),
                                                                ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_PhidgetDCmotorDCC1000controller)])

    global PhidgetDCmotorDCC1000controller_SetupDict_PositionControl
    PhidgetDCmotorDCC1000controller_SetupDict_PositionControl = dict([("GUIparametersDict", PhidgetDCmotorDCC1000controller_GUIparametersDict),
                                                                        ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                        ("VINT_DesiredSerialNumber", -1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("VINT_DesiredPortNumber", 0), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG", 1),
                                                                        ("VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100", 1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("DesiredDeviceID", 57),
                                                                        ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                        ("NameToDisplay_UserSet", "Reuben's Test PhidgetDCmotorDCC1000controller"),
                                                                        ("ENABLE_GETS_MAINTHREAD", 1),
                                                                        ("FailsafeTime_Milliseconds", 10000),
                                                                        ("MainThread_TimeToSleepEachLoop", 0.001),
                                                                        ("ControlMode", "position"),  #position or velocity
                                                                        ("CurrentLimit_Amps_UserSet", 25.0),
                                                                        ("VelocityMinLimit_PhidgetsUnits_UserSet", 0.0),
                                                                        ("VelocityMaxLimit_PhidgetsUnits_UserSet", 10000.0),
                                                                        ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                                                                        ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100000.0),
                                                                        ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                                                                        ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                                                                        ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                                                                        ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                                                                        ("UpdateDeltaT_ms", 20)]) #100 min for velocity, 20 min for position

    global PhidgetDCmotorDCC1000controller_SetupDict_VelocityControl
    PhidgetDCmotorDCC1000controller_SetupDict_VelocityControl = dict([("GUIparametersDict", PhidgetDCmotorDCC1000controller_GUIparametersDict),
                                                                        ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                        ("VINT_DesiredSerialNumber", -1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("VINT_DesiredPortNumber", 0), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG", 1),
                                                                        ("VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100", 1), #CHANGE THIS TO MATCH YOUR UNIQUE VINT
                                                                        ("DesiredDeviceID", 57),
                                                                        ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                        ("NameToDisplay_UserSet", "Reuben's Test PhidgetDCmotorDCC1000controller"),
                                                                        ("ENABLE_GETS_MAINTHREAD", 1),
                                                                        ("FailsafeTime_Milliseconds", 10000),
                                                                        ("MainThread_TimeToSleepEachLoop", 0.001),
                                                                        ("ControlMode", "velocity"),  #position or velocity
                                                                        ("CurrentLimit_Amps_Max_UserSet", 25.0),
                                                                        ("VelocityMinLimit_PhidgetsUnits_UserSet", -1.0),
                                                                        ("VelocityMaxLimit_PhidgetsUnits_UserSet", 1.0),
                                                                        ("BrakingStrengthLimit_VelControl_Percent_UserSet", 100.0),
                                                                        ("AccelerationMaxLimit_PhidgetsUnits_UserSet", 100.0),
                                                                        ("PositionMinLimit_PhidgetsUnits_UserSet", -1000.0),
                                                                        ("PositionMaxLimit_PhidgetsUnits_UserSet", 1000.0),
                                                                        ("Kp_PosControl_Gain_UserSet", 20000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("Ki_PosControl_Gain_UserSet", 2.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("Kd_PosControl_Gain_UserSet", 40000.0),  #IF MOTOR-CONTROL FAILS, THEN TRY ALL-NEGATIVE-GAIN-VALUES (Kp, Ki, and KD)!
                                                                        ("DeadBand_PosControl_PhidgetsUnits_UserSet", 10.0),  #Lower DeadBand value is a tighter Position loop (allows less error)
                                                                        ("RescaleFactor_MultipliesPhidgetsUnits_UserSet", 1.0),
                                                                        ("UpdateDeltaT_ms", 100)]) #100 min for velocity, 20 min for position

    #################################################
    global PhidgetDCmotorDCC1000controller_SetupDict

    if USE_PositionControl_FLAG == 1:
        PhidgetDCmotorDCC1000controller_SetupDict = PhidgetDCmotorDCC1000controller_SetupDict_PositionControl
    else:
        PhidgetDCmotorDCC1000controller_SetupDict = PhidgetDCmotorDCC1000controller_SetupDict_VelocityControl
    #################################################

    if USE_PhidgetDCmotorDCC1000controller_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            PhidgetDCmotorDCC1000controller_Object = PhidgetDCmotorDCC1000controller_ReubenPython2and3Class(PhidgetDCmotorDCC1000controller_SetupDict)
            PhidgetDCmotorDCC1000controller_OPEN_FLAG = PhidgetDCmotorDCC1000controller_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetDCmotorDCC1000controller_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################
    
    #################################################
    #################################################
    if USE_PhidgetDCmotorDCC1000controller_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if PhidgetDCmotorDCC1000controller_OPEN_FLAG != 1:
                print("Failed to open PhidgetDCmotorDCC1000controller_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################
    
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPrint_GUIparametersDict
    MyPrint_GUIparametersDict = dict([("USE_GUI_FLAG", USE_GUI_FLAG and SHOW_IN_GUI_MyPrint_FLAG),
                                        ("UseBorderAroundThisGuiObjectFlag", 0),
                                        ("GUI_ROW", GUI_ROW_MyPrint),
                                        ("GUI_COLUMN", GUI_COLUMN_MyPrint),
                                        ("GUI_PADX", GUI_PADX_MyPrint),
                                        ("GUI_PADY", GUI_PADY_MyPrint),
                                        ("GUI_ROWSPAN", GUI_ROWSPAN_MyPrint),
                                        ("GUI_COLUMNSPAN", GUI_COLUMNSPAN_MyPrint)])

    global MyPrint_SetupDict
    MyPrint_SetupDict = dict([("NumberOfPrintLines", 10),
                            ("WidthOfPrintingLabel", 200),
                            ("PrintToConsoleFlag", 1),
                            ("LogFileNameFullPath", os.path.join(os.getcwd(), "TestLog.txt")),
                            ("GUIparametersDict", MyPrint_GUIparametersDict)])

    if USE_MyPrint_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPrint_Object = MyPrint_ReubenPython2and3Class(MyPrint_SetupDict)
            MyPrint_OPEN_FLAG = MyPrint_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPrint_Object __init__: Exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPrint_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPrint_OPEN_FLAG != 1:
                print("Failed to open MyPrint_Object.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    #################################################
    #################################################
    global MyPlotterPureTkinterStandAloneProcess_GUIparametersDict
    MyPlotterPureTkinterStandAloneProcess_GUIparametersDict = dict([("EnableInternal_MyPrint_Flag", 1),
                                                                    ("NumberOfPrintLines", 10),
                                                                    ("GraphCanvasWidth", 900),
                                                                    ("GraphCanvasHeight", 700),
                                                                    ("GraphCanvasWindowStartingX", 0),
                                                                    ("GraphCanvasWindowStartingY", 0),
                                                                    ("GraphCanvasWindowTitle", "My plotting example!"),
                                                                    ("GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents", 30)])


    global MyPlotterPureTkinterStandAloneProcess_SetupDict
    MyPlotterPureTkinterStandAloneProcess_SetupDict = dict([("GUIparametersDict", MyPlotterPureTkinterStandAloneProcess_GUIparametersDict),
                                                            ("ParentPID", os.getpid()),
                                                            ("WatchdogTimerDurationSeconds_ExpirationWillEndStandAlonePlottingProcess", 5.0),
                                                            ("CurvesToPlotNamesAndColorsDictOfLists", dict([("NameList", ["Commanded", "Actual"]),
                                                                                                        ("MarkerSizeList", [2]*2),
                                                                                                        ("LineWidthList", [2]*2),
                                                                                                        ("IncludeInXaxisAutoscaleCalculationList", [1]*2),
                                                                                                        ("IncludeInYaxisAutoscaleCalculationList", [1]*2),
                                                                                                        ("ColorList", ["Green", "Red"])])),
                                                            ("SmallTextSize", 7),
                                                            ("LargeTextSize", 12),
                                                            ("NumberOfDataPointToPlot", 100),
                                                            ("XaxisNumberOfTickMarks", 10),
                                                            ("YaxisNumberOfTickMarks", 10),
                                                            ("XaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("YaxisNumberOfDecimalPlacesForLabels", 3),
                                                            ("XaxisAutoscaleFlag", 1),
                                                            ("YaxisAutoscaleFlag", 1),
                                                            ("X_min", 0.0),
                                                            ("X_max", 5.0),
                                                            ("Y_min", -5.0),
                                                            ("Y_max", 5.0),
                                                            ("XaxisDrawnAtBottomOfGraph", 0),
                                                            ("XaxisLabelString", "Time (sec)"),
                                                            ("YaxisLabelString", "Y-units (units)"),
                                                            ("ShowLegendFlag", 1),
                                                            ("GraphNumberOfLeadingZeros", 0),
                                                            ("GraphNumberOfDecimalPlaces", 3),
                                                            ("SavePlot_DirectoryPath", os.path.join(os.getcwd(), "SavedImagesFolder")),
                                                            ("KeepPlotterWindowAlwaysOnTopFlag", 0),
                                                            ("RemoveTitleBorderCloseButtonAndDisallowWindowMoveFlag", 0),
                                                            ("AllowResizingOfWindowFlag", 1)])

    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        try:
            MyPlotterPureTkinterStandAloneProcess_Object = MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class(MyPlotterPureTkinterStandAloneProcess_SetupDict)
            MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG = MyPlotterPureTkinterStandAloneProcess_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

        except:
            exceptions = sys.exc_info()[0]
            print("MyPlotterPureTkinterStandAloneProcess_Object, exceptions: %s" % exceptions)
            traceback.print_exc()
    #################################################
    #################################################

    #################################################
    #################################################
    if USE_MyPlotterPureTkinterStandAloneProcess_FLAG == 1:
        if EXIT_PROGRAM_FLAG == 0:
            if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG != 1:
                print("Failed to open MyPlotterPureTkinterStandAloneProcess_ReubenPython2and3Class.")
                ExitProgram_Callback()
    #################################################
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    if USE_KEYBOARD_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        keyboard.on_press_key("esc", ExitProgram_Callback)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## SHOWS HOW TO OFFSET THE ANGLE
    ##########################################################################################################
    ##########################################################################################################
    #if USE_PhidgetDCmotorDCC1000controller_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
    #    if PhidgetDCmotorDCC1000controller_SetupDict["ControlMode"] == "position":
    #        time.sleep(0.5)
    #        PhidgetDCmotorDCC1000controller_Object.SetPositionOffsetOnBoardWithoutMoving(90)
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## KEY GUI LINE
    ##########################################################################################################
    ##########################################################################################################
    if USE_GUI_FLAG == 1 and EXIT_PROGRAM_FLAG == 0:
        print("Starting GUI thread...")
        GUI_Thread_ThreadingObject = threading.Thread(target=GUI_Thread, daemon=True) #Daemon=True means that the GUI thread is destroyed automatically when the main thread is destroyed
        GUI_Thread_ThreadingObject.start()
    else:
        root = None
        Tab_MainControls = None
        Tab_PhidgetDCmotorDCC1000controller = None
        Tab_MyPrint = None
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    print("Starting main loop 'test_program_for_PhidgetDCmotorDCC1000controller_ReubenPython2and3Class.")
    StartingTime_MainLoopThread = getPreciseSecondsTimeStampString()

    while(EXIT_PROGRAM_FLAG == 0):

        #################################################
        #################################################
        #################################################
        CurrentTime_MainLoopThread = getPreciseSecondsTimeStampString() - StartingTime_MainLoopThread
        #################################################
        #################################################
        #################################################

        ################################################# GET's
        #################################################
        #################################################
        if PhidgetDCmotorDCC1000controller_OPEN_FLAG == 1:

            PhidgetDCmotorDCC1000controller_MostRecentDict = PhidgetDCmotorDCC1000controller_Object.GetMostRecentDataDict()

            if "Time" in PhidgetDCmotorDCC1000controller_MostRecentDict:
                PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_TO_BE_SET = PhidgetDCmotorDCC1000controller_MostRecentDict["Position_PhidgetsUnits_TO_BE_SET"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_TO_BE_SET = PhidgetDCmotorDCC1000controller_MostRecentDict["Velocity_PhidgetsUnits_TO_BE_SET"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_FromDevice = PhidgetDCmotorDCC1000controller_MostRecentDict["Position_PhidgetsUnits_FromDevice"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_FromDevice = PhidgetDCmotorDCC1000controller_MostRecentDict["Velocity_PhidgetsUnits_FromDevice"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedRaw = PhidgetDCmotorDCC1000controller_MostRecentDict["Velocity_PhidgetsUnits_DifferentiatedRaw"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_DifferentiatedSmoothed = PhidgetDCmotorDCC1000controller_MostRecentDict["Velocity_PhidgetsUnits_DifferentiatedSmoothed"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_DutyCycle_PhidgetsUnits_FromDevice = PhidgetDCmotorDCC1000controller_MostRecentDict["DutyCycle_PhidgetsUnits_FromDevice"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Temperature_DegC_FromDevice = PhidgetDCmotorDCC1000controller_MostRecentDict["Temperature_DegC_FromDevice"]
                PhidgetDCmotorDCC1000controller_MostRecentDict_Time = PhidgetDCmotorDCC1000controller_MostRecentDict["Time"]

        #################################################
        #################################################
        #################################################

        ################################################# SET's
        #################################################
        #################################################
        if PhidgetDCmotorDCC1000controller_OPEN_FLAG == 1:

            if USE_PeriodicInput_FLAG == 1:

                ####################################################
                PeriodicInput_CalculatedValue_PositionControl = GetLatestWaveformValue(CurrentTime_MainLoopThread, 
                                                                    PeriodicInput_MinValue_PositionControl, 
                                                                    PeriodicInput_MaxValue_PositionControl, 
                                                                    PeriodicInput_Period_PositionControl, 
                                                                    PeriodicInput_Type_PositionControl)
                ###################################################
                
                ####################################################
                PeriodicInput_CalculatedValue_VelocityControl = GetLatestWaveformValue(CurrentTime_MainLoopThread, 
                                                                    PeriodicInput_MinValue_VelocityControl, 
                                                                    PeriodicInput_MaxValue_VelocityControl, 
                                                                    PeriodicInput_Period_VelocityControl, 
                                                                    PeriodicInput_Type_VelocityControl)
                ###################################################

                ###################################################
                if USE_PositionControl_FLAG == 1:
                    PhidgetDCmotorDCC1000controller_Object.CommandMotorFromExternalProgram_PositionControl(PeriodicInput_CalculatedValue_PositionControl)

                else:
                    PhidgetDCmotorDCC1000controller_Object.CommandMotorFromExternalProgram_VelocityControl(PeriodicInput_CalculatedValue_VelocityControl)
                ###################################################
                
        #################################################
        #################################################
        #################################################

        ################################################### SETs
        ###################################################
        ###################################################
        if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:

            ###################################################
            ###################################################
            MyPlotterPureTkinterStandAloneProcess_MostRecentDict = MyPlotterPureTkinterStandAloneProcess_Object.GetMostRecentDataDict()

            if "StandAlonePlottingProcess_ReadyForWritingFlag" in MyPlotterPureTkinterStandAloneProcess_MostRecentDict:
                MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag = MyPlotterPureTkinterStandAloneProcess_MostRecentDict["StandAlonePlottingProcess_ReadyForWritingFlag"]

                if MyPlotterPureTkinterStandAloneProcess_MostRecentDict_ReadyForWritingFlag == 1:
                    if CurrentTime_MainLoopThread - LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess >= MyPlotterPureTkinterStandAloneProcess_GUIparametersDict["GUI_RootAfterCallbackInterval_Milliseconds_IndependentOfParentRootGUIloopEvents"]/1000.0 + 0.001:

                        if USE_PositionControl_FLAG == 1:
                            CommandedToPlot = PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_TO_BE_SET
                            ActualToPlot = PhidgetDCmotorDCC1000controller_MostRecentDict_Position_PhidgetsUnits_FromDevice

                        else:
                            CommandedToPlot = PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_TO_BE_SET
                            ActualToPlot = PhidgetDCmotorDCC1000controller_MostRecentDict_Velocity_PhidgetsUnits_FromDevice

                        MyPlotterPureTkinterStandAloneProcess_Object.ExternalAddPointOrListOfPointsToPlot(["Commanded", "Actual"],
                                                                                                        [CurrentTime_MainLoopThread]*2,
                                                                                                        [CommandedToPlot, ActualToPlot])

                        LastTime_MainLoopThread_MyPlotterPureTkinterStandAloneProcess = CurrentTime_MainLoopThread
            ###################################################
            ###################################################

        ###################################################
        ###################################################
        ###################################################

        time.sleep(0.060)

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## THIS IS THE EXIT ROUTINE!
    ##########################################################################################################
    ##########################################################################################################
    print("Exiting main program 'test_program_for_PhidgetDCmotorDCC1000controller_ReubenPython2and3Class.")

    #################################################
    if PhidgetDCmotorDCC1000controller_OPEN_FLAG == 1:
        PhidgetDCmotorDCC1000controller_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPrint_OPEN_FLAG == 1:
        MyPrint_Object.ExitProgram_Callback()
    #################################################

    #################################################
    if MyPlotterPureTkinterStandAloneProcess_OPEN_FLAG == 1:
        MyPlotterPureTkinterStandAloneProcess_Object.ExitProgram_Callback()
    #################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

##########################################################################################################
##########################################################################################################
##########################################################################################################
##########################################################################################################