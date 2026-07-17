import tkinter as tk
from tkinter import ttk
from Models.Agrupamento_de_Figuras import Rabisco, Linha, Retangulo, Oval, Circulo, PoligonoReto, PoligonoRegular
from Controllers.CanvasController import CanvasController


class CanvasView:

    def __init__(self, janela_raiz, model):

        self.janela = janela_raiz
        self.model = model
        self.janela.title("Python Paint")
        self.controller = None

        self.mapeamento_formas = {
            'Rabisco': Rabisco,
            'Linha': Linha,
            'Retângulo': Retangulo,
            'Oval': Oval,
            'Círculo': Circulo,
            'Poligono Reto': PoligonoReto,
            'Poligono Regular': PoligonoRegular,
            'Seleção': 'Seleção'
        }

        self.configurar_interface()

    def set_controller(self, controller):
        self.controller = controller
        self.controller.vincular_eventos()

    def configurar_interface(self):

        self.frame = ttk.Frame(self.janela)
        self.frame.pack(padx=6, pady=6)

        self.tipo_figura_var = tk.StringVar(value='Rabisco')
        self.cor_pincel_var = tk.StringVar(value='black')
        self.cor_preenchimento_var = tk.StringVar(value='')

        ttk.Label(self.frame,text='Formas:').grid(column=0, row=0)
        ttk.OptionMenu(self.frame,self.tipo_figura_var,
                    'Rabisco',*self.mapeamento_formas.keys()).grid(column=1, row=0)

        ttk.Label(self.frame,text='Cores:').grid(column=2, row=0)
        ttk.OptionMenu(self.frame,self.cor_pincel_var,
                    'black','black','red','green','blue','yellow').grid(column=3, row=0)

        ttk.Label(self.frame,text='Preenchimento:').grid(column=4, row=0)
        ttk.OptionMenu(self.frame,self.cor_preenchimento_var,
                    '','','black','red','green','blue','yellow').grid(column=5, row=0)

        self.botao_abrir = ttk.Button(self.frame, text='Abrir')
        self.botao_abrir.grid(column=6, row=0, padx=(0, 4))

        self.botao_salvar = ttk.Button(self.frame, text='Salvar')
        self.botao_salvar.grid(column=7, row=0, padx=(0, 4))

        self.botao_salvar_como = ttk.Button(self.frame, text='Salvar como')
        self.botao_salvar_como.grid(column=8, row=0, padx=(0, 4))

        self.botao_limpar = ttk.Button(self.frame,text='Limpar tela')
        self.botao_limpar.grid(column=9,row=0)

        self.canvas = tk.Canvas(self.frame,bg='white',width=2400,height=1600)
        self.canvas.grid(column=0,row=1,columnspan=20)

    def atualizar(self):
        self.canvas.delete("all")

        for figura in self.model.figuras:
            figura.desenhar(self.canvas)
            if figura in self.model.figuras_selecionadas:
                figura.desenhar(self.canvas, tracejado=(5, 2))

        if self.model.figura_nova:
            self.model.figura_nova.desenhar(
                self.canvas,
                tracejado=(4, 2)
            )

        if self.model.figuras_selecionadas:
            group_bounds = [figura.obter_limites() for figura in self.model.figuras_selecionadas]

            if len(group_bounds) == 1:
                try:
                    x1, y1, x2, y2 = group_bounds[0]
                    self.canvas.create_rectangle(
                        x1 - 4,
                        y1 - 4,
                        x2 + 4,
                        y2 + 4,
                        outline='blue',
                        width=2,
                        dash=(4, 2)
                    )
                except Exception:
                    pass
            else:
                x1 = min(b[0] for b in group_bounds)
                y1 = min(b[1] for b in group_bounds)
                x2 = max(b[2] for b in group_bounds)
                y2 = max(b[3] for b in group_bounds)
                self.canvas.create_rectangle(
                    x1 - 6,
                    y1 - 6,
                    x2 + 6,
                    y2 + 6,
                    outline='navy',
                    width=2
                )

        if self.model.poligono_em_construcao:
            self.model.poligono_em_construcao.desenhar(
                self.canvas,
                tracejado=(4, 2)
            )

            if len(self.model.poligono_em_construcao.pontos) > 0:
                ultimo_x, ultimo_y = self.model.poligono_em_construcao.pontos[-1]

                self.canvas.create_line(
                    ultimo_x,
                    ultimo_y,
                    self.controller.mouse_x,
                    self.controller.mouse_y,
                    dash=(4, 2),
                    fill=self.model.poligono_em_construcao.cor_pincel
                )

        if hasattr(self.controller, 'estado') and getattr(self.controller.estado, 'selecao_rect', None):
            x1, y1, x2, y2 = self.controller.estado.selecao_rect
            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                outline='blue',
                dash=(3, 2),
                width=1
            )
