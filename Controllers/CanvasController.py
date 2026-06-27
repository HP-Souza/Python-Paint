from Models.PoligonoReto import PoligonoReto
from Models.Desenhos import Desenhos


class CanvasController:

    def __init__(self, view):
        self.view = view

        self.figuras = Desenhos().figuras
        self.figura_nova = None
        self.poligono_em_construcao = None


        self.mouse_x = 0
        self.mouse_y = 0

    def vincular_eventos(self):

        self.view.canvas.bind('<ButtonPress-1>',self.clique_esquerdo)
        self.view.canvas.bind('<B1-Motion>',self.atualizar_figura_nova)
        self.view.canvas.bind('<ButtonRelease-1>',self.incluir_figura_nova)
        self.view.canvas.bind('<Button-3>',self.finalizar_poligono)
        self.view.canvas.bind('<Motion>',self.atualizar_mouse)
        self.view.botao_limpar.config(command=self.apagar_tudo)

    def finalizar_poligono(self, event=None):
        if self.poligono_em_construcao:

            if not self.poligono_em_construcao.figura_incompleta():

                self.poligono_em_construcao.fechado = True
                self.figuras.append(self.poligono_em_construcao)

            self.poligono_em_construcao = None
            self.atualizar_tela()

    def iniciar_figura_nova(self, event):
        forma = self.view.tipo_figura_var.get()
        cor = self.view.cor_pincel_var.get()
        preenchimento = self.view.cor_preenchimento_var.get()
        classe = self.view.mapeamento_formas[forma]

        self.figura_nova = classe(
            event.x,
            event.y,
            cor,
            preenchimento
        )

    def atualizar_figura_nova(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            return

        if self.figura_nova:
            self.figura_nova.atualizar_coordenadas(event.x,event.y)
            self.atualizar_tela()

    def apagar_tudo(self):
        self.view.canvas.delete("all")
        self.figuras.clear()

    def clique_esquerdo(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':

            if self.poligono_em_construcao is None:

                self.poligono_em_construcao = PoligonoReto(
                    event.x,
                    event.y,
                    self.view.cor_pincel_var.get(),
                    self.view.cor_preenchimento_var.get()
                )
            

            elif (self.poligono_em_construcao and len(self.poligono_em_construcao.pontos) > 2
                and (self.poligono_em_construcao.pontos[0][0] - 25 <= event.x <= self.poligono_em_construcao.pontos[0][0] + 25)
                and (self.poligono_em_construcao.pontos[0][1] - 25 <= event.y <= self.poligono_em_construcao.pontos[0][1] + 25)):

                self.poligono_em_construcao.fechado = True
                self.figuras.append(self.poligono_em_construcao)
                self.poligono_em_construcao = None

            else:
                self.poligono_em_construcao.adicionar_ponto(event.x,event.y)

            self.atualizar_tela()

        else:
            self.iniciar_figura_nova(event)

    def atualizar_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

        if self.poligono_em_construcao:
            self.atualizar_tela()

    def incluir_figura_nova(self, event):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            return

        if (self.figura_nova and not self.figura_nova.figura_incompleta()):
            self.figuras.append(self.figura_nova)

        self.figura_nova = None
        self.atualizar_tela()

    def atualizar_tela(self):
        self.view.canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(self.view.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar(
                self.view.canvas,
                tracejado=(4, 2)
            )

        if self.poligono_em_construcao:
            self.poligono_em_construcao.desenhar(
                self.view.canvas,
                tracejado=(4, 2)
            )

            if len(self.poligono_em_construcao.pontos) > 0:
                ultimo_x, ultimo_y = self.poligono_em_construcao.pontos[-1]

                self.view.canvas.create_line(
                    ultimo_x,
                    ultimo_y,
                    self.mouse_x,
                    self.mouse_y,
                    dash=(4, 2),
                    fill=self.poligono_em_construcao.cor_pincel
                )