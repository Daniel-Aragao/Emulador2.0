from COMPUTADOR import Constantes as Consts
from ILOGS.Logs import LogNone
import time
import sys
import threading


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
            self.cache_dict[pos].vezes_usado = 1
            self.atualizar_na_memoria(pos)

    def inc_hit(self, pos):
        self.hit += 1
        self.cache_dict[pos].data = time.time()
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


class CacheCoolDown:

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
        self.cooldown = Consts.CACHE_COOLDOWN

        self.dict_lock = threading.Lock()
        self.cooldown_thread = threading.Thread(target=self.checar_cooldown, name="Cooldown")
        self.cooldown_thread.start()

    def get(self, pos):
        self.dict_lock.acquire()

        if pos in self.cache_dict:
            self.inc_hit(pos)
            self.dict_lock.release()
            return self.cache_dict[pos].dado
        else:
            self.inc_miss()
            self.dict_lock.release()
            return None

    def update(self, pos, dado):
        if pos not in self.cache_dict:
            raise MemoryError("Pos de memoria nao esta em cache")

        self.in_dict -= get_data_size(self.cache_dict[pos].dado)
        self.cache_dict[pos].dado = dado
        self.in_dict += get_data_size(dado)
        self.inc_hit(pos)

    def add(self, pos, dado):
        self.dict_lock.acquire()

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
                        if removido is None or value.data <= self.cache_dict[removido].data:
                            if removido is not None and value.data == self.cache_dict[removido].data:
                                if value.vezes_usado < self.cache_dict[removido].vezes_usado:
                                    removido = key
                            else:
                                removido = key

                    self.remover(removido)

                    self.cache_dict[pos] = CacheCelula(dado)
                    self.in_dict += get_data_size(dado)
                else:
                    self.atualizar(pos, dado)

                    self.dict_lock.release()
                    return

        if self.cache_dict[pos].vezes_usado % Consts.LIMITE_DE_ATUALIZACOES == 0:
            self.atualizar_na_memoria(pos)

        self.dict_lock.release()

    def inc_hit(self, pos):
        self.hit += 1
        self.cache_dict[pos].vezes_usado += 1
        self.cache_dict[pos].data = time.time()

    def inc_miss(self):
        self.miss += 1

    def percemhit(self):
        return int((self.hit / (self.hit + self.miss + 0.0))*100)

    def remover(self, pos):
        self.atualizar_na_memoria(pos)
        removido = self.cache_dict.pop(pos)
        tamanho_removido = get_data_size(removido)
        self.in_dict -= tamanho_removido
        if self.in_dict < 0:
            # Consts.running = False
            # raise Warning('tamanho do cache n pode ser negativo')
            pass

    def cabe(self, dado):
        return (self.in_dict + get_data_size(dado)) <= self.tamanho

    def atualizar_na_memoria(self, pos):
        self.atualizar(pos, self.cache_dict[pos].dado)

    def atualizar_todos(self):
        self.dict_lock.acquire()

        for key, values in self.cache_dict.iteritems():
            self.atualizar_na_memoria(key)

        self.dict_lock.release()

    def checar_cooldown(self):
        while Consts.running:
            remove = []

            self.dict_lock.acquire()

            tempoatual = time.time()
            for key, value in self.cache_dict.iteritems():
                if (value.data + Consts.CACHE_COOLDOWN) < tempoatual:
                    remove.append(key)

            while len(remove):
                self.remover(remove.pop())

            self.dict_lock.release()


def get_data_size(dado):
    return sys.getsizeof(dado)
