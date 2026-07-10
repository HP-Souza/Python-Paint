from States.Ferramentas import Ferramentas
from Models.Agrupamento_de_Figuras import PoligonoReto
from Models.Desenhos import Desenhos


class EstadoPoligonoReto(Ferramentas):

    def clique_esquerdo(self, event):
        if self.controller.model.poligono_em_construcao is None:

            self.controller.model.poligono_em_construcao = PoligonoReto(
                event.x,
                event.y,
                self.controller.view.cor_pincel_var.get(),
                self.controller.view.cor_preenchimento_var.get()
            )
        

        elif (self.controller.model.poligono_em_construcao and len(self.controller.model.poligono_em_construcao.pontos) > 2
            and (self.controller.model.poligono_em_construcao.pontos[0][0] - 25 <= event.x <= self.controller.model.poligono_em_construcao.pontos[0][0] + 25)
            and (self.controller.model.poligono_em_construcao.pontos[0][1] - 25 <= event.y <= self.controller.model.poligono_em_construcao.pontos[0][1] + 25)):

            self.controller.model.poligono_em_construcao.fechado = True
            self.controller.model.adicionar_figura(self.controller.model.poligono_em_construcao)
            self.controller.model.poligono_em_construcao = None

        else:
            self.controller.model.poligono_em_construcao.adicionar_ponto(event.x,event.y)

    def atualizar_figura_nova(self, event):
        pass

    def incluir_figura_nova(self, event):
        pass

    def finalizar_poligono(self, event=None):
        if self.controller.model.poligono_em_construcao:

            if not self.controller.model.poligono_em_construcao.figura_incompleta():

                self.controller.model.poligono_em_construcao.fechado = True
                self.controller.model.adicionar_figura(self.controller.model.poligono_em_construcao)

            self.controller.model.poligono_em_construcao = None

    def atualizar_mouse(self, event):
        pass

    def iniciar_figura_nova(self, event):
        pass