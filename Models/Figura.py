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

    def desenhar(self, canvas, tracejado=None):
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

    def obter_limites(self):
        return (
            min(self.x1, self.x2),
            min(self.y1, self.y2),
            max(self.x1, self.x2),
            max(self.y1, self.y2)
        )

    def para_dados(self):
        dados = {
            'tipo': self.__class__.__name__,
            'x1': self.x1,
            'y1': self.y1,
            'x2': self.x2,
            'y2': self.y2,
            'cor_pincel': self.cor_pincel,
            'cor_preenchimento': self.cor_preenchimento
        }
        return dados

    @classmethod
    def from_dados(cls, item):
        obj = cls(
            item['x1'],
            item['y1'],
            item.get('cor_pincel', ''),
            item.get('cor_preenchimento', '')
        )
        obj.x2 = item.get('x2', item['x1'])
        obj.y2 = item.get('y2', item['y1'])
        return obj