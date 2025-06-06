import pygame

# Dimensões do Grid e Célula - AUMENTADAS
NUM_LINHAS_MAPA_PADRAO = 20  # Era 25, agora 35
NUM_COLUNAS_MAPA_PADRAO = 43  # Era 40, agora 60
TAMANHO_CELULA = 44  # Era 20, agora 25

# Cores (formato RGB)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
CINZA_ESCURO = (160, 160, 160)

COR_RUA = (220, 220, 220)
COR_CONSTRUCAO = (100, 100, 100)
COR_PARTIDA = (0, 0, 0)
COR_CHEGADA = (64, 224, 208)
COR_CARRO = (50, 50, 200)

# Cores para o caminho sugerido e tráfego
VERDE_CAMINHO = (60, 179, 113)
AMARELO_CAMINHO = (255, 215, 0)
LARANJA_CAMINHO = (255, 140, 0)
VERMELHO_CAMINHO = (220, 20, 60)
COR_ACIDENTE_VISUAL = (75, 0, 130)

# Tipos de Célula
TIPO_RUA = 0
TIPO_CONSTRUCAO = 1
TIPO_PARTIDA = 2
TIPO_CHEGADA = 3
TIPO_CAMINHO_SUGERIDO = 5

# Novos tipos de estruturas da cidade
TIPO_CASA_GRANDE = 6
TIPO_CASA_MARROM = 7
TIPO_CASA_PRETA = 8
TIPO_DELEGACIA = 9
TIPO_ESCOLA = 10
TIPO_HOTEL = 11
TIPO_IGREJA = 12
TIPO_MERCADO = 13
TIPO_PREDIO = 14

# Tipos de Eventos de Tráfego
TIPO_RUA_LIVRE = 20
TIPO_RUA_ENGARRAFAMENTO_LEVE = 21
TIPO_RUA_ENGARRAFAMENTO_MODERADO = 22
TIPO_RUA_ENGARRAFAMENTO_PESADO = 23
TIPO_RUA_ACIDENTE = 24

# Custos de Movimento Associados (para Pathfinder)
CUSTO_LIVRE = 1
CUSTO_ENG_LEVE = 3
CUSTO_ENG_MODERADO = 6
CUSTO_ENG_PESADO = 10
CUSTO_ACIDENTE = float('inf')

# Dimensões da Tela e Painel de UI - AUMENTADAS
LARGURA_MAPA = NUM_COLUNAS_MAPA_PADRAO * TAMANHO_CELULA  # 60 * 25 = 1500
ALTURA_MAPA = NUM_LINHAS_MAPA_PADRAO * TAMANHO_CELULA     # 35 * 25 = 875

ALTURA_PAINEL_UI = 120  # Era 100, agora 120 para mais espaço
LARGURA_TELA = LARGURA_MAPA  # 1500
ALTURA_TELA = ALTURA_MAPA + ALTURA_PAINEL_UI  # 875 + 120 = 995

# Jogo e Simulação
FPS = 30
EVENTO_ATUALIZAR_TRAFEGO = pygame.USEREVENT + 1
INTERVALO_ATUALIZACAO_TRAFEGO = 2500

# Configurações da UI - AUMENTADAS
COR_PAINEL_UI = (50, 50, 50)
COR_TEXTO_UI = (240, 240, 240)
TAMANHO_FONTE_UI_PADRAO = 28  # Era 24, agora 28
TAMANHO_FONTE_NOTIFICACAO = 24  # Era 20, agora 24

# Pincel Editor
PINCEL_RUA = TIPO_RUA
PINCEL_CONSTRUCAO = TIPO_CONSTRUCAO
PINCEL_CASA_GRANDE = TIPO_CASA_GRANDE
PINCEL_CASA_MARROM = TIPO_CASA_MARROM
PINCEL_CASA_PRETA = TIPO_CASA_PRETA
PINCEL_DELEGACIA = TIPO_DELEGACIA
PINCEL_ESCOLA = TIPO_ESCOLA
PINCEL_HOTEL = TIPO_HOTEL
PINCEL_IGREJA = TIPO_IGREJA
PINCEL_MERCADO = TIPO_MERCADO
PINCEL_PREDIO = TIPO_PREDIO
PINCEL_REMOVER_EVENTO = 99

# Geração de Mapa Procedural (Mantido, mas não usado por padrão)
DENSIDADE_CONSTRUCAO = 0.20
MIN_COMPRIMENTO_RUA = 3
MAX_COMPRIMENTO_RUA = 7

# Carro
VELOCIDADE_BASE_CARRO_TICKS = 10
MODIFICADOR_VEL_ENG_LEVE = 1.5
MODIFICADOR_VEL_ENG_MODERADO = 2.5
MODIFICADOR_VEL_ENG_PESADO = 4.0

# Direções para o carro
DIRECAO_NENHUMA = -1
DIRECAO_CIMA = 0
DIRECAO_BAIXO = 1
DIRECAO_ESQUERDA = 2
DIRECAO_DIREITA = 3

# Estados do Jogo
ESTADO_MENU_INICIAL = 0
ESTADO_MODO_EDITOR = 1
ESTADO_SIMULACAO = 2
ESTADO_SAINDO = 3

# Cores para interface - AUMENTADAS PARA TELA MAIOR
COR_FUNDO_MENU = (25, 30, 45)           # Azul escuro 
COR_FUNDO_GRADIENTE_1 = (35, 45, 65)    # Gradiente início
COR_FUNDO_GRADIENTE_2 = (15, 25, 40)    # Gradiente fim
COR_TITULO_PRINCIPAL = (255, 255, 255)  # Branco para título
COR_TITULO_SOMBRA = (100, 120, 150)     # Sombra do título
COR_BOTAO_NORMAL = (70, 130, 180)       # Azul 
COR_BOTAO_HOVER = (100, 160, 220)       # Azul claro no hover
COR_BOTAO_TEXTO = (255, 255, 255)       # Texto branco
COR_BOTAO_BORDA = (50, 100, 150)        # Borda dos botões
COR_DESTAQUE = (255, 215, 0)            # Dourado para destaques
COR_ICONE = (180, 200, 255)             # Azul claro para ícones

# Tamanhos para interface - AUMENTADOS
TAMANHO_TITULO_PRINCIPAL = 84  # Era 72, agora 84
TAMANHO_SUBTITULO = 28         # Era 24, agora 28
TAMANHO_TEXTO_BOTAO = 24       # Era 20, agora 24
ESPACO_ENTRE_BOTOES = 25       # Era 20, agora 25
LARGURA_BOTAO = 350            # Era 300, agora 350
ALTURA_BOTAO = 70              # Era 60, agora 70
RAIO_BORDA_BOTAO = 18          # Era 15, agora 18

# Mapeamento de estruturas para arquivos de imagem
ESTRUTURAS_IMAGENS = {
    TIPO_CASA_GRANDE: "casa_grande.png",
    TIPO_CASA_MARROM: "casa_marrom.png",
    TIPO_CASA_PRETA: "casa_preta.png",
    TIPO_DELEGACIA: "delegacia2.png",
    TIPO_ESCOLA: "escola.png",
    TIPO_HOTEL: "hotel.png",
    TIPO_IGREJA: "igreja.png",
    TIPO_MERCADO: "mercado.png",
    TIPO_PREDIO: "predio.png"
}

# Nomes das estruturas para exibição
NOMES_ESTRUTURAS = {
    TIPO_CONSTRUCAO: "Construção",
    TIPO_CASA_GRANDE: "Casa Grande",
    TIPO_CASA_MARROM: "Casa Marrom",
    TIPO_CASA_PRETA: "Casa Preta",
    TIPO_DELEGACIA: "Delegacia",
    TIPO_ESCOLA: "Escola",
    TIPO_HOTEL: "Hotel",
    TIPO_IGREJA: "Igreja",
    TIPO_MERCADO: "Mercado",
    TIPO_PREDIO: "Prédio"
}

# Lista de todos os tipos de estruturas (obstáculos)
TIPOS_ESTRUTURAS = [
    TIPO_CONSTRUCAO, TIPO_CASA_GRANDE, TIPO_CASA_MARROM, TIPO_CASA_PRETA,
    TIPO_DELEGACIA, TIPO_ESCOLA, TIPO_HOTEL, TIPO_IGREJA, TIPO_MERCADO, TIPO_PREDIO
]