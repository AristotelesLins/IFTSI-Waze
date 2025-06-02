import pygame
import math
import constantes

class MenuModerno:
    def __init__(self):
        self.fonte_titulo = None
        self.fonte_botao = None
        self.botoes = []
        self.botao_hover = -1
        self.tempo_animacao = 0
        self._inicializar_fontes()
        self._criar_botoes()
    
    def _inicializar_fontes(self):
        try:
            self.fonte_titulo = pygame.font.Font(None, constantes.TAMANHO_TITULO_PRINCIPAL)
            self.fonte_botao = pygame.font.Font(None, constantes.TAMANHO_TEXTO_BOTAO)
        except:
            self.fonte_titulo = pygame.font.Font(None, 72)
            self.fonte_botao = pygame.font.Font(None, 20)
    
    def _criar_botoes(self):
        centro_x = constantes.LARGURA_TELA // 2
        inicio_y = constantes.ALTURA_TELA // 2 + 50
        
        textos_botoes = [
            "Criar Novo Mapa",
            "Carregar 'cidade_salva.txt'", 
            "Sair"
        ]
        
        self.botoes = []
        for i, texto in enumerate(textos_botoes):
            y = inicio_y + i * (constantes.ALTURA_BOTAO + constantes.ESPACO_ENTRE_BOTOES)
            botao = {
                'rect': pygame.Rect(
                    centro_x - constantes.LARGURA_BOTAO // 2,
                    y,
                    constantes.LARGURA_BOTAO,
                    constantes.ALTURA_BOTAO
                ),
                'texto': texto,
                'ativo': False
            }
            self.botoes.append(botao)
    
    def _desenhar_fundo_gradiente(self, tela):
        """Desenha um fundo com gradiente vertical"""
        for y in range(constantes.ALTURA_TELA):
            progresso = y / constantes.ALTURA_TELA
            
            r = int(constantes.COR_FUNDO_GRADIENTE_1[0] * (1 - progresso) + 
                   constantes.COR_FUNDO_GRADIENTE_2[0] * progresso)
            g = int(constantes.COR_FUNDO_GRADIENTE_1[1] * (1 - progresso) + 
                   constantes.COR_FUNDO_GRADIENTE_2[1] * progresso)
            b = int(constantes.COR_FUNDO_GRADIENTE_1[2] * (1 - progresso) + 
                   constantes.COR_FUNDO_GRADIENTE_2[2] * progresso)
            
            pygame.draw.line(tela, (r, g, b), (0, y), (constantes.LARGURA_TELA, y))
    
    def _desenhar_titulo_com_efeito(self, tela):
        """Desenha o título com sombra e efeito pulsante"""
        titulo = "Waze Particular"
        
        # Efeito pulsante baseado no tempo
        pulso = math.sin(self.tempo_animacao * 0.003) * 5 + 5
        
        # Sombra do título
        superficie_sombra = self.fonte_titulo.render(titulo, True, constantes.COR_TITULO_SOMBRA)
        rect_sombra = superficie_sombra.get_rect(center=(constantes.LARGURA_TELA // 2 + 3, 
                                                        constantes.ALTURA_TELA // 4 + 3))
        tela.blit(superficie_sombra, rect_sombra)
        
        # Título principal com efeito de pulso
        superficie_titulo = self.fonte_titulo.render(titulo, True, constantes.COR_TITULO_PRINCIPAL)
        rect_titulo = superficie_titulo.get_rect(center=(constantes.LARGURA_TELA // 2, 
                                                        constantes.ALTURA_TELA // 4 - pulso))
        tela.blit(superficie_titulo, rect_titulo)
        
        # Linha decorativa
        linha_y = rect_titulo.bottom + 20
        pygame.draw.line(tela, constantes.COR_DESTAQUE, 
                        (constantes.LARGURA_TELA // 2 - 150, linha_y),
                        (constantes.LARGURA_TELA // 2 + 150, linha_y), 3)
    def _desenhar_botao_moderno(self, tela, botao, index):
        """Desenha um botão com visual moderno e efeitos"""
        rect = botao['rect']
        
        # Efeito hover
        if self.botao_hover == index:
            cor_fundo = constantes.COR_BOTAO_HOVER
            offset_y = -2
            escala_hover = 1.02  # Aumenta ligeiramente o botão
        else:
            cor_fundo = constantes.COR_BOTAO_NORMAL
            offset_y = 0
            escala_hover = 1.0
        
        # Calcular tamanho com escala para hover
        largura_hover = int(rect.width * escala_hover)
        altura_hover = int(rect.height * escala_hover)
        x_hover = rect.x - (largura_hover - rect.width) // 2
        y_hover = rect.y + offset_y - (altura_hover - rect.height) // 2
        
        # Rect ajustado para efeito hover
        rect_ajustado = pygame.Rect(x_hover, y_hover, largura_hover, altura_hover)
        
        # Sombra do botão (sempre atrás)
        rect_sombra = pygame.Rect(rect.x + 4, rect.y + 4, rect.width, rect.height)
        pygame.draw.rect(tela, (20, 20, 30), rect_sombra, border_radius=constantes.RAIO_BORDA_BOTAO)
        
        # Botão principal
        pygame.draw.rect(tela, cor_fundo, rect_ajustado, border_radius=constantes.RAIO_BORDA_BOTAO)
        
        # Borda do botão
        pygame.draw.rect(tela, constantes.COR_BOTAO_BORDA, rect_ajustado, 
                        width=2, border_radius=constantes.RAIO_BORDA_BOTAO)
        
        # Texto do botão
        superficie_texto = self.fonte_botao.render(botao['texto'], True, constantes.COR_BOTAO_TEXTO)
        rect_texto = superficie_texto.get_rect(center=rect_ajustado.center)
        tela.blit(superficie_texto, rect_texto)
        
        # Efeito de brilho melhorado no hover
        if self.botao_hover == index:
            # Criar superficie para brilho com bordas arredondadas
            superficie_brilho = pygame.Surface((rect_ajustado.width, rect_ajustado.height), pygame.SRCALPHA)
            
            # Brilho gradiente do topo
            altura_brilho = rect_ajustado.height // 2
            for i in range(altura_brilho):
                alpha = int(40 * (1 - i / altura_brilho))
                cor_brilho = (255, 255, 255, alpha)
                pygame.draw.rect(superficie_brilho, cor_brilho, 
                               (0, i, rect_ajustado.width, 1))
            
            # Aplicar máscara de bordas arredondadas
            mascara = pygame.Surface((rect_ajustado.width, rect_ajustado.height), pygame.SRCALPHA)
            pygame.draw.rect(mascara, (255, 255, 255, 255), 
                           (0, 0, rect_ajustado.width, rect_ajustado.height), 
                           border_radius=constantes.RAIO_BORDA_BOTAO)
            
            # Aplicar a máscara ao brilho
            superficie_brilho.blit(mascara, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            # Desenhar o brilho no botão
            tela.blit(superficie_brilho, rect_ajustado.topleft, special_flags=pygame.BLEND_ALPHA_SDL2)
            
            # Adicionar contorno sutil brilhante
            pygame.draw.rect(tela, (255, 255, 255, 100), rect_ajustado, 
                           width=1, border_radius=constantes.RAIO_BORDA_BOTAO)
    
    def _desenhar_elementos_decorativos(self, tela):
        """Adiciona elementos visuais decorativos"""
        # Círculos decorativos animados
        for i in range(3):
            raio = 30 + math.sin(self.tempo_animacao * 0.002 + i) * 10
            alpha = 50 + math.sin(self.tempo_animacao * 0.003 + i) * 20
            
            superficie_circulo = pygame.Surface((raio * 2, raio * 2), pygame.SRCALPHA)
            pygame.draw.circle(superficie_circulo, (*constantes.COR_ICONE, int(alpha)), 
                             (raio, raio), raio, 2)
            
            x = 100 + i * (constantes.LARGURA_TELA - 200) // 2
            y = 100 + math.sin(self.tempo_animacao * 0.001 + i) * 30
            tela.blit(superficie_circulo, (x - raio, y - raio))
    
    def atualizar(self, mouse_pos):
        """Atualiza estado do menu baseado na posição do mouse"""
        self.tempo_animacao += 1
        self.botao_hover = -1
        
        for i, botao in enumerate(self.botoes):
            if botao['rect'].collidepoint(mouse_pos):
                self.botao_hover = i
                break
    
    def desenhar(self, tela):
        """Desenha o menu completo"""
        # Fundo com gradiente
        self._desenhar_fundo_gradiente(tela)
        
        # Elementos decorativos
        self._desenhar_elementos_decorativos(tela)
        
        # Título com efeitos
        self._desenhar_titulo_com_efeito(tela)
        
        # Botões modernos
        for i, botao in enumerate(self.botoes):
            self._desenhar_botao_moderno(tela, botao, i)
    
    def processar_clique(self, pos_mouse):
        """Retorna o índice do botão clicado ou -1 se nenhum foi clicado"""
        for i, botao in enumerate(self.botoes):
            if botao['rect'].collidepoint(pos_mouse):
                return i
        return -1