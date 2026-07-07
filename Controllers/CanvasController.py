from Models.Desenhos import Desenhos
from States.EstadosDesenho2Pontos import EstadoDesenho2Pontos
from States.EstadosPoligonoReto import EstadoPoligonoReto


class CanvasController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.mouse_x = 0
        self.mouse_y = 0

        self.estado = EstadoDesenho2Pontos(self)
        self.view.tipo_figura_var.trace_add('write', self.alternar_estado)

    def alternar_estado(self, *args):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            self.estado = EstadoPoligonoReto(self)
        else:
            self.estado = EstadoDesenho2Pontos(self)

    def vincular_eventos(self):

        self.view.canvas.bind('<ButtonPress-1>',self.clique_esquerdo)
        self.view.canvas.bind('<B1-Motion>',self.atualizar_figura_nova)
        self.view.canvas.bind('<ButtonRelease-1>',self.incluir_figura_nova)
        self.view.canvas.bind('<Button-3>',self.finalizar_poligono)
        self.view.canvas.bind('<Motion>',self.atualizar_mouse)
        self.view.botao_limpar.config(command=self.apagar_tudo)

    def finalizar_poligono(self, event=None):
        self.estado.finalizar_poligono(event)
        self.view.atualizar()

    def iniciar_figura_nova(self, event):
        self.estado.iniciar_figura_nova(event)

    def atualizar_figura_nova(self, event):
        self.estado.atualizar_figura_nova(event)
        self.view.atualizar()

    def apagar_tudo(self):
        self.model.limpar()
        self.view.atualizar()

    def clique_esquerdo(self, event):
        self.estado.clique_esquerdo(event)
        self.view.atualizar()

    def atualizar_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.estado.atualizar_mouse(event)
        self.view.atualizar()

    def incluir_figura_nova(self, event):
        self.estado.incluir_figura_nova(event)
        self.view.atualizar()