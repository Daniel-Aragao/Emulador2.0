import unittest
from ENTRADA.Buffer import BufferReader as Buffer
from ENTRADA.Regex import Regex


class MyTestCase(unittest.TestCase):
    defaultPath = r"C:\\Users\danda_000\\Documents\\Estudos, Unifor\\Python\\workspace" \
                  r"\\Arquitetura2.0\\res\\assembly_com_loop.txt"

    def passar_assembly_com_loop__receber_resultado_correto(self):
        lines = Buffer.importar_codigo(MyTestCase.defaultPath)

        codes = Regex.traduzir(lines)

        correto = [
            [6, -1, 4, -1, -1, -1],
            [6, -65, -1, -1, -1, -1],
            [6, -66, 3, -1, -1, -1],
            [5, -65, -66, -1, -1, -1],
            [3, -1, -1, -1, -1, -1],
            [7, -67, -65, -66, -1, -1],
            [4, 18, -1, -1, -1, -1],
            [2, -65, -1, -1, -1, -1],
            [8, -65, 1, -67, 18, 0],
            [6, -2, -65, -1, -1, -1],
            [1, -1, -1, -1, -1, -1]
        ]

        self.assertItemsEqual(correto, codes)


if __name__ == '__main__':
    unittest.main()
