from States.Ferramentas import Ferramentas
import copy

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

        def copiar(self, event=None):
            if self.controller.model.figura_selecionada:
                self.area_transferencia = copy.deepcopy(
                    self.controller.model.figura_selecionada
                )

        def colar(self, event=None):
            if self.area_transferencia:
                nova = copy.deepcopy(self.area_transferencia)
                nova.mover(self.mouse_x, self.mouse_y)
                self.controller.model.figuras.append(nova)
                self.controller.model.figura_selecionada = nova

        def mover_frente(self):
            figura = self.controller.model.figura_selecionada

            if figura is None:
                return

            i = self.controller.model.figuras.index(figura)

            if i < len(self.controller.model.figuras) - 1:
                self.controller.model.figuras[i], self.controller.model.figuras[i + 1] = \
                    self.controller.model.figuras[i + 1], self.controller.model.figuras[i]

                
        def mover_tras(self):

            figura = self.controller.model.figura_selecionada

            if figura is None:
                return

            indice = self.controller.model.figuras.index(figura)

            if indice > 0:
                self.controller.model.figuras[indice], self.controller.model.figuras[indice-1] = \
                    self.controller.model.figuras[indice-1], self.controller.model.figuras[indice]
                
        def mudar_cor(self, event=None):

            figura = self.controller.model.figura_selecionada

            if figura is None:
                return

            figura.cor_pincel = self.controller.view.cor_pincel_var.get()
            figura.cor_preenchimento = self.controller.view.cor_preenchimento_var.get()