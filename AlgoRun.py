# Created by: Nathan Rong (nrong@cpp.edu)
# Date: 03/30/2025
# Version: 2.1
# Python Version 3.13.0 or greater recommended
# For use of OpenMDAO Simple Genetic Algorithm
# with CHARM software for optimization

# Note: Associated Files:
# GeneticAI.py
# SingleFileMakerCHARM.py
# GABasebd.inp
# GABaserw.inp
# GACHARMrun.sh (linux shell script)
# ALL Files listed above are REQUIRED for use of this script

import openmdao.api as om
from datetime import datetime
import subprocess
from GeneticAl import staging, data_filter, log_file_parse
from SingleFileMakerCHARM import FileMaker

# Define filename
db = staging('GA_FileName')


class Optimizer(om.ExplicitComponent):
    """
    This class serves as the backbone for the Algorithm
    Connecting CHARM to OpenMDAO's Simple Genetic Algorithm Driver
    Representing an optimization component that inherits from OpenMDAO's ExplicitComponent

    Attributes:
    -----------
    sim_worked : bool
        Check if CHARM Simulation worked as expected
    """
    def setup(self):
        """
        Initialize Algorithm inputs, outputs, and constraints
        """
        self.sim_worked = False
        # Intialize inputs
        for variable in ['Twist', 'Anhedral', 'Twist1', 'Twist2', 'Twist3', 'Twist4',
                         'Twist5', 'Twist6', 'Twist7', 'Twist8', 'Twist9', 'Twist10', 'ZDistance']:
            self.add_input(variable, val=1)
        
        # Initialize outputs
        for observer in [21, 22, 23, 24, 25, 2]:
            self.add_output(f'Observer{observer}', val=1.0)
        for output in ['Thrust_Total', 'Yaw_Total', 'Coef_Power', 'Rotor_Eff']:
            self.add_output(output, val=1.0)
        
        # Initialize Constraints
        for constraint in ['Obs2_Constraint', 'Obs25_Constraint', 'Thrust_Constraint', 'RotorEff_Constraint']:
            self.add_output(constraint, val=1.0)

    def compute(self, inputs, outputs):
        """
        Create CHARM run files, run CHARM, and log data to CSV File
        Compute method is used strictly by Algorithm driver to perform calculations

        Parameters:
        -----------
        inputs : tuple
            list of inputs
        outputs : tuple
            list of outputs
        """
        # Store new inputs to local variables
        Twist = inputs['Twist']
        Anhedral = inputs['Anhedral']
        ZDistance = inputs['ZDistance']
        Twist1 = inputs['Twist1']
        Twist2 = inputs['Twist2']
        Twist3 = inputs['Twist3']
        Twist4 = inputs['Twist4']
        Twist5 = inputs['Twist5']
        Twist6 = inputs['Twist6']
        Twist7 = inputs['Twist7']
        Twist8 = inputs['Twist8']
        Twist9 = inputs['Twist9']
        Twist10 = inputs['Twist10']
        
        # Get iteration count from openMDAO
        integer = next(prob.iter_count_iter(True, True, True), 0)[2]

        # # Create CHARM input files
        FileMaker(1, 2, Twist[0], Anhedral[0], ZDistance[0], Twist1[0], Twist2[0], Twist3[0], Twist4[0],
                  Twist5[0], Twist6[0], Twist7[0], Twist8[0], Twist9[0], Twist10[0])
        
        try:
            # Calcualte outputs
            subprocess.run(["./GACHARMrun.sh"])
            outputs['Observer2'] = data_filter('GAlgoRunsname_oaspldBA.dat', 2, 'Total').temp
            outputs['Observer21'] = data_filter('GAlgoRunsname_oaspldBA.dat', 21, 'Total').temp
            outputs['Observer22'] = data_filter('GAlgoRunsname_oaspldBA.dat', 22, 'Total').temp
            outputs['Observer23'] = data_filter('GAlgoRunsname_oaspldBA.dat', 23, 'Total').temp
            outputs['Observer24'] = data_filter('GAlgoRunsname_oaspldBA.dat', 24, 'Total').temp
            outputs['Observer25'] = data_filter('GAlgoRunsname_oaspldBA.dat', 25, 'Total').temp
            outputs['Thrust_Total'] = log_file_parse('GAlgoRunsname.log').dict.get('TotalThrust')
            outputs['Yaw_Total'] = log_file_parse('GAlgoRunsname.log').dict.get('TotalYaw')
            outputs['Coef_Power'] = log_file_parse('GAlgoRunsname.log').dict.get('PowerCoef')
            outputs['Rotor_Eff'] = log_file_parse('GAlgoRunsname.log').dict.get('RotorEff')
            self.sim_worked = True
        
        except:
            # If CHARM files return error, that iteration does not conform to physics
            # Results in extreme punishment

            # Dictionary with output names and their corresponding values
            output_values = {
                'Observer2': 1000, 'Observer21': 1000, 'Observer22': 1000, 'Observer23': 1000,
                'Observer24': 1000, 'Observer25': 1000, 'Thrust_Total': -1000, 'Yaw_Total': -1000,
                'Coef_Power': -1000, 'Rotor_Eff': -10
            }
            for key, value in output_values.items():
                outputs[key] = value

            self.sim_worked = False
            

        # Assign Constraints
        outputs['Obs2_Constraint'] = outputs['Observer2']
        outputs['Obs25_Constraint'] = outputs['Observer25']
        outputs['Thrust_Constraint'] = outputs['Thrust_Total']
        outputs['RotorEff_Constraint'] = outputs['Rotor_Eff']
        
        # Append all inputs and integer
        staging.append_iterations(db, integer)
        for input in ['Twist', 'Anhedral', 'Twist1', 'Twist2', 'Twist3', 'Twist4',
                        'Twist5', 'Twist6', 'Twist7', 'Twist8', 'Twist9', 'Twist10', 'ZDistance']:
            staging.append_vals(db, integer, locals()[input], input)

        # Append all outputs
        if self.sim_worked == True:
            staging.append_vals(db, integer, log_file_parse('GAlgoRunsname.log').dict)
        for i in [21, 22, 23, 24, 25, 2]:
            staging.append_vals(db, integer, outputs[f'Observer{i}'], f'Observer{i}')
        # Append time
        staging.append_vals(db, integer, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Time')
        

# Problem initialization
# In this script, SGA driver initialization are done outside of the main loop for readability
prob = om.Problem()
prob.model.add_subsystem('GeneticAlgorithm', Optimizer(), promotes=['*'])

# Implement OpenMDAO sqlite Recorder
# Records run data to database filetype (sqlite)
# View database contents using sqlite_reader.py file
# or external SQLite database browser
recordersq = om.SqliteRecorder('optimization_results.db')
prob.driver.add_recorder(recordersq)


# Add design variable constraints
prob.model.add_design_var('Twist', lower=-10, upper=45)
prob.model.add_design_var('Anhedral', lower=-1, upper=15)
# When simulating 1 rotor, set ZDistance to zero at all times
# This will result in non fatal RunTimeWarning error, ignore it
prob.model.add_design_var('ZDistance', lower=0, upper=0)
for i in range(1, 11):
    prob.model.add_design_var(f'Twist{i}', lower=0, upper=8)

# Add algorithm objectives
# -1 is maximize, 1 is minimize 
for i in [21, 22, 23, 24, 25, 2]:
    prob.model.add_objective(f'Observer{i}', scaler=1)
prob.model.add_objective('Thrust_Total', scaler=-1)
prob.model.add_objective('Yaw_Total', scaler=-1)
prob.model.add_objective('Coef_Power', scaler=-1)
prob.model.add_objective('Rotor_Eff', scaler=-1)

# Apply output constraints
# An output cannot be formatted as both constraint and objective
# In the case a value is both, create a separate variable for each
prob.model.add_constraint('Obs2_Constraint', upper=70.0)
prob.model.add_constraint('Obs25_Constraint', upper=45.0)
prob.model.add_constraint('Thrust_Constraint', lower=15.0)
prob.model.add_constraint('RotorEff_Constraint', lower=0.0, upper=1.0)

# Set up problem by adjusting driver (declaring options)
# Configure the optimization features
prob.driver = om.SimpleGADriver()
prob.driver.options['max_gen'] = 2
# Population Heuristic Theory
prob.driver.options['pop_size'] = 10
# Bits of resolution of each variable
# Variables are stored as bits scaled by range of possible values
# When bit resolution not specified, the below equation is used:
# bit_range = log2(upper_bound - lower_bound + 1)
# Possible values can be found using the below equation:
# Value = lower_bound + (R/ 2^n - 1) * upper_bound
# where R = range and n = number of bits
# Higher bit = higher resolution = significantly increased memory usage and computational complexity
# If bit resolution not specified, the value will be encoded as an integer
prob.driver.options['bits'] = {'Anhedral': 5, 'Twist1': 8, 'Twist2': 8, 
                               'Twist3': 8, 'Twist4': 8, 'Twist5': 8, 'Twist6': 8,
                                'Twist7': 8, 'Twist8': 8, 'Twist9': 8, 'Twist10': 8, 
                                'ZDistance': 8}
# Enables Gray Binary encoding, allows for smoother mutations by lowering the gap between numbers in binary
# Done by using bitwise XOR gates, then shifting to the right
prob.driver.options['gray'] = True
# Enables elitism, guarantees best iteration from each generation survives
prob.driver.options['elitism'] = True
# Penalty Function: fp(x) = f(x) + sum(C * d ^ k)
# fp(x) is penalty function, f(x) is objective function, C is penalty parameter, k is penalty exponent
# d is distance from constraint
prob.driver.options['penalty_parameter'] = 10
# Default is 1, more is harsher, less is lenient
prob.driver.options['penalty_exponent'] = 2
# Pc is crossover rate from 0 to 1, 0 being no crossover, 1 being 100% crossover
prob.driver.options['Pc'] = 0.6
# Pm is mutation rate from 0 to 1, 0 being no crossover, 1 being 100% crossover
# Note: this is mutation rate per chromosome, not per bit
prob.driver.options['Pc'] = 0.4
# Weight scaling for Objectives
prob.driver.options['multi_obj_weights'] = {'Observer2': 1, 'Observer21': 1, 'Observer22': 1,
                                            'Observer23': 1, 'Observer24': 1, 'Observer25': 2,
                                            'Thrust_Total': 3, 'Yaw_Total': 2, 'Coef_Power': 1,
                                            'Rotor_Eff': 2}
# Multi-objective weighting exponent, higher rewards higher weighted objectives
prob.driver.options['multi_obj_exponent'] = 2
# Enables pareto front calculation, used for trade-offs in multi-objective optimizations
# Does not consider objective weighting
# Generally use when 1) multiple objectives 2) objectives are conflicting (i.e. thrust and noise)
prob.driver.options['compute_pareto'] = True


prob.setup()

# Assign start values to all variables
prob.set_val('Twist', 0.0)
prob.set_val('Anhedral', 0.0)
prob.set_val('ZDistance', 0.0)
prob.set_val('Twist1', 2.75)
prob.set_val('Twist2', 0.5)
prob.set_val('Twist3', 0.75)
prob.set_val('Twist4', 0.75)
prob.set_val('Twist5', 1.0)
prob.set_val('Twist6', 1.0)
prob.set_val('Twist7', 0.5)
prob.set_val('Twist8', 0.0)
prob.set_val('Twist9', 0.0)
prob.set_val('Twist10', 0.0)

# Main Loop
try:
    prob.run_driver()

    # Print these to view output data
    desvar_nd = prob.driver.get_design_var_values()
    nd_obj = prob.driver.get_objective_values()

    print('Algorithm has completed successfully!')
    print(desvar_nd)
    print(nd_obj)

except (KeyboardInterrupt, GeneratorExit) as e:
    print(f"Program interrupted. Error {e}. Saving data...")
    # save any data in progress before exiting
    staging.save_to_csv(db)

except Exception as e:
    print(f"Caught an unexpected error of type {type(e).__name__}: {e}")
    staging.save_to_csv(db)


# New changes:
# 0) change bit sizes to match what i want
# 1) Mess with sqlite recorder to plot pareto front
# 4) Implement chord optimization and actual twist distribution
# 4b) Define function? or give free reign with constraints
# 5) Compare output (c/R vs r/R and beta vs r/R) to datasheet from UIUC and APC websites
# 6) if have time, make file creation dynamic
