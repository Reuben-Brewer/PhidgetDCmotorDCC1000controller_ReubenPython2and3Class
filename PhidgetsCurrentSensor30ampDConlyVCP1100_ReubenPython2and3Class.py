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
from LowPassFilterForDictsOfLists_ReubenPython2and3Class import *
###########################################################

###########################################################
import os
import sys
import platform
import time
import datetime
import math
import collections
from copy import * #for deepcopy
import inspect #To enable 'TellWhichFileWereIn'
import threading
import queue as Queue
import traceback
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

###########################################################
from Phidget22.PhidgetException import *
from Phidget22.Phidget import *
from Phidget22.Devices.Log import *
from Phidget22.LogLevel import *
from Phidget22.Devices.CurrentInput import *
###########################################################

##########################################################################################################
##########################################################################################################

class PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict): #Subclass the Tkinter Frame

        print("#################### PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0

        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0

        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        self.DetectedDeviceSerialNumber = "default"

        self.CurrentSensorList_PhidgetsCurrentSensorObjects = list()

        self.NumberOfCurrentSensors = 1

        self.CurrentSensorList_AttachedAndOpenFlag = [0.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_NeedsToBeHomedFlag = [0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_UpdateDeltaTseconds = [0.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_UpdateFrequencyHz = [0.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_ErrorCallbackFiredFlag = [0.0] * self.NumberOfCurrentSensors

        self.CurrentSensorList_Current_Amps_Raw = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_Current_Amps_Filtered = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_CurrentDerivative_AmpsPerSec = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_LowPassFilter_ReubenPython2and3ClassObject = list()

        self.CurrentSensorList_Current_Amps_Raw_LAST = [-11111.0] * self.NumberOfCurrentSensors

        self.CurrentSensorList_CurrentTime_CurrentSensorGENERALonCurrentChangeCallback = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_StartingTime_CurrentSensorGENERALonCurrentChangeCallback = [self.getPreciseSecondsTimeStampString()] * self.NumberOfCurrentSensors
        self.CurrentSensorList_LastTime_CurrentSensorGENERALonCurrentChangeCallback = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_DataStreamingFrequency_CurrentSensorGENERALonCurrentChangeCallback = [-11111.0] * self.NumberOfCurrentSensors
        self.CurrentSensorList_DataStreamingDeltaT_CurrentSensorGENERALonCurrentChangeCallback = [-11111.0] * self.NumberOfCurrentSensors

        self.CurrentSensorList_ListOfOnAttachCallbackFunctionNames = [self.CurrentSensor0onAttachCallback]
        self.CurrentSensorList_ListOfOnDetachCallbackFunctionNames = [self.CurrentSensor0onDetachCallback]
        self.CurrentSensorList_ListOfOnErrorCallbackFunctionNames = [self.CurrentSensor0onErrorCallback]
        self.CurrentSensorList_ListOfOnCurrentChangeCallbackFunctionNames = [self.CurrentSensor0onCurrentChangeCallback]

        self.MostRecentDataDict = dict()
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if platform.system() == "Linux":

            if "raspberrypi" in platform.uname(): #os.uname() doesn't work in windows
                self.my_platform = "pi"
            else:
                self.my_platform = "linux"

        elif platform.system() == "Windows":
            self.my_platform = "windows"

        elif platform.system() == "Darwin":
            self.my_platform = "mac"

        else:
            self.my_platform = "other"

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUI_STICKY: " + str(self.GUI_STICKY))
            #########################################################
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredSerialNumber" in SetupDict:
            try:
                self.VINT_DesiredSerialNumber = int(SetupDict["VINT_DesiredSerialNumber"])
            except:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, VINT_DesiredSerialNumber invalid.")
        else:
            self.VINT_DesiredSerialNumber = -1

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber" in SetupDict:
            try:
                self.VINT_DesiredPortNumber = int(SetupDict["VINT_DesiredPortNumber"])
            except:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, VINT_DesiredPortNumber invalid.")
        else:
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredDeviceID" in SetupDict:
            try:
                self.DesiredDeviceID = int(SetupDict["DesiredDeviceID"])
            except:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, DesiredDeviceID invalid.")
        else:
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, must initialize object with 'DesiredDeviceID' argument.")
            return

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DataCallbackUpdateDeltaT_ms" in SetupDict:
            self.DataCallbackUpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("DataCallbackUpdateDeltaT_ms", SetupDict["DataCallbackUpdateDeltaT_ms"], 20.0, 60000.0))
        else:
            self.DataCallbackUpdateDeltaT_ms = 20

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DataCallbackUpdateDeltaT_ms: " + str(self.DataCallbackUpdateDeltaT_ms))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CurrentSensorList_Current_Amps_ExponentialFilterLambda" in SetupDict:
            CurrentSensorList_Current_Amps_ExponentialFilterLambda_TEMP = SetupDict["CurrentSensorList_Current_Amps_ExponentialFilterLambda"]
            if self.IsInputList(CurrentSensorList_Current_Amps_ExponentialFilterLambda_TEMP) == 1 and len(CurrentSensorList_Current_Amps_ExponentialFilterLambda_TEMP) == self.NumberOfCurrentSensors:
                self.CurrentSensorList_Current_Amps_ExponentialFilterLambda = list()
                for CurrentSensorChannel, SpeedExponentialFilterLambda_TEMP in enumerate(CurrentSensorList_Current_Amps_ExponentialFilterLambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentSensorList_Current_Amps_ExponentialFilterLambda, CurrentSensorChannel " + str(CurrentSensorChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.CurrentSensorList_Current_Amps_ExponentialFilterLambda.append(SpeedExponentialFilterLambda)
            else:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, 'CurrentSensorList_Current_Amps_ExponentialFilterLambda' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.CurrentSensorList_Current_Amps_ExponentialFilterLambda = [0.95] * self.NumberOfCurrentSensors #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: CurrentSensorList_Current_Amps_ExponentialFilterLambda: " + str(self.CurrentSensorList_Current_Amps_ExponentialFilterLambda))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda" in SetupDict:
            CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda_TEMP = SetupDict["CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda"]
            if self.IsInputList(CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda_TEMP) == 1 and len(CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda_TEMP) == self.NumberOfCurrentSensors:
                self.CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda = list()
                for CurrentSensorChannel, SpeedExponentialFilterLambda_TEMP in enumerate(CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda_TEMP):
                    SpeedExponentialFilterLambda = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda, CurrentSensorChannel " + str(CurrentSensorChannel), SpeedExponentialFilterLambda_TEMP, 0.0, 1.0)
                    self.CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda.append(SpeedExponentialFilterLambda)
            else:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Error, 'CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda' must be a length of length 4 with values of 0 or 1.")
                return
        else:
            self.CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda = [0.95] * self.NumberOfCurrentSensors #Default to no filtering, new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda: " + str(self.CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda))
        #########################################################
        #########################################################

        ''' #NOT USING MainThread in this code as it's not doing anything (callback is sufficient)
        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################
        '''


        #########################################################
        #########################################################
        try:

            for CurrentSensorChannel in range(0, self.NumberOfCurrentSensors):

                #########################################################
                DictOfVariableFilterSettings = dict([("Current", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.CurrentSensorList_Current_Amps_ExponentialFilterLambda[CurrentSensorChannel])])),
                                                    ("CurrentDerivative", dict([("UseMedianFilterFlag", 0), ("UseExponentialSmoothingFilterFlag", 1),("ExponentialSmoothingFilterLambda", self.CurrentSensorList_CurrentDerivative_AmpsPerSec_ExponentialFilterLambda[CurrentSensorChannel])]))])

                LowPassFilterForDictsOfLists_SetupDict = dict([("DictOfVariableFilterSettings", DictOfVariableFilterSettings)])

                LowPassFilterForDictsOfLists_Object = LowPassFilterForDictsOfLists_ReubenPython2and3Class(LowPassFilterForDictsOfLists_SetupDict)
                #########################################################

                self.CurrentSensorList_LowPassFilter_ReubenPython2and3ClassObject.append(LowPassFilterForDictsOfLists_Object)
                LowPassFilterForDictsOfLists_OPEN_FLAG = self.CurrentSensorList_LowPassFilter_ReubenPython2and3ClassObject[CurrentSensorChannel].OBJECT_CREATED_SUCCESSFULLY_FLAG

                if LowPassFilterForDictsOfLists_OPEN_FLAG != 1:
                    print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to open LowPassFilterForDictsOfLists_Object.")
                    return

        except:
            exceptions = sys.exc_info()[0]
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.PrintToGui_Label_TextInputHistory_List = [" "]*self.NumberOfPrintLines
        self.PrintToGui_Label_TextInput_Str = ""
        self.GUI_ready_to_be_updated_flag = 0
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            #########################################################
            for CurrentSensorChannel in range(0, self.NumberOfCurrentSensors):
                self.CurrentSensorList_PhidgetsCurrentSensorObjects.append(CurrentInput())
                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setHubPort(self.VINT_DesiredPortNumber)

                if self.VINT_DesiredSerialNumber != -1: #'-1' means we should open the device regardless of serial number.
                    self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setOnCurrentChangeHandler(self.CurrentSensorList_ListOfOnCurrentChangeCallbackFunctionNames[CurrentSensorChannel])
                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setOnAttachHandler(self.CurrentSensorList_ListOfOnAttachCallbackFunctionNames[CurrentSensorChannel])
                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setOnDetachHandler(self.CurrentSensorList_ListOfOnDetachCallbackFunctionNames[CurrentSensorChannel])
                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setOnErrorHandler(self.CurrentSensorList_ListOfOnErrorCallbackFunctionNames[CurrentSensorChannel])
                self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            #########################################################

            self.PhidgetsDeviceConnectedFlag = 1

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to attach, Phidget Exception %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, os.getcwd() + "\PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class_PhidgetLog_INFO.txt")
                    print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceName = self.CurrentSensorList_PhidgetsCurrentSensorObjects[0].getDeviceName()
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.CurrentSensorList_PhidgetsCurrentSensorObjects[0].getDeviceSerialNumber()
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceID = self.CurrentSensorList_PhidgetsCurrentSensorObjects[0].getDeviceID()
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to call 'getDesiredDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceVersion = self.CurrentSensorList_PhidgetsCurrentSensorObjects[0].getDeviceVersion()
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.CurrentSensorList_PhidgetsCurrentSensorObjects[0].getLibraryVersion()
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.VINT_DesiredSerialNumber != -1: #'-1' means we should open the device regardless os serial number.
                if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                    print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: The desired Serial Number (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                    input("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Press any key (and enter) to exit.")
                    sys.exit()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: The desired DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                input("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class __init__: Press any key (and enter) to exit.")
                sys.exit()
            #########################################################
            #########################################################

            #########################################################
            ######################################################### DON'T NEED THIS WHEN THERE'S A CALLBACK AND NOTHING TO DO IN THE MainThread!
            #self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            #self.MainThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################
            #########################################################

        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_IntOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = int(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def LimitNumber_FloatOutputOnly(self, min_val, max_val, test_val):
        if test_val > max_val:
            test_val = max_val

        elif test_val < min_val:
            test_val = min_val

        else:
            test_val = test_val

        test_val = float(test_val)

        return test_val
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThrough0and1values_ExitProgramOtherwise(self, InputNameString, InputNumber, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error. InputNumber must be a numerical value, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            if InputNumber_ConvertedToFloat == 0.0 or InputNumber_ConvertedToFloat == 1.0:
                return InputNumber_ConvertedToFloat

            else:

                print("PassThrough0and1values_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be 0 or 1 (value was " +
                      str(InputNumber_ConvertedToFloat) +
                      ").")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()

                else:
                    return -1
                ##########################

            ##########################################################################################################

        except:

            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThrough0and1values_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -1
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def PassThroughFloatValuesInRange_ExitProgramOtherwise(self, InputNameString, InputNumber, RangeMinValue, RangeMaxValue, ExitProgramIfFailureFlag=1):

        ##########################################################################################################
        ##########################################################################################################
        try:
            ##########################################################################################################
            InputNumber_ConvertedToFloat = float(InputNumber)
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. InputNumber must be a float value, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        try:

            ##########################################################################################################
            InputNumber_ConvertedToFloat_Limited = self.LimitNumber_FloatOutputOnly(RangeMinValue, RangeMaxValue, InputNumber_ConvertedToFloat)

            if InputNumber_ConvertedToFloat_Limited != InputNumber_ConvertedToFloat:
                print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error. '" +
                      str(InputNameString) +
                      "' must be in the range [" +
                      str(RangeMinValue) +
                      ", " +
                      str(RangeMaxValue) +
                      "] (value was " +
                      str(InputNumber_ConvertedToFloat) + ")")

                ##########################
                if ExitProgramIfFailureFlag == 1:
                    sys.exit()
                else:
                    return -11111.0
                ##########################

            else:
                return InputNumber_ConvertedToFloat_Limited
            ##########################################################################################################

        except:
            ##########################################################################################################
            exceptions = sys.exc_info()[0]
            print("PassThroughFloatValuesInRange_ExitProgramOtherwise Error, Exceptions: %s" % exceptions)
            traceback.print_exc()

            ##########################
            if ExitProgramIfFailureFlag == 1:
                sys.exit()
            else:
                return -11111.0
            ##########################

            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TellWhichFileWereIn(self):

        #We used to use this method, but it gave us the root calling file, not the class calling file
        #absolute_file_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        #filename = absolute_file_path[absolute_file_path.rfind("\\") + 1:]

        frame = inspect.stack()[1]
        filename = frame[1][frame[1].rfind("\\") + 1:]
        filename = filename.replace(".py","")

        return filename
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensorGENERALonAttachCallback(self, CurrentSensorChannel):

        try:
            ##############################
            self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setDataInterval(self.DataCallbackUpdateDeltaT_ms)
            print("CurrentSensorGENERALonAttachCallback: Set CurrentSensorChannel " + \
                  str(CurrentSensorChannel) + \
                  " DataInterval to " + \
                  str(self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].getDataInterval()) + \
                  "ms.")

            self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].setCurrentChangeTrigger(0) #Setting the trigger to 0 makes the onCurrentChange callback fire every self.DataCallbackUpdateDeltaT_ms
            print("CurrentSensorGENERALonAttachCallback: Set CurrentSensorChannel " + \
            str(CurrentSensorChannel) + \
            " CurrentChangeTrigger to " + \
            str(self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].getCurrentChangeTrigger()))
            ##############################

            self.CurrentSensorList_AttachedAndOpenFlag[CurrentSensorChannel] = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ CurrentSensorGENERALonAttachCallback event for CurrentSensorChannel " + str(CurrentSensorChannel) + ", Attached! $$$$$$$$$$")

        except PhidgetException as e:
            self.CurrentSensorList_AttachedAndOpenFlag[CurrentSensorChannel] = 0
            self.MyPrint_WithoutLogFile("CurrentSensorGENERALonAttachCallback event for CurrentSensorChannel " + str(CurrentSensorChannel) + ", ERROR: Failed to attach CurrentSensor0, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensorGENERALonDetachCallback(self, CurrentSensorChannel):

        self.CurrentSensorList_AttachedAndOpenFlag[CurrentSensorChannel] = 0
        self.MyPrint_WithoutLogFile("$$$$$$$$$$ CurrentSensorGENERALonDetachCallback event for CurrentSensorChannel " + str(CurrentSensorChannel) + ", Detatched! $$$$$$$$$$")

        try:
            self.CurrentSensorList_PhidgetsCurrentSensorObjects[CurrentSensorChannel].openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("CurrentSensorGENERALonDetachCallback event for CurrentSensor Channel " + str(CurrentSensorChannel) + ", failed to openWaitForAttachment, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def CurrentSensorGENERALonCurrentChangeCallback(self, CurrentSensorChannel, Current_Amps):

        try:
            ############################################################
            ############################################################
            ############################################################
            if self.EXIT_PROGRAM_FLAG == 0:

                ############################################################
                ############################################################
                self.CurrentSensorList_Current_Amps_Raw[CurrentSensorChannel] = Current_Amps

                self.CurrentSensorList_CurrentTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel] = self.getPreciseSecondsTimeStampString() - self.CurrentSensorList_StartingTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]
                self.CurrentSensorList_DataStreamingDeltaT_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel] = self.CurrentSensorList_CurrentTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel] - self.CurrentSensorList_LastTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]

                if self.CurrentSensorList_DataStreamingDeltaT_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]  != 0.0:
                    ############################################################
                    self.CurrentSensorList_DataStreamingFrequency_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]  = 1.0/self.CurrentSensorList_DataStreamingDeltaT_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]

                    results = self.CurrentSensorList_LowPassFilter_ReubenPython2and3ClassObject[CurrentSensorChannel].AddDataDictFromExternalProgram(dict([("Current", self.CurrentSensorList_Current_Amps_Raw[CurrentSensorChannel])]))
                    self.CurrentSensorList_Current_Amps_Filtered[CurrentSensorChannel] = results["Current"]["Filtered_MostRecentValuesList"][0]

                    CurrentSensorList_CurrentDerivative_AmpsPerSec_TEMP = (self.CurrentSensorList_Current_Amps_Raw[CurrentSensorChannel] - self.CurrentSensorList_Current_Amps_Raw_LAST[CurrentSensorChannel])/self.CurrentSensorList_DataStreamingDeltaT_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]
                    results_deriv = self.CurrentSensorList_LowPassFilter_ReubenPython2and3ClassObject[CurrentSensorChannel].AddDataDictFromExternalProgram(dict([("CurrentDerivative", CurrentSensorList_CurrentDerivative_AmpsPerSec_TEMP)]))

                    self.CurrentSensorList_CurrentDerivative_AmpsPerSec[CurrentSensorChannel] = results_deriv["CurrentDerivative"]["Filtered_MostRecentValuesList"][0]

                    self.CurrentSensorList_LastTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel] = self.CurrentSensorList_CurrentTime_CurrentSensorGENERALonCurrentChangeCallback[CurrentSensorChannel]
                    self.CurrentSensorList_Current_Amps_Raw_LAST[CurrentSensorChannel] = self.CurrentSensorList_Current_Amps_Raw [CurrentSensorChannel]

                    #print("CurrentSensorGENERALonCurrentChangeCallback event fired for Channel " + str(CurrentSensorChannel))
                    ############################################################

                ############################################################
                ############################################################

            ############################################################
            ############################################################
            ############################################################

            ############################################################ MUST CLOSE THE PHIDGETS TO STOP CALLBACK FUNCTIONS WHEN EXITING THE PROGRAM
            ############################################################
            ############################################################
            else:
                for PhidgetsCurrentSensorObject in self.CurrentSensorList_PhidgetsCurrentSensorObjects:
                    PhidgetsCurrentSensorObject.close()
            ############################################################
            ############################################################
            ############################################################

        except:
            exceptions = sys.exc_info()[0]
            print("CurrentSensorGENERALonCurrentChangeCallback: CurrentSensorChannel = " + str(CurrentSensorChannel) +", Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensorGENERALonErrorCallback(self, CurrentSensorChannel, code, description):

        self.CurrentSensorList_ErrorCallbackFiredFlag[CurrentSensorChannel] = 1

        self.MyPrint_WithoutLogFile("CurrentSensorGENERALonErrorCallback event for CurrentSensor Channel " + str(CurrentSensorChannel) + ", Error Code " + ErrorEventCode.getName(code) + ", description: " + str(description))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensor0onAttachCallback(self, HandlerSelf):

        CurrentSensorChannel = 0
        self.CurrentSensorGENERALonAttachCallback(CurrentSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensor0onDetachCallback(self, HandlerSelf):

        CurrentSensorChannel = 0
        self.CurrentSensorGENERALonDetachCallback(CurrentSensorChannel)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensor0onCurrentChangeCallback(self, HandlerSelf, Current_Amps):

        CurrentSensorChannel = 0
        self.CurrentSensorGENERALonCurrentChangeCallback(CurrentSensorChannel, Current_Amps)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentSensor0onErrorCallback(self, HandlerSelf, code, description):

        CurrentSensorChannel = 0
        self.CurrentSensorGENERALonErrorCallback(CurrentSensorChannel, code, description)

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getPreciseSecondsTimeStampString(self):
        ts = time.time()

        return ts
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            #Updating self.MostRecentDataDict here because there is NO MainThread where we could do so.
            self.MostRecentDataDict = dict([("CurrentSensorList_Current_Amps_Raw", self.CurrentSensorList_Current_Amps_Raw),
                                                 ("CurrentSensorList_Current_Amps_Filtered", self.CurrentSensorList_Current_Amps_Filtered),
                                                 ("CurrentSensorList_CurrentDerivative_AmpsPerSec", self.CurrentSensorList_CurrentDerivative_AmpsPerSec),
                                                 ("CurrentSensorList_ErrorCallbackFiredFlag", self.CurrentSensorList_ErrorCallbackFiredFlag),
                                                 ("Time", self.CurrentSensorList_CurrentTime_CurrentSensorGENERALonCurrentChangeCallback[0])])

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_MainThread(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                self.DataStreamingFrequency_CalculatedFromMainThread = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ''' 
    ########################################################################################################## Not using MainThread as callback is sufficient in this code
    ########################################################################################################## unicorn
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class object.")

        self.MainThread_still_running_flag = 1

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################

            ########################################################################################################## USE THE TIME.SLEEP() TO SET THE LOOP FREQUENCY
            self.UpdateFrequencyCalculation_MainThread()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished MainThread for PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class object.")

        self.MainThread_still_running_flag = 0
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    '''

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class, CreateGUIobjects event fired.")

        #################################################
        #################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        #################################################
        #################################################

        #################################################
        #################################################
        self.myFrame = Frame(self.root)

        if self.UseBorderAroundThisGuiObjectFlag == 1:
            self.myFrame["borderwidth"] = 2
            self.myFrame["relief"] = "ridge"

        self.myFrame.grid(row = self.GUI_ROW,
                          column = self.GUI_COLUMN,
                          padx = self.GUI_PADX,
                          pady = self.GUI_PADY,
                          rowspan = self.GUI_ROWSPAN,
                          columnspan= self.GUI_COLUMNSPAN,
                          sticky = self.GUI_STICKY)
        #################################################
        #################################################

        #################################################
        #################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        #################################################
        #################################################

        #################################################
        #################################################
        self.DeviceInfo_Label = Label(self.myFrame, text="Device Info", width=125)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                        "\nDevice Name: " + self.DetectedDeviceName + \
                                        "\nDevice Serial Number: " + str(self.VINT_DetectedSerialNumber) + \
                                        "\nDevice ID: " + str(self.DetectedDeviceID) + \
                                        "\nDevice Version: " + str(self.DetectedDeviceVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.CurrentSensor_Label = Label(self.myFrame, text="CurrentSensor_Label", width=125)
        self.CurrentSensor_Label.grid(row=1, column=0, padx=10, pady=10, columnspan=1, rowspan=1)
        #################################################
        #################################################

        #################################################
        #################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=125)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=2, column=0, padx=10, pady=10, columnspan=10, rowspan=10)
        #################################################
        #################################################

        #################################################
        #################################################
        self.GUI_ready_to_be_updated_flag = 1
        #################################################
        #################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1:

            #######################################################
            #######################################################
            #######################################################
            #######################################################
            if self.EXIT_PROGRAM_FLAG == 0:

                #######################################################
                #######################################################
                #######################################################
                if self.GUI_ready_to_be_updated_flag == 1:

                    #######################################################
                    #######################################################
                    try:

                        #######################################################
                        self.CurrentSensor_Label["text"] = self.ConvertDictToProperlyFormattedStringForPrinting(self.MostRecentDataDict,
                                                                                                    NumberOfDecimalsPlaceToUse = 5,
                                                                                                    NumberOfEntriesPerLine = 1,
                                                                                                    NumberOfTabsBetweenItems = 3)
                        #######################################################

                        #######################################################
                        self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                        #######################################################

                    except:
                        exceptions = sys.exc_info()[0]
                        print("PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
                        traceback.print_exc()
                    #######################################################
                    #######################################################

                #######################################################
                #######################################################
                #######################################################

            #######################################################
            #######################################################
            #######################################################
            #######################################################

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        #######################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def MyPrint_WithoutLogFile(self, input_string):

        input_string = str(input_string)

        if input_string != "":

            #input_string = input_string.replace("\n", "").replace("\r", "")

            ################################ Write to console
            # Some people said that print crashed for pyinstaller-built-applications and that sys.stdout.write fixed this.
            # http://stackoverflow.com/questions/13429924/pyinstaller-packaged-application-works-fine-in-console-mode-crashes-in-window-m
            if self.PrintToConsoleFlag == 1:
                sys.stdout.write(input_string + "\n")
            ################################

            ################################ Write to GUI
            self.PrintToGui_Label_TextInputHistory_List.append(self.PrintToGui_Label_TextInputHistory_List.pop(0)) #Shift the list
            self.PrintToGui_Label_TextInputHistory_List[-1] = str(input_string) #Add the latest value

            self.PrintToGui_Label_TextInput_Str = ""
            for Counter, Line in enumerate(self.PrintToGui_Label_TextInputHistory_List):
                self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + Line

                if Counter < len(self.PrintToGui_Label_TextInputHistory_List) - 1:
                    self.PrintToGui_Label_TextInput_Str = self.PrintToGui_Label_TextInput_Str + "\n"
            ################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsInputList(self, InputToCheck):

        result = isinstance(InputToCheck, list)
        return result
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self, input, number_of_leading_numbers = 4, number_of_decimal_places = 3):

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
                    ListOfStringsToJoin.append(self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append("TUPLE" + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(element, number_of_leading_numbers, number_of_decimal_places))

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
                    ListOfStringsToJoin.append(str(Key) + ": " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(input[Key], number_of_leading_numbers, number_of_decimal_places))

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
    def ConvertDictToProperlyFormattedStringForPrinting(self, DictToPrint, NumberOfDecimalsPlaceToUse = 3, NumberOfEntriesPerLine = 1, NumberOfTabsBetweenItems = 3):

        ProperlyFormattedStringForPrinting = ""
        ItemsPerLineCounter = 0

        for Key in DictToPrint:

            ##########################################################################################################
            if isinstance(DictToPrint[Key], dict): #RECURSION
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ":\n" + \
                                                     self.ConvertDictToProperlyFormattedStringForPrinting(DictToPrint[Key], NumberOfDecimalsPlaceToUse, NumberOfEntriesPerLine, NumberOfTabsBetweenItems)

            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + \
                                                     str(Key) + ": " + \
                                                     self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(DictToPrint[Key], 0, NumberOfDecimalsPlaceToUse)
            ##########################################################################################################

            ##########################################################################################################
            if ItemsPerLineCounter < NumberOfEntriesPerLine - 1:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\t"*NumberOfTabsBetweenItems
                ItemsPerLineCounter = ItemsPerLineCounter + 1
            else:
                ProperlyFormattedStringForPrinting = ProperlyFormattedStringForPrinting + "\n"
                ItemsPerLineCounter = 0
            ##########################################################################################################

        return ProperlyFormattedStringForPrinting
    ##########################################################################################################
    ##########################################################################################################
