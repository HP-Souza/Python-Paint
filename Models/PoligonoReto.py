from Models.Figura import Figura

class PoligonoReto(Figura):
    def __init__(self, x_inicial, y_inicial,cor_pincel, cor_preenchimento):
        super().__init__(x_inicial,y_inicial,cor_pincel,cor_preenchimento)

        self.pontos = [(x_inicial, y_inicial)]
        self.fechado = False

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=None):

        if len(self.pontos) < 2:
            return

        if self.fechado:
            canvas.create_polygon(
                self.pontos, outline=self.cor_pincel,
                fill=self.cor_preenchimento, dash=tracejado)

        else:
            canvas.create_line(
                self.pontos, fill=self.cor_pincel,
                dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) < 3