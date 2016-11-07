import re
from Code import Code
from COMPUTADOR import Constantes as Consts


class Regex:

    def __init__(self):
        pass

    @staticmethod
    def traduzir(lines):
        codes = []

        pettern = r"(\w+)\s*"
        operacao = re.compile(pettern)

        patterns = {
            "add": r"(add)\s+(\w+)\s*,\s*(\w+)\s*",
            "mov": r"(mov)\s+(\w+)\s*,\s*(\w+)\s*",
            "imul": r"(imul)\s+(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*",
            "inc": r"(inc)\s+(\w+)\s*",
            "dec": r"(dec)\s+(\w+)\s*",
            "label": r"(label)\s+([^0]\d*)",
            "condicao": r"(\w+)\s*(<>|<|>|==)\s*(\w+)\s*[?]\s*(?:jump\s+|)(0|\d+)\s*:\s*(?:jump\s+|)(0|\d+)",
            "end": "end"
        }

        for line in lines:
            instrucao = operacao.match(line).group(1)
            reresult = None
            codetype = None
            if instrucao in patterns:
                reresult = re.match(patterns[instrucao], line)
                if reresult is None:
                    raise SyntaxError(line)

                reresult = reresult.groups()[1::]
                codetype = Consts.INSTRUCOES[instrucao]
            else:
                reresult = re.match(patterns["condicao"], line)
                if reresult is None:
                    raise SyntaxError(line)

                reresult = reresult.groups()
                codetype = Consts.INSTRUCOES["condicao"]

            codes.append(Code(codetype, reresult))

            if instrucao == "end":
                break

        return codes
