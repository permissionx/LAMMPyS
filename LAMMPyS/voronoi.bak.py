import LAMMPyS as lp


def sv(refdump, lammpssvdump, svdump):
    refatoms = lp.read_dump(refdump)[0].atoms
    steps = lp.read_dump(lammpssvdump)
    properties = ['type', 'x', 'y', 'z', 'c_2[1]']
    new_steps = []
    for step in steps:
        new_atoms = lp.Atoms(properties=properties)
        for atom in step.atoms:
            new_atom = atom.copy()
            new_atom.x = refatoms.id(atom.id).x
            new_atom.y = refatoms.id(atom.id).y
            new_atom.z = refatoms.id(atom.id).z
            new_atoms.append(new_atom)
        new_step = lp.Step(new_atoms, step.timestep, step.box)
        new_steps.append(new_step)
    lp.write_dump(new_steps, svdump)


if __name__ == '__main__':
    sv(refdump='ref.dump', lammpssvdump='lammps_sv.dump',
       svdump='sv.dump')
