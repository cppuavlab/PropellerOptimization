# Created by: Nathan Rong (nrong@cpp.edu)
# Date: 03/01/2025
# Version: 1.0
# Python Version 3.13.0
# For use of OpenMDAO Simple Genetic Algorithm
# with CHARM software for optimization

# Note: Associated Files:
# GeneticAI.py
# SingleFileMakerCHARM.py
# GABasebd.inp
# GABaserw.inp
# GACHARMrun.sh (linux shell script)
# ALL Files listed above are REQUIRED for use of this script
# Failure to have all of thes files will result in a FileNotFound error


import openmdao.api as om
from datetime import datetime
import subprocess
from GeneticAl import staging, data_filter
from SingleFileMakerCHARM import FileMaker

# Define filename
db = staging('GA_FileName')

# Houses main functions of Genetic Algorithm Driver
class Optimizer(om.ExplicitComponent):

    def setup(self):
        # Intialize inputs
        for variable in ['Twist', 'Anhedral', 'Twist1', 'Twist2', 'Twist3', 'Twist4',
                         'Twist5', 'Twist6', 'Twist7', 'Twist8', 'Twist9', 'Twist10', 'ZDistance']:
            self.add_input(variable, val=1)
        
        # Initalize outputs
        for i in [21, 22, 23, 24, 25, 2]:
            self.add_output(f'Observer{i}', val=1.0)
        self.prev_val, self.threshhold_hit = None, 0
        self.change_Twist, self.change_Anhedral, self.change_ZDistance = None, None, None

    def compute(self, inputs, outputs):
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

        # Early stop feature
        # Detects repetition in the algorithm
        # Replicate structure and apply to ALL relevant inputs/outputs
        if self.prev_val is not None:
            # Calculate change in design variables
            self.change_Twist = abs(Twist[0] - self.prev_val['Twist'])
            self.change_Anhedral = abs(Anhedral[0] - self.prev_val['Anhedral'])
            self.change_ZDistance = abs(ZDistance[0] - self.prev_val['ZDistance'])
            
            # Define a threshold for change (adjust as needed)
            threshold = 0.1
            if self.change_Twist < threshold and self.change_Anhedral < threshold and self.change_ZDistance < threshold:
                self.threshhold_hit += 1
            else:
                self.threshhold_hit = 0
            # if threshhold is hit more than 50 times, end the loop
            if self.threshhold_hit > 50:
                print('Requesting Early Stop for early convergence...')
                raise UserWarning
        
        # Log previous values and get iteration count
        self.prev_val = {'Twist': Twist[0], 'Anhedral': Anhedral[0], 'ZDistance': ZDistance[0]}
        
        gen = prob.iter_count_iter(True, True, True)
        if type(next(gen, 0)) is int:
            integer = next(gen, 0)
        else:
            integer = next(gen, 0)[2]

        FileMaker(Twist[0], Anhedral[0], ZDistance[0], Twist1[0], Twist2[0], Twist3[0], Twist4[0],
                  Twist5[0], Twist6[0], Twist7[0], Twist8[0], Twist9[0], Twist10[0])
        
        # time.sleep(5)

        # Calcualte outputs
        subprocess.run(["./GACHARMrun.sh"])
        outputs['Observer2'] = data_filter('GAlgoRunsname_oaspldBA.dat', 2, 'Total').temp
        outputs['Observer21'] = data_filter('GAlgoRunsname_oaspldBA.dat', 21, 'Total').temp
        outputs['Observer22'] = data_filter('GAlgoRunsname_oaspldBA.dat', 22, 'Total').temp
        outputs['Observer23'] = data_filter('GAlgoRunsname_oaspldBA.dat', 23, 'Total').temp
        outputs['Observer24'] = data_filter('GAlgoRunsname_oaspldBA.dat', 24, 'Total').temp
        outputs['Observer25'] = data_filter('GAlgoRunsname_oaspldBA.dat', 25, 'Total').temp
        
        # Output equations for TESTING PURPOSES ONLY
        # Uncomment to test outputs, comment out when in operation
        # outputs['Observer2'] = Twist * Anhedral
        # outputs['Observer21'] = Twist * ZDistance
        # outputs['Observer22'] = 2*Twist*ZDistance + 2*Twist*Anhedral + 2*ZDistance*Anhedral
        # outputs['Observer23'] = Twist*ZDistance*Anhedral
        # outputs['Observer24'] = Twist * Anhedral + 1
        # outputs['Observer25'] = Twist * ZDistance

        # Append all inputs and integer
        staging.append_iterations(db, integer)
        for input in ['Twist', 'Anhedral', 'Twist1', 'Twist2', 'Twist3', 'Twist4',
                         'Twist5', 'Twist6', 'Twist7', 'Twist8', 'Twist9', 'Twist10', 'ZDistance']:
            staging.append_vals(db, integer, locals()[input], input)

        # Append all outputs
        for i in [21, 22, 23, 24, 25, 2]:
            staging.append_vals(db, integer, outputs[f'Observer{i}'], f'Observer{i}')
        # Append time
        staging.append_vals(db, integer, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'Time')
        
# Problem initialization
prob = om.Problem()
prob.model.add_subsystem('GeneticAlgorithm', Optimizer(), promotes=['*'])

# Configure the optimization features
prob.driver = om.SimpleGADriver()
prob.driver.options['max_gen'] = 200
prob.driver.options['pop_size'] = 50
prob.driver.options['bits'] = {'Twist': 3, 'Anhedral': 3, 'Twist1': 3, 'Twist2': 3, 
                               'Twist3': 3, 'Twist4': 3, 'Twist5': 3, 'Twist6': 3,
                                'Twist7': 3, 'Twist8': 3, 'Twist9': 3, 'Twist10': 3, 
                                'ZDistance': 3}
prob.driver.options['penalty_parameter'] = 10
prob.driver.options['compute_pareto'] = True

# Add design variable constraints
prob.model.add_design_var('Twist', lower=-10, upper=40)
prob.model.add_design_var('Anhedral', lower=-15, upper=15)
prob.model.add_design_var('ZDistance', lower=-0.75, upper=0.75)
for i in range(1, 11):
    prob.model.add_design_var(f'Twist{i}', lower=0, upper=8)

# Add algorithm objectives
# -1 is maximize, 1 is minimize 
for i in [21, 22, 23, 24, 25, 2]:
    prob.model.add_objective(f'Observer{i}', scaler=1)

# Add output constraints (if any)
# prob.model.add_constraint('Observer2', upper=85)

prob.setup()

# Assign start values to all variables
prob.set_val('Twist', 0)
prob.set_val('Anhedral', -10)
prob.set_val('ZDistance', 0)
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
    desvar_nd = prob.driver.desvar_nd
    nd_obj = prob.driver.obj_nd

    print('Algorithm has completed successfully!')

except (KeyboardInterrupt, ValueError, FileNotFoundError) as e:
    print(f"Program interrupted. Error {e}. Saving data...")
    # save any data in progress before exiting
    staging.save_to_csv(db)

except UserWarning:
    print(f"Program interrupted. Error {UserWarning}. Saving data...")
    print('Error Cause: Early Stop has been requested!')
