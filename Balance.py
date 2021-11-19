from sympy import Matrix
from sympy.solvers import solve
from fractions import Fraction
from Molecules import Molecule
import math
import re

# modos: redox(ácido y básico), ácido-base, desplazamiento, dismutación
# cuando falta algo de algún lado?
# cargas?
# si hay más de una opción? cómo elegir


class Reaction:

    def __init__(self, reacts, prods, mode=1):
        self.reacts = reacts
        self.prods = prods
        self.mode = mode
        self.neto = 0           # agregar o no e-

    def starter(self):
        atoms = []
        charges = []

        info_r = {}

        for elem in self.reacts:
            molecule = Molecule(elem)
            molecule.get_symbol()
            charges.append(molecule.charge)
            atoms += molecule.get_elements()
            info_r[elem] = dict(zip(molecule.get_elements(), molecule.get_indexes()))

        info_p = {}

        for elem in self.prods:
            molecule = Molecule(elem)
            molecule.get_symbol()
            charges.append(molecule.charge)
            atoms += molecule.get_elements()
            info_p[elem] = dict(zip(molecule.get_elements(), molecule.get_indexes()))

        return (info_r, info_p), list(set(atoms)), charges


    def fix_charges(self, charges):
        my_charges = []
        for cha in charges:
            if type(cha) is str:
                x = re.split("(?<=\d)(?=\D)|(?<=\D)(?=\d)", cha)
                if len(x) == 1:
                    x.insert(0, "1")
                if not x[0].isnumeric():
                    x[0], x[1] = x[1], x[0]
                if x[1] == "+":
                    my_charges.append(int(x[0]))
                else:
                    my_charges.append(-int(x[0]))

            else:
                my_charges.append(0)

        return my_charges


    def set_matrix(self):
        columns = []
        info, atoms, charges = self.starter()
        new_charges = self.fix_charges(charges)
        for side in info:
            for molec in side:
                v = []
                for atom in atoms:
                    v.append(int(side[molec].get(atom, 0)))
                columns.append(Matrix(v))

        return Matrix.hstack(*columns), atoms, new_charges


    def get_coeffs(self):
        mat, atoms, charges = self.set_matrix()
        zeros = Matrix.zeros(len(atoms), 1)
        first, taus = mat.gauss_jordan_solve(zeros)
        dot_p = first.dot(Matrix(charges))
        unos = dict.fromkeys(taus[:-1], 1)
        try:
            ultimo = solve(dot_p.subs(unos))[0]
        except IndexError:
            ultimo = 0

        if self.mode == 2 or ultimo <= 0:
            intento = first.subs(dict.fromkeys(taus, 1)).tolist()
            self.neto = Matrix(charges).dot(Matrix(intento))
            return [float(abs(e[0])) for e in intento]

        unos[taus[-1]] = ultimo
        s = first.subs(unos).tolist()
        s_joined = [float(abs(e[0])) for e in s]
        return s_joined


    def normalizer(self):
        coffs = self.get_coeffs()
        denoms = [Fraction(x).limit_denominator().denominator for x in coffs]

        for d in denoms:
            coffs = [d*values for values in coffs]
            self.neto = self.neto*d
        coffs = [int(f) for f in coffs]
        gcd = math.gcd(*coffs)
        if gcd == 0:
            gcd = 1
        coffs = [int(e/gcd) for e in coffs]

        self.neto = int(self.neto/gcd)

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

        # s += str(self.neto)
        if self.neto < 0:
            s += " + " + str(abs(self.neto)) + " e-"

        s += " → "

        for j in range(len(self.prods)):
            m = Molecule(self.prods[j])
            s += str(coefficients.pop(0)) + " " + m.get_symbol()
            if j != len(self.prods) - 1:
                s += " + "

        if self.neto > 0:
            s += " + " + str(self.neto) + " e-"

        # s += self.molar_mass_printer()
        return s, self.molar_mass_printer()

    def molar_mass_printer(self):
        s = []
        # s += "<br><br>Masas molares:<br>"
        for molecule in set(self.reacts + self.prods):
            m = Molecule(molecule)
            s.append(m.get_symbol() + " → " + str(m.get_molar_mass()))
        return s


