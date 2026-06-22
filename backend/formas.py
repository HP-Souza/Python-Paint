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
    
class Linha(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_pincel, dash=tracejado)

class Rabisco(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.pontos.append((x_atual,y_atual))

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_pincel, dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) <= 1

class Retangulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)

class Oval(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
        
class Circulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                           outline=self.cor_pincel, fill=self.cor_preenchimento, dash=tracejado)
        
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

class PoligonoReto(Figura):
    def __init__(self, x_inicial, y_inicial,
                 cor_pincel, cor_preenchimento):
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