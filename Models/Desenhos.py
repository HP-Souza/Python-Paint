import copy
import json
import os


class Desenhos:

    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_regular_em_construcao = None
        self.figura_selecionada = None
        self.figuras_selecionadas = []
        self.caminho_arquivo = "desenhos.json"
        self.area_transferencia = None
        self.contagem_colagens = 0 

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar_selecao(self):
        self.figuras_selecionadas = []
        self.figura_selecionada = None

    def definir_selecao(self, figuras):
        self.figuras_selecionadas = list(figuras)
        self.figura_selecionada = figuras[-1] if figuras else None

    def adicionar_a_selecao(self, figura):
        if figura not in self.figuras_selecionadas:
            self.figuras_selecionadas.append(figura)
            self.figura_selecionada = figura

    def remover_da_selecao(self, figura):
        if figura in self.figuras_selecionadas:
            self.figuras_selecionadas.remove(figura)
            self.figura_selecionada = self.figuras_selecionadas[-1] if self.figuras_selecionadas else None

    def remover_figura(self):
        if self.figuras_selecionadas:
            for figura in list(self.figuras_selecionadas):
                if figura in self.figuras:
                    self.figuras.remove(figura)
            self.limpar_selecao()
        elif self.figura_selecionada is not None:
            if self.figura_selecionada in self.figuras:
                self.figuras.remove(self.figura_selecionada)
            self.figura_selecionada = None

    def limpar(self):
        self.figuras.clear()
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.poligono_regular_em_construcao = None
        self.limpar_selecao()

    def para_dados(self):
        dados = []
        for figura in self.figuras:
            if hasattr(figura, 'para_dados'):
                dados.append(figura.para_dados())
            else:
                item = {
                    'tipo': figura.__class__.__name__,
                    'x1': figura.x1,
                    'y1': figura.y1,
                    'x2': figura.x2,
                    'y2': figura.y2,
                    'cor_pincel': figura.cor_pincel,
                    'cor_preenchimento': figura.cor_preenchimento
                }
                if hasattr(figura, 'pontos'):
                    item['pontos'] = figura.pontos
                if hasattr(figura, 'fechado'):
                    item['fechado'] = figura.fechado
                dados.append(item)
        return dados

    def carregar_de_dados(self, dados):
        from Models.Agrupamento_de_Figuras import criar_figura_por_dados

        for item in dados:
            fig = criar_figura_por_dados(item)
            if fig is not None:
                self.figuras.append(fig)

    def salvar(self, caminho=None):
        if caminho:
            self.caminho_arquivo = caminho

        try:
            with open(self.caminho_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.para_dados(), f, indent=2, ensure_ascii=False)
        except Exception as arquivo:
            print(f"Erro ao salvar: {arquivo}")

    def carregar(self, caminho=None):
        if caminho:
            self.caminho_arquivo = caminho

        if not os.path.exists(self.caminho_arquivo):
            return

        try:
            self.limpar()
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as f:
                dados = json.load(f)
                self.carregar_de_dados(dados)
        except Exception as arquivo:
            print(f"Erro ao carregar: {arquivo}")

    def mover_figuras_selecionadas(self, dx, dy):
        for figura in self.figuras_selecionadas:
            figura.mover(dx, dy)

    def selecionar_dentro_retangulo(self, x1, y1, x2, y2):
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        figuras_internas = []
        for figura in self.figuras:
            fx1, fy1, fx2, fy2 = figura.obter_limites()
            if not (fx2 < x1 or fx1 > x2 or fy2 < y1 or fy1 > y2):
                figuras_internas.append(figura)
        self.definir_selecao(figuras_internas)

    def copiar_selecionadas(self):
        if self.figuras_selecionadas:
            self.area_transferencia = [copy.deepcopy(f) for f in self.figuras_selecionadas]
        elif self.figura_selecionada:
            self.area_transferencia = [copy.deepcopy(self.figura_selecionada)]
        else:
            return
        self.contagem_colagens = 0

    def colar_area_transferencia(self, deslocamento=20):
        if not self.area_transferencia:
            return
        self.contagem_colagens += 1
        offset = deslocamento * self.contagem_colagens

        novas = []
        for figura in self.area_transferencia:
            nova = copy.deepcopy(figura)
            nova.mover(offset, offset)
            self.figuras.append(nova)
            novas.append(nova)
        self.definir_selecao(novas)

    def agrupar_selecionadas(self):
        if len(self.figuras_selecionadas) > 1:
            from Models.Agrupamento_de_Figuras import GrupoFiguras
            grupo = self.figuras_selecionadas.copy()
            for figura in grupo:
                self.figuras.remove(figura)
            grupo_figuras = GrupoFiguras(grupo)
            self.adicionar_figura(grupo_figuras)
            self.definir_selecao([grupo_figuras])

    def _grupos_selecionados(self):
        grupos = []
        grupo_atual = []
        for i, figura in enumerate(self.figuras):
            if figura in self.figuras_selecionadas:
                grupo_atual.append(i)
            else:
                if grupo_atual:
                    grupos.append(grupo_atual)
                    grupo_atual = []
        if grupo_atual:
            grupos.append(grupo_atual)
        return grupos

    def mover_frente_1(self):
        if not self.figuras_selecionadas:
            return
        for grupo in self._grupos_selecionados():
            s, e = grupo[0], grupo[-1]
            if e < len(self.figuras) - 1:
                bloco = self.figuras[s:e + 2]          # bloco + vizinho de depois
                self.figuras[s:e + 2] = [bloco[-1]] + bloco[:-1]

    def mover_tras_1(self):
        if not self.figuras_selecionadas:
            return
        for grupo in self._grupos_selecionados():
            s, e = grupo[0], grupo[-1]
            if s > 0:
                bloco = self.figuras[s - 1:e + 1]       # vizinho de antes + bloco
                self.figuras[s - 1:e + 1] = bloco[1:] + [bloco[0]]

    def mover_frente_todos(self):
        if not self.figuras_selecionadas:
            return
        selecionadas_em_ordem = [f for f in self.figuras if f in self.figuras_selecionadas]
        for figura in selecionadas_em_ordem:
            self.figuras.remove(figura)
            self.figuras.append(figura)

    def mover_tras_todos(self):
        if not self.figuras_selecionadas:
            return
        selecionadas_em_ordem = [f for f in self.figuras if f in self.figuras_selecionadas]
        for figura in reversed(selecionadas_em_ordem):
            self.figuras.remove(figura)
            self.figuras.insert(0, figura)

    def mudar_cor_selecionadas(self, cor_pincel, cor_preenchimento):
        alvo = self.figuras_selecionadas or (
            [self.figura_selecionada] if self.figura_selecionada else []
        )
        for figura in alvo:
            figura.cor_pincel = cor_pincel
            figura.cor_preenchimento = cor_preenchimento