from Models import PoligonoReto


class CanvasController:

    def __init__(self, view):
        self.view = view

    def finalizar_poligono(self, event=None):
        if self.view.poligono_em_construcao:

            if not self.view.poligono_em_construcao.figura_incompleta():

                self.view.poligono_em_construcao.fechado = True
                self.view.figuras.append(self.view.poligono_em_construcao)

            self.view.poligono_em_construcao = None
            self.atualizar_tela()

    def iniciar_figura_nova(self, event):
        forma = self.view.tipo_figura_var.get()
        cor = self.view.cor_pincel_var.get()
        preenchimento = self.view.cor_preenchimento_var.get()
        classe = self.view.mapeamento_formas[forma]

        self.view.figura_nova = classe(
            event.x,
            event.y,
            cor,
            preenchimento
        )

    def atualizar_figura_nova(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            return

        if self.view.figura_nova:
            self.view.figura_nova.atualizar_coordenadas(event.x,event.y)
            self.atualizar_tela()

    def apagar_tudo(self):
        self.view.canvas.delete("all")
        self.view.figuras.clear()

    def clique_esquerdo(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':

            if self.view.poligono_em_construcao is None:

                self.view.poligono_em_construcao = PoligonoReto(
                    event.x,
                    event.y,
                    self.view.cor_pincel_var.get(),
                    self.view.cor_preenchimento_var.get()
                )

            elif (self.view.poligono_em_construcao and not self.view.poligono_em_construcao.figura_incompleta()
                and (self.view.poligono_em_construcao.pontos[0][0] - 25<= event.x<= self.view.poligono_em_construcao.pontos[0][0] + 25)
                and (self.view.poligono_em_construcao.pontos[0][1] - 25<= event.y<= self.view.poligono_em_construcao.pontos[0][1] + 25)):

                self.view.poligono_em_construcao.fechado = True
                self.view.figuras.append(self.view.poligono_em_construcao)
                self.view.poligono_em_construcao = None

            else:
                self.view.poligono_em_construcao.adicionar_ponto(event.x,event.y)

            self.atualizar_tela()

        else:
            self.iniciar_figura_nova(event)

    def atualizar_mouse(self, event):
        self.view.mouse_x = event.x
        self.view.mouse_y = event.y

        if self.view.poligono_em_construcao:
            self.atualizar_tela()

    def incluir_figura_nova(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            return

        if (self.view.figura_nova and not self.view.figura_nova.figura_incompleta()):
            self.view.figuras.append(self.view.figura_nova)

        self.view.figura_nova = None
        self.atualizar_tela()

    def atualizar_tela(self):
        self.view.canvas.delete("all")

        for figura in self.view.figuras:
            figura.desenhar(self.view.canvas)

        if self.view.figura_nova:
            self.view.figura_nova.desenhar(
                self.view.canvas,
                tracejado=(4, 2)
            )

        if self.view.poligono_em_construcao:
            self.view.poligono_em_construcao.desenhar(
                self.view.canvas,
                tracejado=(4, 2)
            )

            if len(self.view.poligono_em_construcao.pontos) > 0:
                ultimo_x, ultimo_y = self.view.poligono_em_construcao.pontos[-1]

                self.view.canvas.create_line(
                    ultimo_x,
                    ultimo_y,
                    self.view.mouse_x,
                    self.view.mouse_y,
                    dash=(4, 2),
                    fill=self.view.poligono_em_construcao.cor_pincel
                )