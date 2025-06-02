import pygame
import constantes

class PainelUI:
    def __init__(self, largura, altura, posicao_y):
        self.largura = largura
        self.altura = altura
        self.posicao_y = posicao_y
        self.cor_fundo = constantes.COR_PAINEL_UI
        self.cor_texto = constantes.COR_TEXTO_UI
        self.fonte_grande = pygame.font.Font(None, constantes.TAMANHO_FONTE_UI_PADRAO)
        self.fonte_pequena = pygame.font.Font(None, constantes.TAMANHO_FONTE_NOTIFICACAO)
        self.superficie = pygame.Surface((self.largura, self.altura))
        
        self.ultima_notificacao_geral = "Modo Editor: Construa ou carregue um mapa."
        self.ultima_notificacao_caminho = "S: Salvar | L: Carregar | Enter: Iniciar Simulação"
        self.estado_pincel_editor = "Pincel: Construção"

    def definir_notificacao_geral(self, msg):
        self.ultima_notificacao_geral = msg
    
    def definir_notificacao_caminho(self, msg):
        self.ultima_notificacao_caminho = msg

    def definir_estado_pincel(self, msg):
        self.estado_pincel_editor = msg

    def desenhar(self, tela_principal, modo_editor_ativo):
        self.superficie.fill(self.cor_fundo)

        if modo_editor_ativo:
            texto_linha1_str = self.estado_pincel_editor
        else:
            texto_linha1_str = self.ultima_notificacao_geral
        
        texto_linha1 = self.fonte_grande.render(texto_linha1_str, True, self.cor_texto)
        self.superficie.blit(texto_linha1, (10, 10))

        texto_linha2 = self.fonte_pequena.render(self.ultima_notificacao_caminho, True, self.cor_texto)
        self.superficie.blit(texto_linha2, (10, 10 + constantes.TAMANHO_FONTE_UI_PADRAO + 5))
        
        if modo_editor_ativo:
            instrucoes = "Estruturas: [1-9] | [R]ua [C]onst [X]Rem.Evento | S/L: Mapa | Enter: Jogar | Esc: Sair"
        else:
            instrucoes = "Setas: Mover | R: Recalc. Rota | Espaço: Parar | Esc: Sair"

        texto_instrucoes = self.fonte_pequena.render(instrucoes, True, self.cor_texto)
        self.superficie.blit(texto_instrucoes, (10, 10 + constantes.TAMANHO_FONTE_UI_PADRAO + 5 + constantes.TAMANHO_FONTE_NOTIFICACAO + 5))

        tela_principal.blit(self.superficie, (0, self.posicao_y))