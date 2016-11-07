import threading
from COMPUTADOR import Constantes as Consts
from Queue import Queue
from ENTRADA.Buffer import BufferReader
from ENTRADA.Code import Code


class Entrada(threading.Thread):
    # defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace\\Arquitetura2.0\\res\\file_sample.txt"
    defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
                  r"\\Arquitetura2.0\\res\\assembly_com_loop.txt"

    def __init__(self, barramento, path=defaultPath):
        super(Entrada, self).__init__()
        self.barramento = barramento
        self.bufferReader = BufferReader(path)
        self.sinais = Queue()

    def run(self):
        while Consts.running:
            if not self.sinais.empty():
                self.processar_sinal(self.sinais.get(timeout=Consts.timeout))

    def receber_sinal(self, sinal):
        self.sinais.put(sinal, timeout=Consts.timeout)

    def processar_sinal(self, sinal):

        if sinal[Consts.T_ORIGEM] == Consts.RAM and sinal[Consts.T_TIPO] == Consts.T_L_INSTRUCAO:
            code = self.bufferReader.get_line().byte_array

        # enviar pro barramento => memoria
