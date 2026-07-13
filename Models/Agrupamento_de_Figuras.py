from Models.Figura import Figura

class Circulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                            outline=self.cor_pincel, fill=self.cor_preenchimento, dash=tracejado)
        
    def contem_ponto(self, x_clique, y_clique):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5

        if ((self.x1 - x_clique)**2 + (self.y1 - y_clique)**2)**0.5 <= raio :
            return True
        return False

class Linha(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_pincel, dash=tracejado)
    
    def contem_ponto(self, x_clique, y_clique):
        # 1. Primeiro verificamos se o clique está dentro da caixa limite da linha (com uma folga de 5px)
        if not (min(self.x1, self.x2) - 5 <= x_clique <= max(self.x1, self.x2) + 5 and \
                min(self.y1, self.y2) - 5 <= y_clique <= max(self.y1, self.y2) + 5):
            return False

        # 2. Fórmula matemática da distância de um ponto a uma reta
        numerador = abs((self.y2 - self.y1) * x_clique - (self.x2 - self.x1) * y_clique + self.x2 * self.y1 - self.y2 * self.x1)
        denominador = ((self.y2 - self.y1)**2 + (self.x2 - self.x1)**2)**0.5
        
        if denominador == 0:  # Evita divisão por zero caso a linha seja um ponto único
            return False
            
        distancia = numerador / denominador
        return distancia <= 5  # Retorna True se o clique foi a até 5 pixels de distância da linha


class Oval(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
        
    def contem_ponto(self, x_clique, y_clique):
        #centro da elipse, h referente ao eixo x e k ao eixo y:
        h = (self.x1 + self.x2) / 2
        k = (self.y1 + self.y2) / 2
        
        #semieixos, a é referente à largura e b à altura:
        a = abs(self.x1 - self.x2) / 2
        b = abs(self.y1 - self.y2) / 2
        
        if a == 0 or b == 0:  
            return False
        
        '''Equação da elipse ((x-h)^2 / a^2) + ((y-k)^2 / b^2) = 1, só que, nesse caso,o resultado tem que ser
          menor ou igual a 1, para que o clique conte dentro da elipse também.'''
        resultado = ((x_clique - h)**2 / a**2) + ((y_clique - k)**2 / b**2)
        
        return resultado <= 1
        

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
    
    def contem_ponto(self, x_clique, y_clique):
    # Definimos uma margem de tolerância de 6 pixels para facilitar o clique
        tolerancia = 6
        # Varre todos os pontos guardados na lista do rabisco
        for px, py in self.pontos:
            # Calcula a distância simples até o ponto atual
            distancia = ((px - x_clique)**2 + (py - y_clique)**2)**0.5
            if distancia <= tolerancia:
                return True
        return False    
    
    
    

class Retangulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
    
    def contem_ponto(self, x_clique, y_clique):
        if (max(self.x1, self.x2) >= x_clique >= min(self.x1, self.x2)) and (max(self.y1, self.y2) >= y_clique >= min(self.y1, self.y2)):
            return True
        return False
        