import pygame
import sys
import random
import traceback
import os

import constantes
from mapa import Mapa
from pathfinder import Pathfinder
from carro import Carro
from eventos_trafego import GerenciadorEventos
from ui import PainelUI
from menu_moderno import MenuModerno
from gerenciador_assets import inicializar_gerenciador_assets, obter_gerenciador_assets

mapa_jogo = None
pathfinder = None
gerenciador_eventos = None
painel_ui_jogo = None
carro_jogador = None
caminho_sugerido_atual = []

estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
rodando_aplicacao = True
largura_tela_atual = 0
altura_tela_atual = 0
altura_mapa_para_ui = 0
tipo_pincel_atual_editor = constantes.PINCEL_RUA
trafego_ativo_simulacao = False

def obter_nome_pincel(tipo_pincel):
    """Retorna o nome do pincel atual para exibição na UI"""
    if tipo_pincel == constantes.PINCEL_RUA:
        return "Rua"
    elif tipo_pincel == constantes.PINCEL_REMOVER_EVENTO:
        return "Remover Evento"
    elif tipo_pincel in constantes.NOMES_ESTRUTURAS:
        return constantes.NOMES_ESTRUTURAS[tipo_pincel]
    else:
        return "Desconhecido"

def desenhar_menu(tela, fonte_titulo, fonte_botao, itens_menu, item_selecionado_idx=None):
    tela.fill(constantes.COR_PAINEL_UI)
    titulo_surf = fonte_titulo.render("Waze Particular", True, constantes.COR_TEXTO_UI)
    titulo_rect = titulo_surf.get_rect(center=(tela.get_width() // 2, 100))
    tela.blit(titulo_surf, titulo_rect)

    botoes_rects = []
    for i, (texto_botao, _) in enumerate(itens_menu):
        cor = constantes.COR_TEXTO_UI
        if item_selecionado_idx is not None and i == item_selecionado_idx:
            cor = constantes.AMARELO_CAMINHO
        botao_surf = fonte_botao.render(texto_botao, True, cor)
        altura_botao = 250 + i * 70
        botao_rect = botao_surf.get_rect(center=(tela.get_width() // 2, altura_botao))
        tela.blit(botao_surf, botao_rect)
        botoes_rects.append(botao_rect)
    return botoes_rects

def inicializar_componentes_comuns_jogo():
    global pathfinder, gerenciador_eventos, painel_ui_jogo, mapa_jogo
    if not mapa_jogo:
        mapa_jogo = Mapa(constantes.NUM_LINHAS_MAPA_PADRAO, constantes.NUM_COLUNAS_MAPA_PADRAO)
    
    pathfinder = Pathfinder(mapa_jogo)
    gerenciador_eventos = GerenciadorEventos(mapa_jogo)
    
    largura_mapa_real = mapa_jogo.num_colunas * constantes.TAMANHO_CELULA
    altura_mapa_real = mapa_jogo.num_linhas * constantes.TAMANHO_CELULA
    painel_ui_jogo = PainelUI(largura_mapa_real, constantes.ALTURA_PAINEL_UI, altura_mapa_real)

def iniciar_modo_editor():
    global estado_atual_jogo, tipo_pincel_atual_editor, mapa_jogo
    mapa_jogo = Mapa(constantes.NUM_LINHAS_MAPA_PADRAO, constantes.NUM_COLUNAS_MAPA_PADRAO)
    inicializar_componentes_comuns_jogo()
    
    estado_atual_jogo = constantes.ESTADO_MODO_EDITOR
    tipo_pincel_atual_editor = constantes.PINCEL_RUA
    nome_pincel = obter_nome_pincel(tipo_pincel_atual_editor)
    painel_ui_jogo.definir_estado_pincel(f"Editor - Pincel: {nome_pincel}")
    painel_ui_jogo.definir_notificacao_geral("Modo Editor: Desenhe seu mapa!")
    painel_ui_jogo.definir_notificacao_caminho("S: Salvar | L: Carregar | Enter: Jogar | Esc: Menu")

def carregar_e_editar_mapa(nome_arquivo):
    global estado_atual_jogo, tipo_pincel_atual_editor, mapa_jogo
    global largura_tela_atual, altura_tela_atual, altura_mapa_para_ui
    
    mapa_jogo = Mapa(constantes.NUM_LINHAS_MAPA_PADRAO, constantes.NUM_COLUNAS_MAPA_PADRAO)
    
    if mapa_jogo.carregar_mapa(nome_arquivo):
        inicializar_componentes_comuns_jogo()
        estado_atual_jogo = constantes.ESTADO_MODO_EDITOR
        tipo_pincel_atual_editor = constantes.PINCEL_RUA
        nome_pincel = obter_nome_pincel(tipo_pincel_atual_editor)
        painel_ui_jogo.definir_estado_pincel(f"Editor - Pincel: {nome_pincel}")
        painel_ui_jogo.definir_notificacao_geral(f"Editando: {nome_arquivo}")
        painel_ui_jogo.definir_notificacao_caminho("S: Salvar | L: Carregar | Enter: Jogar | Esc: Menu")
        
        nova_largura_mapa = mapa_jogo.num_colunas * constantes.TAMANHO_CELULA
        nova_altura_mapa = mapa_jogo.num_linhas * constantes.TAMANHO_CELULA
        
        if nova_largura_mapa != (largura_tela_atual) or \
           (nova_altura_mapa + constantes.ALTURA_PAINEL_UI) != altura_tela_atual:
            return True
    else:
        if not painel_ui_jogo:
             painel_temp = PainelUI(constantes.LARGURA_TELA, constantes.ALTURA_PAINEL_UI, constantes.ALTURA_MAPA)
             painel_temp.definir_notificacao_geral("Falha ao carregar mapa.")
        else:
            painel_ui_jogo.definir_notificacao_geral("Falha ao carregar mapa.")
            painel_ui_jogo.definir_notificacao_caminho("Verifique o console. Voltando ao menu...")
        
        estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
    return False

def iniciar_simulacao_do_editor():
    global estado_atual_jogo, trafego_ativo_simulacao, carro_jogador, mapa_jogo, painel_ui_jogo
    
    if not mapa_jogo:
        estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
        return

    if not mapa_jogo.definir_partida_chegada_aleatorias():
        painel_ui_jogo.definir_notificacao_geral("ERRO: Ruas insuficientes para partida/chegada.")
        painel_ui_jogo.definir_notificacao_caminho("Adicione mais ruas e tente novamente.")
        return

    estado_atual_jogo = constantes.ESTADO_SIMULACAO
    trafego_ativo_simulacao = True
    inicializar_componentes_comuns_jogo()
    
    carro_jogador = Carro(mapa_jogo.ponto_partida[0], mapa_jogo.ponto_partida[1], mapa_jogo)
    
    painel_ui_jogo.definir_notificacao_geral("Modo Simulação: Guie o carro!")
    recalcular_e_mostrar_caminho_simulacao()

def recalcular_e_mostrar_caminho_simulacao():
    global caminho_sugerido_atual, painel_ui_jogo, carro_jogador, pathfinder, mapa_jogo
    
    if not painel_ui_jogo or not carro_jogador or not pathfinder or not mapa_jogo: return
    if not mapa_jogo.ponto_partida or not mapa_jogo.ponto_chegada : return

    mapa_jogo.limpar_visualizacao_caminho_sugerido()
    caminho_sugerido_atual = []

    p_partida_coords = carro_jogador.obter_posicao_atual()
    p_chegada_coords = mapa_jogo.ponto_chegada
    direcao_carro = carro_jogador.direcao_atual
    
    if p_partida_coords and p_chegada_coords:
        caminho = pathfinder.encontrar_caminho(
            p_partida_coords[0], p_partida_coords[1],
            p_chegada_coords[0], p_chegada_coords[1],
            direcao_carro
        )
        if caminho:
            caminho_sugerido_atual = caminho
            max_custo = 0
            for cel in caminho:
                cel.marcar_como_caminho_sugerido()
                if cel.custo_movimento != float('inf'): max_custo = max(max_custo, cel.custo_movimento)
            
            msg = f"Rota: {len(caminho)}p. "
            if max_custo >= constantes.CUSTO_ENG_PESADO: msg += "Trânsito PESADO!"
            elif max_custo >= constantes.CUSTO_ENG_MODERADO: msg += "Trânsito MODERADO."
            elif max_custo >= constantes.CUSTO_ENG_LEVE: msg += "Trânsito LEVE."
            else: msg += "Caminho LIVRE!"
            painel_ui_jogo.definir_notificacao_caminho(msg)
        else:
            painel_ui_jogo.definir_notificacao_caminho("Nenhuma rota encontrada.")
    else:
        painel_ui_jogo.definir_notificacao_caminho("Aguardando partida/chegada.")

def main_game_loop():
    global rodando_aplicacao, estado_atual_jogo, tipo_pincel_atual_editor, trafego_ativo_simulacao
    global mapa_jogo, painel_ui_jogo, carro_jogador, caminho_sugerido_atual
    global largura_tela_atual, altura_tela_atual, altura_mapa_para_ui

    pygame.init()
    
    # Inicializar o gerenciador de assets
    inicializar_gerenciador_assets()

    menu_moderno = MenuModerno()

    largura_tela_atual = constantes.LARGURA_TELA
    altura_tela_atual = constantes.ALTURA_TELA
    altura_mapa_para_ui = constantes.ALTURA_MAPA
    
    tela = pygame.display.set_mode((largura_tela_atual, altura_tela_atual))
    pygame.display.set_caption("Waze Particular")
    relogio = pygame.time.Clock()

    fonte_titulo_menu = pygame.font.Font(None, 74)
    fonte_botao_menu = pygame.font.Font(None, 50)
    mapa_salvo_padrao = "cidade_salva.txt"
    
    pygame.time.set_timer(constantes.EVENTO_ATUALIZAR_TRAFEGO, constantes.INTERVALO_ATUALIZACAO_TRAFEGO)

    while rodando_aplicacao:
        mouse_pos = pygame.mouse.get_pos()
        precisa_recriar_tela = False

        # Atualizar menu moderno se estivermos no estado inicial
        if estado_atual_jogo == constantes.ESTADO_MENU_INICIAL:
            menu_moderno.atualizar(mouse_pos)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando_aplicacao = False
                estado_atual_jogo = constantes.ESTADO_SAINDO

            if estado_atual_jogo == constantes.ESTADO_MENU_INICIAL:
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    botao_clicado = menu_moderno.processar_clique(mouse_pos)
                    
                    if botao_clicado == 0:  # Criar Novo Mapa
                        iniciar_modo_editor()
                    elif botao_clicado == 1:  # Carregar mapa
                        if carregar_e_editar_mapa(mapa_salvo_padrao):
                            precisa_recriar_tela = True
                    elif botao_clicado == 2:  # Sair
                        rodando_aplicacao = False
                        estado_atual_jogo = constantes.ESTADO_SAINDO
                        
                if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                    rodando_aplicacao = False
                    estado_atual_jogo = constantes.ESTADO_SAINDO
            
            elif estado_atual_jogo == constantes.ESTADO_MODO_EDITOR:
                if not mapa_jogo or not painel_ui_jogo:
                    estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
                    continue

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
                        mapa_jogo = None
                        painel_ui_jogo = None
                        carro_jogador = None
                        caminho_sugerido_atual = []
                        continue
                    
                    # Controles de pincel básicos
                    if evento.key == pygame.K_r:
                        tipo_pincel_atual_editor = constantes.PINCEL_RUA
                    elif evento.key == pygame.K_c:
                        tipo_pincel_atual_editor = constantes.PINCEL_CONSTRUCAO
                    elif evento.key == pygame.K_x:
                        tipo_pincel_atual_editor = constantes.PINCEL_REMOVER_EVENTO
                    # Controles de estruturas com números
                    elif evento.key == pygame.K_1:
                        tipo_pincel_atual_editor = constantes.PINCEL_CASA_GRANDE
                    elif evento.key == pygame.K_2:
                        tipo_pincel_atual_editor = constantes.PINCEL_CASA_MARROM
                    elif evento.key == pygame.K_3:
                        tipo_pincel_atual_editor = constantes.PINCEL_CASA_PRETA
                    elif evento.key == pygame.K_4:
                        tipo_pincel_atual_editor = constantes.PINCEL_DELEGACIA
                    elif evento.key == pygame.K_5:
                        tipo_pincel_atual_editor = constantes.PINCEL_ESCOLA
                    elif evento.key == pygame.K_6:
                        tipo_pincel_atual_editor = constantes.PINCEL_HOTEL
                    elif evento.key == pygame.K_7:
                        tipo_pincel_atual_editor = constantes.PINCEL_IGREJA
                    elif evento.key == pygame.K_8:
                        tipo_pincel_atual_editor = constantes.PINCEL_MERCADO
                    elif evento.key == pygame.K_9:
                        tipo_pincel_atual_editor = constantes.PINCEL_PREDIO
                    
                    # Atualizar UI com o nome do pincel
                    nome_pincel = obter_nome_pincel(tipo_pincel_atual_editor)
                    painel_ui_jogo.definir_estado_pincel(f"Editor - Pincel: {nome_pincel}")
                    
                    # Outros controles
                    if evento.key == pygame.K_s:
                        if mapa_jogo.salvar_mapa(mapa_salvo_padrao):
                            painel_ui_jogo.definir_notificacao_caminho(f"Mapa salvo como '{mapa_salvo_padrao}'")
                        else:
                            painel_ui_jogo.definir_notificacao_caminho("Erro ao salvar.")
                    elif evento.key == pygame.K_l:
                        if carregar_e_editar_mapa(mapa_salvo_padrao):
                            precisa_recriar_tela = True
                    elif evento.key == pygame.K_RETURN:
                        iniciar_simulacao_do_editor()

                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    if mouse_pos[1] < (mapa_jogo.num_linhas * constantes.TAMANHO_CELULA):
                        col = mouse_pos[0] // constantes.TAMANHO_CELULA
                        lin = mouse_pos[1] // constantes.TAMANHO_CELULA
                        if 0 <= lin < mapa_jogo.num_linhas and 0 <= col < mapa_jogo.num_colunas:
                            if tipo_pincel_atual_editor == constantes.PINCEL_REMOVER_EVENTO:
                                mapa_jogo.limpar_evento_trafego_celula(lin, col)
                            else:
                                mapa_jogo.definir_tipo_base_celula(lin, col, tipo_pincel_atual_editor)
                            mapa_jogo.adicionar_vizinhos_para_todas_celulas()
            
            elif estado_atual_jogo == constantes.ESTADO_SIMULACAO:
                if not carro_jogador or not painel_ui_jogo or not gerenciador_eventos or not pathfinder or not mapa_jogo:
                    estado_atual_jogo = constantes.ESTADO_MENU_INICIAL
                    continue

                if evento.type == constantes.EVENTO_ATUALIZAR_TRAFEGO and trafego_ativo_simulacao:
                    gerenciador_eventos.simular_eventos_aleatorios()
                    not_ev = gerenciador_eventos.obter_ultima_notificacao_evento()
                    if not_ev and ("EVENTO:" not in painel_ui_jogo.ultima_notificacao_caminho or not_ev not in painel_ui_jogo.ultima_notificacao_caminho):
                        painel_ui_jogo.definir_notificacao_caminho(f"EVENTO: {not_ev} (Rota recalculada)")
                    else:
                        recalcular_e_mostrar_caminho_simulacao()
                    if not_ev:
                        recalcular_e_mostrar_caminho_simulacao()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        estado_atual_jogo = constantes.ESTADO_MODO_EDITOR
                        trafego_ativo_simulacao = False
                        nome_pincel = obter_nome_pincel(tipo_pincel_atual_editor)
                        painel_ui_jogo.definir_estado_pincel(f"Editor - Pincel: {nome_pincel}")
                        painel_ui_jogo.definir_notificacao_geral("Modo Editor: Retomado.")
                        painel_ui_jogo.definir_notificacao_caminho("S: Salvar | L: Carregar | Enter: Jogar | Esc: Menu")
                        if mapa_jogo.ponto_partida:
                            mapa_jogo.obter_celula(mapa_jogo.ponto_partida[0], mapa_jogo.ponto_partida[1]).definir_tipo_base(constantes.TIPO_RUA)
                            mapa_jogo.ponto_partida = None
                        if mapa_jogo.ponto_chegada:
                            mapa_jogo.obter_celula(mapa_jogo.ponto_chegada[0], mapa_jogo.ponto_chegada[1]).definir_tipo_base(constantes.TIPO_RUA)
                            mapa_jogo.ponto_chegada = None
                        mapa_jogo.limpar_visualizacao_caminho_sugerido()
                        carro_jogador = None
                        continue
                    
                    if trafego_ativo_simulacao:
                        if evento.key == pygame.K_UP:
                            carro_jogador.definir_proxima_direcao(constantes.DIRECAO_CIMA)
                        elif evento.key == pygame.K_DOWN:
                            carro_jogador.definir_proxima_direcao(constantes.DIRECAO_BAIXO)
                        elif evento.key == pygame.K_LEFT:
                            carro_jogador.definir_proxima_direcao(constantes.DIRECAO_ESQUERDA)
                        elif evento.key == pygame.K_RIGHT:
                            carro_jogador.definir_proxima_direcao(constantes.DIRECAO_DIREITA)
                        elif evento.key == pygame.K_SPACE:
                            carro_jogador.parar_movimento_automatico()
                            painel_ui_jogo.definir_notificacao_geral("Carro parado.")
                    if evento.key == pygame.K_r:
                        recalcular_e_mostrar_caminho_simulacao()

        if precisa_recriar_tela:
            largura_tela_atual = mapa_jogo.num_colunas * constantes.TAMANHO_CELULA
            altura_mapa_para_ui = mapa_jogo.num_linhas * constantes.TAMANHO_CELULA
            altura_tela_atual = altura_mapa_para_ui + constantes.ALTURA_PAINEL_UI
            tela = pygame.display.set_mode((largura_tela_atual, altura_tela_atual))
            if painel_ui_jogo:
                painel_ui_jogo = PainelUI(largura_tela_atual, constantes.ALTURA_PAINEL_UI, altura_mapa_para_ui)
                if estado_atual_jogo == constantes.ESTADO_MODO_EDITOR:
                    nome_pincel = obter_nome_pincel(tipo_pincel_atual_editor)
                    painel_ui_jogo.definir_estado_pincel(f"Editor - Pincel: {nome_pincel}")
                    painel_ui_jogo.definir_notificacao_geral(f"Editando: {mapa_salvo_padrao}")
            precisa_recriar_tela = False

        # Atualizar lógica do jogo
        if estado_atual_jogo == constantes.ESTADO_SIMULACAO and carro_jogador and trafego_ativo_simulacao:
            pos_ant = carro_jogador.obter_posicao_atual()
            carro_jogador.atualizar()
            pos_nova = carro_jogador.obter_posicao_atual()
            if pos_ant != pos_nova:
                recalcular_e_mostrar_caminho_simulacao()
            if (carro_jogador.linha, carro_jogador.coluna) == mapa_jogo.ponto_chegada:
                painel_ui_jogo.definir_notificacao_geral("PARABÉNS! Destino alcançado!")
                painel_ui_jogo.definir_notificacao_caminho("ESC para voltar ao editor.")
                trafego_ativo_simulacao = False
                mapa_jogo.limpar_visualizacao_caminho_sugerido()

        # Desenhar baseado no estado atual
        if estado_atual_jogo == constantes.ESTADO_MENU_INICIAL:
            menu_moderno.desenhar(tela)
        elif estado_atual_jogo == constantes.ESTADO_MODO_EDITOR:
            if mapa_jogo and painel_ui_jogo:
                tela.fill(constantes.BRANCO)
                mapa_jogo.desenhar(tela)
                painel_ui_jogo.desenhar(tela, True)
        elif estado_atual_jogo == constantes.ESTADO_SIMULACAO:
            if mapa_jogo and painel_ui_jogo:
                tela.fill(constantes.BRANCO)
                mapa_jogo.desenhar(tela)
                if carro_jogador:
                    carro_jogador.desenhar(tela)
                painel_ui_jogo.desenhar(tela, False)

        pygame.display.flip()
        relogio.tick(constantes.FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    try:
        main_game_loop()
    except Exception as e:
        print("ERRO FATAL NA EXECUÇÃO DO JOGO:")
        print(str(e))
        traceback.print_exc()
        pygame.quit()
        sys.exit()