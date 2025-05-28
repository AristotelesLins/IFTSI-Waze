import pygame
import constantes

class Celula:
    def __init__(self, linha, coluna):
        self.linha = linha
        self.coluna = coluna
        self._tipo_base = constantes.TIPO_RUA
        self._tipo_trafego_evento = constantes.TIPO_RUA_LIVRE

        self.faz_parte_caminho_sugerido = False
        self.cor_caminho_sugerido = None

        self.cor = self._determinar_cor()
        self.custo_movimento = self._determinar_custo_movimento()

        self.g_custo = float('inf')
        self.h_custo = float('inf')
        self.f_custo = float('inf')
        self.pai = None
        self.vizinhos = []

    def _determinar_cor(self):
        if self.faz_parte_caminho_sugerido and self.cor_caminho_sugerido:
            return self.cor_caminho_sugerido

        if self._tipo_base == constantes.TIPO_CONSTRUCAO:
            return constantes.COR_CONSTRUCAO
        elif self._tipo_base == constantes.TIPO_PARTIDA:
            return constantes.COR_PARTIDA
        elif self._tipo_base == constantes.TIPO_CHEGADA:
            return constantes.COR_CHEGADA
        else:
            if self._tipo_trafego_evento == constantes.TIPO_RUA_ACIDENTE:
                return constantes.COR_ACIDENTE_VISUAL
            return constantes.COR_RUA

    def _determinar_custo_movimento(self):
        if self._tipo_base == constantes.TIPO_CONSTRUCAO:
            return float('inf')
        
        if self._tipo_trafego_evento == constantes.TIPO_RUA_LIVRE:
            return constantes.CUSTO_LIVRE
        elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_LEVE:
            return constantes.CUSTO_ENG_LEVE
        elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_MODERADO:
            return constantes.CUSTO_ENG_MODERADO
        elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_PESADO:
            return constantes.CUSTO_ENG_PESADO
        elif self._tipo_trafego_evento == constantes.TIPO_RUA_ACIDENTE:
            return constantes.CUSTO_ACIDENTE
        return constantes.CUSTO_LIVRE

    def desenhar(self, tela):
        x_pixel = self.coluna * constantes.TAMANHO_CELULA
        y_pixel = self.linha * constantes.TAMANHO_CELULA
        rect = pygame.Rect(x_pixel, y_pixel, constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA)
        
        cor_atual = self._determinar_cor()
        pygame.draw.rect(tela, cor_atual, rect)
        pygame.draw.rect(tela, constantes.CINZA_ESCURO, rect, 1)

    def definir_tipo_base(self, novo_tipo_base):
        self._tipo_base = novo_tipo_base
        if self._tipo_base == constantes.TIPO_CONSTRUCAO:
            self._tipo_trafego_evento = constantes.TIPO_RUA_LIVRE 
        self.atualizar_estado()

    def definir_tipo_trafego_evento(self, novo_tipo_evento):
        if self._tipo_base == constantes.TIPO_RUA or \
           self._tipo_base == constantes.TIPO_PARTIDA or \
           self._tipo_base == constantes.TIPO_CHEGADA:
            self._tipo_trafego_evento = novo_tipo_evento
            self.atualizar_estado()
    
    def limpar_evento_trafego(self):
        self.definir_tipo_trafego_evento(constantes.TIPO_RUA_LIVRE)

    def atualizar_estado(self):
        self.custo_movimento = self._determinar_custo_movimento()
        self.cor = self._determinar_cor()

    def eh_obstaculo(self):
        return self._tipo_base == constantes.TIPO_CONSTRUCAO or \
               self._tipo_trafego_evento == constantes.TIPO_RUA_ACIDENTE

    def eh_navegavel(self):
        return not self.eh_obstaculo()

    def resetar_para_caminho(self):
        self.g_custo = float('inf')
        self.h_custo = float('inf')
        self.f_custo = float('inf')
        self.pai = None
        self.faz_parte_caminho_sugerido = False
        self.cor_caminho_sugerido = None
        self.atualizar_estado()

    def marcar_como_caminho_sugerido(self):
        self.faz_parte_caminho_sugerido = True
        if self._tipo_base not in [constantes.TIPO_PARTIDA, constantes.TIPO_CHEGADA]:
            if self._tipo_trafego_evento == constantes.TIPO_RUA_LIVRE:
                self.cor_caminho_sugerido = constantes.VERDE_CAMINHO
            elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_LEVE:
                self.cor_caminho_sugerido = constantes.AMARELO_CAMINHO
            elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_MODERADO:
                self.cor_caminho_sugerido = constantes.LARANJA_CAMINHO
            elif self._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_PESADO or \
                 self._tipo_trafego_evento == constantes.TIPO_RUA_ACIDENTE:
                self.cor_caminho_sugerido = constantes.VERMELHO_CAMINHO
            else:
                 self.cor_caminho_sugerido = constantes.VERDE_CAMINHO
        self.atualizar_estado()