# Created by: Nathan Rong (nrong@cpp.edu)
# Date: 03/01/2025
# Version: 1.0
# Python Version 3.13.0
# For use of OpenMDAO Simple Genetic Algorithm
# with CHARM software for optimization

# This script houses important methods for file parsing, storage, and deletion
# Read comments in and above each method before using/editing
# Direct any questions to Nathan Rong (nrong@cpp.edu)


import pandas as pd
import os

# Class for dynamically writing values into CSV file
class staging():
    def __init__(self, filename):
        self.file = filename + '.csv'
        try:
            # if file is found, open it and edit it
            self.df = pd.read_csv(self.file)

        # if file is not found, make a new one
        except FileNotFoundError:
            self.df = pd.DataFrame(columns = ['Iteration', 
            'Time', 'Twist', 'Anhedral', 'ZDistance', 'Twist1', 'Twist2', 
            'Twist3', 'Twist4', 'Twist5', 'Twist6', 'Twist7', 'Twist8', 
            'Twist9', 'Twist10','Observer2', 'Observer21', 'Observer22', 
            'Observer23', 'Observer24', 'Observer25'])


    def save_to_csv(self):
        self.df.to_csv(self.file, index=False)

    # Appends current iteration of Genetic Algorithm
    # All other columns must be filled with filler values
    # Filler values must correspond to the data type expected in that column
    # Failure to keep consistent data types will result in an error
    # Failure to have the correct dataframe size will result in an error
    def append_iterations(self, iteration):
        # maybe make some way so that this is automated
        self.df.loc[len(self.df)] = [iteration, '', float(0), float(0), float(0), 
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0)] 
        self.save_to_csv()

    # Should append all inputs before appending any outputs
    def append_vals(self, iteration, input_data, header_name):
        # input_data is a single value
        if type(input_data) is str:
            self.df.loc[self.df['Iteration'] == iteration, header_name] = input_data
        else:
            self.df.loc[self.df['Iteration'] == iteration, header_name] = round(input_data[0], 3)
        self.save_to_csv()



# Batch file maker for injecting python commands through windows envrionment
# Automatically uses scripts to access the Linux WSL environment
# Edit your file name
# class batch_file_maker_and_run():
#     def __init__(self):
#         self.content = [r'@echo off', 
#                      f'wsl.exe bash -c "export PATH=\$PATH:. && cd ~/CHARM/CHARM_PREMIUM_v7.3gamma/NOISE && clear && runv7 . GAlgoRunsname"']
#         self.content.append(r'echo %date% %time% & tzutil /g')
#         # to print current time
#         self.directory = os.getcwd()
#         # edit your file name below
#         self.file_path = f"{self.directory}/GAlgoRuns.bat"

#         with open(self.file_path, 'w') as f:
#             f.write("\n".join(self.content))

#         # Execute batch file in DOS terminal
#         os.system(self.file_path)


# Filters data only to structured files, use only for .dat CHARM outputs
# or select applications in .csv or other structured file types
class data_filter():
    def __init__(self, file_name, observer, header_name):
        self.temp = pd.read_csv(file_name, sep=r'\s+').at[observer-1, header_name]

# Specificy list of files to delete in current working directory
# !!WARNING!! this is a permanent deletion
# !!WARNING!! BE CAREFUL not to delete important files
# !!WARNING!! Files deleted through this method will not easily be restorable
# !!WARNING!! Files deleted through this method will not be found in Recycle Bin
class delete_files():
    def __init__(self):
        # make sure to be in the right directory, os.chdir?
        list_of_files = ['GAlgoRunsrw.inp', 'GAlgoRunsbg.inp', 'GAlgoRunsname.inp']
        for item in list_of_files:
            os.remove(item)
