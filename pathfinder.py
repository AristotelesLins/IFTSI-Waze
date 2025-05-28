import constantes

class Pathfinder:
    def __init__(self, mapa):
        self.mapa = mapa

    def _calcular_heuristica(self, celula_a, celula_b):
        return abs(celula_a.linha - celula_b.linha) + abs(celula_a.coluna - celula_b.coluna)

    def _reconstruir_caminho(self, celula_final):
        caminho = []
        atual = celula_final
        while atual is not None:
            caminho.insert(0, atual)
            atual = atual.pai
        return caminho

    def _obter_direcao_oposta(self, direcao):
        if direcao == constantes.DIRECAO_CIMA: return constantes.DIRECAO_BAIXO
        if direcao == constantes.DIRECAO_BAIXO: return constantes.DIRECAO_CIMA
        if direcao == constantes.DIRECAO_ESQUERDA: return constantes.DIRECAO_DIREITA
        if direcao == constantes.DIRECAO_DIREITA: return constantes.DIRECAO_ESQUERDA
        return constantes.DIRECAO_NENHUMA

    def _calcular_direcao_para_vizinho(self, celula_atual, celula_vizinha):
        dr = celula_vizinha.linha - celula_atual.linha
        dc = celula_vizinha.coluna - celula_atual.coluna

        if dr == -1 and dc == 0: return constantes.DIRECAO_CIMA
        if dr == 1 and dc == 0: return constantes.DIRECAO_BAIXO
        if dr == 0 and dc == -1: return constantes.DIRECAO_ESQUERDA
        if dr == 0 and dc == 1: return constantes.DIRECAO_DIREITA
        return constantes.DIRECAO_NENHUMA

    def encontrar_caminho(self, linha_inicio, col_inicio, linha_fim, col_fim, direcao_carro_atual=constantes.DIRECAO_NENHUMA):
        self.mapa.resetar_celulas_para_nova_busca()
        self.mapa.adicionar_vizinhos_para_todas_celulas()

        celula_inicial = self.mapa.obter_celula(linha_inicio, col_inicio)
        celula_final = self.mapa.obter_celula(linha_fim, col_fim)

        if not celula_inicial or not celula_final or \
           not celula_inicial.eh_navegavel() or not celula_final.eh_navegavel():
            return None

        open_set = []
        closed_set_flags = [[False for _ in range(self.mapa.num_colunas)] for _ in range(self.mapa.num_linhas)]

        celula_inicial.g_custo = 0
        celula_inicial.h_custo = self._calcular_heuristica(celula_inicial, celula_final)
        celula_inicial.f_custo = celula_inicial.g_custo + celula_inicial.h_custo
        open_set.append(celula_inicial)

        iteracoes = 0
        max_iteracoes = self.mapa.num_linhas * self.mapa.num_colunas * 2

        while len(open_set) > 0 and iteracoes < max_iteracoes:
            iteracoes += 1
            
            atual = open_set[0]
            indice_atual_na_open_set = 0
            for i in range(1, len(open_set)):
                if open_set[i].f_custo < atual.f_custo:
                    atual = open_set[i]
                    indice_atual_na_open_set = i
                elif open_set[i].f_custo == atual.f_custo and open_set[i].h_custo < atual.h_custo:
                    atual = open_set[i]
                    indice_atual_na_open_set = i
            
            open_set.pop(indice_atual_na_open_set)
            closed_set_flags[atual.linha][atual.coluna] = True

            if atual == celula_final:
                return self._reconstruir_caminho(celula_final)

            for vizinho in atual.vizinhos:
                if closed_set_flags[vizinho.linha][vizinho.coluna]:
                    continue

                custo_mov_para_vizinho = vizinho.custo_movimento
                if atual == celula_inicial and direcao_carro_atual != constantes.DIRECAO_NENHUMA:
                    direcao_para_vizinho = self._calcular_direcao_para_vizinho(atual, vizinho)
                    direcao_oposta_carro = self._obter_direcao_oposta(direcao_carro_atual)

                    if direcao_para_vizinho == direcao_oposta_carro:
                        custo_mov_para_vizinho += 50
                g_custo_tentativo = atual.g_custo + custo_mov_para_vizinho

                if g_custo_tentativo < vizinho.g_custo:
                    vizinho.pai = atual
                    vizinho.g_custo = g_custo_tentativo
                    vizinho.h_custo = self._calcular_heuristica(vizinho, celula_final)
                    vizinho.f_custo = vizinho.g_custo + vizinho.h_custo

                    esta_na_open_set = False
                    for celula_na_open in open_set:
                        if celula_na_open == vizinho:
                            esta_na_open_set = True
                            break
                    if not esta_na_open_set:
                        open_set.append(vizinho)
        
        return None