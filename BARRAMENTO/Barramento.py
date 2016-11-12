from COMPUTADOR import Constantes as Consts
import threading
import time
import sys
from ILOGS.Logs import LogNone


class Barramento(threading.Thread):

    def __init__(self, log=LogNone(), logi=LogNone()):
        super(Barramento, self).__init__(name="Barramento")
        self.log = log
        self.logi = logi

        self.sinalLock = threading.Lock()
        self.fila_sinal = []
        self.sinal_bytes = 0

        self.enderecoLock = threading.Lock()
        self.fila_endereco = []
        self.enderecos_bytes = 0

        self.dadosLock = threading.Lock()
        self.fila_dados = []
        self.dados_bytes = 0

    # Estrutura de sinais
    def enviar_sinal(self, sinal):
        self.sinalLock.acquire()

        self.fila_sinal.append(sinal)

        self.sinalLock.release()

    # Estrutura de Enderecos
    def enviar_endereco(self, endereco):
        self.enderecoLock.acquire()

        self.fila_endereco.append(endereco)

        self.enderecoLock.release()

    # Estrutura de dados
    def enviar_dado(self, dado):
        self.dadosLock.acquire()

        self.fila_dados.append(dado)

        self.dadosLock.release()

    def run(self):
        self.log.write_line("Barramento => start")

        lasttime = time.time()
        totaltime = 0
        while Consts.running:
            self.disparar_sinais()

            self.disparar_enderecos()

            self.disparar_dados()

            totaltime += time.time() - lasttime
            if totaltime >= Consts.sleep:
                self.exibir_dados()

                totaltime = 0
                self.sinal_bytes = 0
                self.enderecos_bytes = 0
                self.dados_bytes = 0

            lasttime = time.time()

        self.log.write_line("Barramento => end")

    def exibir_dados(self):
        self.logi.write_line("---------dados-do-segundo-------")
        self.logi.write_line("registradores: " + str(Consts.Componentes[Consts.CPU].registradores))
        mem = Consts.Componentes[Consts.RAM]
        if Consts.MEMORIA_X < 9:
            self.logi.write_line("memoria codigo: " + str(mem.memoria[:mem.code_slice:]))
            self.logi.write_line("memoria valores: " + str(mem.memoria[mem.code_slice+1::]))
        else:
            self.logi.write_line("memoria codigo: " + str(mem.memoria[:mem.code_slice:][:500:]))
            self.logi.write_line("memoria valores: " + str(mem.memoria[mem.code_slice + 1::][:500:]))

        self.logi.write_line("fila_sinal: " + str(self.sinal_bytes))
        self.logi.write_line("fila_enderecos: " + str(self.enderecos_bytes))
        self.logi.write_line("fila_dados: " + str(self.dados_bytes))
        tempo = time.localtime()
        self.logi.write_line("tempo: " + str(tempo.tm_hour) + ":" + str(tempo.tm_min) + ":" + str(tempo.tm_sec))
        self.logi.write_line("--------------------------------")

    def disparar_sinais(self):
        self.sinalLock.acquire()

        length = len(self.fila_sinal)

        if length:
            sinal = self.fila_sinal[0]

            tamanhofinal = (len(sinal) * sys.getsizeof(0)) + sys.getsizeof(sinal) + self.sinal_bytes

            if tamanhofinal <= Consts.larguraBanda:
                self.log.write_line('barramento => disparar sinais')

                destino = sinal[Consts.T_DESTINO]
                Consts.Componentes[destino].receber_sinal(sinal)

                self.sinal_bytes = tamanhofinal
                self.fila_sinal.pop(0)

        self.sinalLock.release()

    def disparar_enderecos(self):
        self.enderecoLock.acquire()

        length = len(self.fila_endereco)

        if length:
            endereco = self.fila_endereco[0]

            tamanhoendereco = (len(endereco) * sys.getsizeof(0)) + sys.getsizeof(endereco) + self.enderecos_bytes

            if tamanhoendereco <= Consts.larguraBanda:
                self.log.write_line('barramento => disparar enderecos')

                destino = endereco[Consts.T_DESTINO]
                Consts.Componentes[destino].receber_endereco(endereco)

                self.enderecos_bytes = tamanhoendereco
                self.fila_endereco.pop(0)

        self.enderecoLock.release()

    def disparar_dados(self):
        self.dadosLock.acquire()

        length = len(self.fila_dados)

        if length:
            dado = self.fila_dados[0]

            tamanhodado = (len(dado) * sys.getsizeof(0)) + sys.getsizeof(dado) + self.dados_bytes
            if tamanhodado <= Consts.larguraBanda:
                self.log.write_line('barramento => disparar dados')

                destino = dado[Consts.T_DESTINO]
                Consts.Componentes[destino].receber_dado(dado)

                self.dados_bytes = tamanhodado
                self.fila_dados.pop(0)

        self.dadosLock.release()
