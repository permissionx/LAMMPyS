import LAMMPyS as lp


def divide(atoms, cut):
	atoms = atoms.add_p('included')
	atoms = atoms.add_p('new_included')

def distance(atom0,atom1):
	distance = 0
	for x in ['x','y','z']:
		distance += (atom0.p(x)-atom1.p(x))**2
	return distance**0.5


def Group:
	def __init__(self,atoms):
		self.members = atoms

	def include(self, atoms, cut):
		full = False
		while not full:
			for atom in atoms: