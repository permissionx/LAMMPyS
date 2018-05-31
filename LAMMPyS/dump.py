import linecache
import numpy as np


class Atoms(np.ndarray):
    # for both atom and atoms
    # need to add __getattribute__ and __setattribute__
    def __new__(cls, input_array, step = None):
        obj = np.asarray(input_array).view(cls)
        obj.step = step
        return obj

    def __array_finalize__(self, obj):
        self.step = getattr(obj, 'step', None)

    def p(self, p):
        if len(self.shape) == 2:
            return self[:, self.step.pi(p)]
        else:
            return self[self.step.pi(p)]

    def id(self, id):
        return self[self.step.dic[id]]

    def select(self, p, n):
        if len(self.shape) == 2:
            ps = self.p(p)
            try:
                index = np.where(ps == n)[0][0]
            except IndexError:
                print('Atom with {0} equals {1} not found.'.format(p, n))
                raise IndexError
            return self[index]
        else:
            print('Selection must used in atoms')

    def set_p(self, p, n):
        if p in self.step._properties:
            if len(self.shape) == 2:
                self[:, self.step.pi(p)] = n
            else:
                self[self.step.pi(p)] = n
        else:
            print(
                'Property {0} not exit, please add_p(_properties) first.'.format(p))

    def update(self):
        ids = self.p('id')
        atoms = []
        for id in ids:
            atom = self.step.atoms.id(id)
            atoms.append(atom)
        atoms = Atoms(atoms, self.step)
        return atoms

    def add_p(self, p):
        # if atoms add_p, their step weill add_p, then step.atoms will add_p.
        if p not in self.step._properties:
            self.step.add_p(p)
            atoms = self.update()
            return atoms
        else:
            print('Property {0} already exit.'.format(p))


class Step:
    def __init__(self, atoms, _properties, timestep, box, dic):
        # atoms: np.array
        # _properties: [str...]
        self.atoms = Atoms(np.array(atoms), self)
        self._properties = _properties
        self.timestep = timestep
        self.box = box
        self.dic = dic

    def pi(self, p):
        # property index or property initialization
        # atom[step.pi('id')]
        return self._properties.index(p)

    def add_p(self, p):
        if p not in self._properties:
            self._properties.append(p)
            zeros = np.zeros(len(self.atoms))
            self.atoms = Atoms(np.c_[self.atoms, zeros], self)
        else:
            print('Property {0} already exit.'.format(p))

    def append(self, atom):
        step.atoms = Atoms(np.r_[self, atom], self)
        return self.step.atoms

    def write(self, dump_file, append=True):
        print('Start writing timestep {0} in {1}...'.format(
            self.timestep, dump_file))
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
        for p in self._properties:
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
    _properties = lines[n + 8].split()[2:]
    id_index = _properties.index('id')
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
    step = Step(atoms, _properties, timestep, box, dic)
    print('Load {0} atoms compeleted.'.format(natoms))
    return step


def append(step, atom):
    if step.atoms.shape[0] == 0:
        step.atoms = np.array([atom])
    else:
        step.atoms = np.apend(atoms, [atom])


def init_dump(filename):
    with open(filename, 'w') as file:
        pass


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
    step = steps[-1]
    atoms = step.atoms
