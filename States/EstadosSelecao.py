from States.Ferramentas import Ferramentas

class EstadoSelecao(Ferramentas):

        def __init__(self, controller):
            super().__init__(controller)

            self.arrastando = False
            self.ultimo_x = 0
            self.ultimo_y = 0

        def clique_esquerdo(self, event):

            self.controller.model.figura_selecionada = None

            for figura in reversed(self.controller.model.figuras):

                if figura.contem_ponto(event.x, event.y):
                    self.controller.model.figura_selecionada = figura
                    self.arrastando = True
                    self.ultimo_x = event.x
                    self.ultimo_y = event.y
                    break

        def atualizar_figura_nova(self, event):

            if not self.arrastando:
                return

            figura = self.controller.model.figura_selecionada

            if figura:
                dx = event.x - self.ultimo_x
                dy = event.y - self.ultimo_y
                figura.mover(dx, dy)
                self.ultimo_x = event.x
                self.ultimo_y = event.y

        def incluir_figura_nova(self, event):
            self.arrastando = False

        def finalizar_poligono(self, event=None):
            pass

        def atualizar_mouse(self, event):
            pass

        def iniciar_figura_nova(self, event):
            pass