import numpy as np
import LAMMPyS as lp


def sia_va(refdump, cascadedump, siavadump):
    steps = lp.rdump(refdump)
    refatoms = steps[0].atoms
    with open(cascadedump, 'r') as file:
        cascade_lines = file.readlines()
    with open(siavadump, 'w') as file:
        nline = 0
        nstep = 0
        while nline < len(cascade_lines):
            for i in range(4):
                line = cascade_lines[nline]
                file.write(line)
                nline += 1
            ndefects = int(line.split()[0])
            for i in range(4):
                line = cascade_lines[nline]
                file.write(line)
                nline += 1
            for i in range(1):
                line = "ITEM: ATOMS id type x y z c_2[1]\n"
                file.write(line)
                nline += 1
            for i in range(ndefects):
                line = cascade_lines[nline]
                words = line.split()
                id = int(words[0])
                r = [refatoms.id(id).x, refatoms.id(id).y, refatoms.id(id).z]
                words = words[:2] + [str(xs) for xs in r] + words[2:]
                words[2:5] = [str(xs) for xs in r]
                line = "{0} {1} {2} {3} {4} {5}\n".format(
                    words[0], words[1], words[2], words[3], words[4], words[5])
                file.write(line)
                nline += 1
            nstep += 1
            if (nstep % 100 == 0):
                print(nstep)

if __name__ == '__main__':
    sia_va(refdump='ref.dump', cascadedump='cell_lammps.dump',
           siavadump='cell.dump')
