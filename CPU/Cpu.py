from COMPUTADOR import Constantes as Consts
import threading
from ILOGS.Logs import LogNone


class Cpu(threading.Thread):
    PASSO_SINAL = 0
    PASSO_ENDERECO_DADO = 1
    PASSO_PROCESSAMENTO = 2

    def __init__(self, barramento, log=LogNone()):
        super(Cpu, self).__init__(name="Cpu")
        self.log = log

        self.registradores = {"A": 0, "B": 0, "C": 0, "D": 0, "CI": 0}
        self.barramento = barramento
        self.passo = Cpu.PASSO_SINAL
        self.tipoSinal = Consts.T_L_INSTRUCAO
        self.endereco = None
        self.dado = None
        self.loops = []

    """
    PASSO_SINAL
    enviar sinal com origem, destino, valor de ci e o tipo de leitura
    apos enviar o passo vira de endereco_dado

    PASSO_ENDERECO_DADO
    ESPERAR endereco(nova ci) e dado(a ser processado)
    quando os dois forem recebidos o passo vira de processamento

    PASSO_PROCESSAMENTO
    se o dado for o fim do codigo running vira false e dar um continue
    se a lista de loops NAO for vazia
        se a instrucao nao eh fim de loop
            se ci igual ao inicio do primeiro loop
                raise out of memory
        se nao
            se eh fim do ultimo loop
                ultimo = retiro o ultimo loop
                testo a condicao do loop
                se a condicao eh verdadeira
                    ci recebe ultimo.linha
                    tipo de leitura eh releitura( nao pega do disco na releitura)
                se nao
                    tipo de leitura eh leitura
            se nao
                raise exception

    processar dado
    se o dado eh uma label
        armazenar label no vetor de loops juntamente do endereco desse label

    enviar sinal novamente
    """

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

        self.log.write_line("Cpu => end")

    def enviar_sinal(self):
        if self.registradores["CI"] != -1:
            sinalram = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, self.registradores["CI"],
                                                self.tipoSinal)
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
            self.registradores["CI"] = self.endereco[Consts.T_DADOS]
            self.passo = Cpu.PASSO_PROCESSAMENTO

    def passo_processamento(self):
        """
        se o dado for o fim do codigo running vira false e dar um continue
        se a lista de loops NAO for vazia
            se a instrucao nao eh fim de loop
                se ci igual ao inicio do primeiro loop
                    raise out of memory


        processar dado
        no processamento caso seja fim de loop:
            ultimo = pego o ultimo loop sem retirar
            testo a condicao do loop
            se a condicao eh verdadeira
                ci recebe ultimo.linha
                tipo de leitura eh releitura( nao pega do disco na releitura)
            se nao
                tipo de leitura eh leitura
        """
        instrucao = self.dado[Consts.T_DADOS]
        if len(self.loops):
            if self.registradores["CI"] == self.loops[0].posmem:
                raise MemoryError("memoria insuficiente")

        self.processar(instrucao)
        # fim do metodo
        self.dado = None
        self.endereco = None
        self.passo = Cpu.PASSO_SINAL
        self.log.write_line('cpu => processado')

    def processar(self, instrucao):
        if instrucao[0] == Consts.INSTRUCOES["end"].codigo:
            Consts.running = False
            self.registradores["CI"] = -1
        elif instrucao[0] == Consts.INSTRUCOES["inc"].codigo:
            val = instrucao[1]
            if self.is_registrador(val):
                self.registradores[chr(int(-val))] += 1
            elif self.is_pos_memoria(val):
                valor = self.get_valor(val)
                self.enviar_valor_memoria(-val, valor + 1)
            else:
                raise ValueError(val + " precisa ser posicao de memoria ou um registrador para a operacao 'inc'")

        elif instrucao[0] == Consts.INSTRUCOES["dec"].codigo:
            val = instrucao[1]
            if self.is_registrador(val):
                self.registradores[chr(int(-val))] -= 1
            elif self.is_pos_memoria(val):
                valor = self.get_valor(val)
                self.enviar_valor_memoria(-val, valor - 1)
            else:
                raise ValueError(val + " precisa ser posicao de memoria ou um registrador para a operacao 'dec'")

        elif instrucao[0] == Consts.INSTRUCOES["add"].codigo:
            val = self.get_valor(instrucao[1]) + self.get_valor(instrucao[2])
            if self.is_registrador(instrucao[1]):
                self.registradores[chr(int(-instrucao[1]))] = val
            elif self.is_pos_memoria(instrucao[1]):
                self.enviar_valor_memoria(-instrucao[1], val)

        elif instrucao[0] == Consts.INSTRUCOES["mov"].codigo:
            val = self.get_valor(instrucao[2])
            if self.is_registrador(instrucao[1]):
                self.registradores[chr(int(-instrucao[1]))] = val
            elif self.is_pos_memoria(instrucao[1]):
                self.enviar_valor_memoria(-instrucao[1], val)

        elif instrucao[0] == Consts.INSTRUCOES["imul"].codigo:
            val = self.get_valor(instrucao[3]) * self.get_valor(instrucao[2])
            if self.is_registrador(instrucao[1]):
                self.registradores[chr(int(-instrucao[1]))] = val
            elif self.is_pos_memoria(instrucao[1]):
                self.enviar_valor_memoria(-instrucao[1], val)

        elif instrucao[0] == Consts.INSTRUCOES["label"].codigo:
            if not self.existe_label(instrucao[1]):
                self.loops.append(Loop(self.registradores["CI"], instrucao[1]))
            else:
                raise Exception("a label " + instrucao[1] + " ja existe")

        elif instrucao[0] == Consts.INSTRUCOES["condicao"].codigo:
            val1 = self.get_valor(instrucao[1])
            val2 = self.get_valor(instrucao[3])

            condicao = eval(str(val1) + Consts.get_condicao_string(instrucao[2]) + str(val2))

            if condicao:
                self.go_to_loop(instrucao[4])
            else:
                self.go_to_loop(instrucao[5])
        else:
            raise Exception("instrucao invalida codigo:"+str(instrucao[0]))

        self.log.write_line(str(self.registradores))

    def go_to_loop(self, label):
        if label:
            loop = self.get_loop(label)
            if loop is None:
                raise Exception("label nao encontrada")
            else:
                self.registradores["CI"] = loop.posmem
                self.tipoSinal = Consts.T_RL_INSTRUCAO
                # se sair do loop interno ele saira do externo tbm se tiver soh esse controle, para consertar
                # sugiro colocar mais um atributo ao objeto loop que controlaria se esta ou n nesse label e ao
                # passar pela possibilidade de chamar a label remover de la o atributo sendo que se entrar
                # novamente colocaria o atributo de novo
                # outra sugestao eh guardar a ci mais antiga ja visitada, resposta provavelmente insoluvel
        else:
            self.tipoSinal = Consts.T_L_INSTRUCAO

    def existe_label(self, label):
        for i in self.loops:
            if i.codigo == label:
                return True
        return False

    def get_loop(self, label):
        for i in self.loops:
            if i.codigo == label:
                return i
        return None

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
        self.dado = None
        sinal = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, -dado, Consts.T_L_VALOR)
        self.barramento.enviar_sinal(sinal)

        while self.dado is None:
            # self.log.write_line("cpu => esperando dado")
            pass

        return self.dado[Consts.T_DADOS]

    def enviar_valor_memoria(self, pos, valor):
        sinal = Consts.get_vetor_conexao(Consts.CPU, Consts.RAM, pos, Consts.T_E_VALOR, len=Consts.T_EVLENGTH)
        sinal[Consts.T_EVALOR_POS] = valor
        self.barramento.enviar_sinal(sinal)


class Loop:

    def __init__(self, posmem, codigo):
        self.posmem = posmem
        self.codigo = codigo
