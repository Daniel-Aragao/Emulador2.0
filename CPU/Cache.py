from COMPUTADOR import Constantes as Consts
from ILOGS.Logs import LogNone
import time
import sys


class CacheCelula:
    def __init__(self, dado):
        self.dado = dado
        self.data = time.time()
        self.vezes_usado = 1


class CacheLRU:

    def __init__(self, tamanho_memoria, atualizar, log=LogNone()):
        self.log = log
        self.tamanho_memoria = tamanho_memoria
        self.atualizar = atualizar

        if Consts.CACHE_TAX > Consts.CACHE_TAX_MAX:
            Consts.CACHE_TAX = Consts.MEMORIA_X_MAX
            log.write_line('taxa maxima do cache excedida, tamanho maximo escolhido')
        elif Consts.CACHE_TAX < Consts.CACHE_TAX_MIN:
            Consts.CACHE_TAX = Consts.CACHE_TAX_MIN
            log.write_line('taxa minima do cache excedida, tamanho minimo escolhido')

        self.tamanho = int(Consts.CACHE_TAX * tamanho_memoria)
        self.cache_dict = {}
        self.in_dict = 0
        self.hit = 0
        self.miss = 0

    def get(self, pos):
        if pos in self.cache_dict:
            self.inc_hit(pos)
            return self.cache_dict[pos].dado
        else:
            self.inc_miss()
            return None

    def update(self, pos, dado):
        if pos not in self.cache_dict:
            raise MemoryError("Pos de memoria nao esta em cache")

        self.cache_dict[pos].dado = dado
        self.cache_dict[pos].vezes_usado += 1
        self.inc_hit(pos)

    def add(self, pos, dado):
        if pos in self.cache_dict:
            self.update(pos, dado)
        else:
            self.inc_miss()
            if self.cabe(dado):
                self.cache_dict[pos] = CacheCelula(dado)
                self.in_dict += get_data_size(dado)
            else:
                if get_data_size(dado) <= self.tamanho:
                    removido = None
                    for key, value in self.cache_dict.iteritems():
                        if removido is None or value.data < self.cache_dict[removido].data:
                            removido = key

                    self.remover(removido)

                    self.cache_dict[pos] = CacheCelula(dado)
                    self.in_dict += get_data_size(dado)
                else:
                    self.atualizar(pos, dado)
                    return

        if self.cache_dict[pos].vezes_usado >= Consts.LIMITE_DE_ATUALIZACOES:
            self.cache_dict[pos].vezes_usado = 0
            self.atualizar_na_memoria(pos)

    def inc_hit(self, pos):
        self.hit += 1
        self.cache_dict[pos].data = time.time()

    def inc_miss(self):
        self.miss += 1

    def percemhit(self):
        return int((self.hit / (self.hit + self.miss + 0.0))*100)

    def remover(self, pos):
        self.atualizar_na_memoria(pos)
        self.in_dict -= get_data_size(self.cache_dict.pop(pos))

    def cabe(self, dado):
        return (self.in_dict + get_data_size(dado)) <= self.tamanho

    def atualizar_na_memoria(self, pos):
        self.atualizar(pos, self.cache_dict[pos].dado)

    def atualizar_todos(self):
        for key, values in self.cache_dict.iteritems():
            self.atualizar_na_memoria(key)


class CacheLFU:

    def __init__(self, tamanho_memoria, atualizar, log=LogNone()):
        self.log = log
        self.tamanho_memoria = tamanho_memoria
        self.atualizar = atualizar

        if Consts.CACHE_TAX > Consts.CACHE_TAX_MAX:
            Consts.CACHE_TAX = Consts.MEMORIA_X_MAX
            log.write_line('taxa maxima do cache excedida, tamanho maximo escolhido')
        elif Consts.CACHE_TAX < Consts.CACHE_TAX_MIN:
            Consts.CACHE_TAX = Consts.CACHE_TAX_MIN
            log.write_line('taxa minima do cache excedida, tamanho minimo escolhido')

        self.tamanho = int(Consts.CACHE_TAX * tamanho_memoria)
        self.cache_dict = {}
        self.in_dict = 0
        self.hit = 0
        self.miss = 0

    def get(self, pos):
        if pos in self.cache_dict:
            self.inc_hit(pos)
            return self.cache_dict[pos].dado
        else:
            self.inc_miss()
            return None

    def update(self, pos, dado):
        if pos not in self.cache_dict:
            raise MemoryError("Pos de memoria nao esta em cache")

        self.cache_dict[pos].dado = dado
        self.inc_hit(pos)

    def add(self, pos, dado):
        if pos in self.cache_dict:
            self.update(pos, dado)
        else:
            self.inc_miss()
            if self.cabe(dado):
                self.cache_dict[pos] = CacheCelula(dado)
                self.in_dict += get_data_size(dado)
            else:
                if get_data_size(dado) <= self.tamanho:
                    removido = None
                    for key, value in self.cache_dict.iteritems():
                        if removido is None or value.vezes_usado <= self.cache_dict[removido].vezes_usado:
                            if removido is not None and value.vezes_usado == self.cache_dict[removido].vezes_usado:
                                if value.data < self.cache_dict[removido].data:
                                    removido = key
                            else:
                                removido = key

                    self.remover(removido)

                    self.cache_dict[pos] = CacheCelula(dado)
                    self.in_dict += get_data_size(dado)
                else:
                    self.atualizar(pos, dado)
                    return

        if self.cache_dict[pos].vezes_usado % Consts.LIMITE_DE_ATUALIZACOES == 0:
            self.atualizar_na_memoria(pos)

    def inc_hit(self, pos):
        self.hit += 1
        self.cache_dict[pos].vezes_usado += 1

    def inc_miss(self):
        self.miss += 1

    def percemhit(self):
        return int((self.hit / (self.hit + self.miss + 0.0))*100)

    def remover(self, pos):
        self.atualizar_na_memoria(pos)
        self.in_dict -= get_data_size(self.cache_dict.pop(pos))

    def cabe(self, dado):
        return (self.in_dict + get_data_size(dado)) <= self.tamanho

    def atualizar_na_memoria(self, pos):
        self.atualizar(pos, self.cache_dict[pos].dado)

    def atualizar_todos(self):
        for key, values in self.cache_dict.iteritems():
            self.atualizar_na_memoria(key)


def get_data_size(dado):
    if isinstance(dado, type([])):
        return (len(dado) * sys.getsizeof(dado[0])) + sys.getsizeof(dado)

    return sys.getsizeof(dado)
