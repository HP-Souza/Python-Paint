class Figura:
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        self.x1 = x_inicial
        self.y1 = y_inicial
        self.x2 = x_inicial
        self.y2 = y_inicial
        self.cor_pincel = cor_pincel
        self.cor_preenchimento = cor_preenchimento

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.x2 = x_atual
        self.y2 = y_atual

    def desenho(self, canvas, tracejado=None):
        pass

    def figura_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)
    
    def contem_ponto(self, x_clique, y_clique):
        pass

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy