from ENTRADA.Regex import Regex


class BufferReader:

    def __init__(self, path):
        self.lines = BufferReader.importar_codigo(path)
        self.codes = []
        self.lines_to_code(self.lines)

    @staticmethod
    def importar_codigo(path):
        f = open(path, 'r')
        return f.read().splitlines()

    def lines_to_code(self, lines):
        for line in lines:
            self.codes.append(Regex.traduzir(line))

    def get_line(self):
        return self.codes.pop(0)

    def empty(self):
        return not len(self.codes)
