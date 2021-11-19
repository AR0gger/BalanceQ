from sympy import Matrix
from fractions import Fraction
from Molecules import Molecule
import math
import re

# modos: redox(ácido y básico), ácido-base, desplazamiento, dismutación
# cuando falta algo de algún lado?

class Reaction:

    def __init__(self, reacts, prods, mode=1):
        self.reacts = reacts
        self.prods = prods
        self.mode = mode

    def starter(self):
        info_r = {}
        atoms = []

        for elem in self.reacts:
            molecule = Molecule(elem)
            atoms += molecule.get_elements()
            info_r[elem] = dict(zip(molecule.get_elements(), molecule.get_indexes()))

        info_p = {}

        for elem in self.prods:
            molecule = Molecule(elem)
            atoms += molecule.get_elements()
            info_p[elem] = dict(zip(molecule.get_elements(), molecule.get_indexes()))

        return (info_r, info_p), list(set(atoms))

    def set_matrix(self):
        columns = []
        info, atoms = self.starter()

        for side in info:
            for molec in side:
                v = []
                for atom in atoms:
                    v.append(int(side[molec].get(atom, 0)))
                columns.append(Matrix(v))

        return Matrix.hstack(*columns), atoms

    def get_coeffs(self):
        mat, atoms = self.set_matrix()
        zeros = Matrix.zeros(len(atoms), 1)
        first = mat.gauss_jordan_solve(zeros)[0]
        second = "".join([str(x) for x in first.values()])
        r = set(re.findall("tau.", second))                         # de tau0 a tau9
        third = dict.fromkeys(r, 1)                 # a todos los tau. les asigna 1
        s = first.subs(third).tolist()
        s_joined = [float(abs(e[0])) for e in s]
        return s_joined

    def normalizer(self):
        coffs = self.get_coeffs()
        denoms = [Fraction(x).limit_denominator().denominator for x in coffs]

        for d in denoms:
            coffs = [d*values for values in coffs]
        coffs = [int(f) for f in coffs]
        gcd = math.gcd(*coffs)
        if gcd == 0:
            gcd = 1
        coffs = [int(e/gcd) for e in coffs]

        return coffs


class Balanced(Reaction):

    def __init__(self, reacts, prods, mode=1):
        super().__init__(reacts, prods, mode)

    def reaction_printer(self):
        coefficients = self.normalizer()
        s = ""
        for i in range(len(self.reacts)):
            m = Molecule(self.reacts[i])
            s += str(coefficients.pop(0)) + " " + m.get_symbol()
            if i != len(self.reacts) - 1:
                s += " + "

        s += " → "

        for j in range(len(self.prods)):
            m = Molecule(self.prods[j])
            s += str(coefficients.pop(0)) + " " + m.get_symbol()
            if j != len(self.prods) - 1:
                s += " + "

        # s += self.molar_mass_printer()
        return s, self.molar_mass_printer()

    def molar_mass_printer(self):
        s = []
        # s += "<br><br>Masas molares:<br>"
        for molecule in set(self.reacts + self.prods):
            m = Molecule(molecule)
            s.append(m.get_symbol() + " → " + str(m.get_molar_mass()))
        return s


