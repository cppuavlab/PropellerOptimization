# Created by: Nathan Rong (nrong@cpp.edu)
# Date: 03/30/2025
# Version: 2.1
# Python Version 3.13.0 or greater recommended
# For use of OpenMDAO Simple Genetic Algorithm
# with CHARM software for optimizationn

# This script houses important methods for file parsing, storage, and deletion
# Read comments in and above each method before using/editing
# Direct any questions to Nathan Rong (nrong@cpp.edu)


import pandas as pd
import numpy as np


class staging():
    """
    This class supports data logging from individual inputs to a structured CSV dataframe

    Attributes:
    -----------
    file : string
        File path
    df : dataframe
        Dataframe to log data into
    """
    def __init__(self, filename):
        """
        Initialize dataframe

        Parameters:
        ----------
        filename : string
            File name for output CSV file
        """
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
            'Observer23', 'Observer24', 'Observer25', 'Thrust1', 'Thrust2', 
            'TotalThrust', 'YawMoment1', 'YawMoment2', 'TotalYaw', 'PowerCoef', 'RotorEff'])


    def save_to_csv(self):
        # save Dataframe as CSV file
        self.df.to_csv(self.file, index=False)

 
    def append_iterations(self, iteration):
        """
        Append rows to structured Dataframe

        Parameters:
        ----------
        iteration : int
            Row number to create row
        """
        # maybe make some way so that this is automated
        self.df.loc[len(self.df)] = [iteration, '', float(0), float(0), float(0), 
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0),
                                     float(0), float(0), float(0), float(0)] 
        self.save_to_csv()

    
    def append_vals(self, iteration, input_data, header_name = None):
        """
        Append values into rows in structured Dataframe

        Parameters:
        ----------
        iteration : int
            Row to append value to
        input_data : float
            Value to append
        header_name : str
            Column name to append value into
        """
        # Check if input is a single value
        if type(input_data) is str:
            if header_name is None:
                raise ValueError('header_name must be provided when input_data is a string')
            self.df.loc[self.df['Iteration'] == iteration, header_name] = input_data
            
        # Check if input is a dictionary
        elif type(input_data) is dict:
            for key, val in input_data.items():
                self.df.loc[self.df['Iteration'] == iteration, key] = val
        
        # Check if input is a list
        elif isinstance(input_data, np.ndarray):
            if header_name is None:
                raise ValueError('header_name must be provided when input_data is a np.ndarray')
            self.df.loc[self.df['Iteration'] == iteration, header_name] = round(input_data[0], 3)
       
        else:
            raise ValueError('Recieved unexpected input data type while logging to CSV...')
        self.save_to_csv()


class data_filter():
    """
    This class transforms information from tabulated .DAT file format
    Specifically for OASPL CHARM Simulation predictions

    Parameters:
    ----------
    file_name : str
        File name for .DAT file
    observer : int
        Observer number
    header_name : str
        Column header for data in original table
    """
    def __init__(self, file_name, observer, header_name):
        self.temp = pd.read_csv(file_name, sep=r'\s+').at[observer-1, header_name]


class log_file_parse():
    """
    This class is specifically for parsing CHARM run log files for aerodynamic data

    Attributes:
    -----------
    dict : dict
        Dictionary of parsed data

    Parameters:
    -----------
    log_file_name : str
        File name of CHARM run log
    rotor_num : int
        Number of rotors being simulated
    """
    def __init__(self, log_file_name, rotor_num=1):
        # Check for correct inputs
        if rotor_num not in (1,2):
            raise TypeError('log_file_parse recieved incorrect argument... \n rotor_num must be a 1 or 2')
        with open(log_file_name, 'r') as f:
            # Initial file read
            content = f.read()
        # Create dictionary to store data
        self.dict = {}
        # Aircraft Aerodynamics data parse
        rotor1 = content.split('Aircraft 1 loads (inertial frame): ')[1].split('Rotor  1 loads:')[1].split('Rotor  2 loads:')[0]
        totals = content.split('Aircraft 1 loads (inertial frame): ')[1].split('Total aircraft loads:')[1].split('!!!!')[0]
        self.dict['Thrust1'] = -1*float(rotor1.split('+z-dir)')[1].split('Roll')[0].split('lb')[0].strip())
        self.dict['TotalThrust'] = -1*float(totals.split('z-dir)')[1].split('lb')[0].strip())
        self.dict['YawMoment1'] = float(rotor1.split('about +z)')[1].split('ft')[0].strip())
        
        self.dict['TotalYaw'] = float(totals.split('about +z)')[1].split('ft')[0].strip())

        # Wind Axis data parse
        extra_content = content.split('WIND AXES:')[-1].split('Drag to lift')[0]
        self.dict['PowerCoef'] = float(extra_content.split('balance)')[1].split('Rotor')[0].strip().split(' ')[-1])
        self.dict['RotorEff'] = float(extra_content.split('efficiency')[1].split('Kapp')[0].strip().split(' ')[-1])

        # Rotor 2 parse
        if rotor_num == 2:
            try:
                rotor2 = content.split('Aircraft 1 loads (inertial frame): ')[1].split('Rotor  2 loads:')[1].split('Total aircraft loads:')[0]
                self.dict['Thrust2'] = -1*float(rotor2.split('+z-dir)')[1].split('Roll')[0].split('lb')[0].strip())
                self.dict['YawMoment2'] = float(rotor2.split('about +z)')[1].split('ft')[0].strip())
            except:
                raise TypeError('log_file_parse recieved incorrect argument... \n Rotor 2 not found')



if __name__ == '__main__':
    print(log_file_parse('example_onerotor.log').dict)
