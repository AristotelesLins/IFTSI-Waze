# Waze Particular (IFTSI-Waze)

## Descrição do Projeto

**Waze Particular** é um projeto desenvolvido para a disciplina de Algoritmos e Estruturas de Dados. Trata-se de um simulador de tráfego 2D onde o objetivo é guiar um veículo de um ponto de partida a um ponto de chegada em um mapa. O sistema sugere a melhor rota dinamicamente, considerando eventos de tráfego aleatórios (como congestionamentos e acidentes) que podem surgir e alterar as condições das vias.

O projeto permite que o usuário crie seus próprios mapas em um modo editor ou carregue mapas existentes. Ao iniciar a simulação, os pontos de partida e chegada são definidos aleatoriamente no mapa carregado/criado.

## Funcionalidades Principais

* **Criação e Edição de Mapas:**
    * Interface gráfica para desenhar ruas e construções (obstáculos).
    * Opção para salvar e carregar mapas personalizados.
* **Simulação de Tráfego Dinâmica:**
    * O usuário controla a direção de um veículo no mapa.
    * O sistema calcula e exibe a rota ótima sugerida do ponto atual do veículo até o destino.
    * A rota é colorida para indicar as condições de tráfego (livre, lento, muito lento, bloqueado).
* **Eventos Aleatórios:**
    * Geração de engarrafamentos (leve, moderado, pesado) e acidentes em locais aleatórios do mapa.
    * Os eventos alteram o custo de travessia das ruas e podem tornar trechos intransponíveis (acidentes).
* **Recálculo de Rotas:**
    * A rota sugerida é recalculada automaticamente quando eventos de tráfego impactam o percurso atual ou quando o veículo se desvia significativamente.
    * O usuário pode solicitar um recálculo manual.
* **Interface do Usuário:**
    * Painel com notificações sobre o status da rota, eventos de tráfego e instruções.
* **Algoritmo de Busca de Caminho:**
    * Utiliza o algoritmo A* (A-estrela) para encontrar o caminho de menor custo entre dois pontos, considerando os custos dinâmicos das células (ruas com tráfego).

## Tecnologias Utilizadas

* **Linguagem de Programação:** Python
* **Biblioteca Gráfica:** Pygame

## Como Executar o Projeto

### Pré-requisitos

* Python 3.x instalado ([python.org](https://www.python.org/))
* Pygame instalado:
    ```bash
    pip install pygame
    ```

### Execução

1.  Clone este repositório (ou baixe os arquivos):
    ```bash
    git clone [https://github.com/AristotelesLins/IFTSI-Waze.git](https://github.com/AristotelesLins/IFTSI-Waze.git)
    ```
    (Substitua pela URL correta do seu repositório após criá-lo)
2.  Navegue até a pasta do projeto:
    ```bash
    cd IFTSI-Waze
    ```
3.  Execute o arquivo principal:
    ```bash
    python main.py
    ```
    (Ou `python3 main.py` dependendo da sua configuração)

### Instruções do Jogo

**Tela de Menu Inicial:**
* **Criar Novo Mapa:** Inicia o modo editor com um mapa em branco.
* **Carregar 'cidade_salva.txt':** Carrega o último mapa salvo (ou o mapa padrão `cidade_salva.txt`).
* **Sair:** Fecha a aplicação.

**Modo Editor:**
* **Pincéis (selecionar com as teclas):**
    * `R`: Rua
    * `C`: Construção
    * `X`: Remover Evento de Tráfego (limpa engarrafamentos/acidentes da célula)
* **Mouse:** Clique com o botão esquerdo para aplicar o pincel selecionado.
* **Comandos:**
    * `S`: Salvar o mapa atual (como `cidade_salva.txt`).
    * `L`: Carregar o mapa `cidade_salva.txt`.
    * `Enter`: Iniciar a simulação com o mapa atual (partida e chegada serão definidas aleatoriamente).
    * `Esc`: Voltar para o Menu Inicial.

**Modo Simulação:**
* **Setas Direcionais:** Definem a direção para onde o carro tentará se mover.
* **Barra de Espaço:** Para o movimento automático do carro (ele para de tentar seguir na direção atual).
* **Comandos:**
    * `R`: Solicitar um recálculo manual da rota sugerida.
    * `Esc`: Voltar para o Modo Editor (o progresso da simulação é perdido, o mapa é mantido para edição).

## Estrutura do Projeto

* `main.py`: Arquivo principal, controla o loop do jogo, estados e interface.
* `mapa.py`: Define a classe `Mapa`, responsável pela grade, células e lógica de edição/carregamento.
* `celula.py`: Define a classe `Celula`, representando cada "quadrinho" do mapa.
* `carro.py`: Define a classe `Carro`, controlada pelo usuário.
* `pathfinder.py`: Implementa o algoritmo A* para busca de caminho.
* `eventos_trafego.py`: Gerencia a simulação de eventos aleatórios no mapa.
* `ui.py`: Controla o painel de informações/notificações.
* `constantes.py`: Armazena todas as constantes globais do jogo (cores, tamanhos, tipos, etc.).
* `assets/` (pasta): Contém recursos gráficos, como a imagem do carro (`carro_img.png`). (Crie esta pasta se usar a imagem).

## Autor

* Aristóteles Lins ([@AristotelesLins](https://github.com/AristotelesLins))
    *(Substitua pelo seu nome e link do GitHub)*

## Licença

*(Opcional: Se você adicionar uma licença ao seu projeto, mencione-a aqui. Ex: MIT License)*