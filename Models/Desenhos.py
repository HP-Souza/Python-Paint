class Desenhos:

    def __init__(self):
        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None

    def adicionar_figura(self, figura):
        self.figuras.append(figura)

    def limpar(self):
        self.figuras.clear()
        self.figura_nova = None
        self.poligono_em_construcao = None