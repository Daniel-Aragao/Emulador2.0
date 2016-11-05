RAM = 0
ENTRADA = 1
CPU = 2
Componentes = [0, 1, 2]

running = False

# clock = [10^2 hz a 10^9 hz]
clock = 100
# lbar = [2^3, 2^7] em bits
larguraBarramento = 8
# lbanda = (clock * lbar)// 8 bits  => 8 bits = 1 byte
larguraBanda = (clock * larguraBarramento) // 8

# tamanho da memoria de 32* 2**0 a 32 * 2**19 ( 32 * 2**X)
MEMORIA_X_MIN = 0
MEMORIA_X_MAX = 19
MEMORIA_X = 0
MEMORIA_CODE_SLICE = 1/2

# tamanho de uma instrucao
CODE_SIZE = 5

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
T_E_VALOR_T = 4

# Tipos de sinal
# L - leitura, RL - releitura, E - escrita
T_L_INSTRUCAO = 0
T_RL_INSTRUCAO = 0
T_L_VALOR = 1
T_E_INSTRUCAO = 2
T_E_VALOR = 3


def get_vetor_conexao(origem, destino, dado, tipo):
    sinal = [i for i in range(T_LENGTH)]
    sinal[T_ORIGEM] = origem
    sinal[T_DESTINO] = destino
    sinal[T_DADOS] = dado
    sinal[T_TIPO] = tipo

    return sinal

