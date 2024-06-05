#!/usr/bin/env python
# coding: utf-8

# In[10]:


#General ase calculation setup script, use as per requirement
from ase.calculators.vasp import Vasp
import ase.io
import itertools

xtl = ase.io.read('POSCAR')

######### General settings for Vasp ###########
calc = Vasp()

kpar=4
npar=2

encut = 650
kpts=[10,8,8]
scell=[2,4,4] #supercell size in case of phonon calcs

static = False
relax = True
is_dos = False
is_bs_run1 = False
is_bs_run2 = False
is_spin_polarized = True
is_phonon = False

#INCAR tags
calc.set(xc='PBE', setups= 'recommended', prec='Accurate', algo = 'Normal', encut = encut, kpts = kpts, gamma=True,
        kpar = kpar, npar = npar, sigma = 0.05, lmaxmix = 4,lasph = True,lorbit = 11, enaug = 4*encut, ediff = 10**(-6), ediffg = -10**(-4))

if is_spin_polarized:
    calc.set(ispin=2)
    magmom_values = list(itertools.chain(*[[2]*4, [0]*8]))
    xtl.set_initial_magnetic_moments(magmom_values)


if is_dos:
        static = True
        calc.set(ismear = -5, sigma = 0.150, isym = 1, nedos = 4001, emin = -20, emax = 20) #dos calculations are static so remember to set static as true

if is_bs_run1:
        static = True
        calc.set(lreal = False, lwave = True, lcharge = True)

if is_bs_run2:
        static = True
        calc.set(algo ='Normal',lreal = False, icharg = 11,lcharg = False)
        bl=xtl.cell.get_bravais_lattice()
        path= bl.bandpath(npoints = 112)
        calc.set(kpts=path.kpts, reciprocal = True)
        

if is_phonon:
        static = True
        kpts = [i/j for i,j in zip(kpts,scell)]
        calc.set(enaug=1, kpts=kpts, ismear = 1, addgrid = True)

if static:
    calc.set(nsw=0)

if relax:
    calc.set(nsw=100,isif=3, ibrion=2)





xtl.calc=calc #or you could use calc = xtl.calc
xtl.get_potential_energy()



# In[ ]:





# In[ ]:



