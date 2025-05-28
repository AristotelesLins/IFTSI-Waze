import pygame
import random
import constantes
from celula import Celula

class Mapa:
    def __init__(self, num_linhas, num_colunas):
        self.num_linhas = num_linhas
        self.num_colunas = num_colunas
        self.grid = []
        self.ponto_partida = None
        self.ponto_chegada = None
        self._inicializar_mapa_vazio()

    def _inicializar_mapa_vazio(self):
        self.grid = []
        for i in range(self.num_linhas):
            linha_atual = []
            for j in range(self.num_colunas):
                celula_obj = Celula(i, j)
                celula_obj.definir_tipo_base(constantes.TIPO_RUA)
                linha_atual.append(celula_obj)
            self.grid.append(linha_atual)
        
        if self.ponto_partida:
            cel_ant_partida = self.obter_celula(self.ponto_partida[0], self.ponto_partida[1])
            if cel_ant_partida and cel_ant_partida._tipo_base == constantes.TIPO_PARTIDA :
                 cel_ant_partida.definir_tipo_base(constantes.TIPO_RUA)
        if self.ponto_chegada:
            cel_ant_chegada = self.obter_celula(self.ponto_chegada[0], self.ponto_chegada[1])
            if cel_ant_chegada and cel_ant_chegada._tipo_base == constantes.TIPO_CHEGADA:
                cel_ant_chegada.definir_tipo_base(constantes.TIPO_RUA)

        self.ponto_partida = None
        self.ponto_chegada = None


    def definir_partida_chegada_aleatorias(self):
        """Define pontos de partida e chegada aleatórios em células de RUA existentes."""

        if self.ponto_partida:
            self.obter_celula(self.ponto_partida[0], self.ponto_partida[1]).definir_tipo_base(constantes.TIPO_RUA)
            self.ponto_partida = None
        if self.ponto_chegada:
            self.obter_celula(self.ponto_chegada[0], self.ponto_chegada[1]).definir_tipo_base(constantes.TIPO_RUA)
            self.ponto_chegada = None

        celulas_rua_validas = []
        for r in range(self.num_linhas):
            for c in range(self.num_colunas):
                if self.grid[r][c]._tipo_base == constantes.TIPO_RUA and not self.grid[r][c].eh_obstaculo():
                    celulas_rua_validas.append((r,c))
        
        if len(celulas_rua_validas) < 2:
            print("AVISO: Não há células de rua suficientes para definir partida e chegada aleatórias.")
            return False

        idx_partida = random.randint(0, len(celulas_rua_validas) - 1)
        self.ponto_partida = celulas_rua_validas.pop(idx_partida)
        self.definir_tipo_base_celula(self.ponto_partida[0], self.ponto_partida[1], constantes.TIPO_PARTIDA)
        
        if not celulas_rua_validas:
             print("AVISO: Apenas uma célula de rua válida. Partida e Chegada serão a mesma.")
             self.ponto_chegada = self.ponto_partida
        else:
            idx_chegada = random.randint(0, len(celulas_rua_validas) - 1)
            self.ponto_chegada = celulas_rua_validas[idx_chegada]
        self.definir_tipo_base_celula(self.ponto_chegada[0], self.ponto_chegada[1], constantes.TIPO_CHEGADA)
        
        print(f"Partida aleatória: {self.ponto_partida}, Chegada aleatória: {self.ponto_chegada}")
        return True


    def gerar_mapa_procedural(self, densidade_construcao=constantes.DENSIDADE_CONSTRUCAO):
        self._inicializar_mapa_vazio()
        for r in range(self.num_linhas):
            self.grid[r][0].definir_tipo_base(constantes.TIPO_CONSTRUCAO)
            self.grid[r][self.num_colunas - 1].definir_tipo_base(constantes.TIPO_CONSTRUCAO)
        for c in range(self.num_colunas):
            self.grid[0][c].definir_tipo_base(constantes.TIPO_CONSTRUCAO)
            self.grid[self.num_linhas - 1][c].definir_tipo_base(constantes.TIPO_CONSTRUCAO)

        for r in range(1, self.num_linhas - 1):
            for c in range(1, self.num_colunas - 1):
                if random.random() < densidade_construcao:
                    self.grid[r][c].definir_tipo_base(constantes.TIPO_CONSTRUCAO)
                else:
                    self.grid[r][c].definir_tipo_base(constantes.TIPO_RUA)
        
        r_atual, c_atual = random.randint(1, self.num_linhas - 2), random.randint(1, self.num_colunas - 2)
        self.grid[r_atual][c_atual].definir_tipo_base(constantes.TIPO_RUA)
        num_passos_caminhante = (self.num_linhas * self.num_colunas) // 4
        for _ in range(num_passos_caminhante):
            direcoes_possiveis = [(0,1), (0,-1), (1,0), (-1,0)]
            random.shuffle(direcoes_possiveis)
            movido_neste_passo = False
            for dr, dc in direcoes_possiveis:
                comprimento_rua = random.randint(constantes.MIN_COMPRIMENTO_RUA, constantes.MAX_COMPRIMENTO_RUA)
                r_temp, c_temp = r_atual, c_atual
                valido_para_criar_rua = True
                segmento_rua = []
                for i_seg in range(comprimento_rua):
                    r_prox = r_temp + dr
                    c_prox = c_temp + dc
                    if 1 <= r_prox < self.num_linhas - 1 and 1 <= c_prox < self.num_colunas - 1:
                        segmento_rua.append((r_prox, c_prox))
                        r_temp, c_temp = r_prox, c_prox
                    else:
                        valido_para_criar_rua = False; break
                if valido_para_criar_rua:
                    for r_seg, c_seg in segmento_rua: self.grid[r_seg][c_seg].definir_tipo_base(constantes.TIPO_RUA)
                    r_atual, c_atual = segmento_rua[-1]; movido_neste_passo = True; break
            if not movido_neste_passo:
                celulas_rua = [(r,c) for r in range(1,self.num_linhas-1) for c in range(1,self.num_colunas-1) if self.grid[r][c]._tipo_base == constantes.TIPO_RUA]
                if celulas_rua: r_atual, c_atual = random.choice(celulas_rua)
                else: break
        if not self.definir_partida_chegada_aleatorias():
             print("Falha ao definir partida/chegada no mapa procedural. Pode ser necessário ajustar a geração.")
        self.adicionar_vizinhos_para_todas_celulas()


    def desenhar(self, tela):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                self.grid[i][j].desenhar(tela)

    def obter_celula(self, linha, coluna):
        if 0 <= linha < self.num_linhas and 0 <= coluna < self.num_colunas:
            return self.grid[linha][coluna]
        return None

    def definir_tipo_base_celula(self, linha, coluna, novo_tipo_base):
        celula = self.obter_celula(linha, coluna)
        if celula:
            if novo_tipo_base == constantes.TIPO_PARTIDA:
                if self.ponto_partida and self.ponto_partida != (linha, coluna):
                    l_ant, c_ant = self.ponto_partida
                    if self.obter_celula(l_ant, c_ant)._tipo_base == constantes.TIPO_PARTIDA:
                        self.obter_celula(l_ant, c_ant).definir_tipo_base(constantes.TIPO_RUA)
                self.ponto_partida = (linha, coluna)
            elif novo_tipo_base == constantes.TIPO_CHEGADA:
                if self.ponto_chegada and self.ponto_chegada != (linha, coluna):
                    l_ant, c_ant = self.ponto_chegada
                    if self.obter_celula(l_ant, c_ant)._tipo_base == constantes.TIPO_CHEGADA:
                        self.obter_celula(l_ant, c_ant).definir_tipo_base(constantes.TIPO_RUA)
                self.ponto_chegada = (linha, coluna)
            
            if celula._tipo_base == constantes.TIPO_PARTIDA and novo_tipo_base != constantes.TIPO_PARTIDA:
                if self.ponto_partida == (linha, coluna): self.ponto_partida = None
            if celula._tipo_base == constantes.TIPO_CHEGADA and novo_tipo_base != constantes.TIPO_CHEGADA:
                if self.ponto_chegada == (linha, coluna): self.ponto_chegada = None
            
            celula.definir_tipo_base(novo_tipo_base)


    def definir_evento_trafego_celula(self, linha, coluna, tipo_evento):
        celula = self.obter_celula(linha, coluna)
        if celula and celula._tipo_base == constantes.TIPO_RUA :
            celula.definir_tipo_trafego_evento(tipo_evento)
            
    def limpar_evento_trafego_celula(self, linha, coluna):
        celula = self.obter_celula(linha, coluna)
        if celula:
            celula.limpar_evento_trafego()

    def adicionar_vizinhos_para_todas_celulas(self):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                celula_atual = self.grid[i][j]
                celula_atual.vizinhos = [] 
                if celula_atual.eh_navegavel(): 
                    self._encontrar_e_adicionar_vizinhos_para_celula(celula_atual)

    def _encontrar_e_adicionar_vizinhos_para_celula(self, celula):
        movimentos = [(0, 1), (0, -1), (1, 0), (-1, 0)] 
        for dr, dc in movimentos:
            viz_linha, viz_coluna = celula.linha + dr, celula.coluna + dc
            vizinho = self.obter_celula(viz_linha, viz_coluna)
            if vizinho and vizinho.eh_navegavel():
                celula.vizinhos.append(vizinho)

    def resetar_celulas_para_nova_busca(self):
        for i in range(self.num_linhas):
            for j in range(self.num_colunas):
                self.grid[i][j].resetar_para_caminho()
    
    def limpar_visualizacao_caminho_sugerido(self):
        for r in range(self.num_linhas):
            for c in range(self.num_colunas):
                celula = self.grid[r][c]
                if celula.faz_parte_caminho_sugerido:
                    celula.faz_parte_caminho_sugerido = False
                    celula.cor_caminho_sugerido = None
                    celula.atualizar_estado()

    def salvar_mapa(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'w') as f:
                f.write(f"{self.num_linhas}\n")
                f.write(f"{self.num_colunas}\n")
                f.write("None\n")
                f.write("None\n")
                
                for i in range(self.num_linhas):
                    tipos_base_linha = []
                    for j in range(self.num_colunas):
                        tipo_a_salvar = self.grid[i][j]._tipo_base
                        if tipo_a_salvar == constantes.TIPO_PARTIDA or tipo_a_salvar == constantes.TIPO_CHEGADA:
                            tipo_a_salvar = constantes.TIPO_RUA
                        tipos_base_linha.append(str(tipo_a_salvar))
                    f.write(",".join(tipos_base_linha) + "\n")
            print(f"Mapa salvo em {nome_arquivo}")
            return True
        except Exception as e:
            print(f"Erro ao salvar mapa: {e}")
            return False

    def carregar_mapa(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as f:
                num_linhas = int(f.readline().strip())
                num_colunas = int(f.readline().strip())
                
                if self.num_linhas != num_linhas or self.num_colunas != num_colunas:
                    self.num_linhas = num_linhas
                    self.num_colunas = num_colunas
                    constantes.NUM_LINHAS_MAPA_PADRAO = num_linhas
                    constantes.NUM_COLUNAS_MAPA_PADRAO = num_colunas
                    constantes.LARGURA_MAPA = num_colunas * constantes.TAMANHO_CELULA
                    constantes.ALTURA_MAPA = num_linhas * constantes.TAMANHO_CELULA
                    print(f"Mapa carregado com novas dimensões: {num_linhas}x{num_colunas}.")

                self._inicializar_mapa_vazio()

                f.readline()
                f.readline()
                
                for i in range(self.num_linhas):
                    tipos_base_linha = f.readline().strip().split(',')
                    for j in range(self.num_colunas):
                        tipo_base = int(tipos_base_linha[j])
                        self.grid[i][j].definir_tipo_base(tipo_base)
                
            print(f"Mapa carregado de {nome_arquivo}. Partida/Chegada serão definidos aleatoriamente.")
            self.adicionar_vizinhos_para_todas_celulas() 
            return True
        except Exception as e:
            print(f"Erro ao carregar mapa: {e}")
            return False