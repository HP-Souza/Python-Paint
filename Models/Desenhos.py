import json
import os


class Desenhos:

    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.figura_selecionada = None
        self.figuras_selecionadas = []
        self.caminho_arquivo = "desenhos.json"

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