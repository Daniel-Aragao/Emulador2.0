from COMPUTADOR import Constantes as Consts


class Code:
    """
    "end": 1,
    "inc": 2,
    "dec": 3,
    "label": 4,
    "add": 5,
    "mov": 6,
    "imul": 7,
    "condicao": 8
    """
    def __init__(self, instrucao, groups):
        self.groups = groups
        self.instrucao = instrucao
        self.byte_array = self.get_byte_array()

    def get_byte_array(self):
        # codigo talvez va precisar de flags de memoria, registrador ou valor
        code = [-1 for i in range(Consts.CODE_SIZE)]

        # instrucao
        code[0] = self.instrucao.codigo
        # primeiro parametro que todos possuem

        if self.instrucao.nome == "mov":
            hasarroba = self.groups[0][0] == '@'
            if hasarroba:
                code[1] = 1
                code[2] = Code.solve_value(self.groups[0][1::])
            else:
                code[1] = 0
                code[2] = Code.solve_value(self.groups[0])
            code[3] = Code.solve_value(self.groups[1])

            return code

        for i in range(self.instrucao.numparametros):
            if self.instrucao.nome == "condicao" and i == 1:
                code[i + 1] = Consts.CONDICOES[self.groups[i]]
            else:
                code[i+1] = Code.solve_value(self.groups[i])

        return code

    @staticmethod
    def solve_value(valor):
        retorno = None
        try:
            # tenta converter para inteiro
            retorno = int(valor)
            if retorno < 0:
                Consts.running = False
                raise Exception("Impossivel ler valores negativos")
            return retorno
        except ValueError:
            pass

        try:
            # tenta converter para registrador
            retorno = -float(ord(valor))
            if retorno >= 0:
                Consts.running = False
                raise Exception("Registrador invalido")
            return retorno
        except TypeError:
            pass

        # converte para posicao de memoria
        if retorno is None:
            retorno = -int(valor, 16)
            if retorno > 0:
                Consts.running = False
                raise Exception("Nao existe posicao de memoria negativa")
        return retorno
