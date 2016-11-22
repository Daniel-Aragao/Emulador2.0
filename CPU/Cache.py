from COMPUTADOR import Constantes as Consts


class CacheLRU:

    def __init__(self, tamanho_memoria):
        self.tamanho_memoria = tamanho_memoria
        self.tamanho = Consts.CACHE_TAX * tamanho_memoria
