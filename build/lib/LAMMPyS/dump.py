import numpy as np
import pandas as pd
import linecache
import math


class Atoms:

    def __init__(self, df_atoms):
        self._df = df_atoms      # pandas.DataFrame

    def __len__(self):
        return len(self._df)

    def __getitem__(self, n):
        atom = Atom(self, self._df.iloc[n])
        return atom

    def properties(self):
        return ['id'] + list(self._df.columns)

    def id(self, n):
        atom = Atom(self, self._df.loc[n])
        return atom

    def find_neibour(self, taget_atoms, con=lambda atom: True):
        def c_distance(atom1, atom2):
            r = math.sqrt((atom2['x'] - atom1['x'])**2 +
                          (atom2['y'] - atom1['y'])**2 +
                          (atom2['z'] - atom1['z'])**2)
            return r

        for atom in self:
            if con(atom):
                atoms_sorted = sorted(target_atoms,
                                      key=lambda target_atom: c_distance(atom, target_atom))
                self.set_property(atom, 'neibours1',
                                  atoms_sorted[1]._name)
                self.set_property(atom, 'neibours2',
                                  atoms_sorted[2]._name)

    def set_property(self, atom, property, value):
        if property in self.properties():
            self._df.set_value(atom.id, property, value)
        else:
            self._df[property] = 0
            self._df.set_value(atom.id, property, value)

        # 统一属性 添加属性等于添加列 添加功能等于给所有原子添加功能


class Atom():

    def __init__(self, atoms, df_atom):
        self.__dict__['_df'] = df_atom
        self.__dict__['atoms'] = atoms

    def __str__(self):
        return str(self._df)

    def __getattr__(self, name):
        if name == 'id':
            return self.__dict__['_df'].name
        else:
            return self.__dict__['_df'][name]

    def __setattr__(self, property, value):
        self.atoms.set_property(self, property, value)
        self.__dict__['_df'].set_value(property, value)


class Step:

    def __init__(self, atoms, timestep, box):
        self.atoms = atoms
        self.timestep = timestep
        self.box = box
        atoms._step = self


class CachedLineList:

    def __init__(self, filename):
        self._filename = filename

    def __getitem__(self, n):
        return linecache.getline(self._filename, n + 1)


def read_dump(dumpfile):
    print('Loading dump file...')
    lines = CachedLineList(dumpfile)
    n = 0
    steps = []
    while True:
        if len(lines[n + 1]) == 0:
            break
        timestep = int(lines[n + 1].split()[0])
        natoms = int(lines[n + 3].split()[0])
        box = []
        for i in range(3):
            boundary = [float(word) for word in lines[n + 5 + i].split()]
            box.append(boundary)
        box = np.array(box)
        properties = lines[n + 8].split()[2:]
        df_atoms = pd.read_csv(dumpfile, header=None, delim_whitespace=True,
                               names=properties, index_col=0,
                               skiprows=9 + n, nrows=natoms)
        atoms = Atoms(df_atoms)
        step = Step(atoms, timestep, box)
        steps.append(step)
        n += 9 + natoms
    print('Loading compeleted')
    return steps


def write_dump(steps, filename):
    print('Start writing...')
    with open(filename, 'w') as file:
        for step in steps:
            file.write('ITEM: TIMESTEP\n')
            file.write(str(step.timestep) + '\n')
            file.write('ITEM: NUMBER OF ATOMS\n')
            file.write(str(len(step.atoms)) + '\n')
            file.write('ITEM: BOX BOUNDS pp pp pp\n')
            for d in step.box:
                file.write('{0} {1}\n'.format(d[0], d[1]))
            file.write('ITEM: ATOMS ')
            for p in step.atoms.properties():
                file.write(p + ' ')
            file.write('\n')
            for atom in step.atoms:
                file.write(str(atom._name) + ' ')
                for p in atom:
                    file.write(str(p) + ' ')
                file.write('\n')
    print('Writing compeleted.')


if __name__ == '__main__':
    steps = read_dump('high.dump')
    atoms = steps[0].atoms
    # write_dump(steps, 'ref.out.dump')
