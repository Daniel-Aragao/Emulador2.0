from COMPUTADOR import Constantes as Consts
import threading
from ILOGS.Logs import LogNone
from Cache import CacheLRU
from Cache import CacheLFU


class Cpu(threading.Thread):
    # onde for get, valor ou endereco, deve ser verificado antes na cache qual a posicao
    # a ser pesquisada, pois a mesma pode estar salva na cache
    # toda vez q algo vier da memoria deve ser salvo em cache, instrucoes, pos de memoria
    # objeto representara uma celula do cache
    PASSO_SINAL = 0
    PASSO_ENDERECO_DADO = 1
    PASSO_PROCESSAMENTO = 2

    def __init__(self, barramento, tamanho_ram, log=LogNone()):
        super(Cpu, self).__init__(name="Cpu")
        self.log = log

        self.registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "CI": 0}
        self.barramento = barramento
        self.passo = Cpu.PASSO_SINAL
        self.tipoSinal = Consts.T_L_INSTRUCAO
        self.endereco = None
        self.dado = None
        self.loops = []
        # self.cache = CacheLRU(tamanho_ram, self.atualizar)
        self.cache = CacheLFU(tamanho_ram, self.atualizar)
        # self.cache = CacheCoolDown(tamanho_ram, self.atualizar)

    def run(self):
        self.log.write_line("Cpu => start")
        while Consts.running:
            if self.passo == Cpu.PASSO_SINAL:
                self.enviar_sinal()
                # self.log.write_line('cpu => enviar_sinal')

            elif self.passo == Cpu.PASSO_ENDERECO_DADO:
                self.esperar_informacao()
                # self.log.write_line('cpu => receber endereco e dado')

            elif self.passo == Cpu.PASSO_PROCESSAMENTO:
                self.passo_processamento()
                # self.log.write_line('cpu => processar instrucao')
        self.cache.atualizar_todos()
        self.log.write_line("Cpu => end")

    def enviar_sinal(self):
        if self.registradores["CI"] != -1:
            sinalram = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, self.registradores["CI"],
                                                self.tipoSinal)

            # neste ponto vai buscar no cache, caso nao tenha, vai buscar na memoria( continua o processo normal)
            cacheresult = self.cache.get(self.registradores["CI"])

            if cacheresult is not None:
                # cacheresult sera uma tupla com proximo ci[0] e a informacao guardada[1]
                self.registradores["CI"] = cacheresult[0]
                self.dado = cacheresult[1]
                self.passo = Cpu.PASSO_PROCESSAMENTO
            else:
                self.barramento.enviar_sinal(sinalram)

                if self.tipoSinal == Consts.T_L_INSTRUCAO:
                    sinalentrada = Consts.get_vetor_conexao(Consts.CPU, Consts.ENTRADA, self.registradores["CI"],
                                                            self.tipoSinal)
                    self.barramento.enviar_sinal(sinalentrada)

                self.passo = Cpu.PASSO_ENDERECO_DADO
                self.log.write_line('cpu => sinal enviado')

    def receber_endereco(self, endereco):
        self.endereco = endereco

    def receber_dado(self, dado):
        self.dado = dado

    def esperar_informacao(self):
        if (self.dado is not None) and (self.endereco is not None):
            self.log.write_line('cpu => endereco e dado recebidos')
            endereco_anterior = self.registradores["CI"]
            self.registradores["CI"] = self.endereco[Consts.T_DADOS]
            self.passo = Cpu.PASSO_PROCESSAMENTO

            # quando a informacao chegar ela deve ser colocada na cache
            self.cache.add(endereco_anterior, (self.registradores["CI"], self.dado))

    def passo_processamento(self):
        instrucao = self.dado[Consts.T_DADOS]
        if len(self.loops):
            if self.registradores["CI"] == self.loops[0].posmem:
                Consts.running = False
                raise MemoryError("memoria insuficiente")

        self.processar(instrucao)
        # fim do metodo
        self.dado = None
        self.endereco = None
        self.passo = Cpu.PASSO_SINAL
        self.log.write_line('cpu => processado')

    def processar(self, instrucao):
        if instrucao[0] == Consts.INSTRUCOES["end"].codigo:
            self.cache.atualizar_todos()
            Consts.running = False
            self.registradores["CI"] = -1
            self.barramento.exibir_dados()
        elif instrucao[0] == Consts.INSTRUCOES["inc"].codigo:
            val = instrucao[1]
            if self.is_registrador(val):
                self.registradores[chr(int(-val))] += 1
            elif self.is_pos_memoria(val):
                valor = self.get_valor(val)
                self.enviar_valor_memoria(val, valor + 1)
            else:
                Consts.running = False
                raise ValueError(val + " precisa ser posicao de memoria ou um registrador para a operacao 'inc'")

        elif instrucao[0] == Consts.INSTRUCOES["dec"].codigo:
            val = instrucao[1]
            if self.is_registrador(val):
                self.registradores[chr(int(-val))] -= 1
            elif self.is_pos_memoria(val):
                valor = self.get_valor(val)
                self.enviar_valor_memoria(val, valor - 1)
            else:
                Consts.running = False
                raise ValueError(val + " precisa ser posicao de memoria ou um registrador para a operacao 'dec'")

        elif instrucao[0] == Consts.INSTRUCOES["add"].codigo:
            val = self.get_valor(instrucao[1]) + self.get_valor(instrucao[2])
            if self.is_registrador(instrucao[1]):
                self.registradores[chr(int(-instrucao[1]))] = val
            elif self.is_pos_memoria(instrucao[1]):
                self.enviar_valor_memoria(instrucao[1], val)

        elif instrucao[0] == Consts.INSTRUCOES["mov"].codigo:
            pointer = bool(instrucao[1])
            val = self.get_valor(instrucao[3])
            if not pointer and self.is_registrador(instrucao[2]):
                self.registradores[chr(int(-instrucao[2]))] = val
            elif pointer or self.is_pos_memoria(instrucao[2]):
                if pointer:
                    if not self.is_registrador(instrucao[2]):
                        Consts.running = False
                        raise SyntaxError("Ponteiros devem ser acompanhados de um registrador")

                    self.enviar_valor_memoria(-self.registradores[chr(int(-instrucao[2]))], val)
                else:
                    self.enviar_valor_memoria(instrucao[2], val)

        elif instrucao[0] == Consts.INSTRUCOES["imul"].codigo:
            val = self.get_valor(instrucao[3]) * self.get_valor(instrucao[2])
            if self.is_registrador(instrucao[1]):
                self.registradores[chr(int(-instrucao[1]))] = val
            elif self.is_pos_memoria(instrucao[1]):
                self.enviar_valor_memoria(instrucao[1], val)

        elif instrucao[0] == Consts.INSTRUCOES["label"].codigo:
            if not self.existe_label(instrucao[1]):
                self.loops.append(Loop(self.registradores["CI"], instrucao[1]))
            else:
                Consts.running = False
                raise Exception("a label " + str(instrucao[1]) + " ja existe")

        elif instrucao[0] == Consts.INSTRUCOES["condicao"].codigo:
            val1 = self.get_valor(instrucao[1])
            val2 = self.get_valor(instrucao[3])

            condicao = eval(str(val1) + Consts.get_condicao_string(instrucao[2]) + str(val2))

            if condicao:
                self.go_to_loop(instrucao[4])
            else:
                self.go_to_loop(instrucao[5])
        else:
            Consts.running = False
            raise Exception("instrucao invalida codigo:"+str(instrucao[0]))

        self.log.write_line(str(self.registradores))

    def go_to_loop(self, label):
        if label:
            loop = self.get_loop(label)
            # talvez se remover todos os loops apos esse da lista evite problemas com labels seguintes
            if loop is None:
                Consts.running = False
                raise SyntaxError("label " + str(label) + " nao encontrada")
            else:
                self.registradores["CI"] = loop.posmem
                self.tipoSinal = Consts.T_RL_INSTRUCAO
        else:
            self.clean_loops()
            self.tipoSinal = Consts.T_L_INSTRUCAO

    def clean_loops(self):
        self.loops = []

    def existe_label(self, label):
        for i in self.loops:
            if i.codigo == label:
                return True
        return False

    def remove_loop(self, label):
        for i in self.loops:
            if i.codigo == label:
                label = i
                break
        self.loops.pop(label)

    def get_loop(self, label):
        loop = None
        for i in self.loops:
            if i.codigo == label:
                loop = i

        if loop is not None:
            index = self.loops.index(loop)
            self.loops = self.loops[:index+1:]

        return loop

    @staticmethod
    def is_registrador(valor):
        return type(valor) is float and valor < 0

    @staticmethod
    def is_pos_memoria(valor):
        return type(valor) is not float and valor < 0

    def get_valor(self, dado):
        # apenas um valor
        if dado >= 0:
            return dado

        # um registrador
        if self.is_registrador(dado):
            return self.registradores[chr(int(-dado))]

        # uma posicao de memoria
        return self.get_valor_da_memoria(dado)

    def get_valor_da_memoria(self, dado):
        # verificar cache antes
        cacheresult = self.cache.get(dado)
        self.dado = None
        if cacheresult is not None:
            return cacheresult
        else:
            sinal = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, -dado, Consts.T_L_VALOR)
            self.barramento.enviar_sinal(sinal)
            while self.dado is None:
                # self.log.write_line("cpu => esperando dado")
                pass
            self.cache.add(dado, self.dado[Consts.T_DADOS])
            return self.dado[Consts.T_DADOS]

    def enviar_valor_memoria(self, pos, valor):
        # enviar ao cache
        self.cache.add(pos, valor)

    def atualizar(self, pos, valor):
        if not isinstance(valor, type(())):
            sinal = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, -pos, Consts.T_E_VALOR, len=Consts.T_EVLENGTH)
            sinal[Consts.T_EVALOR_POS] = valor
            self.barramento.enviar_sinal(sinal)
            # raise NotImplementedError("Eeeeita")


class Loop:

    def __init__(self, posmem, codigo):
        self.posmem = posmem
        self.codigo = codigo
