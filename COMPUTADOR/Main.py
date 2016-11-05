from COMPUTADOR import Constantes as Consts
from CPU.Cpu import Cpu
from BARRAMENTO.Barramento import Barramento


class Computador:

    def __init__(self):
        # perg. o arquivo assembly e as configuracoes ao iniciar
        # importar arquivo no construtor da e/s
        self.criar_componentes()

    @staticmethod
    def criar_componentes():
        barramento = Barramento()
        Consts.running = True

        ram = Ram(barramento)
        entrada = Entrada(barramento)
        cpu = Cpu(barramento)

        Consts.Componentes[Consts.RAM] = ram
        Consts.Componentes[Consts.ENTRADA] = entrada
        Consts.Componentes[Consts.CPU] = cpu

        entrada.start()
        ram.start()
        Cpu.start()

if __name__ == '__main__':
    Computador()
