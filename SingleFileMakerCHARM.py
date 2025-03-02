# Created by: Nathan Rong (nrong@cpp.edu)
# Date: 03/01/2025
# Version: 1.0
# Python Version 3.13.0
# For use of OpenMDAO Simple Genetic Algorithm
# with CHARM software for optimization

# Designed to work with Genetic Algorithm Files 
# Read comments in and above each method before using/editing
# Direct any questions to Nathan Rong (nrong@cpp.edu)


# Creates dynamic CHARM input files
# Only for creating RW, BG, and Name Input files
# bd file and static (non-changing) rw files are attached and titled
# GABasebd.inp
# GABaserw.inp
class FileMaker():

    def __init__(self, val1, val2, val3, vala, valb, valc, vald, 
                 vale, valf, valg, valh, vali, valj):
        # List of file name parts
        self.fp_list = ['GAlgoRuns', 'bg', 'rw', 'name']
        
        # File names
        bgfilename = f'{self.fp_list[0]}{self.fp_list[1]}.inp'
        rwfilename = f'{self.fp_list[0]}{self.fp_list[2]}.inp'
        rcfilename = f'{self.fp_list[0]}{self.fp_list[3]}.inp'

        # Generate file content
        bg_content = self.generate_bg_content(val1, val2, vala, valb, valc, 
                                              vald, vale, valf, valg, valh, vali, valj)
        rw_content = self.generate_rw_content(val3)
        rc_content = self.generate_name_content(rwfilename, bgfilename)

        # Write content to files
        with open(bgfilename, 'w') as f:
            f.write(bg_content)
            f.flush()
        with open(rwfilename, 'w') as f:
            f.write(rw_content)
            f.flush()
        with open(rcfilename, 'w') as f:
            f.write(rc_content)
            # This can probably be eliminated
        
    def generate_bg_content(self, val1, val2, vala, valb, valc, 
                            vald, vale, valf, valg, valh, vali, valj):
        return f"""# Generated BG File
KBGEOM
    0
NSEG
    10
CUTOUT
    0.0680    
SL(ISEG)
    .0417  .0417  .0417  .0417  .0417   .0417   .0833 .5000  .0313  .0104
CHORD(ISEG)
    .1200  .1172  .1145  .1354  .1458   .1563   .1771  .1667 .0833  .0729   .0213
ELOFSG(ISEG) - (elastic axis offset)
    11*0.0
SWEEPD(ISEG)
    5.0  -10.0  -10.0  -10.0  -20.0  -10.0  -5.0  2.0  0.0  0.0
TWRD (Blade root twist at zero collective in degrees)
    {val1:.2f}
TWSTGD(ISEG)
    {vala:.2f}  {valb:.2f}  {valc:.2f}  {vald:.2f}  {vale:.2f}  {valf:.2f}  {valg:.2f}  {valh:.2f}  {vali:.2f}  {valj:.2f}
ANHD(ISEG)
    11*{val2:.2f}
THIKND(ISEG)
    11*0.1200
KFLAP(ISEG)
    11*0
FLAPND(ISEG)
    11*0.0
FLHNGE(ISEG)
    11*0.0
FLDEFL(ISEG)
    11*0.0
NCAM
    0
NCHORD  NSPAN  ICOS
    1      -72    0
"""

    def generate_rw_content(self, val3):
        return f"""# Generated RW File 
NBLADE  OMEGA
    1      500
IROTAT      XROTOR           X,Y,Z tilt     ITILT
    1     0.0   0.0  {val3:.1f}    0.0  0.0  30.0      1
ICOLL   COLL     CT
    0      0     .004
ITRIM    A1W    B1W    A1S    B1S
    0      0.0    0.0    0.0    0.0
NOWAKE   ICNVCT   NWAKES   NPWAKE   IFAR   MBCVE
    0        2        1       10       0      0
KSCHEME  KPC
    0      0
NCUT   AOVLAP   ISKEW   IUNS
    1       -1       1      1
NZONE   (NVORT(I), I=1,NZONE)
    3       30  30  2 
(NPTFW(I), I=1,NZONE)
    48  48  96
(CORLIM(NV,IZONE,1), NV=1,NVORT(IZONE) IZONE=1 (Min core radii)
    15*0.5  15*0.01
(CORLIM(NV,IZONE,2), NV=1,NVORT(IZONE) IZONE=1 (Max core radii)
    1.0
(CORLIM(NV,IZONE,1), NV=1,NVORT(IZONE) IZONE=2 (Min core radii)
    0.01
(CORLIM(NV,IZONE,2), NV=1,NVORT(IZONE) IZONE=2 (Max core radii)
    1.0
(CORLIM(NV,IZONE,1), NV=1,NVORT(IZONE) IZONE=3 (Min core radii)
    0.5  0.1
(CORLIM(NV,IZONE,2), NV=1,NVORT(IZONE) IZONE=3 (Max core radii)
    0.5  0.1
(CUTLIM(NV,IZONE,1), NV=1,NVORT(IZONE) IZONE=1 (Min cutoff distances)
    15*0.5  15*0.01
(CUTLIM(NV,IZONE,2), NV=1,NVORT(IZONE)  IZONE=1 (Max cutoff distances)
    1.0
(CUTLIM(NV,IZONE,1), NV=1,NVORT (IZONE) IZONE=2 (Min cutoff distances)
    0.01
(CUTLIM(NV,IZONE,2), NV=1,NVORT(IZONE) IZONE=2 (Max cutoff distances)
    1.0
(CUTLIM(NV, IZONE,1), NV=1,NVORT(IZONE) IZONE=3 (Min cutoff distances)
    0.5  0.1
(CUTLIM(NV,IZONE,2), NV=1,NVORT(IZONE) IZONE=3 (Max cutoff distances)
    0.5  0.1
IDYNM
    1
SRAD   SHGHT
    0.0    0.0
NHHI (Higher harmonic cyclic pitch input flag)
    0
"""

    def generate_name_content(self, rwfile, bgfile):
        return f"""# Generated Name File
KSIM
    0
NROTOR
    2
PATHNAME
    ../
INPUT FILENAMESFront right rotor
    GABaserw.inp
    {bgfile}
    GABasebd.inp
    0012air.inp
    None
INPUT FILENAMESFront right rotor
    {rwfile}
    {bgfile}
    GABasebd.inp
    0012air.inp
    None
SSPD     RHO
    1116.    0.002378
SFRAME
    1
U   V   W      P   Q   R
    0.0 0.0 0.0    0.0 0.0 0.0
NPSI    NREV    CONVG1    CONVG2   CONVG3   MREV
    24      3     -1.0     -1.0      -1.0      0
IRST  IFREE  IGPR
    0      0      0
IOUT   NRS   (ROUT(I),I=1,NRS)
    4     10  0.2  0.3  0.4  0.5  0.6  0.7  0.8  0.9  0.95  0.99
NPRINT   IBLPLT   (IFILPLT(I),I=1,4)
    0        0        3  3  3  3
KOPT
    0
ISCAN (Scan plane flag)
    1
ISTRSS (Stress calculation flag)
    0
IFV    IQUIK1
    0       1
ISURF
    0
ISHIP
    0
IRECON   NOISE
    0        4
ACOUSTICS_CODE
    1
NLS
    0
"""