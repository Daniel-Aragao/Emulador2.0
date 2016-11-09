import threading
from COMPUTADOR import Constantes as Consts
from Queue import Queue
from ENTRADA.Buffer import BufferReader
from ILOGS.Logs import LogNone


class Entrada(threading.Thread):
    # defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace\\Arquitetura2.0\\res\\file_sample.txt"
    defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
                  r"\\Arquitetura2.0\\res\\assembly_com_loop.txt"
    # defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
    #               r"\\Arquitetura2.0\\res\\inc_end.txt"

    def __init__(self, barramento, path=defaultPath, log=LogNone()):
        super(Entrada, self).__init__(name="Entrada")
        self.log = log

        self.barramento = barramento
        self.bufferReader = BufferReader(path)
        self.sinais = Queue()
        self.endereco = None

    def run(self):
        self.log.write_line("Entrada start")
        while Consts.running:
            if not self.sinais.empty():
                self.log.write_line('entrada => receber sinal')
                self.processar_sinal(self.sinais.get(timeout=Consts.timeout))

        self.log.write_line("Entrada end")

    def receber_sinal(self, sinal):
        self.sinais.put(sinal, timeout=Consts.timeout)

    def receber_endereco(self, endereco):
        self.endereco = endereco

    def processar_sinal(self, sinal):

        if sinal[Consts.T_ORIGEM] == Consts.CPU and sinal[Consts.T_TIPO] == Consts.T_L_INSTRUCAO:
            code = self.bufferReader.get_line().byte_array

            # enviar pra memoria
            sinal = Consts.get_vetor_conexao(Consts.ENTRADA, Consts.RAM, sinal[Consts.T_DADOS], Consts.T_E_INSTRUCAO)
            self.barramento.enviar_sinal(sinal)
            self.log.write_line('entrada => sinal enviado')

            # esperar confirmacao da memoria
            while not self.endereco:
                # self.log.write_line("entrada => esperando endereco")
                pass
            self.endereco = None

            dado = Consts.get_vetor_conexao(Consts.ENTRADA, Consts.RAM, code, None)
            self.barramento.enviar_dado(dado)
        else:
            raise Exception("sinal invalido")


        #eriko: a cpu vai enviar pra entrada o pedido de codigo e a entrada enviara para memoria q enviara pra cpu
        #o endereco com os dados