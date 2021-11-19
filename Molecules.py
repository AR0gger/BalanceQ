# paréntesis --
# no considera doble ocurrencia de elemento!! --
from DATA import Atoms
import re


class Molecule:
    def __init__(self, symbol):
        self.symbol = symbol
        self.charge = None
        if self.symbol[-1].isalpha():
            self.symbol += "1"

    def get_symbol(self):
        ss = {"2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇",
                "8": "₈", "9": "₉", "1": "₁", "0": "₀"}
        sp = {"+": "⁺", "-": "⁻", "2": "²", "3": "³", "4": "⁴",
              "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "1": "", "0": "⁰"}
        subp = self.symbol
        sub_rep = re.findall("(?:(?<=[A-Z][a-z])|(?<=[A-Z])|(?<=[)]))([0-9]+)", subp)
        sub_rep = list(map(lambda x: "".join([ss[i] if (len(x) != 1 or i != "1") else "" for i in [*x]]), sub_rep))
        for r in sub_rep:
            subp = re.sub("(?:(?<=[A-Z][a-z])|(?<=[A-Z])|(?<=[)]))([0-9]+)", r, subp, count=1)

        slate = "((?<=[(])[+-][0-9]*.?(?=[)]))|([+-][0-9]*[+-]?)|([+-]?[0-9]*[+-])"      # revisar/ mejorar
        t = re.search(slate, subp)
        if t is None:
            self.charge = 0
            return subp
        # print(t.group())
        self.charge = t.group()
        if len(t.group()) == 1:
            charge, value = (t.group(), "1")
        elif t.group()[0].isnumeric():
            value, charge = (t.group()[:-1], t.group()[-1])
        else:
            charge, value = (t.group()[0], t.group()[1:])
        # print(charge, value)
        t2 = re.sub(slate, "$$", subp)
        t3 = re.sub("([(][$]{2}[)])|([$]{2})", sp[charge] + sp[value], t2)
        return t3

    def change_symbol(self, change):
        self.symbol = change

    def get_elements(self):
        elements = []
        copia = list(self.symbol)
        while len(copia) > 0:
            first = copia.pop(0)
            if first in ["(", ")"]:
                continue
            if first.isupper():
                elements.append(first)
            if first.islower():
                elements[-1] += first
            if elements.count(elements[-1]) > 1:
                elements.pop()
        return elements

    def get_indexes(self):
        elements = self.get_elements()
        indexes = []
        for el in elements:
            follows = list(self.symbol.split(el))
            # print(follows, "start")
            ind = 0
            # for follow in follows[1:]:
            for i in range(1, len(follows)):
                follow = follows[i]
                follow = list(follow)
                fus = ""
                while len(follow) > 0 and follow[0].isnumeric():
                    fus += follow.pop(0)
                if fus == "":
                    fus = "1"
                if len(follow) > 0 and follow[0].islower():
                    continue
                factor = 1
                left = "".join(follows[:i])
                right = "".join(follows[i:])
                p_count = left.count("(")-left.count(")")
                f_count = 0
                right = list(right)
                while p_count > 0:
                    r = right.pop(0)
                    if r == "(":
                        f_count += 1
                        continue
                    elif r == ")":
                        if f_count > 0:
                            f_count -= 1
                            continue
                        else:
                            p_count -= 1
                    else:
                        continue
                    n = ""
                    while len(right) > 0 and right[0].isnumeric():
                        n += right.pop(0)
                    if n == "":
                        n = "1"
                    factor *= int(n)

                ind += int(fus) * factor
            indexes.append(str(ind))
        return indexes

    def get_molar_mass(self):
        elements = self.get_elements()
        indexes = self.get_indexes()
        mass = 0
        for el, ind in zip(elements, indexes):
            try:
                mass += Atoms[el][0]*int(ind)
            except KeyError:
                return "no se reconoce el elemento: {}".format(el)
            except TypeError:
                return Atoms[el][0]
        return round(mass, 2)


# m = Molecule("H+")
# print(m.get_molar_mass())
# print(m.get_symbol())
# print(m.get_elements())
# print(m.get_indexes())



# print(Molecule("BaO2").get_molar_mass())