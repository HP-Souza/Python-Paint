from Models.Figura import Figura

class Retangulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
