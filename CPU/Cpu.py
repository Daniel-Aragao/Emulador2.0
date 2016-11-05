from COMPUTADOR import Constantes as Consts
import threading


class Cpu(threading.Thread):
    PASSO_SINAL = 0
    PASSO_ENDERECO_DADO = 1
    PASSO_PROCESSAMENTO = 2

    def __init__(self, barramento):
        super(Cpu, self).__init__()
        self.registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "CI": 0}
        self.barramento = barramento
        self.loops = []
        self.passo = Cpu.PASSO_SINAL
        self.tipoSinal = Consts.T_L_INSTRUCAO

    """
    enviar sinal com origem, destino, valor de ci e o tipo de leitura
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
    se o dado eh uma label
        armazenar label no vetor de loops juntamente do endereco desse label

    enviar sinal novamente
    """

    def run(self):
        while Consts.running:
            if self.passo == Cpu.PASSO_SINAL:
                """
                enviar sinal com origem, destino, valor de ci e o tipo de leitura
                apos anviar o passo vira de endereco_dado
                """
                self.enviar_sinal()
            elif self.passo == Cpu.PASSO_ENDERECO_DADO:
                """
                receber endereco(nova ci) e dado(a ser processado)
                quando os dois forem recebidos o passo vira de processamento
                """
                pass
            elif self.passo == Cpu.PASSO_PROCESSAMENTO:
                """
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
                se o dado eh uma label
                    armazenar label no vetor de loops juntamente do endereco desse label
                """

    def enviar_sinal(self):
        if self.registradores["CI"] != -1:
            sinal = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, self.registradores["CI"], self.tipoSinal)

            self.barramento.enviar_sinal(sinal)

            self.passo = Cpu.PASSO_ENDERECO_DADO

    def receber_endereco(self, endereco):
        pass

    def receber_dado(self, dado):
        pass
