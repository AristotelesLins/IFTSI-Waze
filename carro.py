import pygame
import constantes

class Carro:
    def __init__(self, linha_inicial, coluna_inicial, mapa_ref):
        self.linha = linha_inicial
        self.coluna = coluna_inicial
        self.mapa = mapa_ref
        self.cor = constantes.COR_CARRO
        self.imagem_original = None
        self.imagem_atual = None
        
        try:
            self.imagem_original = pygame.image.load("assets/carro_img.png") 
            self.imagem_original = pygame.transform.scale(self.imagem_original, (constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA))
            self.imagem_atual = self.imagem_original
        except pygame.error as e:
            print(f"Aviso: Imagem do carro 'assets/carro_img.png' não encontrada. Usando cor. {e}")
            self.imagem_original = None
            self.imagem_atual = None

        self.direcao_atual = constantes.DIRECAO_DIREITA
        self.proxima_direcao = constantes.DIRECAO_NENHUMA
        
        self.ticks_para_proximo_movimento = 0
        self.movendo_automaticamente = False

    def definir_proxima_direcao(self, direcao_input):
        if self.direcao_atual == constantes.DIRECAO_CIMA and direcao_input == constantes.DIRECAO_BAIXO: return
        if self.direcao_atual == constantes.DIRECAO_BAIXO and direcao_input == constantes.DIRECAO_CIMA: return
        if self.direcao_atual == constantes.DIRECAO_ESQUERDA and direcao_input == constantes.DIRECAO_DIREITA: return
        if self.direcao_atual == constantes.DIRECAO_DIREITA and direcao_input == constantes.DIRECAO_ESQUERDA: return

        self.proxima_direcao = direcao_input
        self.movendo_automaticamente = True

    def parar_movimento_automatico(self):
        self.movendo_automaticamente = False

    def _obter_delta_por_direcao(self, direcao):
        if direcao == constantes.DIRECAO_CIMA: return -1, 0
        if direcao == constantes.DIRECAO_BAIXO: return 1, 0
        if direcao == constantes.DIRECAO_ESQUERDA: return 0, -1
        if direcao == constantes.DIRECAO_DIREITA: return 0, 1
        return 0,0

    def atualizar(self):
        if not self.movendo_automaticamente and self.proxima_direcao == constantes.DIRECAO_NENHUMA:
            return

        self.ticks_para_proximo_movimento -= 1
        if self.ticks_para_proximo_movimento > 0:
            return

        direcao_escolhida_para_tentar = constantes.DIRECAO_NENHUMA

        if self.proxima_direcao != constantes.DIRECAO_NENHUMA:
            direcao_escolhida_para_tentar = self.proxima_direcao
        elif self.movendo_automaticamente:
            direcao_escolhida_para_tentar = self.direcao_atual
        
        if direcao_escolhida_para_tentar == constantes.DIRECAO_NENHUMA:
            self.movendo_automaticamente = False
            return

        d_linha, d_coluna = self._obter_delta_por_direcao(direcao_escolhida_para_tentar)
        nova_linha = self.linha + d_linha
        nova_coluna = self.coluna + d_coluna
        celula_destino = self.mapa.obter_celula(nova_linha, nova_coluna)

        moved_this_update = False
        if celula_destino and celula_destino.eh_navegavel():
            self.linha = nova_linha
            self.coluna = nova_coluna
            self.direcao_atual = direcao_escolhida_para_tentar
            moved_this_update = True
        else:
            self.movendo_automaticamente = False

        celula_atual_no_mapa = self.mapa.obter_celula(self.linha, self.coluna)
        modificador_custo_ticks = 1.0
        if celula_atual_no_mapa:
            if celula_atual_no_mapa._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_LEVE:
                modificador_custo_ticks = constantes.MODIFICADOR_VEL_ENG_LEVE
            elif celula_atual_no_mapa._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_MODERADO:
                modificador_custo_ticks = constantes.MODIFICADOR_VEL_ENG_MODERADO
            elif celula_atual_no_mapa._tipo_trafego_evento == constantes.TIPO_RUA_ENGARRAFAMENTO_PESADO:
                modificador_custo_ticks = constantes.MODIFICADOR_VEL_ENG_PESADO
            elif celula_atual_no_mapa._tipo_trafego_evento == constantes.TIPO_RUA_ACIDENTE:
                modificador_custo_ticks = 999

        self.ticks_para_proximo_movimento = int(constantes.VELOCIDADE_BASE_CARRO_TICKS * modificador_custo_ticks)

    def desenhar(self, tela):
        x_pixel = self.coluna * constantes.TAMANHO_CELULA
        y_pixel = self.linha * constantes.TAMANHO_CELULA
        
        if self.imagem_original:
            if self.direcao_atual == constantes.DIRECAO_CIMA:
                self.imagem_atual = self.imagem_original
            elif self.direcao_atual == constantes.DIRECAO_BAIXO:
                self.imagem_atual = pygame.transform.rotate(self.imagem_original, 180)
            elif self.direcao_atual == constantes.DIRECAO_ESQUERDA:
                self.imagem_atual = pygame.transform.rotate(self.imagem_original, 90)
            elif self.direcao_atual == constantes.DIRECAO_DIREITA:
                self.imagem_atual = pygame.transform.rotate(self.imagem_original, -90)
            else:
                 pass

            if self.imagem_atual:
                tela.blit(self.imagem_atual, (x_pixel, y_pixel))
        else:
            rect = pygame.Rect(x_pixel, y_pixel, constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA)
            pygame.draw.rect(tela, self.cor, rect)
            
            centro_x = x_pixel + constantes.TAMANHO_CELULA // 2
            centro_y = y_pixel + constantes.TAMANHO_CELULA // 2
            ponta_x, ponta_y = centro_x, centro_y

            if self.direcao_atual == constantes.DIRECAO_CIMA: ponta_y = y_pixel + 3
            elif self.direcao_atual == constantes.DIRECAO_BAIXO: ponta_y = y_pixel + constantes.TAMANHO_CELULA - 3
            elif self.direcao_atual == constantes.DIRECAO_ESQUERDA: ponta_x = x_pixel + 3
            elif self.direcao_atual == constantes.DIRECAO_DIREITA: ponta_x = x_pixel + constantes.TAMANHO_CELULA - 3
            
            if self.direcao_atual != constantes.DIRECAO_NENHUMA:
                 pygame.draw.line(tela, constantes.PRETO, (centro_x, centro_y), (ponta_x, ponta_y), 3)


    def obter_posicao_atual(self):
        return self.linha, self.coluna