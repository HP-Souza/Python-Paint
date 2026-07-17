from States.Ferramentas import Ferramentas
import copy


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
        figura_encontrada = None
        for figura in reversed(self.controller.model.figuras):
            if figura.contem_ponto(event.x, event.y):
                figura_encontrada = figura
                break

        if figura_encontrada:
            if event.state & 0x0004:
                self.controller.model.adicionar_a_selecao(figura_encontrada)
            elif figura_encontrada in self.controller.model.figuras_selecionadas:
                pass
            else:
                self.controller.model.definir_selecao([figura_encontrada])

            self.arrastando = True
            self.dentro_retangulo = False
            self.ultimo_x = event.x
            self.ultimo_y = event.y
            self.selecao_rect = None
            self.inicio_rect = None
        elif self.controller.model.figuras_selecionadas:
            limites = [figura.obter_limites() for figura in self.controller.model.figuras_selecionadas]
            x1 = min(l[0] for l in limites)
            y1 = min(l[1] for l in limites)
            x2 = max(l[2] for l in limites)
            y2 = max(l[3] for l in limites)

            if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                self.arrastando = True
                self.dentro_retangulo = False
                self.ultimo_x = event.x
                self.ultimo_y = event.y
                self.selecao_rect = None
                self.inicio_rect = None
                return

            self.controller.model.limpar_selecao()
            self.arrastando = False
            self.dentro_retangulo = True
            self.inicio_rect = (event.x, event.y)
            self.selecao_rect = (event.x, event.y, event.x, event.y)
        else:
            self.controller.model.limpar_selecao()
            self.arrastando = False
            self.dentro_retangulo = True
            self.inicio_rect = (event.x, event.y)
            self.selecao_rect = (event.x, event.y, event.x, event.y)

    def atualizar_figura_nova(self, event):
        if self.arrastando and self.controller.model.figuras_selecionadas:
            dx = event.x - self.ultimo_x
            dy = event.y - self.ultimo_y
            for selecionada in self.controller.model.figuras_selecionadas:
                selecionada.mover(dx, dy)
            self.ultimo_x = event.x
            self.ultimo_y = event.y
        elif self.dentro_retangulo and self.inicio_rect is not None:
            x1, y1 = self.inicio_rect
            self.selecao_rect = (x1, y1, event.x, event.y)

    def incluir_figura_nova(self, event):
        if self.dentro_retangulo and self.inicio_rect and self.selecao_rect:
            x1, y1, x2, y2 = self.selecao_rect
            x1, x2 = sorted([x1, x2])
            y1, y2 = sorted([y1, y2])
            figuras_internas = []

            for figura in self.controller.model.figuras:
                fx1, fy1, fx2, fy2 = figura.obter_limites()
                if not (fx2 < x1 or fx1 > x2 or fy2 < y1 or fy1 > y2):
                    figuras_internas.append(figura)

            self.controller.model.definir_selecao(figuras_internas)

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
        if self.controller.model.figuras_selecionadas:
            self.controller.model.area_transferencia = [copy.deepcopy(fig) for fig in self.controller.model.figuras_selecionadas]
        elif self.controller.model.figura_selecionada:
            self.controller.model.area_transferencia = [copy.deepcopy(self.controller.model.figura_selecionada)]

    def colar(self, event=None):
        if not getattr(self.controller.model, 'area_transferencia', None):
            return
        novas = []
        for figura in self.controller.model.area_transferencia:
            nova = copy.deepcopy(figura)
            nova.mover(20, 20)
            self.controller.model.figuras.append(nova)
            novas.append(nova)
        self.controller.model.definir_selecao(novas)

    def agrupar_figuras(self, event=None):
        if len(self.controller.model.figuras_selecionadas) > 1:
            grupo = self.controller.model.figuras_selecionadas.copy()
            for figura in grupo:
                self.controller.model.figuras.remove(figura)
            from Models.Agrupamento_de_Figuras import GrupoFiguras
            grupo_figuras = GrupoFiguras(grupo)
            self.controller.model.adicionar_figura(grupo_figuras)
            self.controller.model.definir_selecao([grupo_figuras])

    def mover_frente_1(self):
        if not self.controller.model.figuras_selecionadas:
            return
        ultima = self.controller.model.figuras_selecionadas[-1]
        i = self.controller.model.figuras.index(ultima)
        if i < len(self.controller.model.figuras) - 1:
            self.controller.model.figuras[i], self.controller.model.figuras[i + 1] = \
                self.controller.model.figuras[i + 1], self.controller.model.figuras[i]

    def mover_tras_1(self):
        if not self.controller.model.figuras_selecionadas:
            return
        ultima = self.controller.model.figuras_selecionadas[-1]
        i = self.controller.model.figuras.index(ultima)
        if i > 0:
            self.controller.model.figuras[i], self.controller.model.figuras[i - 1] = \
                self.controller.model.figuras[i - 1], self.controller.model.figuras[i]

    def mover_frente_todos(self):
        if not self.controller.model.figuras_selecionadas:
            return
        for figura in self.controller.model.figuras_selecionadas:
            if figura in self.controller.model.figuras:
                self.controller.model.figuras.remove(figura)
                self.controller.model.figuras.append(figura)

    def mover_tras_todos(self):
        if not self.controller.model.figuras_selecionadas:
            return
        for figura in list(self.controller.model.figuras_selecionadas):
            if figura in self.controller.model.figuras:
                self.controller.model.figuras.remove(figura)
                self.controller.model.figuras.insert(0, figura)

    def mudar_cor(self, event=None):
        if self.controller.model.figuras_selecionadas:
            for figura in self.controller.model.figuras_selecionadas:
                figura.cor_pincel = self.controller.view.cor_pincel_var.get()
                figura.cor_preenchimento = self.controller.view.cor_preenchimento_var.get()
        elif self.controller.model.figura_selecionada:
            figura = self.controller.model.figura_selecionada
            figura.cor_pincel = self.controller.view.cor_pincel_var.get()
            figura.cor_preenchimento = self.controller.view.cor_preenchimento_var.get()
