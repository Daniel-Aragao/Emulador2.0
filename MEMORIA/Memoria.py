from COMPUTADOR import Constantes as Consts
import threading
# import time
from Queue import Queue
from ILOGS.ConsoleLog import ConsoleLog
from COMPUTADOR.ArrayTools import ArrayTools as At


class Memoria(threading.Thread):

    def __init__(self, barramento, tamanho, log=ConsoleLog()):
        super(Memoria, self).__init__(name="Memoria")
        self.log = log

        if tamanho < Consts.MEMORIA_X_MIN:
            tamanho = Consts.MEMORIA_X_MIN
            log.write_line('tamanho de memoria muito pequeno, o tamanho minimo foi escolhido')
        elif tamanho > Consts.MEMORIA_X_MAX:
            tamanho = Consts.MEMORIA_X_MAX
            log.write_line('tamanho de memoria muito grande, o tamanho maximo foi escolhido')

        self.tamanho = 32 * 2**tamanho
        slice = Consts.get_memoria_code_sliced(self.tamanho)
        self.code_slice = slice - slice % Consts.CODE_SIZE
        self.memoria = [0 for i in range(self.tamanho)]
        self.sinais = Queue()
        self.dado = None
        self.barramento = barramento
        self.esperando_entrada = False

    def receber_sinal(self, sinal):
        self.sinais.put(sinal, timeout=Consts.timeout)

    def receber_endereco(self):
        pass

    def receber_dado(self, d):
        self.dado = d

    def run(self):
        self.log.write_line("Memoria start")
        while Consts.running:
            if not self.sinais.empty():
                self.processar_sinal(self.sinais.get(timeout=Consts.timeout))
        self.log.write_line("Memoria end")

    def processar_sinal(self, sinal):
        origem = sinal[Consts.T_ORIGEM]

        if origem == Consts.CPU:
            self.tratar_sinal_cpu(sinal)
        elif origem == Consts.ENTRADA:
            self.tratar_sinal_entrada(sinal)

    def tratar_sinal_cpu(self, sinal):
        tipo = sinal[Consts.T_TIPO]
        if tipo == Consts.T_L_INSTRUCAO:
            # deve continuar rodando a memoria, porem deve esperar a entrada enviar dados para poder agir
            self.esperando_entrada = True
        elif tipo == Consts.T_RL_INSTRUCAO:
            # if tipo == Consts.T_L_INSTRUCAO:
            #     # pego na entrada e ponho na posicao do ci e fico esperando via loop
            #     self.get_instrucao_entrada(sinal[Consts.T_DADOS])

            self.enviar_endereco_dado_cpu(sinal[Consts.T_DADOS], tipo)

        elif tipo == Consts.T_L_VALOR:
            endereco = sinal[Consts.T_DADOS]
            endereco += self.code_slice

            if self.tamanho - 1 < endereco:
                raise MemoryError("Posicao de memoria inexistente")

            dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, self.memoria[endereco], tipo)

            self.barramento.enviar_dado(dado)

        elif tipo == Consts.T_E_VALOR:
            endereco = sinal[Consts.T_DADOS]

            endereco += self.code_slice

            if self.tamanho - 1 < endereco:
                raise MemoryError("Posicao de memoria inexistente")

            self.memoria[endereco] = sinal[Consts.T_EVALOR_POS]

        else:
            raise Exception("sinal invalido")

    def enviar_endereco_dado_cpu(self, posmem, tipo):
        proximoendereco = self.proximo_endereco(posmem)
        endereco = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, proximoendereco, tipo)
        self.barramento.enviar_endereco(endereco)

        instrucao = self.ler_instrucao(posmem)
        dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, instrucao, tipo)
        self.barramento.enviar_dado(dado)

    def tratar_sinal_entrada(self, sinal):
        tipo = sinal[Consts.T_TIPO]

        if tipo == Consts.T_E_INSTRUCAO:
            self.get_instrucao_entrada(sinal)
        else:
            raise Exception("sinal invalido")

    def proximo_endereco(self, endereco):
        return (endereco + Consts.CODE_SIZE) % self.code_slice

    def anterior_endereco(self, endereco):
        return (endereco - Consts.CODE_SIZE) % self.code_slice

    def ler_instrucao(self, endereco):
        if endereco + Consts.CODE_SIZE > self.code_slice:
            raise MemoryError("instrucoes devem ser encontradas ate a posicao "
                              "de memoria "+str(self.anterior_endereco(self.code_slice)) + " informado "+str(endereco))

        return At.sub_array(self.memoria, endereco, Consts.CODE_SIZE)

    def escrever_instrucao(self, pos, instrucao):
        if pos + Consts.CODE_SIZE > self.code_slice:
            raise MemoryError("instrucoes devem ser encontradas ate a posicao "
                              "de memoria "+str(self.anterior_endereco(self.code_slice)) + " informado "+str(pos))
        At.append_array(instrucao, self.memoria, pos, Consts.CODE_SIZE)

    def get_instrucao_entrada(self, sinal):
        pos = sinal[Consts.T_DADOS]
        endereco = Consts.get_vetor_conexao(Consts.RAM, Consts.ENTRADA, pos, Consts.T_E_INSTRUCAO)

        self.barramento.enviar_endereco(endereco)

        while self.dado is None:
            pass

        self.escrever_instrucao(pos, self.dado[Consts.T_DADOS])

        self.dado = None

        if self.esperando_entrada:
            self.esperando_entrada = False
            self.enviar_endereco_dado_cpu(pos, Consts.T_L_INSTRUCAO)
