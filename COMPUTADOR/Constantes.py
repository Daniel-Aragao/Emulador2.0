RAM = 0
ENTRADA = 1
CPU = 2
Componentes = []

running = False

# clock = [10^2 hz a 10^9 hz]
clock = 100
# lbar = [2^3, 2^7] em bits
larguraBarramento = 8
# lbanda = (clock * lbar)// 8 bits  => 8 bits = 1 byte
larguraBanda = (clock * larguraBarramento) // 8

sleep = 1

# Estrutura do vetor de conexao com os componentes

# Geral
T_LENGTH = 4
# Origem, destino, dados
T_ORIGEM = 0
T_DESTINO = 1
T_DADOS = 2
T_TIPO = 3

# Tipos de sinal
# L - leitura, RL - releitura, E - escrita
T_L_INSTRUCAO = 0
T_RL_INSTRUCAO = 0
T_L_VALOR = 1
T_E_INSTRUCAO = 2
T_E_VALOR = 3
