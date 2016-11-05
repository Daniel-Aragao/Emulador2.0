
class Cpu:

    def __init__(self, barramento):
        self.registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "CI": 0}
        self.barramento = barramento
        self.loops = [] # pilha

    """
    enviar sinal com o valor de ci o tipo de leitura
    receber endereco(nova ci) e dado(a ser processado)
    se a lista de loops NAO for vazia
        se a instrucao nao eh fim de loop
            se ci igual ao inicio do primeiro loop
                raise out of memory
        se nao
            se eh fim do ultimo loop
                ultimo = retiro o ultimo loop
                testo a condicao do loop
                se a condicao eh verdadeira
                    ci recebe ultimo.linha
                    tipo de leitura eh releitura( nao pega do disco na releitura)
                se nao
                    tipo de leitura eh leitura
            se nao
                raise exception

    processar dado
    """
