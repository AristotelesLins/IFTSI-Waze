import random
import constantes

class GerenciadorEventos:
    def __init__(self, mapa):
        self.mapa = mapa
        self.ultima_notificacao_evento = ""

    def simular_eventos_aleatorios(self):
        novas_notificacoes = []
        num_eventos_a_tentar = (self.mapa.num_linhas * self.mapa.num_colunas) // 10

        for _ in range(num_eventos_a_tentar):
            linha_aleatoria = random.randint(0, self.mapa.num_linhas - 1)
            coluna_aleatoria = random.randint(0, self.mapa.num_colunas - 1)
            celula = self.mapa.obter_celula(linha_aleatoria, coluna_aleatoria)

            if celula and (celula._tipo_base == constantes.TIPO_RUA or \
                          celula._tipo_base == constantes.TIPO_PARTIDA or \
                          celula._tipo_base == constantes.TIPO_CHEGADA):

                chance = random.random()

                if celula._tipo_trafego_evento != constantes.TIPO_RUA_LIVRE and chance < 0.5:
                    celula.definir_tipo_trafego_evento(constantes.TIPO_RUA_LIVRE)
                elif chance < 0.015 and celula._tipo_trafego_evento != constantes.TIPO_RUA_ACIDENTE :
                    celula.definir_tipo_trafego_evento(constantes.TIPO_RUA_ACIDENTE)
                    novas_notificacoes.append(f"ACIDENTE em L{linha_aleatoria},C{coluna_aleatoria}!")
                elif chance < 0.12:
                    celula.definir_tipo_trafego_evento(constantes.TIPO_RUA_ENGARRAFAMENTO_PESADO)
                elif chance < 0.25:
                    celula.definir_tipo_trafego_evento(constantes.TIPO_RUA_ENGARRAFAMENTO_MODERADO)
                elif chance < 0.35:
                    celula.definir_tipo_trafego_evento(constantes.TIPO_RUA_ENGARRAFAMENTO_LEVE)
        
        if novas_notificacoes:
            self.ultima_notificacao_evento = random.choice(novas_notificacoes)
        elif not self.ultima_notificacao_evento.startswith("Rota:") and \
             not self.ultima_notificacao_evento.startswith("Nenhuma rota") and \
             not self.ultima_notificacao_evento.startswith("Saiu da rota"):
            self.ultima_notificacao_evento = ""

    def obter_ultima_notificacao_evento(self):
        return self.ultima_notificacao_evento

    def definir_notificacao_caminho(self, msg):
        self.ultima_notificacao_evento = msg