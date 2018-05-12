import LAMMPyS as lp
import numpy as np


def sv(refdump, lammpssvdump, svdump):
    refsteps = lp.Steps(refdump)
    refstep = refsteps[0]
    steps = lp.Steps(lammpssvdump)
    # add properties
    lp.init_dump(svdump)
    for step in steps:
        for x in ['x', 'y', 'z']:
            atoms = step.atoms.add_p(x)
        for atom in atoms:
            refatom = refstep.atoms.id(atom.p('id'))
            for x in ['x', 'y', 'z']:
                atom.set_p(x,refatom.p(x))
        step.write(svdump)


if __name__ == '__main__':
    import os
    os.system('date > ini')
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
    os.system('date > end')
