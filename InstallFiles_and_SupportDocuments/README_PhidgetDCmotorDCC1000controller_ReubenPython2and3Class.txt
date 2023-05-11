########################  

PhidgetDCmotorDCC1000controller_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to control 1 DC (NOT brushless/BLDC) motor
with optional encoder feedback via VINT (also has analog voltage and digital inputs).
Supports both velocity and position control modes.
STILL NEED TO ADD CALLBACK FUNCTIONS FOR READING ENCODER, ANALOG VOLTAGE, AND DIGITAL INPUT.

From Phidgets' website:
"Control one high-current brushed DC motor with this powerful Phidget.
The encoder input and analog input can enable precise control motor velocity and position."

DC Motor Phidget
ID: DCC1000_0
https://www.phidgets.com/?tier=3&catid=18&pcid=15&prodid=965

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision F, 05/10/2023

Verified working on: 
Python 2.7, 3.8
Windows 8.1, 10 64-bit
Raspberry Pi Buster 
(no Mac testing yet, but might work while not in GUI-mode)

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

########################  

########################### Python module installation instructions, all OS's

PhidgetDCmotorDCC1000controller_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'Phidget22', 'PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class']
PhidgetDCmotorDCC1000controller_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']
PhidgetDCmotorDCC1000controller_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'numpy', 'Phidget22']
PhidgetDCmotorDCC1000controller_ReubenPython2and3Class, ListOfModuleDependencies_All:['future.builtins', 'LowPassFilter_ReubenPython2and3Class', 'LowPassFilterForDictsOfLists_ReubenPython2and3Class', 'MyPrint_ReubenPython2and3Class', 'numpy', 'Phidget22', 'PhidgetsCurrentSensor30ampDConlyVCP1100_ReubenPython2and3Class']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:
pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -
sudo apt-get install -y libphidget22
 
###########################