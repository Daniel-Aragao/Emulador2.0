from COMPUTADOR import Constantes as Consts
import threading
import time


class Barramento(threading.Thread):

    def __init__(self):
        super(Barramento, self).__init__()
        self.sinalLock = threading.Lock()
        self.fila_sinal = []

        self.enderecoLock = threading.Lock()
        self.fila_endereco = []

        self.dadosLock = threading.Lock()
        self.fila_dados = []

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
        while Consts.running:
            self.disparar_sinais()
            self.disparar_enderecos()
            self.disparar_dados()
            # dados novos estao esperando 1 seg para serem lancados, corrigir!
            time.sleep(Consts.sleep)

    def disparar_sinais(self):
        self.sinalLock.acquire()
        enviado = 0

        for sinal in self.fila_sinal:
            tamanhosinal = len(sinal)
            if enviado + tamanhosinal > Consts.larguraBanda:
                break
            enviado += tamanhosinal

            destino = sinal[Consts.T_DESTINO]
            Consts.Componentes[destino].receber_sinal(sinal)

        self.sinalLock.release()

    def disparar_enderecos(self):
        self.enderecoLock.acquire()

        enviado = 0

        for endereco in self.fila_endereco:
            tamanhoendereco = len(endereco)
            if enviado + tamanhoendereco > Consts.larguraBanda:
                break
            enviado += tamanhoendereco

            destino = endereco[Consts.T_DESTINO]
            Consts.Componentes[destino].receber_endereco(endereco)

        self.enderecoLock.release()

    def disparar_dados(self):
        self.dadosLock.acquire()

        enviado = 0

        for dado in self.fila_dados:
            tamanhodado = len(dado)
            if enviado + tamanhodado > Consts.larguraBanda:
                break
            enviado += tamanhodado

            destino = dado[Consts.T_DESTINO]
            Consts.Componentes[destino].receber_dado(dado)

        self.dadosLock.release()
