from Models.Figura import Figura

class PoligonoLivre(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.pontos.append((x_atual,y_atual))

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) > 1:
            canvas.create_polygon(self.pontos, outline=self.cor_pincel,
                                  fill=self.cor_preenchimento, dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) <= 2
