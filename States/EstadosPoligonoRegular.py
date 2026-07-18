from States.Ferramentas import Ferramentas
from Models.Agrupamento_de_Figuras import PoligonoRegular


class EstadoPoligonoRegular(Ferramentas):

    LADOS_INICIAIS = 3

    def clique_esquerdo(self, event):
        poligono = self.controller.model.poligono_regular_em_construcao

        if poligono is None:
            poligono = PoligonoRegular( 
                event.x,
                event.y,
                self.controller.view.cor_pincel_var.get(),
                self.controller.view.cor_preenchimento_var.get(),
                lados=self.LADOS_INICIAIS
            )
            self.controller.model.poligono_regular_em_construcao = poligono
        else:
            poligono.lados += 1

    def finalizar_poligono(self, event=None):
        poligono = self.controller.model.poligono_regular_em_construcao

        if poligono and not poligono.figura_incompleta():
            self.controller.model.adicionar_figura(poligono)

        self.controller.model.poligono_regular_em_construcao = None

    def atualizar_figura_nova(self, event):
        pass

    def incluir_figura_nova(self, event):
        pass

    def atualizar_mouse(self, event):
        poligono = self.controller.model.poligono_regular_em_construcao
        if poligono:
            poligono.atualizar_coordenadas(event.x, event.y)

    def iniciar_figura_nova(self, event):
        pass

    def copiar(self, event=None):
        pass

    def colar(self, event=None):
        pass

    def mover_frente_1(self, event):
        pass

    def mover_tras_1(self, event):
        pass

    def mover_frente_todos(self, event):
        pass

    def mover_tras_todos(self, event):
        pass

    def mudar_cor(self, event=None):
        pass

    def agrupar_figuras(self, event=None):
        pass