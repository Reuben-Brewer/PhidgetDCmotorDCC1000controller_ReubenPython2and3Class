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
from LowPassFilter_ReubenPython2and3Class import *
from PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class import *
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
from Phidget22.Devices.Encoder import *
from Phidget22.Devices.VoltageRatioInput import *
from Phidget22.Devices.TemperatureSensor import *
from Phidget22.Devices.CurrentInput import *
from Phidget22.Devices.DCMotor import * #Velocity control
from Phidget22.Devices.MotorPositionController import * #Position Control
###########################################################

##########################################################################################################
##########################################################################################################

class PhidgetDCmotorDCC1000controller_ReubenPython2and3Class(Frame): #Subclass the Tkinter Frame

    ##########################################################################################################
    ##########################################################################################################
    def __init__(self, SetupDict):

        print("#################### PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__ starting. ####################")

        #########################################################
        self.EXIT_PROGRAM_FLAG = 0
        self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
        self.EnableInternal_MyPrint_Flag = 0
        self.MainThread_still_running_flag = 0
        self.ThisIsFirstTimeEverAttachingFlag = 1
        self.PhidgetsDeviceConnectedFlag = 0
        self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG = 0
        #########################################################

        #########################################################
        self.CurrentTime_CalculatedFromMainThread = -11111.0
        self.LastTime_CalculatedFromMainThread = -11111.0
        self.StartingTime_CalculatedFromMainThread = -11111.0
        self.DataStreamingFrequency_CalculatedFromMainThread = -11111.0
        self.DataStreamingDeltaT_CalculatedFromMainThread = -11111.0
        #########################################################

        #########################################################
        self.CurrentTime_OnPositionChangeCallbackFunction = -11111.0
        self.LastTime_OnPositionChangeCallbackFunction = -11111.0
        self.DataStreamingFrequency_OnPositionChangeCallbackFunction = -11111.0
        self.DataStreamingDeltaT_OnPositionChangeCallbackFunction = -11111.0
        #########################################################

        #########################################################
        self.CurrentTime_OnVelocityUpdateCallbackFunction = -11111.0
        self.LastTime_OnVelocityUpdateCallbackFunction = -11111.0
        self.DataStreamingFrequency_OnVelocityUpdateCallbackFunction = -11111.0
        self.DataStreamingDeltaT_OnVelocityUpdateCallbackFunction = -11111.0
        #########################################################

        #########################################################
        self.DetectedDeviceName = "default"
        self.DetectedDeviceID = "default"
        self.DetectedDeviceVersion = "default"
        #########################################################

        self.LastTime_FailsafeWasReset = -11111.0

        self.StopMotor_NeedsToBeChangedFlag = 0

        self.Temperature_DegC_FromDevice = -11111.0

        self.Position_PhidgetsUnits_FromDevice = -11111.0
        self.Position_PhidgetsUnits_FromDevice_Last = -11111.0
        self.Position_PhidgetsUnits_TO_BE_SET = 0.0
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.Velocity_PhidgetsUnits_FromDevice = -11111.0
        self.Velocity_PhidgetsUnits_TO_BE_SET = 0.0
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.Velocity_PhidgetsUnits_DifferentiatedRaw = -11111.0
        self.Velocity_PhidgetsUnits_DifferentiatedSmoothed = -11111.0

        self.DutyCycle_PhidgetsUnits_FromDevice = -11111

        self.Acceleration_PhidgetsUnits_FromDevice = -11111
        self.Acceleration_PhidgetsUnits_TO_BE_SET = 0.0
        self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        self.CurrentLimit_Amps_Max_FromDevice = -11111
        self.CurrentLimit_Amps_Max_TO_BE_SET = 0.0
        self.CurrentLimit_Amps_Max_NeedsToBeChangedFlag = 1
        self.CurrentLimit_Amps_Max_GUI_NeedsToBeChangedFlag = 1

        self.CurrentLimit_Amps_Min_DeviceHardLimit = 2.0
        self.CurrentLimit_Amps_Max_DeviceHardLimit = 25.0

        self.DeadBand_PosControl_PhidgetsUnits_FromDevice = -11111
        self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = 0.0
        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 0
        self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0

        self.EngagedState_PhidgetsUnits_FromDevice = -11111
        self.EngagedState_TO_BE_SET = -1
        self.EngagedState_NeedsToBeChangedFlag = 0

        self.HomeMotorInPlace_NeedsToBeHomedFlag = 0

        self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0

        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Raw = [-11111.0]
        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Filtered = [-11111.0]
        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_ErrorCallbackFiredFlag = [-11111.0]
        self.DC30AmpCurrentSensor_MostRecentDict_Time = -11111.0

        self.MostRecentDataDict = dict()

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

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: The OS platform is: " + self.my_platform)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "GUIparametersDict" in SetupDict:
            self.GUIparametersDict = SetupDict["GUIparametersDict"]

            #########################################################
            if "USE_GUI_FLAG" in self.GUIparametersDict:
                self.USE_GUI_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_GUI_FLAG", self.GUIparametersDict["USE_GUI_FLAG"])
            else:
                self.USE_GUI_FLAG = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))
            #########################################################

            #########################################################
            if "EnableInternal_MyPrint_Flag" in self.GUIparametersDict:
                self.EnableInternal_MyPrint_Flag = self.PassThrough0and1values_ExitProgramOtherwise("EnableInternal_MyPrint_Flag", self.GUIparametersDict["EnableInternal_MyPrint_Flag"])
            else:
                self.EnableInternal_MyPrint_Flag = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: EnableInternal_MyPrint_Flag: " + str(self.EnableInternal_MyPrint_Flag))
            #########################################################

            #########################################################
            if "PrintToConsoleFlag" in self.GUIparametersDict:
                self.PrintToConsoleFlag = self.PassThrough0and1values_ExitProgramOtherwise("PrintToConsoleFlag", self.GUIparametersDict["PrintToConsoleFlag"])
            else:
                self.PrintToConsoleFlag = 1

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: PrintToConsoleFlag: " + str(self.PrintToConsoleFlag))
            #########################################################

            #########################################################
            if "NumberOfPrintLines" in self.GUIparametersDict:
                self.NumberOfPrintLines = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("NumberOfPrintLines", self.GUIparametersDict["NumberOfPrintLines"], 0.0, 50.0))
            else:
                self.NumberOfPrintLines = 10

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: NumberOfPrintLines: " + str(self.NumberOfPrintLines))
            #########################################################

            #########################################################
            if "UseBorderAroundThisGuiObjectFlag" in self.GUIparametersDict:
                self.UseBorderAroundThisGuiObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UseBorderAroundThisGuiObjectFlag", self.GUIparametersDict["UseBorderAroundThisGuiObjectFlag"])
            else:
                self.UseBorderAroundThisGuiObjectFlag = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: UseBorderAroundThisGuiObjectFlag: " + str(self.UseBorderAroundThisGuiObjectFlag))
            #########################################################

            #########################################################
            if "GUI_ROW" in self.GUIparametersDict:
                self.GUI_ROW = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROW", self.GUIparametersDict["GUI_ROW"], 0.0, 1000.0))
            else:
                self.GUI_ROW = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_ROW: " + str(self.GUI_ROW))
            #########################################################

            #########################################################
            if "GUI_COLUMN" in self.GUIparametersDict:
                self.GUI_COLUMN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMN", self.GUIparametersDict["GUI_COLUMN"], 0.0, 1000.0))
            else:
                self.GUI_COLUMN = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_COLUMN: " + str(self.GUI_COLUMN))
            #########################################################

            #########################################################
            if "GUI_PADX" in self.GUIparametersDict:
                self.GUI_PADX = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADX", self.GUIparametersDict["GUI_PADX"], 0.0, 1000.0))
            else:
                self.GUI_PADX = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_PADX: " + str(self.GUI_PADX))
            #########################################################

            #########################################################
            if "GUI_PADY" in self.GUIparametersDict:
                self.GUI_PADY = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_PADY", self.GUIparametersDict["GUI_PADY"], 0.0, 1000.0))
            else:
                self.GUI_PADY = 0

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_PADY: " + str(self.GUI_PADY))
            #########################################################

            #########################################################
            if "GUI_ROWSPAN" in self.GUIparametersDict:
                self.GUI_ROWSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_ROWSPAN", self.GUIparametersDict["GUI_ROWSPAN"], 1.0, 1000.0))
            else:
                self.GUI_ROWSPAN = 1

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_ROWSPAN: " + str(self.GUI_ROWSPAN))
            #########################################################

            #########################################################
            if "GUI_COLUMNSPAN" in self.GUIparametersDict:
                self.GUI_COLUMNSPAN = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("GUI_COLUMNSPAN", self.GUIparametersDict["GUI_COLUMNSPAN"], 1.0, 1000.0))
            else:
                self.GUI_COLUMNSPAN = 1

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_COLUMNSPAN: " + str(self.GUI_COLUMNSPAN))
            #########################################################

            #########################################################
            if "GUI_STICKY" in self.GUIparametersDict:
                self.GUI_STICKY = str(self.GUIparametersDict["GUI_STICKY"])
            else:
                self.GUI_STICKY = "w"

            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUI_STICKY = " + str(self.GUI_STICKY))
            #########################################################

        else:
            self.GUIparametersDict = dict()
            self.USE_GUI_FLAG = 0
            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: No GUIparametersDict present, setting USE_GUI_FLAG: " + str(self.USE_GUI_FLAG))

        #print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: GUIparametersDict: " + str(self.GUIparametersDict))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UsePhidgetsLoggingInternalToThisClassObjectFlag" in SetupDict:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = self.PassThrough0and1values_ExitProgramOtherwise("UsePhidgetsLoggingInternalToThisClassObjectFlag", SetupDict["UsePhidgetsLoggingInternalToThisClassObjectFlag"])
        else:
            self.UsePhidgetsLoggingInternalToThisClassObjectFlag = 1

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: UsePhidgetsLoggingInternalToThisClassObjectFlag: " + str(self.UsePhidgetsLoggingInternalToThisClassObjectFlag))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "WaitForAttached_TimeoutDuration_Milliseconds" in SetupDict:
            self.WaitForAttached_TimeoutDuration_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("WaitForAttached_TimeoutDuration_Milliseconds", SetupDict["WaitForAttached_TimeoutDuration_Milliseconds"], 0.0, 60000.0))

        else:
            self.WaitForAttached_TimeoutDuration_Milliseconds = 5000

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: WaitForAttached_TimeoutDuration_Milliseconds: " + str(self.WaitForAttached_TimeoutDuration_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredSerialNumber" in SetupDict:
            try:
                self.VINT_DesiredSerialNumber = int(SetupDict["VINT_DesiredSerialNumber"])
            except:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, VINT_DesiredSerialNumber invalid.")
        else:
            self.VINT_DesiredSerialNumber = -1

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: VINT_DesiredSerialNumber: " + str(self.VINT_DesiredSerialNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber" in SetupDict:
            try:
                self.VINT_DesiredPortNumber = int(SetupDict["VINT_DesiredPortNumber"])
            except:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, VINT_DesiredPortNumber invalid.")
        else:
            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber' argument.")
            return

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: VINT_DesiredPortNumber: " + str(self.VINT_DesiredPortNumber))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG" in SetupDict:
            print("fuck")
            self.USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG = self.PassThrough0and1values_ExitProgramOtherwise("USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG", SetupDict["USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG"])
        else:
            self.USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG = 0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG: " + str(self.USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100" in SetupDict:
            try:
                self.VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100 = int(SetupDict["VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100"])
            except:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100 invalid.")
        else:
            if self.USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG == 1:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, must initialize object with 'VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100' argument.")
                return

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100: " + str(self.VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DesiredDeviceID" in SetupDict:
            try:
                self.DesiredDeviceID = int(SetupDict["DesiredDeviceID"])
            except:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, DesiredDeviceID invalid.")
        else:
            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, must initialize object with 'DesiredDeviceID' argument.")
            return

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: DesiredDeviceID: " + str(self.DesiredDeviceID))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "NameToDisplay_UserSet" in SetupDict:
            self.NameToDisplay_UserSet = str(SetupDict["NameToDisplay_UserSet"])
        else:
            self.NameToDisplay_UserSet = ""

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: NameToDisplay_UserSet: " + str(self.NameToDisplay_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "MainThread_TimeToSleepEachLoop" in SetupDict:
            self.MainThread_TimeToSleepEachLoop = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("MainThread_TimeToSleepEachLoop", SetupDict["MainThread_TimeToSleepEachLoop"], 0.001, 100000)

        else:
            self.MainThread_TimeToSleepEachLoop = 0.005

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: MainThread_TimeToSleepEachLoop: " + str(self.MainThread_TimeToSleepEachLoop))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ENABLE_GETS_MAINTHREAD" in SetupDict:
            self.ENABLE_GETS_MAINTHREAD = int(SetupDict["ENABLE_GETS_MAINTHREAD"])

            if self.ENABLE_GETS_MAINTHREAD != 0 and self.ENABLE_GETS_MAINTHREAD != 1:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, ENABLE_GETS_MAINTHREAD in setup dict must be 0 or 1.")
                return
        else:
            self.ENABLE_GETS_MAINTHREAD = 0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: ENABLE_GETS_MAINTHREAD: " + str(self.ENABLE_GETS_MAINTHREAD))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "ControlMode" in SetupDict:
            self.ControlMode = str(SetupDict["ControlMode"]).lower()

            if self.ControlMode != "position" and self.ControlMode != "velocity":
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, ControlMode in setup dict must be 'position' or 'velocity'.")
                return
        else:
            self.ControlMode = "velocity"

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: ControlMode: " + self.ControlMode)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "UpdateDeltaT_ms" in SetupDict:
            if self.ControlMode == "position":
                self.UpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UpdateDeltaT_ms", SetupDict["UpdateDeltaT_ms"], 20.0, 60000.0))

            elif self.ControlMode == "velocity":
                self.UpdateDeltaT_ms = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("UpdateDeltaT_ms", SetupDict["UpdateDeltaT_ms"], 100.0, 60000.0))

        else:
            if self.ControlMode == "position":
                self.UpdateDeltaT_ms = int(20.0)
            elif self.ControlMode == "velocity":
                self.UpdateDeltaT_ms = int(100.0)

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: UpdateDeltaT_ms: " + str(self.UpdateDeltaT_ms))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "FailsafeTime_Milliseconds" in SetupDict:
                self.FailsafeTime_Milliseconds = int(self.PassThroughFloatValuesInRange_ExitProgramOtherwise("FailsafeTime_Milliseconds", SetupDict["FailsafeTime_Milliseconds"], 500.0, 30000.0))
        else:
            if self.ControlMode == "position":
                self.FailsafeTime_Milliseconds = int(1000.0)

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: FailsafeTime_Milliseconds: " + str(self.FailsafeTime_Milliseconds))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CurrentLimit_Amps_Min_UserSet" in SetupDict:
            self.CurrentLimit_Amps_Min_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentLimit_Amps_Min_UserSet", SetupDict["CurrentLimit_Amps_Min_UserSet"], self.CurrentLimit_Amps_Min_DeviceHardLimit, self.CurrentLimit_Amps_Max_DeviceHardLimit)

        else:
            self.CurrentLimit_Amps_Min_UserSet = self.CurrentLimit_Amps_Min_DeviceHardLimit

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: CurrentLimit_Amps_Min_UserSet: " + str(self.CurrentLimit_Amps_Min_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "CurrentLimit_Amps_Max_UserSet" in SetupDict:
            self.CurrentLimit_Amps_Max_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("CurrentLimit_Amps_Max_UserSet", SetupDict["CurrentLimit_Amps_Max_UserSet"], self.CurrentLimit_Amps_Min_DeviceHardLimit, self.CurrentLimit_Amps_Max_DeviceHardLimit)

        else:
            self.CurrentLimit_Amps_Max_UserSet = self.CurrentLimit_Amps_Max_DeviceHardLimit

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: CurrentLimit_Amps_Max_UserSet: " + str(self.CurrentLimit_Amps_Max_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "PositionMinLimit_PhidgetsUnits_UserSet" in SetupDict:
            self.PositionMinLimit_PhidgetsUnits_UserSet = SetupDict["PositionMinLimit_PhidgetsUnits_UserSet"]
        else:
            self.PositionMinLimit_PhidgetsUnits_UserSet = -7.24637681159e+12

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: PositionMinLimit_PhidgetsUnits_UserSet: " + str(self.PositionMinLimit_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "PositionMaxLimit_PhidgetsUnits_UserSet" in SetupDict:
            self.PositionMaxLimit_PhidgetsUnits_UserSet = SetupDict["PositionMaxLimit_PhidgetsUnits_UserSet"]
        else:
            self.PositionMaxLimit_PhidgetsUnits_UserSet = 7.24637681159e+12

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: PositionMaxLimit_PhidgetsUnits_UserSet: " + str(self.PositionMaxLimit_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.PositionMaxLimit_PhidgetsUnits_UserSet < self.PositionMinLimit_PhidgetsUnits_UserSet:
            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, PositionMinLimit_PhidgetsUnits_UserSet must be smaller than PositionMaxLimit_PhidgetsUnits_UserSet!")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VelocityMinLimit_PhidgetsUnits_UserSet" in SetupDict:

            if self.ControlMode == "position":
                if SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"], 0.0, 10000.0)
                else:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"], -10000.0, 0.0)

            elif self.ControlMode == "velocity":
                if SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"], 0.0, 1.0)
                else:
                    self.VelocityMinLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMinLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMinLimit_PhidgetsUnits_UserSet"], -1.0, 0.0)

        else:
            if self.ControlMode == "position":
                self.VelocityMinLimit_PhidgetsUnits_UserSet = -10000.0

            elif self.ControlMode == "velocity":
                self.VelocityMinLimit_PhidgetsUnits_UserSet = -1.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: VelocityMinLimit_PhidgetsUnits_UserSet: " + str(self.VelocityMinLimit_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "VelocityMaxLimit_PhidgetsUnits_UserSet" in SetupDict:

            if self.ControlMode == "position":
                if SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"], 0.0, 10000.0)
                else:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"], -10000.0, 0.0)

            elif self.ControlMode == "velocity":
                if SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"] > 0:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"], 0.0, 1.0)
                else:
                    self.VelocityMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("VelocityMaxLimit_PhidgetsUnits_UserSet", SetupDict["VelocityMaxLimit_PhidgetsUnits_UserSet"], -1.0, 0.0)

        else:
            if self.ControlMode == "position":
                self.VelocityMaxLimit_PhidgetsUnits_UserSet = 10000.0

            elif self.ControlMode == "velocity":
                self.VelocityMaxLimit_PhidgetsUnits_UserSet = 1.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: VelocityMaxLimit_PhidgetsUnits_UserSet: " + str(self.VelocityMaxLimit_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if self.VelocityMaxLimit_PhidgetsUnits_UserSet < self.VelocityMinLimit_PhidgetsUnits_UserSet:
            print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, VelocityMinLimit_PhidgetsUnits_UserSet must be smaller than VelocityMaxLimit_PhidgetsUnits_UserSet!")
            return
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "BrakingStrengthLimit_VelControl_Percent_UserSet" in SetupDict:
            self.BrakingStrengthLimit_VelControl_Percent_UserSet = float(SetupDict["BrakingStrengthLimit_VelControl_Percent_UserSet"])

            if self.BrakingStrengthLimit_VelControl_Percent_UserSet < 0.0 or self.BrakingStrengthLimit_VelControl_Percent_UserSet > 100.0:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, BrakingStrengthLimit_VelControl_Percent_UserSet must be between 0.0 an 100.0 percent.")
                return

        else:
            self.BrakingStrengthLimit_VelControl_Percent_UserSet = 50.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: BrakingStrengthLimit_VelControl_Percent_UserSet: " + str(self.BrakingStrengthLimit_VelControl_Percent_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "DeadBand_PosControl_PhidgetsUnits_UserSet" in SetupDict:
            self.DeadBand_PosControl_PhidgetsUnits_UserSet = float(SetupDict["DeadBand_PosControl_PhidgetsUnits_UserSet"])

            if self.DeadBand_PosControl_PhidgetsUnits_UserSet < 0.0:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, DeadBand_PosControl_PhidgetsUnits_UserSet must be greater than 0.")
                return

        else:
            self.DeadBand_PosControl_PhidgetsUnits_UserSet = 0.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: DeadBand_PosControl_PhidgetsUnits_UserSet: " + str(self.DeadBand_PosControl_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "AccelerationMaxLimit_PhidgetsUnits_UserSet" in SetupDict:

            if self.ControlMode == "position":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AccelerationMaxLimit_PhidgetsUnits_UserSet", SetupDict["AccelerationMaxLimit_PhidgetsUnits_UserSet"], 0.1, 100000.0)

            elif self.ControlMode == "velocity":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = self.PassThroughFloatValuesInRange_ExitProgramOtherwise("AccelerationMaxLimit_PhidgetsUnits_UserSet", SetupDict["AccelerationMaxLimit_PhidgetsUnits_UserSet"], 0.1, 100.0)

        else:
            if self.ControlMode == "position":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = 50000.0

            elif self.ControlMode == "velocity":
                self.AccelerationMaxLimit_PhidgetsUnits_UserSet = 50.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: AccelerationMaxLimit_PhidgetsUnits_UserSet: " + str(self.AccelerationMaxLimit_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Kp_PosControl_Gain_UserSet" in SetupDict:
            self.Kp_PosControl_Gain_UserSet = float(SetupDict["Kp_PosControl_Gain_UserSet"])
        else:
            self.Kp_PosControl_Gain_UserSet = 20000.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Kp_PosControl_Gain_UserSet: " + str(self.Kp_PosControl_Gain_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Ki_PosControl_Gain_UserSet" in SetupDict:
            self.Ki_PosControl_Gain_UserSet = float(SetupDict["Ki_PosControl_Gain_UserSet"])
        else:
            self.Ki_PosControl_Gain_UserSet = 2.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Ki_PosControl_Gain_UserSet: " + str(self.Ki_PosControl_Gain_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "Kd_PosControl_Gain_UserSet" in SetupDict:
            self.Kd_PosControl_Gain_UserSet = float(SetupDict["Kd_PosControl_Gain_UserSet"])
        else:
            self.Kd_PosControl_Gain_UserSet = 40000.0

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Kd_PosControl_Gain_UserSet: " + str(self.Kd_PosControl_Gain_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "RescaleFactor_MultipliesPhidgetsUnits_UserSet" in SetupDict:
            self.RescaleFactor_MultipliesPhidgetsUnits_UserSet = float(SetupDict["RescaleFactor_MultipliesPhidgetsUnits_UserSet"])

            if self.RescaleFactor_MultipliesPhidgetsUnits_UserSet < 0.0:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Error, RescaleFactor_MultipliesPhidgetsUnits_UserSet must be grater than 0.")
                return

        else:
            self.RescaleFactor_MultipliesPhidgetsUnits_UserSet = 1.0

        print("RescaleFactor_MultipliesPhidgetsUnits_UserSet: " + str(self.RescaleFactor_MultipliesPhidgetsUnits_UserSet))

        '''
        print("-----------------------------------------------------------------------"
                "\nFROM PHIDGETS BRUSHLESS DC MOTOR CONTROLLER USER'S GUIDE:"
                "\nInstead of steps, brushless DC motors work in commutations. "
                "\nThe number of commutations per rotation is equal to the number of poles multiplied by the number of phases. "
                "\nSo, if you have an 8-Pole, 3-Phase motor, the motor will have 24 commutations per rotation. "
                "\nFor this motor, to change the target position units from communications to rotations, you would set the rescale factor to 1/24, or 0.0416."
                "\n-----------------------------------------------------------------------")
        '''
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        if "LogFileNameFullPath" in SetupDict:
            self.LogFileNameFullPath = str(SetupDict["LogFileNameFullPath"])

            if self.LogFileNameFullPath.find("/") == -1 and self.LogFileNameFullPath.find("\\") == -1:
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__:  Error, 'LogFileNameFullPath' must be FULL path (should include slashes).")
                return

        else:
            self.LogFileNameFullPath = os.getcwd() + "\PhidgetDCmotorDCC1000controller_ReubenPython2and3Class_PhidgetLog_INFO.txt"

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: LogFileNameFullPath: " + str(self.LogFileNameFullPath))
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
            self.Velocity_LowPassFilter_Object = LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                            ("UseExponentialSmoothingFilterFlag", 1),                                                                                             ("ExponentialSmoothingFilterLambda", 0.2)]))
            time.sleep(0.1)
            self.Velocity_LowPassFilter_OPEN_FLAG = self.Velocity_LowPassFilter_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

            if self.Velocity_LowPassFilter_OPEN_FLAG != 1:
                print("Failed to open Velocity_LowPassFilter_Object.")
                self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 0
                return

        except:
            exceptions = sys.exc_info()[0]
            print("LowPassFilter_ReubenPython2and3Class __init__: Exceptions: %s" % exceptions)
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet = 0.01 * self.BrakingStrengthLimit_VelControl_Percent_UserSet * 1.0
        print("BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet: " + str(self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            self.TemperatureObject = TemperatureSensor()
            print("Created TemperatureSensor object.")

            if self.ControlMode == "velocity":
                self.DCmotorObject = DCMotor() #Create a DCMotor object for velocity control
                print("Created DCMotor object.")

            elif self.ControlMode == "position":
                self.DCmotorObject = MotorPositionController() #Create a MotorPositionController object for position control
                print("Created MotorPositionController object.")

        except PhidgetException as e:
            print("Failed to create main motor object, exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            if self.VINT_DesiredSerialNumber != -1:  # '-1' means we should open the device regardless of serial number.
                self.DCmotorObject.setDeviceSerialNumber(self.VINT_DesiredSerialNumber)

        except PhidgetException as e:
            print("Failed to call 'setDeviceSerialNumber()', exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:
            self.DCmotorObject.setHubPort(self.VINT_DesiredPortNumber)

        except PhidgetException as e:
            print("Failed to call 'setHubPort()', exception:  %i: %s" % (e.code, e.details))
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        try:

            self.TemperatureObject.setOnAttachHandler(self.TemperatureOnAttachCallback)
            self.TemperatureObject.setOnDetachHandler(self.TemperatureOnDetachCallback)
            self.TemperatureObject.setOnTemperatureChangeHandler(self.TemperatureOnChangeCallback)
            self.TemperatureObject.setOnErrorHandler(self.TemperatureOnErrorCallback)

            if self.ControlMode == "velocity":
                self.DCmotorObject.setOnAttachHandler(self.DCmotorOnAttachCallback)
                self.DCmotorObject.setOnDetachHandler(self.DCmotorOnDetachCallback)
                self.DCmotorObject.setOnVelocityUpdateHandler(self.DCmotorOnVelocityUpdateCallback)
                #self.DCmotorObject.setOnPositionChangeHandler(self.DCmotorOnPositionChangeCallback) #DOES NOT EXIST FOR DCMotor()
                self.DCmotorObject.setOnErrorHandler(self.DCmotorOnErrorCallback)

            elif self.ControlMode == "position":
                self.DCmotorObject.setOnAttachHandler(self.DCmotorOnAttachCallback)
                self.DCmotorObject.setOnDetachHandler(self.DCmotorOnDetachCallback)
                self.DCmotorObject.setOnDutyCycleUpdateHandler(self.DCmotorOnDutyCycleUpdateCallback)
                self.DCmotorObject.setOnPositionChangeHandler(self.DCmotorOnPositionChangeCallback)
                self.DCmotorObject.setOnErrorHandler(self.DCmotorOnErrorCallback)

            print("Set callback functions.")

            self.DCmotorObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.TemperatureObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)

            self.PhidgetsDeviceConnectedFlag = 1
            print("Attached the Phidgets objects.")

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            print("Failed to call 'openWaitForAttachment()', exception:  %i: %s" % (e.code, e.details))

            try:
                self.DCmotorObject.close()
                print("Closed the Phidgets objects.")

            except PhidgetException as e:
                print("Failed to call 'close()', exception:  %i: %s" % (e.code, e.details))

        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #########################################################
        if self.PhidgetsDeviceConnectedFlag == 1:

            #########################################################
            #########################################################
            if self.UsePhidgetsLoggingInternalToThisClassObjectFlag == 1:
                try:
                    Log.enable(LogLevel.PHIDGET_LOG_INFO, self.LogFileNameFullPath)
                    print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__Enabled Phidget Logging.")
                except PhidgetException as e:
                    print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__Failed to enable Phidget Logging, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            try:
                self.DetectedDeviceName = self.DCmotorObject.getDeviceName()
                print("DetectedDeviceName: " + self.DetectedDeviceName)

            except PhidgetException as e:
                print("Failed to call 'getDeviceName', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.VINT_DetectedSerialNumber = self.DCmotorObject.getDeviceSerialNumber()
                print("VINT_DetectedSerialNumber: " + str(self.VINT_DetectedSerialNumber))

            except PhidgetException as e:
                print("Failed to call 'getDeviceSerialNumber', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceID = self.DCmotorObject.getDeviceID()
                print("DetectedDeviceID: " + str(self.DetectedDeviceID))

            except PhidgetException as e:
                print("Failed to call 'getDeviceID', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceVersion = self.DCmotorObject.getDeviceVersion()
                print("DetectedDeviceVersion: " + str(self.DetectedDeviceVersion))

            except PhidgetException as e:
                print("Failed to call 'getDeviceVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DetectedDeviceLibraryVersion = self.DCmotorObject.getLibraryVersion()
                print("DetectedDeviceLibraryVersion: " + str(self.DetectedDeviceLibraryVersion))

            except PhidgetException as e:
                print("Failed to call 'getLibraryVersion', Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            if self.VINT_DesiredSerialNumber != -1:
                if self.VINT_DetectedSerialNumber != self.VINT_DesiredSerialNumber:
                    print("The desired VINT_DesiredSerialNumber (" + str(self.VINT_DesiredSerialNumber) + ") does not match the detected serial number (" + str(self.VINT_DetectedSerialNumber) + ").")
                    self.CloseAllPhidgetObjects()
                    time.sleep(0.25)
                    return
            #########################################################
            #########################################################

            #########################################################
            if self.DetectedDeviceID != self.DesiredDeviceID:
                print("The DesiredDeviceID (" + str(self.DesiredDeviceID) + ") does not match the detected Device ID (" + str(self.DetectedDeviceID) + ").")
                self.CloseAllPhidgetObjects()
                time.sleep(0.25)
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:

                #########################################################
                self.FailsafeTimeMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinFailsafeTime()
                print("FailsafeTimeMinLimit_PhidgetsUnits_FromDevice: " + str(self.FailsafeTimeMinLimit_PhidgetsUnits_FromDevice))

                self.FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxFailsafeTime()
                print("FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice: " + str(self.FailsafeTimeMaxLimit_PhidgetsUnits_FromDevice))
                #########################################################

                #########################################################
                if self.ControlMode == "position":
                    self.PositionMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinPosition()
                    print("PositionMinLimit_PhidgetsUnits_FromDevice: " + str(self.PositionMinLimit_PhidgetsUnits_FromDevice))

                    self.PositionMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxPosition()
                    print("PositionMaxLimit_PhidgetsUnits_FromDevice: " + str(self.PositionMaxLimit_PhidgetsUnits_FromDevice))
                #########################################################

                #########################################################
                if self.ControlMode == "velocity":
                    self.VelocityMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinVelocity()
                    self.VelocityMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxVelocity()

                elif self.ControlMode == "position":
                    self.VelocityMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinVelocityLimit()
                    self.VelocityMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxVelocityLimit()

                print("VelocityMinLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMinLimit_PhidgetsUnits_FromDevice))
                print("VelocityMaxLimit_PhidgetsUnits_FromDevice: " + str(self.VelocityMaxLimit_PhidgetsUnits_FromDevice))
                #########################################################

                #########################################################
                self.AccelerationMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinAcceleration()
                print("AccelerationMinLimit_PhidgetsUnits_FromDevice: " + str(self.AccelerationMinLimit_PhidgetsUnits_FromDevice))

                self.AccelerationMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxAcceleration()
                print("AccelerationMaxLimit_PhidgetsUnits_FromDevice: " + str(self.AccelerationMaxLimit_PhidgetsUnits_FromDevice))
                #########################################################

                #########################################################
                self.DataIntervalMin = self.DCmotorObject.getMinDataInterval()
                print("DataIntervalMin: " + str(self.DataIntervalMin))

                self.DataIntervalMax = self.DCmotorObject.getMaxDataInterval()
                print("DataIntervalMax: " + str(self.DataIntervalMax))
                #########################################################

                #########################################################
                if self.ControlMode == "velocity":
                    self.BrakingStrengthMinLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMinBrakingStrength()
                    self.BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice = self.DCmotorObject.getMaxBrakingStrength()
                    print("BrakingStrengthMinLimit_PhidgetsUnits_FromDevice: " + str(self.BrakingStrengthMinLimit_PhidgetsUnits_FromDevice))
                    print("BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice: " + str(self.BrakingStrengthMaxLimit_PhidgetsUnits_FromDevice))
                #########################################################

            except PhidgetException as e:

                #########################################################
                print("Failed to motor limits, Phidget Exception %i: %s" % (e.code, e.details))
                traceback.print_exc()
                return
                #########################################################

            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_Object = LowPassFilter_ReubenPython2and3Class(dict([("UseMedianFilterFlag", 0),
                                                                                                                ("UseExponentialSmoothingFilterFlag", 1),
                                                                                                                ("ExponentialSmoothingFilterLambda", 0.05)])) ##new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

            except:
                exceptions = sys.exc_info()[0]
                print("ArucoTagDetectionFromCameraFeed_ReubenPython3Class __init__: DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_Object, Exceptions: %s" % exceptions)
                traceback.print_exc()
                return
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.MainThread_ThreadingObject = threading.Thread(target=self.MainThread, args=())
            self.MainThread_ThreadingObject.start()
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            try:
                self.PhidgetsCurrentSensor30ampDConlyVCP1100_GUIparametersDict = dict([("USE_GUI_FLAG", self.USE_GUI_FLAG),
                                                                                    ("EnableInternal_MyPrint_Flag", 0),
                                                                                    ("NumberOfPrintLines", 10),
                                                                                    ("UseBorderAroundThisGuiObjectFlag", 0),
                                                                                    ("GUI_ROW", 0),
                                                                                    ("GUI_COLUMN", 0),
                                                                                    ("GUI_PADX", 1),
                                                                                    ("GUI_PADY", 1),
                                                                                    ("GUI_ROWSPAN", 1),
                                                                                    ("GUI_COLUMNSPAN", 1)])

                self.PhidgetsCurrentSensor30ampDConlyVCP1100_SetupDict = dict([("GUIparametersDict", self.PhidgetsCurrentSensor30ampDConlyVCP1100_GUIparametersDict),
                                                                                ("VINT_DesiredSerialNumber", self.VINT_DetectedSerialNumber),
                                                                                ("VINT_DesiredPortNumber", self.VINT_DesiredPortNumber_PhidgetsCurrentSensor30ampDConlyVCP1100),
                                                                                ("DesiredDeviceID", 105),
                                                                                ("WaitForAttached_TimeoutDuration_Milliseconds", 5000),
                                                                                ("NameToDisplay_UserSet", "Current Sensor"),
                                                                                ("UsePhidgetsLoggingInternalToThisClassObjectFlag", 1),
                                                                                ("DataCallbackUpdateDeltaT_ms", 100),
                                                                                ("CurrentSensorList_Current_Amps_ExponentialFilterLambda", [0.95])]) #new_filtered_value = k * raw_sensor_value + (1 - k) * old_filtered_value

                if self.USE_PhidgetsCurrentSensor30ampDConlyVCP1100_FLAG == 1:
                    try:
                        self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object = PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class(self.PhidgetsCurrentSensor30ampDConlyVCP1100_SetupDict)
                        self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG = self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object.OBJECT_CREATED_SUCCESSFULLY_FLAG

                        if self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG != 1:
                            print("PhidgetsCurrentSensor30ampDConlyVCP1100_Object __init__: Failed to open.")
                            return

                    except:
                        exceptions = sys.exc_info()[0]
                        print("PhidgetsCurrentSensor30ampDConlyVCP1100_Object __init__: Exceptions: %s" % exceptions)
                        traceback.print_exc()

            except PhidgetException as e:
                self.PhidgetsDeviceConnectedFlag = 0
                print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class __init__: Failed to attach PhidgetsCurrentSensor30ampDConlyVCP1100_Object, Phidget Exception %i: %s" % (e.code, e.details))
            #########################################################
            #########################################################

            #########################################################
            #########################################################
            self.OBJECT_CREATED_SUCCESSFULLY_FLAG = 1
            #########################################################
            #########################################################

        #########################################################
        #########################################################
        #########################################################

        #########################################################
        #########################################################
        #########################################################
        else:
            print("---------- Failed to open PhidgetDCmotorDCC1000controller_ReubenPython2and3Class for serial number " + str(self.VINT_DesiredSerialNumber) + " ----------")
        #########################################################
        #########################################################
        #########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CloseAllPhidgetObjects(self):

        try:

            self.DCmotorObject.close()
            self.TemperatureObject.close()

            if self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG == 1:
                self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object.ExitProgram_Callback()

        except PhidgetException as e:
            print("CloseAllPhidgetObjects, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def IsNumber0or1(self, InputNumber):

        if float(InputNumber) == 0.0 or float(InputNumber) == 1:
            return 1
        else:
            return 0
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
    def DCmotorOnAttachCallback(self, HandlerSelf):

        try:

            ##############################
            self.DCmotorObject.setDataInterval(self.UpdateDeltaT_ms)
            self.MyPrint_WithoutLogFile("The device currently has DataInterval: " + str(self.DCmotorObject.getDataInterval()))
            ##############################

            ##############################
            if self.ControlMode == "position":
                self.DCmotorObject.setRescaleFactor(self.RescaleFactor_MultipliesPhidgetsUnits_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has RescaleFactor: " + str(self.DCmotorObject.getRescaleFactor()))
            ##############################

            ##############################
            self.Acceleration_PhidgetsUnits_TO_BE_SET = self.AccelerationMaxLimit_PhidgetsUnits_UserSet
            self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1
            self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
            ##############################
            
            ##############################
            self.CurrentLimit_Amps_Max_TO_BE_SET = self.CurrentLimit_Amps_Max_UserSet
            self.CurrentLimit_Amps_Max_NeedsToBeChangedFlag = 1
            self.CurrentLimit_Amps_Max_GUI_NeedsToBeChangedFlag = 0
            ##############################

            ##############################
            if self.ControlMode == "velocity":

                ##############################
                self.DCmotorObject.setTargetBrakingStrength(self.BrakingStrengthLimit_VelControl_PhidgetsUnits_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has BrakingStrength: " + str(self.DCmotorObject.getTargetBrakingStrength()))
                ##############################

                ##############################
                if self.ThisIsFirstTimeEverAttachingFlag == 1:
                    self.Velocity_PhidgetsUnits_TO_BE_SET = 0.0
                else:
                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.Velocity_PhidgetsUnits_FromDevice #Stay wherever you were when you detached

                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                ##############################

            ##############################

            ##############################
            elif self.ControlMode == "position":

                ##############################
                self.DCmotorObject.setKp(self.Kp_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Kp: " + str(self.DCmotorObject.getKp()))

                self.DCmotorObject.setKi(self.Ki_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Ki: " + str(self.DCmotorObject.getKi()))

                self.DCmotorObject.setKd(self.Kd_PosControl_Gain_UserSet)
                self.MyPrint_WithoutLogFile("The device currently has Kd: " + str(self.DCmotorObject.getKd()))
                ##############################

                ##############################
                self.EngagedState_TO_BE_SET = 1
                self.EngagedState_NeedsToBeChangedFlag = 1
                ##############################

                ##############################
                if self.ThisIsFirstTimeEverAttachingFlag == 1:
                    self.Position_PhidgetsUnits_TO_BE_SET = 0.0
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_UserSet

                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.VelocityMaxLimit_PhidgetsUnits_UserSet

                else:
                    self.Position_PhidgetsUnits_TO_BE_SET = self.Position_PhidgetsUnits_FromDevice #Stay wherever you were when you detached
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_FromDevice

                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.VelocityMaxLimit_PhidgetsUnits_UserSet

                self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

                self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                ##############################

            ##############################

            ##############################
            if self.ThisIsFirstTimeEverAttachingFlag == 0:
                self.ThisIsFirstTimeEverAttachingFlag = 1
            ##############################

            self.PhidgetsDeviceConnectedFlag = 1
            self.MyPrint_WithoutLogFile("$$$$$$$$$$ DCmotorOnAttachCallback Attached Event! $$$$$$$$$$")

        except PhidgetException as e:
            self.PhidgetsDeviceConnectedFlag = 0
            self.MyPrint_WithoutLogFile("DCmotorOnAttachCallback ERROR: Failed to initialize the BLDC, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DCmotorOnDetachCallback(self, HandlerSelf):
        self.PhidgetsDeviceConnectedFlag = 0

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ DCmotorOnDetachCallback Detached Event! $$$$$$$$$$")

        try:
            self.DCmotorObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("DCmotorOnDetachCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DCmotorOnVelocityUpdateCallback(self, HandlerSelf, VelocityUpdatedValue):

        self.Velocity_PhidgetsUnits_FromDevice = VelocityUpdatedValue

        self.CurrentTime_OnVelocityUpdateCallbackFunction = self.getPreciseSecondsTimeStampString()
        self.UpdateFrequencyCalculation_OnVelocityUpdateCallbackFunction()

        #self.MyPrint_WithoutLogFile("DCmotorOnVelocityUpdateCallback event: self.Velocity_PhidgetsUnits_FromDevice = " + str(self.Velocity_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DCmotorOnPositionChangeCallback(self, HandlerSelf, PositionChangedValue):

        self.Position_PhidgetsUnits_FromDevice = PositionChangedValue

        self.CurrentTime_OnPositionChangeCallbackFunction = self.getPreciseSecondsTimeStampString()
        self.UpdateFrequencyCalculation_OnPositionChangeCallbackFunction()

        if self.DataStreamingDeltaT_OnPositionChangeCallbackFunction > 0:
            self.Velocity_PhidgetsUnits_DifferentiatedRaw = (self.Position_PhidgetsUnits_FromDevice - self.Position_PhidgetsUnits_FromDevice_Last)/(self.DataStreamingDeltaT_OnPositionChangeCallbackFunction)
            self.Velocity_PhidgetsUnits_DifferentiatedSmoothed = self.Velocity_LowPassFilter_Object.AddDataPointFromExternalProgram(self.Velocity_PhidgetsUnits_DifferentiatedRaw)["SignalOutSmoothed"]

        self.Position_PhidgetsUnits_FromDevice_Last = self.Position_PhidgetsUnits_FromDevice

        #self.MyPrint_WithoutLogFile("DCmotorOnPositionChangeCallback event: self.Position_PhidgetsUnits_FromDevice = " + str(self.Position_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DCmotorOnDutyCycleUpdateCallback(self, HandlerSelf, DutyCycleUpdatedValue):

        self.DutyCycle_PhidgetsUnits_FromDevice = DutyCycleUpdatedValue

        #self.MyPrint_WithoutLogFile("DCmotorOnDutyCycleUpdateCallback event: self.DutyCycle_PhidgetsUnits_FromDevice = " + str(self.DutyCycle_PhidgetsUnits_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DCmotorOnErrorCallback(self, HandlerSelf, code, description):
        self.MyPrint_WithoutLogFile("----------")
        self.MyPrint_WithoutLogFile("DCmotorOnErrorCallback Code: " + ErrorEventCode.getName(code) + ", Description: " + str(description))
        self.MyPrint_WithoutLogFile("----------")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnAttachCallback(self, HandlerSelf):

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureOnAttachCallback Attached Event! $$$$$$$$$$")

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnDetachCallback(self, HandlerSelf):

        self.MyPrint_WithoutLogFile("$$$$$$$$$$ TemperatureOnDetachCallback Detached Event! $$$$$$$$$$")

        try:
            self.TemperatureObject.openWaitForAttachment(self.WaitForAttached_TimeoutDuration_Milliseconds)
            time.sleep(0.250)

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("TemperatureOnDetachCallback failed to waitForAttach, Phidget Exception %i: %s" % (e.code, e.details))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnChangeCallback(self, HandlerSelf, TemperatureChangedValue):

        self.Temperature_DegC_FromDevice = TemperatureChangedValue

        #self.MyPrint_WithoutLogFile("TemperatureOnChangeCallback event: self.Temperature_DegC_FromDevice = " + str(self.Temperature_DegC_FromDevice))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def TemperatureOnErrorCallback(self, HandlerSelf, code, description):
        self.MyPrint_WithoutLogFile("----------")
        self.MyPrint_WithoutLogFile("TemperatureOnErrorCallback Code: " + ErrorEventCode.getName(code) + ", Description: " + str(description))
        self.MyPrint_WithoutLogFile("----------")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def getTimeStampString(self):

        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('date-%m-%d-%Y---time-%H-%M-%S')

        return st
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
    def UpdateFrequencyCalculation_MainThread_Filtered(self):

        try:
            self.DataStreamingDeltaT_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread - self.LastTime_CalculatedFromMainThread

            if self.DataStreamingDeltaT_CalculatedFromMainThread != 0.0:
                DataStreamingFrequency_CalculatedFromMainThread_TEMP = 1.0/self.DataStreamingDeltaT_CalculatedFromMainThread
                self.DataStreamingFrequency_CalculatedFromMainThread = self.DataStreamingFrequency_CalculatedFromMainThread_LowPassFilter_Object.AddDataPointFromExternalProgram(DataStreamingFrequency_CalculatedFromMainThread_TEMP)["SignalOutSmoothed"]

            self.LastTime_CalculatedFromMainThread = self.CurrentTime_CalculatedFromMainThread
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_MainThread_Filtered, Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_OnPositionChangeCallbackFunction(self):

        try:
            self.DataStreamingDeltaT_OnPositionChangeCallbackFunction = self.CurrentTime_OnPositionChangeCallbackFunction - self.LastTime_OnPositionChangeCallbackFunction

            if self.DataStreamingDeltaT_OnPositionChangeCallbackFunction != 0.0:
                self.DataStreamingFrequency_OnPositionChangeCallbackFunction = 1.0/self.DataStreamingDeltaT_OnPositionChangeCallbackFunction

            self.LastTime_OnPositionChangeCallbackFunction = self.CurrentTime_OnPositionChangeCallbackFunction
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_OnPositionChangeCallbackFunction ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def UpdateFrequencyCalculation_OnVelocityUpdateCallbackFunction(self):

        try:
            self.DataStreamingDeltaT_OnVelocityUpdateCallbackFunction = self.CurrentTime_OnVelocityUpdateCallbackFunction - self.LastTime_OnVelocityUpdateCallbackFunction

            if self.DataStreamingDeltaT_OnVelocityUpdateCallbackFunction != 0.0:
                self.DataStreamingFrequency_OnVelocityUpdateCallbackFunction = 1.0/self.DataStreamingDeltaT_OnVelocityUpdateCallbackFunction

            self.LastTime_OnVelocityUpdateCallbackFunction = self.CurrentTime_OnVelocityUpdateCallbackFunction
        except:
            exceptions = sys.exc_info()[0]
            print("UpdateFrequencyCalculation_OnVelocityUpdateCallbackFunction ERROR with Exceptions: %s" % exceptions)
            traceback.print_exc()
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ########################################################################################################## unicorn
    def CommandMotorFromExternalProgram_PositionControl(self, commanded_position_PhidgetsUnits, commanded_velocity_limit_PhidgetsUnits = -11111.0):

        ######################
        if self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG == 0:
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0")
            return 0
        ######################

        ######################
        if self.ControlMode != "position":
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: self.ControlMode must be 'position'")
            return 0
        ######################

        ######################
        self.Position_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, commanded_position_PhidgetsUnits)
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################

        ######################
        if commanded_velocity_limit_PhidgetsUnits != -11111.0:
            if commanded_velocity_limit_PhidgetsUnits != self.Velocity_PhidgetsUnits_TO_BE_SET:
                self.Velocity_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, commanded_velocity_limit_PhidgetsUnits)
                self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CommandMotorFromExternalProgram_VelocityControl(self, commanded_velocity_PhidgetsUnits):

        ######################
        if self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG == 0:
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 0")
            return 0
        ######################
        
        ######################
        if self.ControlMode != "velocity":
            self.MyPrint_WithoutLogFile("CommandMotorFromExternalProgram ERROR: self.ControlMode must be 'velocity'")
            return 0
        ######################

        ######################
        self.Velocity_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, commanded_velocity_PhidgetsUnits)
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
        ######################
        
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def StopMotor(self):

        if self.ControlMode == "velocity":
            self.Velocity_PhidgetsUnits_TO_BE_SET = 0
            self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1
            self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1

        elif self.ControlMode == "position":
            self.EngagedState_TO_BE_SET = 0
            self.EngagedState_NeedsToBeChangedFlag = 1

        self.MyPrint_WithoutLogFile("StopMotor function called!")
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetPositionOffsetOnBoardWithoutMoving(self, commanded_position_offset_value_PhidgetsUnits):

        commanded_position_offset_value_PhidgetsUnits_LIMITED = self.LimitNumber_FloatOutputOnly(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, commanded_position_offset_value_PhidgetsUnits)

        try:
            self.DCmotorObject.addPositionOffset(commanded_position_offset_value_PhidgetsUnits_LIMITED)
            self.MyPrint_WithoutLogFile("SetPositionOffsetOnBoardWithoutMoving issued addPositionOffset for value of " + str(commanded_position_offset_value_PhidgetsUnits_LIMITED))
            return 1

        except PhidgetException as e:
            self.MyPrint_WithoutLogFile("SetPositionOffsetOnBoardWithoutMoving ERROR, Phidget Exception %i: %s" % (e.code, e.details))
            return 0

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    def HomeMotorInPlace(self):

        Position_PhidgetsUnits_FromDevice_JUST_QUERIED = self.DCmotorObject.getPosition()
        self.MyPrint_WithoutLogFile("HomeMotorInPlace Position_PhidgetsUnits_FromDevice_JUST_QUERIED BEFORE adding offset: " + str(Position_PhidgetsUnits_FromDevice_JUST_QUERIED))

        self.DCmotorObject.addPositionOffset(-1.0*Position_PhidgetsUnits_FromDevice_JUST_QUERIED) #MUST HAVE THE MINUS SIGN, OR ELSE THE OFFSET DOESN'T SET UT TO ZERO.

        Position_PhidgetsUnits_FromDevice_JUST_QUERIED = self.DCmotorObject.getPosition()
        self.MyPrint_WithoutLogFile("HomeMotorInPlace Position_PhidgetsUnits_FromDevice_JUST_QUERIED AFTER adding offset: " + str(Position_PhidgetsUnits_FromDevice_JUST_QUERIED))

        if self.ControlMode == "position":
            for counter in range(0, 4): #SEND COMMAND MULTIPLE TIMES TO MAKE SURE THAT IT TAKES!
                self.Position_PhidgetsUnits_TO_BE_SET = 0.0
                self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1
                self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 1
                time.sleep(0.005)

        self.MyPrint_WithoutLogFile("----- HomeMotorInPlace just performed! -----")

    ##########################################################################################################
    ##########################################################################################################

    ########################################################################################################## unicorn
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    def MainThread(self):

        self.MyPrint_WithoutLogFile("Started MainThread for PhidgetDCmotorDCC1000controller_ReubenPython2and3Class.")

        self.MainThread_still_running_flag = 1

        self.ACCEPT_EXTERNAL_POSITION_COMMANDS_FLAG = 1

        self.DCmotorObject.enableFailsafe(self.FailsafeTime_Milliseconds)

        self.StartingTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString()

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        while self.EXIT_PROGRAM_FLAG == 0:

            ##########################################################################################################
            ##########################################################################################################
            self.CurrentTime_CalculatedFromMainThread = self.getPreciseSecondsTimeStampString() - self.StartingTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################

            ##########################################################################################################
            ##########################################################################################################
            if self.CurrentTime_CalculatedFromMainThread - self.LastTime_FailsafeWasReset >= 0.5*self.FailsafeTime_Milliseconds/1000.0: #IF YOU CALL resetFailsafe every PID loop, it'll kill your loop frequency
                #self.MyPrint_WithoutLogFile("RESET FAILSAFE AT TIME = " + str(self.CurrentTime_CalculatedFromMainThread))
                self.DCmotorObject.resetFailsafe() #resetFailsafe is faster than enableFailsafe
                self.LastTime_FailsafeWasReset = self.CurrentTime_CalculatedFromMainThread
            ##########################################################################################################
            ##########################################################################################################

            ########################################################################################################## Start SETs
            ##########################################################################################################

            ##########################################################################################################
            if self.StopMotor_NeedsToBeChangedFlag == 1:
                self.StopMotor()
                self.StopMotor_NeedsToBeChangedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.HomeMotorInPlace_NeedsToBeHomedFlag == 1:
                self.HomeMotorInPlace()
                self.HomeMotorInPlace_NeedsToBeHomedFlag = 0
            ##########################################################################################################

            ##########################################################################################################
            if self.EngagedState_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    self.DCmotorObject.setEngaged(self.EngagedState_TO_BE_SET)
                    if self.DCmotorObject.getEngaged() == 1:
                        self.EngagedState_NeedsToBeChangedFlag = 0
                except:
                    self.MyPrint_WithoutLogFile("ERROR: Failed to change EngagedState!")
            ##########################################################################################################

            ########################################################################################################## Tx portion
            if self.Position_PhidgetsUnits_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    self.Position_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.PositionMinLimit_PhidgetsUnits_UserSet, self.PositionMaxLimit_PhidgetsUnits_UserSet, self.Position_PhidgetsUnits_TO_BE_SET)
                    self.DCmotorObject.setTargetPosition(float(self.Position_PhidgetsUnits_TO_BE_SET))
                    self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setTargetPosition, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################

            ##########################################################################################################
            if self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag == 1:
                try:
                    self.Velocity_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.VelocityMinLimit_PhidgetsUnits_UserSet, self.VelocityMaxLimit_PhidgetsUnits_UserSet, self.Velocity_PhidgetsUnits_TO_BE_SET)

                    if self.ControlMode == "position":
                        self.DCmotorObject.setVelocityLimit(float(self.Velocity_PhidgetsUnits_TO_BE_SET))

                    elif self.ControlMode == "velocity":
                        self.DCmotorObject.setTargetVelocity(float(self.Velocity_PhidgetsUnits_TO_BE_SET))

                    self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setVelocityLimit, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################

            ##########################################################################################################
            if self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag == 1:
                try:
                    self.Acceleration_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.AccelerationMinLimit_PhidgetsUnits_FromDevice, self.AccelerationMaxLimit_PhidgetsUnits_FromDevice, self.Acceleration_PhidgetsUnits_TO_BE_SET)
                    self.DCmotorObject.setAcceleration(float(self.Acceleration_PhidgetsUnits_TO_BE_SET))
                    self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setAcceleration, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################

            ##########################################################################################################
            if self.CurrentLimit_Amps_Max_NeedsToBeChangedFlag == 1:
                try:
                    self.CurrentLimit_Amps_Max_TO_BE_SET = self.LimitNumber_FloatOutputOnly(self.CurrentLimit_Amps_Min_UserSet, self.CurrentLimit_Amps_Max_UserSet, self.CurrentLimit_Amps_Max_TO_BE_SET)
                    self.DCmotorObject.setCurrentLimit(float(self.CurrentLimit_Amps_Max_TO_BE_SET))
                    self.CurrentLimit_Amps_Max_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setCurrentLimit, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################

            ##########################################################################################################
            if self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag == 1 and self.ControlMode == "position":
                try:
                    self.MyPrint_WithoutLogFile("Sending DeadBand to the Phidget, value = " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.LimitNumber_FloatOutputOnly(0, self.PositionMaxLimit_PhidgetsUnits_UserSet, self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET) #Limit to max position since DeadBand is in position units
                    self.DCmotorObject.setDeadBand(float(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    #time.sleep(0.001)
                    self.DeadBand_PosControl_PhidgetsUnits_FromDevice = self.DCmotorObject.getDeadBand()
                    #print("self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET: " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
                    if self.DeadBand_PosControl_PhidgetsUnits_FromDevice == self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET:
                        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 0

                except PhidgetException as e:
                    self.MyPrint_WithoutLogFile("Failed setTargetDeadBand, Phidget Exception %i: %s" % (e.code, e.details))
            ##########################################################################################################

            ##########################################################################################################
            ########################################################################################################## End SETs

            ########################################################################################################## Start GETs
            ##########################################################################################################
            if self.ControlMode == "position":
                self.EngagedState_PhidgetsUnits_FromDevice = self.DCmotorObject.getEngaged() #NOT INCLUDING UNDER ENABLE_GETS_MAINTHREAD BECAUSE THIS IS CRITICAL TO FUNCTIONALITY
            else:
                self.EngagedState_PhidgetsUnits_FromDevice = 1

            if self.ENABLE_GETS_MAINTHREAD == 1:
                self.Acceleration_PhidgetsUnits_FromDevice = self.DCmotorObject.getAcceleration()

                if self.ControlMode == "position":
                    self.DeadBand_PosControl_PhidgetsUnits_FromDevice = self.DCmotorObject.getDeadBand()
                    #print(self.DeadBand_PosControl_PhidgetsUnits_FromDevice)

                #################################################### GET's
                ####################################################
                if self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG == 1:

                    self.DC30AmpCurrentSensor_MostRecentDict = self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object.GetMostRecentDataDict()

                    if "Time" in self.DC30AmpCurrentSensor_MostRecentDict:
                        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Raw = self.DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_Current_Amps_Raw"]
                        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Filtered = self.DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_Current_Amps_Filtered"]
                        self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_ErrorCallbackFiredFlag = self.DC30AmpCurrentSensor_MostRecentDict["CurrentSensorList_ErrorCallbackFiredFlag"]
                        self.DC30AmpCurrentSensor_MostRecentDict_Time = self.DC30AmpCurrentSensor_MostRecentDict["Time"]

                        # print("DC30AmpCurrentSensor_MostRecentDict_Time: " + str(DC30AmpCurrentSensor_MostRecentDict_Time))
                ####################################################
                ####################################################

            ##########################################################################################################
            ########################################################################################################## End GETs

            ##########################################################################################################
            ##########################################################################################################
            self.UpdateFrequencyCalculation_MainThread_Filtered()

            if self.MainThread_TimeToSleepEachLoop > 0.0:
                if self.MainThread_TimeToSleepEachLoop > 0.001:
                    time.sleep(self.MainThread_TimeToSleepEachLoop - 0.001) #The "- 0.001" corrects for slight deviation from intended frequency due to other functions being called.
                else:
                    time.sleep(self.MainThread_TimeToSleepEachLoop)
            ##########################################################################################################
            ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################
        self.CloseAllPhidgetObjects()
        ##########################################################################################################
        ##########################################################################################################
        ##########################################################################################################

        self.MyPrint_WithoutLogFile("Finished the MainThread for PhidgetDCmotorDCC1000controller_ReubenPython2and3Class object.")
        self.MainThread_still_running_flag = 0

    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GetMostRecentDataDict(self):

        if self.EXIT_PROGRAM_FLAG == 0:

            self.MostRecentDataDict = dict([("Position_PhidgetsUnits_TO_BE_SET", self.Position_PhidgetsUnits_TO_BE_SET),
                                            ("Velocity_PhidgetsUnits_TO_BE_SET", self.Velocity_PhidgetsUnits_TO_BE_SET),
                                            ("Position_PhidgetsUnits_FromDevice", self.Position_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_FromDevice", self.Velocity_PhidgetsUnits_FromDevice),
                                            ("Velocity_PhidgetsUnits_DifferentiatedRaw", self.Velocity_PhidgetsUnits_DifferentiatedRaw),
                                            ("Velocity_PhidgetsUnits_DifferentiatedSmoothed", self.Velocity_PhidgetsUnits_DifferentiatedSmoothed),
                                            ("DutyCycle_PhidgetsUnits_FromDevice", self.DutyCycle_PhidgetsUnits_FromDevice),
                                            ("Temperature_DegC_FromDevice", self.Temperature_DegC_FromDevice),
                                            ("Current_Amps_Raw_FromDevice", self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Raw),
                                            ("Current_Amps_Filtered_FromDevice", self.DC30AmpCurrentSensor_MostRecentDict_DC30AmpCurrentSensorList_Current_Amps_Filtered),
                                            ("Time", self.CurrentTime_CalculatedFromMainThread)])

            return deepcopy(self.MostRecentDataDict) #deepcopy IS required as MostRecentDataDict contains lists.

        else:
            return dict() #So that we're not returning variables during the close-down process.
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def ExitProgram_Callback(self):

        print("Exiting all threads for Phidgets4EncoderAndDInput1047_ReubenPython2and3Class object")

        self.EXIT_PROGRAM_FLAG = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CreateGUIobjects(self, TkinterParent):

        print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class, TkinterParent event fired.")

        ###########################################################
        ###########################################################
        self.root = TkinterParent
        self.parent = TkinterParent
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
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
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.TKinter_LightGreenColor = '#%02x%02x%02x' % (150, 255, 150) #RGB
        self.TKinter_LightRedColor = '#%02x%02x%02x' % (255, 150, 150) #RGB
        self.TKinter_LightYellowColor = '#%02x%02x%02x' % (255, 255, 150)  # RGB
        self.TKinter_DefaultGrayColor = '#%02x%02x%02x' % (240, 240, 240)  # RGB
        self.TkinterScaleWidth = 10
        self.TkinterScaleLength = 250
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.AllButtonsFrame = Frame(self.myFrame)
        self.AllButtonsFrame["borderwidth"] = 2
        #self.AllButtonsFrame["relief"] = "ridge"
        self.AllButtonsFrame.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        self.Button_Width = 15
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.HomeMotorInPlaceButton = Button(self.AllButtonsFrame, text='HomeInPlace', state="normal", width=self.Button_Width, command=lambda i=1: self.HomeMotorInPlaceButtonResponse())
        self.HomeMotorInPlaceButton.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        if self.ControlMode == "position":
            self.HomeMotorInPlaceButton["bg"] = self.TKinter_LightGreenColor
        elif self.ControlMode == "velocity":
            self.HomeMotorInPlaceButton["state"] = "disabled"
        ###########################################################
        ###########################################################

        '''
        ########################################################### Cannot set the engaged state in velocity mode, so we're replacing the engaged button with more general stop button
        ###########################################################
        self.EngagedStateButton = Button(self.AllButtonsFrame, text='Engaged: x', state="normal", width=self.Button_Width, command=lambda i=1: self.EngagedStateButtonResponse())
        self.EngagedStateButton.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        if self.ControlMode == "velocity":
            self.EngagedStateButton["state"] = "disabled"
        ###########################################################
        ###########################################################
        '''

        ###########################################################
        ###########################################################
        self.StopMotorButton = Button(self.AllButtonsFrame, text='Stop Motor', state="normal", width=self.Button_Width*2, command=lambda i=1: self.StopMotorButtonResponse())
        self.StopMotorButton.grid(row=0, column=2, padx=1, pady=1, columnspan=1, rowspan=1)
        self.StopMotorButton["bg"] = self.TKinter_LightGreenColor
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.AllLabelsFrame = Frame(self.myFrame)
        self.AllLabelsFrame["borderwidth"] = 2
        #self.AllLabelsFrame["relief"] = "ridge"
        self.AllLabelsFrame.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.DeviceInfo_Label = Label(self.AllLabelsFrame, text="Device Info", width=75)

        self.DeviceInfo_Label["text"] = self.NameToDisplay_UserSet + \
                                         "\nDevice Name: " + self.DetectedDeviceName + \
                                         "\nVINT SerialNumber: " + str(self.VINT_DetectedSerialNumber) + \
                                         "\nDeviceID: " + str(self.DetectedDeviceID) + \
                                         "\nFW Ver: " + str(self.DetectedDeviceVersion) + \
                                         "\nLibrary Ver: " + str(self.DetectedDeviceLibraryVersion)

        self.DeviceInfo_Label.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.Data_Label = Label(self.AllLabelsFrame, text="Data Info", width=75)
        self.Data_Label.grid(row=0, column=1, padx=1, pady=1, columnspan=1, rowspan=1)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.AllScalesFrame = Frame(self.myFrame)
        self.AllScalesFrame["borderwidth"] = 2
        #self.AllScalesFrame["relief"] = "ridge"
        self.AllScalesFrame.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.Position_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Position", width=20)
        self.Position_PhidgetsUnits_ScaleLabel.grid(row=0, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        # self.PositionMinLimit_PhidgetsUnits_UserSet,\  #self.PositionMaxLimit_PhidgetsUnits_UserSet, \
        self.Position_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Position_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.PositionMinLimit_PhidgetsUnits_UserSet,\
                                            to= self.PositionMaxLimit_PhidgetsUnits_UserSet,\
                                            #tickinterval=(self.Position_PhidgetsUnits_max - self.Position_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.1,\
                                            variable=self.Position_PhidgetsUnits_ScaleValue)
        self.Position_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name))
        self.Position_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Position": self.Position_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Position_PhidgetsUnits_Scale.set(self.Position_PhidgetsUnits_TO_BE_SET)
        self.Position_PhidgetsUnits_Scale.grid(row=0, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #Color gets controlled by engaged flag within the main GUI loop

        if self.ControlMode == "velocity":
            self.Position_PhidgetsUnits_Scale["state"] = "disabled"
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.Velocity_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Velocity", width=20)
        self.Velocity_PhidgetsUnits_ScaleLabel.grid(row=1, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Velocity_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Velocity_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.VelocityMinLimit_PhidgetsUnits_UserSet,\
                                            to=self.VelocityMaxLimit_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.Velocity_PhidgetsUnits_max - self.Velocity_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.Velocity_PhidgetsUnits_ScaleValue)
        self.Velocity_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Velocity_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name))
        self.Velocity_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Velocity": self.Velocity_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Velocity_PhidgetsUnits_Scale.set(self.Velocity_PhidgetsUnits_TO_BE_SET)
        self.Velocity_PhidgetsUnits_Scale.grid(row=1, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #Color gets controlled by engaged flag within the main GUI loop
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.Acceleration_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="Acceleration", width=20)
        self.Acceleration_PhidgetsUnits_ScaleLabel.grid(row=2, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.Acceleration_PhidgetsUnits_ScaleValue = DoubleVar()
        self.Acceleration_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.AccelerationMinLimit_PhidgetsUnits_FromDevice,\
                                            to=self.AccelerationMaxLimit_PhidgetsUnits_UserSet, \
                                            #tickinterval=(self.Acceleration_PhidgetsUnits_max - self.Acceleration_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.Acceleration_PhidgetsUnits_ScaleValue)
        self.Acceleration_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name))
        self.Acceleration_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="Acceleration": self.Acceleration_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.Acceleration_PhidgetsUnits_Scale.set(self.Acceleration_PhidgetsUnits_TO_BE_SET)
        self.Acceleration_PhidgetsUnits_Scale.grid(row=2, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #Color gets controlled by engaged flag within the main GUI loop
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.CurrentLimit_Amps_Max_ScaleLabel = Label(self.AllScalesFrame, text="CurrentLimit", width=20)
        self.CurrentLimit_Amps_Max_ScaleLabel.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        self.CurrentLimit_Amps_Max_ScaleValue = DoubleVar()
        self.CurrentLimit_Amps_Max_Scale = Scale(self.AllScalesFrame, \
                                            from_=self.CurrentLimit_Amps_Min_UserSet,\
                                            to=self.CurrentLimit_Amps_Max_UserSet, \
                                            #tickinterval=(self.CurrentLimit_Amps_Max_max - self.CurrentLimit_Amps_Max_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.001,\
                                            variable=self.CurrentLimit_Amps_Max_ScaleValue)
        self.CurrentLimit_Amps_Max_Scale.bind('<Button-1>', lambda event, name="Acceleration": self.CurrentLimit_Amps_Max_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.CurrentLimit_Amps_Max_Scale.bind('<B1-Motion>', lambda event, name="Acceleration": self.CurrentLimit_Amps_Max_ScaleResponse(event, name))
        self.CurrentLimit_Amps_Max_Scale.bind('<ButtonRelease-1>', lambda event, name="Acceleration": self.CurrentLimit_Amps_Max_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.CurrentLimit_Amps_Max_Scale.set(self.CurrentLimit_Amps_Max_TO_BE_SET)
        self.CurrentLimit_Amps_Max_Scale.grid(row=3, column=1, padx=1, pady=1, columnspan=2, rowspan=1)
        #Color gets controlled by engaged flag within the main GUI loop
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.DeadBand_PosControl_PhidgetsUnits_ScaleLabel = Label(self.AllScalesFrame, text="DeadBand", width=20)
        self.DeadBand_PosControl_PhidgetsUnits_ScaleLabel.grid(row=4, column=0, padx=1, pady=1, columnspan=1, rowspan=1)

        # self.DeadBandMinLimit_PhidgetsUnits_UserSet,\  #self.DeadBandMaxLimit_PhidgetsUnits_UserSet, \
        self.DeadBand_PosControl_PhidgetsUnits_ScaleValue = DoubleVar()
        self.DeadBand_PosControl_PhidgetsUnits_Scale = Scale(self.AllScalesFrame, \
                                            from_=0,\
                                            to= self.PositionMaxLimit_PhidgetsUnits_UserSet,\
                                            #tickinterval=(self.DeadBand_PosControl_PhidgetsUnits_max - self.DeadBand_PosControl_PhidgetsUnits_min) / 2.0,\
                                            orient=HORIZONTAL,\
                                            borderwidth=2,\
                                            showvalue=1,\
                                            width=self.TkinterScaleWidth,\
                                            length=self.TkinterScaleLength,\
                                            resolution=0.1,\
                                            variable=self.DeadBand_PosControl_PhidgetsUnits_ScaleValue)
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<Button-1>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<B1-Motion>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name))
        self.DeadBand_PosControl_PhidgetsUnits_Scale.bind('<ButtonRelease-1>', lambda event, name="DeadBand": self.DeadBand_PosControl_PhidgetsUnits_ScaleResponse(event, name)) #Use both '<Button-1>' or '<ButtonRelease-1>'
        self.DeadBand_PosControl_PhidgetsUnits_Scale.set(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET)
        self.DeadBand_PosControl_PhidgetsUnits_Scale.grid(row=4, column=1, padx=1, pady=1, columnspan=2, rowspan=1)

        if self.ControlMode == "velocity":
            self.DeadBand_PosControl_PhidgetsUnits_Scale["state"] = "disabled"
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.CurrentInputFrame = Frame(self.myFrame)
        self.CurrentInputFrame["borderwidth"] = 2
        #self.CurrentInputFrame["relief"] = "ridge"
        self.CurrentInputFrame.grid(row=3, column=0, padx=1, pady=1, columnspan=1, rowspan=1, sticky="W")
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        if self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG == 1:
            self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object.CreateGUIobjects(TkinterParent=self.CurrentInputFrame)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.PrintToGui_Label = Label(self.myFrame, text="PrintToGui_Label", width=75)
        if self.EnableInternal_MyPrint_Flag == 1:
            self.PrintToGui_Label.grid(row=4, column=0, padx=1, pady=1, columnspan=1, rowspan=10)
        ###########################################################
        ###########################################################

        ###########################################################
        ###########################################################
        self.GUI_ready_to_be_updated_flag = 1
        ###########################################################
        ###########################################################

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Position_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Position_PhidgetsUnits_TO_BE_SET = self.Position_PhidgetsUnits_ScaleValue.get()
        self.Position_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Position_PhidgetsUnits_ScaleResponse: Position set to: " + str(self.Position_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Velocity_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Velocity_PhidgetsUnits_TO_BE_SET = self.Velocity_PhidgetsUnits_ScaleValue.get()
        self.Velocity_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Velocity_PhidgetsUnits_ScaleResponse: Velocity set to: " + str(self.Velocity_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def Acceleration_PhidgetsUnits_ScaleResponse(self, event, name):

        self.Acceleration_PhidgetsUnits_TO_BE_SET = self.Acceleration_PhidgetsUnits_ScaleValue.get()
        self.Acceleration_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("Acceleration_PhidgetsUnits_ScaleResponse: Acceleration set to: " + str(self.Acceleration_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def CurrentLimit_Amps_Max_ScaleResponse(self, event, name):

        self.CurrentLimit_Amps_Max_TO_BE_SET = self.CurrentLimit_Amps_Max_ScaleValue.get()
        self.CurrentLimit_Amps_Max_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("CurrentLimit_Amps_Max_ScaleResponse: Acceleration set to: " + str(self.CurrentLimit_Amps_Max_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def DeadBand_PosControl_PhidgetsUnits_ScaleResponse(self, event, name):

        self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET = self.DeadBand_PosControl_PhidgetsUnits_ScaleValue.get()
        self.DeadBand_PosControl_PhidgetsUnits_NeedsToBeChangedFlag = 1

        #self.MyPrint_WithoutLogFile("DeadBand_PosControl_PhidgetsUnits_ScaleResponse: DeadBand set to: " + str(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET))
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def SetEngagedState(self, StateToBeSet):

        if StateToBeSet not in [0, 1]:
            self.MyPrint_WithoutLogFile("SetEngagedState ERROR: StateToBeSet must be 0 or 1.")
            return 0
        else:
            self.EngagedState_TO_BE_SET = StateToBeSet
            self.EngagedState_NeedsToBeChangedFlag = 1
            return 1

    ##########################################################################################################
    ##########################################################################################################

    '''
    ##########################################################################################################
    ##########################################################################################################
    def EngagedStateButtonResponse(self):

        if self.EngagedState_PhidgetsUnits_FromDevice == 1:
            self.SetEngagedState(0)
        else:
            self.SetEngagedState(1)

    ##########################################################################################################
    ##########################################################################################################
    '''

    ##########################################################################################################
    ##########################################################################################################
    def StopMotorButtonResponse(self):

        self.StopMotor_NeedsToBeChangedFlag = 1
    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def HomeMotorInPlaceButtonResponse(self):

        self.HomeMotorInPlace_NeedsToBeHomedFlag = 1

    ##########################################################################################################
    ##########################################################################################################

    ##########################################################################################################
    ##########################################################################################################
    def GUI_update_clock(self):

        #######################################################
        #######################################################
        #######################################################
        #######################################################
        if self.USE_GUI_FLAG == 1 and self.EXIT_PROGRAM_FLAG == 0:

            #######################################################
            #######################################################
            #######################################################
            if self.GUI_ready_to_be_updated_flag == 1:

                #######################################################
                #######################################################
                try:
                    #########################################################
                    self.StopMotorButton["text"] = "Stop Motor\nEngaged State: " + str(self.EngagedState_PhidgetsUnits_FromDevice)

                    if self.ControlMode == "velocity":
                        self.StopMotorButton["text"] = self.StopMotorButton["text"]  + "\n(cannot disengaged in VelMode)"

                    if self.EngagedState_PhidgetsUnits_FromDevice == 0:
                        self.StopMotorButton["bg"] = self.TKinter_LightRedColor

                    elif self.EngagedState_PhidgetsUnits_FromDevice == 1:
                        self.StopMotorButton["bg"] = self.TKinter_LightGreenColor

                    else:
                        self.StopMotorButton["bg"] = self.TKinter_DefaultGrayColor
                    #########################################################

                    #########################################################

                    if self.EngagedState_PhidgetsUnits_FromDevice == 1:

                        if self.ControlMode == "position":
                            self.Position_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.Velocity_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.CurrentLimit_Amps_Max_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.DeadBand_PosControl_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor

                        else:
                            self.Position_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                            self.Velocity_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.CurrentLimit_Amps_Max_Scale["troughcolor"] = self.TKinter_LightGreenColor
                            self.DeadBand_PosControl_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor

                    else:
                        self.Position_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                        self.Velocity_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                        self.Acceleration_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                        self.CurrentLimit_Amps_Max_Scale["troughcolor"] = self.TKinter_LightRedColor
                        self.DeadBand_PosControl_PhidgetsUnits_Scale["troughcolor"] = self.TKinter_LightRedColor
                    #########################################################

                    #########################################################
                    if self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Position_PhidgetsUnits_Scale.set(self.Position_PhidgetsUnits_TO_BE_SET)
                        self.Position_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #########################################################
                    if self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Velocity_PhidgetsUnits_Scale.set(self.Velocity_PhidgetsUnits_TO_BE_SET)
                        self.Velocity_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################
                    
                    #########################################################
                    if self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.Acceleration_PhidgetsUnits_Scale.set(self.Acceleration_PhidgetsUnits_TO_BE_SET)
                        self.Acceleration_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #########################################################
                    if self.CurrentLimit_Amps_Max_GUI_NeedsToBeChangedFlag == 1:
                        self.CurrentLimit_Amps_Max_Scale.set(self.CurrentLimit_Amps_Max_TO_BE_SET)
                        self.CurrentLimit_Amps_Max_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #########################################################
                    if self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag == 1:
                        self.DeadBand_PosControl_PhidgetsUnits_Scale.set(self.DeadBand_PosControl_PhidgetsUnits_TO_BE_SET)
                        self.DeadBand_PosControl_PhidgetsUnits_GUI_NeedsToBeChangedFlag = 0
                    #########################################################

                    #######################################################
                    self.Data_Label["text"] =  "*** ControlMode: " + self.ControlMode + " ***" +\
                                                "\nTime: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.CurrentTime_CalculatedFromMainThread, 0, 3) + \
                                               "\nFrequency MainThread(Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_CalculatedFromMainThread, 0, 3) + \
                                                "\nFrequency Phidgets ON CHANGE Position Rx, can slow to 0 (Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_OnPositionChangeCallbackFunction, 0, 3) + \
                                                "\nFrequency Phidgets ON CHANGE Velocity Rx, can slow to 0 (Hz): " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DataStreamingFrequency_OnVelocityUpdateCallbackFunction, 0, 3) + \
                                                "\nTemperature_DegC_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Temperature_DegC_FromDevice, 0, 3) + \
                                                "\nPosition_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Position_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nVelocity_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Velocity_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\n\tVelocity_PhidgetsUnits_DifferentiatedRaw: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Velocity_PhidgetsUnits_DifferentiatedRaw, 0, 3) + \
                                                "\n\tVelocity_PhidgetsUnits_DifferentiatedSmoothed: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Velocity_PhidgetsUnits_DifferentiatedSmoothed, 0, 3) + \
                                                "\nDutyCycle_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DutyCycle_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nAcceleration_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.Acceleration_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nDeadBand_PosControl_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.DeadBand_PosControl_PhidgetsUnits_FromDevice, 0, 3) + \
                                                "\nEngagedState_PhidgetsUnits_FromDevice: " + self.ConvertFloatToStringWithNumberOfLeadingNumbersAndDecimalPlaces_NumberOrListInput(self.EngagedState_PhidgetsUnits_FromDevice, 0, 3)
                                                #"\n***Position_PhidgetsUnits_TO_BE_SET: " + str(self.Position_PhidgetsUnits_TO_BE_SET)
                    #######################################################

                    #######################################################
                    self.PrintToGui_Label.config(text=self.PrintToGui_Label_TextInput_Str)
                    #######################################################

                    #########################################################
                    if self.PhidgetsCurrentSensor30ampDConlyVCP1100_OPEN_FLAG == 1:
                        self.PhidgetsCurrentSensor30ampDConlyVCP1100_Object.GUI_update_clock()
                    #########################################################

                except:
                    exceptions = sys.exc_info()[0]
                    print("PhidgetDCmotorDCC1000controller_ReubenPython2and3Class GUI_update_clock ERROR: Exceptions: %s" % exceptions)
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


