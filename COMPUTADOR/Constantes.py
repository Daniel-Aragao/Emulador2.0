RAM = 0
ENTRADA = 1
CPU = 2
Componentes = [0, 1, 2]

running = False

# clock = [10^2 hz a 10^9 hz]
clock = 1000
# lbar = [2^3, 2^7] em bits
larguraBarramento = 128  # 16
# lbanda = (clock * lbar)// 8 bits  => 8 bits = 1 byte
larguraBanda = (clock * larguraBarramento) // 8

# tamanho da memoria de 32* 2**0 a 32 * 2**19 ( 32 * 2**X)
MEMORIA_X_MIN = 0
MEMORIA_X_MAX = 19
MEMORIA_X = 2  # 2
MEMORIA_CODE_SLICE = 1.0/2

# cache em porcentagem da memoria 1.0 a 1.1
CACHE_TAX = 1.1


def get_memoria_code_sliced(t):
    return int(t * MEMORIA_CODE_SLICE)

# tamanho de uma instrucao
# maior eh a (condicao a > b ? jump 3 : jump 8)
CODE_SIZE = 6

sleep = 1
timeout = 2*sleep

# Estrutura do vetor de conexao com os componentes
# Geral
T_LENGTH = 4
# Origem, destino, dados
T_ORIGEM = 0
T_DESTINO = 1
T_DADOS = 2
T_TIPO = 3
# Sinal E de valor
T_EVLENGTH = 5
T_EVALOR_POS = 4

# Tipos de sinal
# L - leitura, RL - releitura, E - escrita
T_L_INSTRUCAO = 0
T_RL_INSTRUCAO = 4
T_L_VALOR = 1
T_E_INSTRUCAO = 2
T_E_VALOR = 3


def get_vetor_conexao(origem, destino, dado, tipo, len=T_LENGTH):
    sinal = [i for i in range(len)]
    sinal[T_ORIGEM] = origem
    sinal[T_DESTINO] = destino
    sinal[T_DADOS] = dado
    sinal[T_TIPO] = tipo

    return sinal


class Instrucao:

    def __init__(self, nome, codigo, numparametros):
        self.nome = nome
        self.codigo = codigo
        self.numparametros = numparametros


INSTRUCOES = {
    "end": Instrucao("end", 1, 0),
    "inc": Instrucao("inc", 2, 1),
    "dec": Instrucao("dec", 3, 1),
    "label": Instrucao("label", 4, 1),
    "add": Instrucao("add", 5, 2),
    "mov": Instrucao("mov", 6, 3),
    "imul": Instrucao("imul", 7, 3),
    "condicao": Instrucao("condicao", 8, 5)
}

CONDICOES = {
    "<": 1,
    ">": 2,
    "<>": 3,
    "==": 4,
    ">=": 5,
    "<=": 6
}


def get_condicao_string(valor):
    for cond in CONDICOES:
        if CONDICOES[cond] == valor:
            return cond

# defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace\\Arquitetura2.0\\res\\file_sample.txt"

# defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
#               r"\\Arquitetura2.0\\res\\assembly_com_loop.txt"

# defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
#               r"\\Arquitetura2.0\\res\\inc_end.txt"

defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
              r"\\Arquitetura2.0\\res\\teste.txt"