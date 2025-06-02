import pygame
import os
import constantes

class GerenciadorAssets:
    def __init__(self):
        self.imagens_estruturas = {}
        self.carregar_imagens_estruturas()
    
    def carregar_imagens_estruturas(self):
        """Carrega todas as imagens das estruturas da cidade"""
        for tipo_estrutura, nome_arquivo in constantes.ESTRUTURAS_IMAGENS.items():
            caminho_completo = os.path.join("estruturas da cidade", nome_arquivo)
            try:
                if os.path.exists(caminho_completo):
                    imagem = pygame.image.load(caminho_completo)
                    # Ajustado para o novo tamanho de célula (25x25)
                    imagem = pygame.transform.scale(imagem, (constantes.TAMANHO_CELULA, constantes.TAMANHO_CELULA))
                    self.imagens_estruturas[tipo_estrutura] = imagem
                else:
                    print(f"Aviso: Imagem {caminho_completo} não encontrada. Usando cor padrão.")
                    self.imagens_estruturas[tipo_estrutura] = None
            except pygame.error as e:
                print(f"Erro ao carregar {caminho_completo}: {e}. Usando cor padrão.")
                self.imagens_estruturas[tipo_estrutura] = None
    
    def obter_imagem_estrutura(self, tipo_estrutura):
        """Retorna a imagem da estrutura ou None se não encontrada"""
        return self.imagens_estruturas.get(tipo_estrutura, None)

# Instância global para ser usada em toda a aplicação
gerenciador_assets_global = None

def inicializar_gerenciador_assets():
    global gerenciador_assets_global
    gerenciador_assets_global = GerenciadorAssets()
    return gerenciador_assets_global

def obter_gerenciador_assets():
    global gerenciador_assets_global
    return gerenciador_assets_global