import LAMMPyS as lp
step = lp.read_dump('ref.dump')[0]
atoms = step.atoms
atom = atoms[0]
print(atom)