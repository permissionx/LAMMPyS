import LAMMPyS as lp
import numpy as np

import os
def sv(refdump, lammpssvdump, svdump):
    refsteps = lp.Steps(refdump)
    refstep = refsteps[0]
    steps = lp.Steps(lammpssvdump)
    with open(svdump, 'w') as file:
        pass
    for step in steps:
        for x in ['x', 'y', 'z']:
            step.pi(x)  # property initialization
        atoms = list(step.atoms)
        for atom in atoms:
            id = atom[step.pi('id')]
            refatom = refstep.get_atom('id', id)
            for x in ['x', 'y', 'z']:
                atom[step.pi(x)] = refatom[refstep.pi(x)]
        step.atoms = atoms
        step.write(svdump)


if __name__ == '__main__':

    os.system('date > ini')
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
    os.system('date > end')
