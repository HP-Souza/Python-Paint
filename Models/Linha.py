from Models.Figura import Figura

class Linha(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_pincel, dash=tracejado)
