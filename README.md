## PropellerOptimization Script
Scripts to use OpenMDAO Simple Genetic Algorithm to optimize blade geometry in CHARM.
Can be modified for further analysis and applications in CHARM.

Created by: Nathan Rong
Last Modified: 03/02/2025

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
os (built-in)
subprocess (built-in)
datetime (built-in)

You can install the required packages using the pip commands:
ex. pip install [insert package name]
Note: Installation command may vary depending on install location of your pip
Note: if pip is 'not recognized as internal or external command', try running your local pip, using the command below
Note: python -m pip install [insert package name]

--- Usage ---
All ass
