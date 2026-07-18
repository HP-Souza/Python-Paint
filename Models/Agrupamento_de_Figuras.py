import math
from Models.Figura import Figura


def criar_figura_por_dados(item):
    mapeamento = {
        'Rabisco': Rabisco,
        'Linha': Linha,
        'Retangulo': Retangulo,
        'Oval': Oval,
        'Circulo': Circulo,
        'PoligonoReto': PoligonoReto,
        'PoligonoRegular': PoligonoRegular,
        'GrupoFiguras': GrupoFiguras
    }

    classe = mapeamento.get(item['tipo'])
    if classe is None:
        return None

    if hasattr(classe, 'from_dados'):
        return classe.from_dados(item)

    fig = classe(
        item['x1'],
        item['y1'],
        item.get('cor_pincel', ''),
        item.get('cor_preenchimento', '')
    )
    fig.x2 = item.get('x2', item['x1'])
    fig.y2 = item.get('y2', item['y1'])

    if hasattr(fig, 'pontos') and 'pontos' in item:
        fig.pontos = item['pontos']

    if hasattr(fig, 'fechado') and 'fechado' in item:
        fig.fechado = item['fechado']

    return fig


class Circulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                            outline=self.cor_pincel, fill=self.cor_preenchimento, dash=tracejado)
        
    def contem_ponto(self, x_clique, y_clique):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        return ((self.x1 - x_clique)**2 + (self.y1 - y_clique)**2)**0.5 <= raio

    def obter_limites(self):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        return (self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio)

class Linha(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_pincel, dash=tracejado)
    
    def contem_ponto(self, x_clique, y_clique):
        if not (
            min(self.x1, self.x2) - 5 <= x_clique <= max(self.x1, self.x2) + 5 and
            min(self.y1, self.y2) - 5 <= y_clique <= max(self.y1, self.y2) + 5
        ):
            return False

        # 2. Fórmula matemática da distância de um ponto a uma reta
        numerador = abs((self.y2 - self.y1) * x_clique - (self.x2 - self.x1) * y_clique + self.x2 * self.y1 - self.y2 * self.x1)
        denominador = ((self.y2 - self.y1)**2 + (self.x2 - self.x1)**2)**0.5
        
        if denominador == 0:  # Evita divisão por zero caso a linha seja um ponto único
            return False
            
        distancia = numerador / denominador
        return distancia <= 5


class Oval(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
        
    def contem_ponto(self, x_clique, y_clique):
        h = (self.x1 + self.x2) / 2
        k = (self.y1 + self.y2) / 2
        a = abs(self.x1 - self.x2) / 2
        b = abs(self.y1 - self.y2) / 2

        if a == 0 or b == 0:
            return False
        
        '''Equação da elipse ((x-h)^2 / a^2) + ((y-k)^2 / b^2) = 1, só que, nesse caso,o resultado tem que ser
          menor ou igual a 1, para que o clique conte dentro da elipse também.'''
        resultado = ((x_clique - h)**2 / a**2) + ((y_clique - k)**2 / b**2)
        
        return resultado <= 1
    

class PoligonoReto(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]
        self.fechado = False

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))
        self.x2, self.y2 = x, y

    def obter_limites(self):
        if not self.pontos:
            return super().obter_limites()
        xs = [x for x, _ in self.pontos]
        ys = [y for _, y in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

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
    
    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy

        self.pontos = [
            (x + dx, y + dy)
            for x, y in self.pontos
        ]
        
    def _distancia_ponto_segmento(self, x_clique, y_clique, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return ((x_clique - x1) ** 2 + (y_clique - y1) ** 2) ** 0.5

        t = ((x_clique - x1) * dx + (y_clique - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return ((x_clique - proj_x) ** 2 + (y_clique - proj_y) ** 2) ** 0.5

    def contem_ponto(self, x_clique, y_clique):
        if self.fechado:
            dentro = False
            n = len(self.pontos)
            for i in range(n):
                x1, y1 = self.pontos[i]
                x2, y2 = self.pontos[(i + 1) % n]
                if ((y1 > y_clique) != (y2 > y_clique)):
                    x_intersecao = x1 + (y_clique - y1) * (x2 - x1) / (y2 - y1)
                    if x_clique < x_intersecao:
                        dentro = not dentro
            return dentro

        tolerancia = 8
        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]
            if self._distancia_ponto_segmento(x_clique, y_clique, x1, y1, x2, y2) <= tolerancia:
                return True
        return False

    def obter_limites(self):
        if not self.pontos:
            return super().obter_limites()
        xs = [x for x, _ in self.pontos]
        ys = [y for _, y in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    @classmethod
    def from_dados(cls, item):
        fig = cls(
            item['x1'],
            item['y1'],
            item.get('cor_pincel', ''),
            item.get('cor_preenchimento', '')
        )
        fig.pontos = item.get('pontos', [])
        fig.fechado = item.get('fechado', False)
        if fig.pontos:
            fig.x2, fig.y2 = fig.pontos[-1]
        return fig


class PoligonoRegular(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento, lados=5):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.lados = max(3, lados)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.x2 = x_atual
        self.y2 = y_atual
        self.pontos = self._calcular_pontos()

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) < 3:
            return
        canvas.create_polygon(self.pontos, outline=self.cor_pincel,
                              fill=self.cor_preenchimento, dash=tracejado)

    def figura_incompleta(self):
        return self.x1 == self.x2 and self.y1 == self.y2

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.pontos = [(x + dx, y + dy) for x, y in self.pontos]

    def contem_ponto(self, x_clique, y_clique):
        dentro = False
        n = len(self.pontos)
        for i in range(n):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[(i + 1) % n]
            if ((y1 > y_clique) != (y2 > y_clique)):
                x_intersecao = x1 + (y_clique - y1) * (x2 - x1) / (y2 - y1)
                if x_clique < x_intersecao:
                    dentro = not dentro
        return dentro

    def _calcular_pontos(self):
        raio = ((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2) ** 0.5
        if raio == 0:
            return [(self.x1, self.y1)]

        angulo_inicial = math.atan2(self.y2 - self.y1, self.x2 - self.x1)

        pontos = []
        for i in range(self.lados):
            angulo = angulo_inicial + 2 * math.pi * i / self.lados
            x = self.x1 + math.cos(angulo) * raio
            y = self.y1 + math.sin(angulo) * raio
            pontos.append((x, y))
        return pontos

    def obter_limites(self):
        if not self.pontos:
            return super().obter_limites()
        xs = [x for x, _ in self.pontos]
        ys = [y for _, y in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    def para_dados(self):
        dados = super().para_dados()
        dados['lados'] = self.lados
        dados['pontos'] = self.pontos
        return dados

    @classmethod
    def from_dados(cls, item):
        fig = cls(
            item['x1'],
            item['y1'],
            item.get('cor_pincel', ''),
            item.get('cor_preenchimento', ''),
            item.get('lados', 5)
        )
        fig.x2 = item.get('x2', item['x1'])
        fig.y2 = item.get('y2', item['y1'])
        fig.pontos = item.get('pontos', fig._calcular_pontos())
        return fig


class Rabisco(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.pontos.append((x_atual, y_atual))
        self.x2, self.y2 = x_atual, y_atual

    def obter_limites(self):
        if not self.pontos:
            return super().obter_limites()
        xs = [x for x, _ in self.pontos]
        ys = [y for _, y in self.pontos]
        return min(xs), min(ys), max(xs), max(ys)

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_pincel, dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) <= 1
    
    def _distancia_ponto_segmento(self, x_clique, y_clique, x1, y1, x2, y2):
        dx = x2 - x1
        dy = y2 - y1
        if dx == 0 and dy == 0:
            return ((x_clique - x1) ** 2 + (y_clique - y1) ** 2) ** 0.5

        t = ((x_clique - x1) * dx + (y_clique - y1) * dy) / (dx * dx + dy * dy)
        t = max(0, min(1, t))
        proj_x = x1 + t * dx
        proj_y = y1 + t * dy
        return ((x_clique - proj_x) ** 2 + (y_clique - proj_y) ** 2) ** 0.5

    def contem_ponto(self, x_clique, y_clique):
        tolerancia = 8
        if len(self.pontos) < 2:
            return False

        for i in range(len(self.pontos) - 1):
            x1, y1 = self.pontos[i]
            x2, y2 = self.pontos[i + 1]
            if self._distancia_ponto_segmento(x_clique, y_clique, x1, y1, x2, y2) <= tolerancia:
                return True
        return False

    def mover(self, dx, dy):
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        self.pontos = [(x + dx, y + dy) for x, y in self.pontos]


class Retangulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_rectangle(
            self.x1,
            self.y1,
            self.x2,
            self.y2,
            outline=self.cor_pincel,
            fill=self.cor_preenchimento,
            dash=tracejado
        )

    def contem_ponto(self, x_clique, y_clique):
        return (
            min(self.x1, self.x2) <= x_clique <= max(self.x1, self.x2) and
            min(self.y1, self.y2) <= y_clique <= max(self.y1, self.y2)
        )


class GrupoFiguras(Figura):
    def __init__(self, figuras):
        super().__init__(0, 0, 'black', '')
        self.figuras = list(figuras)
        self.atualizar_limites()

    def atualizar_limites(self):
        if not self.figuras:
            self.x1 = self.y1 = self.x2 = self.y2 = 0
            return

        limites = [fig.obter_limites() for fig in self.figuras]
        self.x1 = min(l[0] for l in limites)
        self.y1 = min(l[1] for l in limites)
        self.x2 = max(l[2] for l in limites)
        self.y2 = max(l[3] for l in limites)

    def desenhar(self, canvas, tracejado=None):
        for figura in self.figuras:
            figura.desenhar(canvas, tracejado=tracejado)

    def contem_ponto(self, x_clique, y_clique):
        return any(figura.contem_ponto(x_clique, y_clique) for figura in self.figuras)

    def mover(self, dx, dy):
        for figura in self.figuras:
            figura.mover(dx, dy)
        self.atualizar_limites()

    def obter_limites(self):
        return self.x1, self.y1, self.x2, self.y2

    def figura_incompleta(self):
        return False

    def para_dados(self):
        dados = super().para_dados()
        dados['figuras'] = [figura.para_dados() for figura in self.figuras]
        return dados

    @classmethod
    def from_dados(cls, item):
        figuras = [criar_figura_por_dados(dado) for dado in item.get('figuras', [])]
        fig = cls([f for f in figuras if f is not None])
        fig.x2 = item.get('x2', fig.x2)
        fig.y2 = item.get('y2', fig.y2)
        return fig
        