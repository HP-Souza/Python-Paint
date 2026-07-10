import json
import os


class Desenhos:

    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.caminho_arquivo = "desenhos.json"

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar(self):
        self.figuras.clear()
        self.figura_nova = None
        self.poligono_em_construcao = None

    def para_dados(self):
        dados = []
        for figura in self.figuras:
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
        from Models.FigurasAgrupadas import Rabisco, Linha, Retangulo, Oval, Circulo, PoligonoLivre, PoligonoReto
        
        
        mapeamento = {
            'Rabisco': Rabisco,
            'Linha': Linha,
            'Retangulo': Retangulo,
            'Oval': Oval,
            'Circulo': Circulo,
            'PoligonoLivre': PoligonoLivre,
            'PoligonoReto': PoligonoReto
        }

        for item in dados:
            classe = mapeamento.get(item['tipo'])
            if classe:
                fig = classe(
                    item['x1'],
                    item['y1'],
                    item['cor_pincel'],
                    item['cor_preenchimento']
                )
                fig.x2 = item['x2']
                fig.y2 = item['y2']
                
                if 'pontos' in item:
                    fig.pontos = item['pontos']
                if 'fechado' in item:
                    fig.fechado = item['fechado']
                
                self.figuras.append(fig)

    def salvar(self):
        try:
            with open(self.caminho_arquivo, 'w') as f:
                json.dump(self.para_dados(), f)
        except Exception as arquivo:
            print(f"Erro ao salvar: {arquivo}")

    def carregar(self):
        if os.path.exists(self.caminho_arquivo):
            try:
                with open(self.caminho_arquivo, 'r') as f:
                    dados = json.load(f)
                    self.carregar_de_dados(dados)
            except Exception as arquivo:
                print(f"Erro ao carregar: {arquivo}")