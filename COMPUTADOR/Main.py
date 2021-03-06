from COMPUTADOR import Constantes as Consts
from CPU.Cpu import Cpu
from BARRAMENTO.Barramento import Barramento
from MEMORIA.Memoria import Memoria
from ENTRADA.Entrada import Entrada
from ILOGS.Logs import *
from INTERFACES.Interface import Tela


class Computador:

    def __init__(self):
        # perg. o arquivo assembly e as configuracoes ao iniciar
        # importar arquivo no construtor da e/s
        self.criar_componentes()

    @staticmethod
    def criar_componentes():
        # log = ConsoleLog()
        Consts.running = True
        barramento = Barramento(logi=LogSegundo())

        ram = Memoria(barramento, Consts.MEMORIA_X)
        entrada = Entrada(barramento)
        cpu = Cpu(barramento, ram.tamanho)

        Consts.Componentes[Consts.RAM] = ram
        Consts.Componentes[Consts.ENTRADA] = entrada
        Consts.Componentes[Consts.CPU] = cpu

        barramento.start()
        entrada.start()
        ram.start()
        cpu.start()

if __name__ != '__main__':
    print "must be main"

# frame = Tela()
# frame.start()

Computador()

