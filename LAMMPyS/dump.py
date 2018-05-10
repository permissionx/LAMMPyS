import linecache
import numpy as np


class Step:
    def __init__(self, atoms, properties, timestep, box, dic):
        # atoms: np.array
        # properties: [str...]
        self.atoms = np.array(atoms)
        self.properties = properties
        self.timestep = timestep
        self.box = box
        self.dic = dic
    
    def pi(self, p):
        # property index or property initialization
        # atom[step.pi('id')]
        if p in self.properties:
        	return self.properties.index(p)
        else:
        	self.properties.append(p)
        	zeros = np.zeros(len(self.atoms))
        	self.atoms = np.c_[self.atoms, zeros]
        	return self.properties.index(p)
    
    def id_get(self,id):
        return self.atoms[self.dic[id]]  # need to exam

    def get_atom(self, p, n):
        # p: str
        index = self.properties.index(p)
        ps = self.atoms[:, index]
        try:
        	atom_index = np.where(ps == n)[0][0]
        except IndexError:
        	print('Atom with {0} equals {1} not found.'.format(p,n))
        	raise IndexError
        atom = self.atoms[atom_index]
        return atom

    def write(self, dump_file, append=True):
        print('Start writing timestep {0}...'.format(self.timestep))
        lines = []
        if append:
        	try:
	            with open(dump_file, 'r') as file:
	                lines = file.readlines()
	        except FileNotFoundError:
	        	pass
        lines.append('ITEM: TIMESTEP\n')
        lines.append(str(self.timestep) + '\n')
        lines.append('ITEM: NUMBER OF ATOMS\n')
        lines.append(str(len(self.atoms)) + '\n')
        lines.append('ITEM: BOX BOUNDS pp pp pp\n')
        for d in self.box:
            lines.append('{0} {1}\n'.format(d[0], d[1]))
        lines.append('ITEM: ATOMS ')
        for p in self.properties:
            lines.append(p + ' ')
        lines.append('\n')
        for atom in self.atoms:
            for p in atom:
                lines.append(str(p) + ' ')
            lines.append('\n')
        with open(dump_file, 'w') as file:
            for line in lines:
            	file.write(line)
        print('Writing compeleted')


class Cached_line_list:
    def __init__(self, filename):
        self._filename = filename

    def __getitem__(self, n):
        return linecache.getline(self._filename, n + 1)


def scan(dump_file):
    print('Scan dump file...')
    step_lines = []
    with open(dump_file, 'r') as file:
        n = 0
        while True:
            line = file.readline()
            if not line:
                break
            if line == 'ITEM: TIMESTEP\n':
                step_lines.append(n)
            n += 1
    print('Scaning {0} steps compeleted.'.format(len(step_lines)))
    return step_lines


def load_step(dump_file, n):
    # from nth line
    lines = Cached_line_list(dump_file)
    timestep = int(lines[n + 1].split()[0])
    natoms = int(lines[n + 3].split()[0])
    box = []
    for i in range(3):
        boundary = [float(word) for word in lines[n + 5 + i].split()]
        box.append(boundary)
    box = np.array(box)
    properties = lines[n + 8].split()[2:]
    id_index = properties.index('id')
    dic = {}
    atoms = []
    nline = n + 9
    natom = 0
    while nline < n + natoms + 9:
        line = lines[nline]
        atom = [float(word) for word in line.split()]
        atoms.append(atom)
        dic[atom[id_index]] = natom
        natom += 1
        nline += 1
    step = Step(atoms, properties, timestep, box, dic)
    print('Load {0} atoms compeleted.'.format(natoms))
    return step


def append(step, atom):
    if step.atoms.shape[0] == 0:
        step.atoms = np.array([atom])
    else:
        step.atoms = np.apend(atoms, [atom])


class Steps:
    # steps read from dump step by step.
    def __init__(self, dump_file):
        self.step_lines = scan(dump_file)
        self.dump_file = dump_file

    def __getitem__(self, nstep):
        print('Loading step {0}...'.format(nstep))
        n = self.step_lines[nstep]
        return load_step(self.dump_file, n)

    def __len__(self):
    	return len(self.step_lines)


if __name__ == '__main__':
    steps = Steps('test.dump')
    with open('test.out.dump','w') as file:
    	pass
    for step in steps:
        step.write('test.out.dump')
