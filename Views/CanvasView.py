import tkinter as tk
from tkinter import ttk
from Models.Rabisco import Rabisco
from Models.Linha import Linha
from Models.Retangulo import Retangulo
from Models.Oval import Oval
from Models.Circulo import Circulo
from Models.PoligonoLivre import PoligonoLivre
from Models.PoligonoReto import PoligonoReto
from Controllers.CanvasController import CanvasController


class CanvasView:

    def __init__(self, janela_raiz):

        self.janela = janela_raiz
        self.janela.title("Python Paint")

        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None

        self.mouse_x = 0
        self.mouse_y = 0

        self.mapeamento_formas = {
            'Rabisco': Rabisco,
            'Linha': Linha,
            'Retângulo': Retangulo,
            'Oval': Oval,
            'Círculo': Circulo,
            'Poligono Livre': PoligonoLivre,
            'Poligono Reto': PoligonoReto
        }

        self.configurar_interface()
        self.controller = CanvasController(self)
        self.vincular_eventos()

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

        self.botao_limpar = ttk.Button(self.frame,text='Limpar tela')
        self.botao_limpar.grid(column=6,row=0)

        self.canvas = tk.Canvas(self.frame,bg='white',width=2400,height=1600)
        self.canvas.grid(column=0,row=1,columnspan=20)

    def vincular_eventos(self):

        self.canvas.bind('<ButtonPress-1>',self.controller.clique_esquerdo)
        self.canvas.bind('<B1-Motion>',self.controller.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>',self.controller.incluir_figura_nova)
        self.canvas.bind('<Button-3>',self.controller.finalizar_poligono)
        self.canvas.bind('<Motion>',self.controller.atualizar_mouse)
        self.botao_limpar.config(command=self.controller.apagar_tudo)