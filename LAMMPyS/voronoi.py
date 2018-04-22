import LAMMPyS as lp


def sv(refdump, lammpssvdump, svdump):
    refatoms = lp.read_dump(refdump)[0].atoms
    steps = lp.read_dump(lammpssvdump)
    for step in steps:
        atoms = step.atoms
        for atom in atoms:
            atom.x = refatoms.id(atom.id).x
            atom.y = refatoms.id(atom.id).y
            atom.z = refatoms.id(atom.id).z
    lp.write_dump(steps, svdump)


if __name__ == '__main__':
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
