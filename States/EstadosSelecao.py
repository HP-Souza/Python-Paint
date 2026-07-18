from States.Ferramentas import Ferramentas


class EstadoSelecao(Ferramentas):

    def __init__(self, controller):
        super().__init__(controller)
        self.arrastando = False
        self.ultimo_x = 0
        self.ultimo_y = 0
        self.selecao_rect = None
        self.inicio_rect = None
        self.dentro_retangulo = False

    def clique_esquerdo(self, event):
        model = self.controller.model
        figura_encontrada = None
        for figura in reversed(model.figuras):
            if figura.contem_ponto(event.x, event.y):
                figura_encontrada = figura
                break

        if figura_encontrada:
            if event.state & 0x0004:
                model.adicionar_a_selecao(figura_encontrada)
            elif figura_encontrada in model.figuras_selecionadas:
                pass
            else:
                model.definir_selecao([figura_encontrada])

            self.arrastando = True
            self.dentro_retangulo = False
            self.ultimo_x, self.ultimo_y = event.x, event.y
            self.selecao_rect = None
            self.inicio_rect = None

        elif model.figuras_selecionadas:
            limites = [figura.obter_limites() for figura in model.figuras_selecionadas]
            x1 = min(l[0] for l in limites)
            y1 = min(l[1] for l in limites)
            x2 = max(l[2] for l in limites)
            y2 = max(l[3] for l in limites)

            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.arrastando = True
                self.dentro_retangulo = False
                self.ultimo_x, self.ultimo_y = event.x, event.y
                self.selecao_rect = None
                self.inicio_rect = None
                return

            model.limpar_selecao()
            self.arrastando = False
            self.dentro_retangulo = True
            self.inicio_rect = (event.x, event.y)
            self.selecao_rect = (event.x, event.y, event.x, event.y)
        else:
            model.limpar_selecao()
            self.arrastando = False
            self.dentro_retangulo = True
            self.inicio_rect = (event.x, event.y)
            self.selecao_rect = (event.x, event.y, event.x, event.y)

    def atualizar_figura_nova(self, event):
        model = self.controller.model
        if self.arrastando and model.figuras_selecionadas:
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y
            model.mover_figuras_selecionadas(dx, dy)
            self.ultimo_x, self.ultimo_y = event.x, event.y
        elif self.dentro_retangulo and self.inicio_rect is not None:
            x1, y1 = self.inicio_rect
            self.selecao_rect = (x1, y1, event.x, event.y)

    def incluir_figura_nova(self, event):
        if self.dentro_retangulo and self.inicio_rect and self.selecao_rect:
            x1, y1, x2, y2 = self.selecao_rect
            self.controller.model.selecionar_dentro_retangulo(x1, y1, x2, y2)

        self.arrastando = False
        self.dentro_retangulo = False
        self.inicio_rect = None
        self.selecao_rect = None

    def finalizar_poligono(self, event=None):
        pass

    def atualizar_mouse(self, event):
        pass

    def iniciar_figura_nova(self, event):
        pass

    def copiar(self, event=None):
        self.controller.model.copiar_selecionadas()

    def colar(self, event=None):
        self.controller.model.colar_area_transferencia()

    def agrupar_figuras(self, event=None):
        self.controller.model.agrupar_selecionadas()

    def mover_frente_1(self):
        self.controller.model.mover_frente_1()

    def mover_tras_1(self):
        self.controller.model.mover_tras_1()

    def mover_frente_todos(self):
        self.controller.model.mover_frente_todos()

    def mover_tras_todos(self):
        self.controller.model.mover_tras_todos()

    def mudar_cor(self, event=None):
        self.controller.model.mudar_cor_selecionadas(
            self.controller.view.cor_pincel_var.get(),
            self.controller.view.cor_preenchimento_var.get()
        )
