import LAMMPyS as lp


def sv(refdump, lammpssvdump, svdump):
    refsteps = lp.Steps(refdump)
    refstep = refsteps[-1]
    steps = lp.Steps(lammpssvdump)
    with open(svdump, 'w') as file:
        pass
    for step in steps:
        for x in ['x', 'y', 'z']:
            step.pi(x)  # property initialization
        for atom in step.atoms:
            id = atom[step.pi('id')]
            refatom = refstep.get_atom('id', id)
            for x in ['x', 'y', 'z']:
                atom[step.pi(x)] = refatom[refstep.pi(x)]
        step.write(svdump)


if __name__ == '__main__':
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
