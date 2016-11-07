import re
from Code import Code


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
            "end": "end code"
        }

        for line in lines:
            instrucao = operacao.match(line).group(1)
            if instrucao in patterns:
                reresult = re.match(patterns[instrucao], line)
            else:
                reresult = re.match(patterns["condicao"], line)

            if reresult is None:
                raise SyntaxError(line)

            codes.append(Code(reresult))

            if instrucao == "end":
                break

        return codes
