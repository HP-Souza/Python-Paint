from States.Ferramentas import Ferramentas


class EstadoDesenho2Pontos(Ferramentas):

    def iniciar_figura_nova(self, event):
        forma = self.controller.view.tipo_figura_var.get()
        cor = self.controller.view.cor_pincel_var.get()
        preenchimento = self.controller.view.cor_preenchimento_var.get()
        classe = self.controller.view.mapeamento_formas[forma]

        self.controller.model.figura_nova = classe(
            event.x,
            event.y,
            cor,
            preenchimento
        )

    def atualizar_figura_nova(self, event):
        if self.controller.model.figura_nova:
            self.controller.model.figura_nova.atualizar_coordenadas(event.x,event.y)

    def incluir_figura_nova(self, event):
        if (self.controller.model.figura_nova and not self.controller.model.figura_nova.figura_incompleta()):
            self.controller.model.adicionar_figura(self.controller.model.figura_nova)

        self.controller.model.figura_nova = None

    def clique_esquerdo(self, event):
        self.iniciar_figura_nova(event)

    def finalizar_poligono(self, event=None):
        pass

    def atualizar_mouse(self, event):
        pass