from Models.Figura import Figura

class Circulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                            outline=self.cor_pincel, fill=self.cor_preenchimento, dash=tracejado)
        