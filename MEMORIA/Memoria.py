from COMPUTADOR import Constantes as Consts
import threading
# import time
from Queue import Queue
from ILOGS.ConsoleLog import ConsoleLog
from COMPUTADOR.ArrayTools import ArrayTools as At


class Memoria(threading.Thread):

    def __init__(self, barramento, tamanho, log=ConsoleLog()):
        super(Memoria, self).__init__()
        self.log = log

        if tamanho < Consts.MEMORIA_X_MIN:
            tamanho = Consts.MEMORIA_X_MIN
            log.write_line('tamanho de memoria muito pequeno, o tamanho minimo foi escolhido')
        elif tamanho > Consts.MEMORIA_X_MAX:
            tamanho = Consts.MEMORIA_X_MAX
            log.write_line('tamanho de memoria muito grande, o tamanho maximo foi escolhido')

        self.tamanho = 32 * 2**tamanho
        self.code_slice = Consts.get_memoria_code_sliced(self.tamanho)
        self.memoria = [0 for i in range(self.tamanho)]
        self.sinais = Queue()
        self.dado = None
        self.barramento = barramento

    def receber_sinal(self, sinal):
        self.sinais.put(sinal, timeout=Consts.timeout)

    def receber_endereco(self):
        pass

    def receber_dado(self, d):
        self.dado = d

    def run(self):
        while Consts.running:
            if not self.sinais.empty():
                self.processar_sinal(self.sinais.get(timeout=Consts.timeout))

    def processar_sinal(self, sinal):
        origem = sinal[Consts.T_ORIGEM]

        if origem == Consts.CPU:
            self.tratar_sinal_cpu(sinal)
        elif origem == Consts.ENTRADA:
            self.tratar_sinal_entrada(sinal)

    def tratar_sinal_cpu(self, sinal):
        tipo = sinal[Consts.T_TIPO]
        if tipo == Consts.T_L_INSTRUCAO or tipo == Consts.T_RL_INSTRUCAO:
            if tipo == Consts.T_L_INSTRUCAO:
                # pego na entrada e ponho na posicao do ci e fico esperando via loop
                self.get_instrucao_entrada(sinal[Consts.T_DADOS])

            proximoendereco = self.proximo_endereco(sinal[Consts.T_DADOS])
            endereco = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, proximoendereco, tipo)
            self.barramento.enviar_endereco(endereco)

            instrucao = self.ler_instrucao(sinal[Consts.T_DADOS])

            dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, instrucao, tipo)

            self.barramento.enviar_dado(dado)

        elif tipo == Consts.T_L_VALOR:
            endereco = sinal[Consts.T_DADOS]
            endereco += self.code_slice

            dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, self.memoria[endereco], tipo)

            self.barramento.enviar_dado(dado)

        elif tipo == Consts.T_E_VALOR:
            endereco, novovalor = sinal[Consts.T_DADOS]

            endereco += self.code_slice
            if self.tamanho < endereco:
                raise MemoryError("Posicao de memoria inexistente")
            self.memoria[endereco] = novovalor

        else:
            raise Exception("sinal invalido")

    def tratar_sinal_entrada(self, sinal):
        pass

    def proximo_endereco(self, endereco):
        return (endereco + Consts.CODE_SIZE) % self.code_slice

    def anterior_endereco(self, endereco):
        return (endereco - Consts.CODE_SIZE) % self.code_slice

    def ler_instrucao(self, endereco):
        if endereco > self.code_slice:
            raise MemoryError("instrucoes devem ser encontradas ate a posicao "
                              "de memoria "+str(Memoria.anterior_endereco(self.code_slice)))

        return At.sub_array(self.memoria, endereco, Consts.CODE_SIZE)

    def get_instrucao_entrada(self, pos):
        conect = Consts.get_vetor_conexao(Consts.RAM, Consts.ENTRADA, None, Consts.T_L_INSTRUCAO)

        self.barramento.enviar_sinal(conect)

        while self.dado is None:
            pass

        At.append_array(self.dado, self.memoria, pos, Consts.CODE_SIZE)

        self.dado = None
