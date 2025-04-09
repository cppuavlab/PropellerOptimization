## PropellerOptimization Script
Scripts to use OpenMDAO Simple Genetic Algorithm to optimize blade geometry in CHARM.
Can be modified for further analysis and applications in CHARM.

Version 2.1

--- Required Dependencies ---
Python Version: 3.13.0
CHARM Version: 8.0
Windows Subsystem for Linux Instance Information: Ubuntu 22.04.3 LTS
WSL Version: WSL2
Linux Kernel Information: 5.15.167.4

--- Required Files for Use ---
  AlgoRun.py
  GeneticAI.py
  SingleFileMakerCHARM.py
  GABasebd.inp
  GABaserw.inp
  GACHARMrun.sh (linux shell script)
!! ALL Files listed above are REQUIRED for use of this script !!

--- Required Python Modules ---
  openmdao
  pandas
  pyDOE3
  subprocess (built-in)
  datetime (built-in)

You can install the required packages using the pip commands:
  pip install [insert package name]
Note: Installation command may vary depending on install location of your pip
Note: if pip is 'not recognized as internal or external command', try running your local pip, using the command below
  python -m pip install [insert package name]

--- Usage ---
Note: All associated files must be in the NOISE directory of CHARM
Note: To navigate to the NOISE directory, you might do the following in a Windows Command Prompt Terminal:
  wsl.exe
  export PATH=\$PATH:.
  cd CHARM/CHARM_PREMIUM_v7.3gamma/NOISE
Note: If you are using the UAV Lab PC, the following windows shortcut could be used instead:
  runCHARM.bat

Note: Once in the NOISE directory, running the Algorithm is simple
  python3 AlgoRun.py
Note: When copying the files into the Linux Environment, the python file may be written with no permissions
Note: Run the following on all python files used in this run
  chmod +x [insert file name]

--- File Specific: AlgoRun.py ---
How to Edit:
Determine desired input and outputs
Initialize all inputs and outputs in the setup method
Reflect all new inputs and outputs throughout the code
Configure the Algorithm by modifying optimization features
Refer to OpenMDAO Simple Genetic Algorithm Website for detailed description of each feature
Change desired name of your output file in Line 25

--- File Specific: GeneticAl.py ---
How to Edit:
Reflect your desired inputs and outputs in the class intialization and append_iterations method
Failure to do so will result in errors

--- File Specific: SingleFileMakerCHARM.py ---
How to use
Determine how many inputs you want
Place f replace where necessary
Add inputs as arguments into relevant file creation methods
Note: If you decide to change the naming convetion of the created files, reflect the relevant changes to the GACHARMrun.sh shell script and AlgoRun.py
Note: Errors will arise if you give CHARM files in an unexpected file format, resulting in script termination

--- File Specific: GACHARMrun.sh ---
This file is a Linux Shell Script. 
It must have the LF end of line sequence, which Linux expects. 
Check end of line sequence in bottom right of Visual Studio Code or check in terminal

--- Revision History ---
** Verison 2.1 ** (March 30, 2025): Added comments and docstrings, SQLite recorder, and modified driver options for increased accuracy

Created by: Nathan Rong
Contact: nrong@cpp.edu
Last Modified: 03/30/2025
