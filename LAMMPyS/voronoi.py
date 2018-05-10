import LAMMPyS as lp


def sv(refdump, lammpssvdump, svdump):
    refsteps = lp.Steps(refdump)
    refstep = refsteps[-1]
    steps = lp.Steps(lammpssvdump)
    with open(svdump,'w') as file:
        pass
    for step in steps:
        for atom in step.atoms:
            id = atom[step.p_index['id']]
            refatom == refstep.get_atom('id', id)
            for x in ['x', 'y', 'z']:
                atom[step.p_index[x]] = refatom[step.p_index[x]]
        step.write(svdump)


if __name__ == '__main__':
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
