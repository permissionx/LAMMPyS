import LAMMPyS as lp
import numpy as np


def sv(refdump, lammpssvdump, svdump):
    refsteps = lp.Steps(refdump)
    refstep = refsteps[0]
    steps = lp.Steps(lammpssvdump)

    # property index
    x_indexs_ref = []
    for x in ['x', 'y', 'z']:
        x_indexs_ref.append(refstep.pi(x))
    id_index = steps[0].pi('id')

    with open(svdump, 'w') as file:
        pass
    for step in steps:
        x_indexs = []
        for x in ['x', 'y', 'z']:
            x_indexs.append(step.pi(x))
        for atom in step.atoms:
            id = atom[id_index]
            refatom = refstep.id_get(id)
            for x_index, x_index_ref in zip(x_indexs, x_indexs_ref):
                atom[x_index] = refatom[x_index_ref]
        step.write(svdump)


if __name__ == '__main__':
    import os
    os.system('date > ini')
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
    os.system('date > end')
