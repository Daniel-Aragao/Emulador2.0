from COMPUTADOR import Constantes as Consts


class Code:
    """
    "end": "end" 1
    "label": r"(label)\s+([^0]\d*)", 2
    "inc": r"(inc)\s+(\w+)\s*", 2
    "dec": r"(dec)\s+(\w+)\s*", 2
    "add": r"(add)\s+(\w+)\s*,\s*(\w+)\s*", 3
    "mov": r"(mov)\s+(\w+)\s*,\s*(\w+)\s*", 3
    "imul": r"(imul)\s+(\w+)\s*,\s*(\w+)\s*,\s*(\w+)\s*", 4
    "condicao": r"(\w+)\s*(<>|<|>|==)\s*(\w+)\s*[?]\s*(?:jump\s+|)(0|\d+)\s*:\s*(?:jump\s+|)(0|\d+)", 5
    """
    def __init__(self, groups):
        self.groups = groups
        self.byte_array = Code.get_byte_array(groups)

    @staticmethod
    def get_byte_array(groups):
        code = [-1 for i in range(Consts.CODE_SIZE)]
    reconhecer a instrucao lá fora e aqui só reconhecer os valores restantes

        return [groups]
