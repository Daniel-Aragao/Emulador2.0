from COMPUTADOR import Constantes as Consts
import threading
# import time
from Queue import Queue
from ILOGS.Logs import LogNone
from COMPUTADOR.ArrayTools import ArrayTools as At


class Memoria(threading.Thread):
    # implementar cache usando lru, lfu e cooldown
    # fazer um relatorio dizendo qual o melhor em termos de hits e misses do cache
    # configurar o algoritmo walk throught da cache x:1 ( x mudanca no cache atualiza a ram, se chegar nao chegar em x
    #   quando o timeout acabar, entao iremos atualizar antes de remover) pro dia 28
    def __init__(self, barramento, tamanho, log=LogNone()):
        super(Memoria, self).__init__(name="Memoria")
        self.log = log
        self.tamanho_informado = tamanho
        if tamanho > 35:
            MemoryError("limite de memoria excedido (32GB ou 32*2**30)")

        if tamanho < Consts.MEMORIA_X_MIN:
            tamanho = Consts.MEMORIA_X_MIN
            log.write_line('tamanho de memoria muito pequeno, o tamanho minimo foi escolhido')
        elif tamanho > Consts.MEMORIA_X_MAX:
            tamanho = Consts.MEMORIA_X_MAX
            # log.write_line('tamanho de memoria muito grande, o tamanho maximo foi escolhido')

        self.tamanho = 32 * (2**tamanho)
        codeslice = Consts.get_memoria_code_sliced(self.tamanho)
        self.code_slice = codeslice - (codeslice % Consts.CODE_SIZE)
        self.tamanho_total_valores = (32 * (2**self.tamanho_informado)) - self.code_slice
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
        self.log.write_line("Memoria= >> start")
        while Consts.running:  # or not self.sinais.empty():
            if not self.sinais.empty():
                self.log.write_line('memoria =>> receber sinal')
                self.processar_sinal(self.sinais.get(timeout=Consts.timeout))
        self.log.write_line("Memoria =>> end")

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

            if self.tamanho - 1 < endereco:
                if (self.tamanho_total_valores + self.code_slice) < endereco:
                    raise MemoryError("Posicao de memoria " + str(endereco - self.code_slice) + " inexistente")

                dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, 0, tipo)

            else:
                dado = Consts.get_vetor_conexao(Consts.RAM, Consts.CPU, self.memoria[endereco], tipo)

            self.barramento.enviar_dado(dado)

        elif tipo == Consts.T_E_VALOR:
            endereco = sinal[Consts.T_DADOS]

            endereco += self.code_slice

            if self.tamanho - 1 < endereco:
                if (self.tamanho_total_valores + self.code_slice) < endereco:
                    Consts.running = False
                    raise MemoryError("Posicao de memoria " + str(endereco - self.code_slice) + " inexistente")
            else:
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
            Consts.running = False
            raise Exception("sinal invalido")

    def proximo_endereco(self, endereco):
        return (endereco + Consts.CODE_SIZE) % self.code_slice

    def anterior_endereco(self, endereco):
        return (endereco - Consts.CODE_SIZE) % self.code_slice

    def ler_instrucao(self, endereco):
        if endereco + Consts.CODE_SIZE > self.code_slice:
            Consts.running = False
            raise MemoryError("instrucoes devem ser encontradas ate a posicao "
                              "de memoria "+str(self.anterior_endereco(self.code_slice)) + " informado "+str(endereco))

        return At.sub_array(self.memoria, endereco, Consts.CODE_SIZE)

    def escrever_instrucao(self, pos, instrucao):
        if pos + Consts.CODE_SIZE > self.code_slice:
            Consts.running = False
            raise MemoryError("instrucoes devem ser encontradas ate a posicao "
                              "de memoria "+str(self.anterior_endereco(self.code_slice)) + " informado "+str(pos))
        At.append_array(instrucao, self.memoria, pos, Consts.CODE_SIZE)

    def get_instrucao_entrada(self, sinal):
        pos = sinal[Consts.T_DADOS]
        endereco = Consts.get_vetor_conexao(Consts.RAM, Consts.ENTRADA, pos, Consts.T_E_INSTRUCAO)

        self.barramento.enviar_endereco(endereco)
        self.log.write_line('memoria => sinal enviado')

        while self.dado is None:
            # self.log.write_line("memoria =>> esperando dado")
            pass

        self.escrever_instrucao(pos, self.dado[Consts.T_DADOS])

        self.dado = None

        if self.esperando_entrada:
            self.esperando_entrada = False
            self.enviar_endereco_dado_cpu(pos, Consts.T_L_INSTRUCAO)
