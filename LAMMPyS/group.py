import LAMMPyS as lp


def _distance(atom0, atom1):
    _distance = 0
    for x in ['x', 'y', 'z']:
        _distance += (atom0.p(x) - atom1.p(x))**2
    return _distance**0.5


class Group:

    def __init__(self, atom):
        self.members = [atom]
        self.freshes = [atom]
        self.candidates = []

    def include(self, atoms, cut):
        while True:
            for fresh in self.freshes:
                for atom in atoms:
                	for mem in self.members:
                		if (atom == mem).all():
                			break
                	else:
	                    if _distance(fresh, atom) < cut:
	                        self.candidates.append(atom)
	                        self.members.append(atom)
            self.freshes = self.candidates
            self.candidates = []
            if len(self.freshes) == 0:
                break
        for member in self.members:
            member.set_p('grouped', 1)
        return self.members


def divide(atoms, cut):
    atoms = atoms.add_p('grouped')
    groups = []
    for atom in atoms:
        if atom.p('grouped') == 1:
            continue
        group = Group(atom)
        groups.append(group.include(atoms, cut))
    return groups


if __name__ == '__main__':
    steps = lp.Steps('sv.dump')
    atoms = steps[0].atoms
    atoms = atoms[atoms.p('Occupancy') == 2,:]
    groups = divide(atoms, 5)
    print(len(groups))
