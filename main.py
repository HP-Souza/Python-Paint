import tkinter as tk
from tkinter import ttk

class Figura:
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        self.x1 = x_inicial
        self.y1 = y_inicial
        self.x2 = x_inicial
        self.y2 = y_inicial
        self.cor_pincel = cor_pincel
        self.cor_preenchimento = cor_preenchimento

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.x2 = x_atual
        self.y2 = y_atual

    def desenho(self, canvas, tracejado=None):
        pass

    def figura_incompleta(self):
        return (self.x1, self.y1) == (self.x2, self.y2)
    
class Linha(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.cor_pincel, dash=tracejado)

class Rabisco(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.pontos.append((x_atual,y_atual))

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) > 1:
            canvas.create_line(self.pontos, fill=self.cor_pincel, dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) <= 1

class Retangulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)

class Oval(Figura):
    def desenhar(self, canvas, tracejado=None):
        canvas.create_oval(self.x1, self.y1, self.x2, self.y2,outline=self.cor_pincel,
                          fill=self.cor_preenchimento, dash=tracejado)
        
class Circulo(Figura):
    def desenhar(self, canvas, tracejado=None):
        raio = ((self.x1 - self.x2)**2 + (self.y1 - self.y2)**2)**0.5
        canvas.create_oval(self.x1 - raio, self.y1 - raio, self.x1 + raio, self.y1 + raio, 
                           outline=self.cor_pincel, fill=self.cor_preenchimento, dash=tracejado)
        
class PoligonoLivre(Figura):
    def __init__(self, x_inicial, y_inicial, cor_pincel, cor_preenchimento):
        super().__init__(x_inicial, y_inicial, cor_pincel, cor_preenchimento)
        self.pontos = [(x_inicial, y_inicial)]

    def atualizar_coordenadas(self, x_atual, y_atual):
        self.pontos.append((x_atual,y_atual))

    def desenhar(self, canvas, tracejado=None):
        if len(self.pontos) > 1:
            canvas.create_polygon(self.pontos, outline=self.cor_pincel,
                                  fill=self.cor_preenchimento, dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) <= 2

class PoligonoReto(Figura):
    def __init__(self, x_inicial, y_inicial,
                 cor_pincel, cor_preenchimento):
        super().__init__(x_inicial,y_inicial,cor_pincel,cor_preenchimento)

        self.pontos = [(x_inicial, y_inicial)]
        self.fechado = False

    def adicionar_ponto(self, x, y):
        self.pontos.append((x, y))

    def desenhar(self, canvas, tracejado=None):

        if len(self.pontos) < 2:
            return

        if self.fechado:
            canvas.create_polygon(
                self.pontos, outline=self.cor_pincel,
                fill=self.cor_preenchimento, dash=tracejado)

        else:
            canvas.create_line(
                self.pontos, fill=self.cor_pincel,
                dash=tracejado)

    def figura_incompleta(self):
        return len(self.pontos) < 3
        
        
class PaintTkinter:
    def __init__(self, janela_raiz):

        self.janela = janela_raiz
        self.janela.title("Python Paint")

        self.figuras = []
        self.figura_nova = None
        self.poligono_em_construcao = None
        self.mouse_x = 0
        self.mouse_y = 0

        self.mapeamento_formas = {'Rabisco': Rabisco,
                       'Linha': Linha,
                       'Retângulo': Retangulo,
                       'Oval': Oval,
                       'Círculo': Circulo,
                       'Poligono Livre': PoligonoLivre,
                       'Poligono Reto': PoligonoReto
                       }
        
        self.configurar_interface()

        self.vincular_eventos()

    def configurar_interface(self):
        self.frame = ttk.Frame(self.janela)
        self.frame.pack(padx=6, pady=6)

        self.tipo_figura_var = tk.StringVar(value='Rabisco')
        self.cor_pincel_var = tk.StringVar(value='black')
        self.cor_preenchimento_var = tk.StringVar(value=None)

        ttk.Label(self.frame, text='Formas:').grid(column=0, row=0, sticky=tk.W, padx=6)
        self.forma_menu = ttk.OptionMenu(self.frame, self.tipo_figura_var, 'Rabisco',
                                          *self.mapeamento_formas.keys())
        self.forma_menu.grid(column=1, row=0, sticky=tk.W, padx=6)

        ttk.Label(self.frame, text='Cores:').grid(column=2, row=0, sticky=tk.W, padx=6)
        self.cor_menu = ttk.OptionMenu(self.frame, self.cor_pincel_var, 'black',
                                        'black', 'red', 'green', 'blue', 'yellow')
        self.cor_menu.grid(column=3, row=0, sticky=tk.W, padx=6)

        ttk.Label(self.frame, text='Preenchimento:').grid(column=4, row=0, sticky=tk.W, padx=6)
        self.preenche_menu = ttk.OptionMenu(self.frame, self.cor_preenchimento_var, None,
                                             None, 'black', 'red', 'green', 'blue', 'yellow')
        self.preenche_menu.grid(column=5, row=0, sticky=tk.W, padx=6)

        ttk.Button(self.frame, text='Limpar tela', command=self.apagar_tudo).grid(column=6, row=0, sticky=tk.W, padx=6)

        self.canvas = tk.Canvas(self.frame, bg='white', width=1200, height=800)
        self.canvas.grid(column=0, row=1, columnspan=7, sticky=tk.W, pady=6)
    
    def vincular_eventos(self):
        self.canvas.bind('<ButtonPress-1>', self.clique_esquerdo)
        self.canvas.bind('<B1-Motion>', self.atualizar_figura_nova)
        self.canvas.bind('<ButtonRelease-1>', self.incluir_figura_nova)
        self.canvas.bind('<Button-3>', self.finalizar_poligono)
        self.canvas.bind('<Motion>', self.atualizar_mouse)

    def clique_esquerdo(self, event):

        if self.tipo_figura_var.get() == 'Poligono Reto':

            if self.poligono_em_construcao is None:

                self.poligono_em_construcao = PoligonoReto(
                    event.x,
                    event.y,
                    self.cor_pincel_var.get(),
                    self.cor_preenchimento_var.get()
                )

            else:

                self.poligono_em_construcao.adicionar_ponto(
                    event.x,
                    event.y
                )

            self.atualizar_tela()

        else:
            self.iniciar_figura_nova(event)

    def finalizar_poligono(self, event):

        if self.poligono_em_construcao:

            if not self.poligono_em_construcao.figura_incompleta():

                self.poligono_em_construcao.fechado = True

                self.figuras.append(
                    self.poligono_em_construcao
                )

            self.poligono_em_construcao = None

            self.atualizar_tela()

    def atualizar_mouse(self, event):

        self.mouse_x = event.x
        self.mouse_y = event.y

        if self.poligono_em_construcao:
            self.atualizar_tela()

    def iniciar_figura_nova(self, event):
        forma_selecionada = self.tipo_figura_var.get()
        cor = self.cor_pincel_var.get()
        preenchimento = self.cor_preenchimento_var.get()

        classe_da_formas = self.mapeamento_formas[forma_selecionada]
        self.figura_nova = classe_da_formas(event.x, event.y, cor, preenchimento)

    def atualizar_figura_nova(self, event):
        if self.tipo_figura_var.get() == 'Poligono Reto':
            return

        if self.figura_nova:
            self.figura_nova.atualizar_coordenadas(event.x, event.y)
            
            self.atualizar_tela()
    
    def incluir_figura_nova(self, event):
        if self.tipo_figura_var.get() == 'Poligono Reto':
            return

        if self.figura_nova and not self.figura_nova.figura_incompleta():
            self.figuras.append(self.figura_nova)
        
        self.figura_nova = None
        self.atualizar_tela()

    def atualizar_tela(self):

        self.canvas.delete("all")

        for figura in self.figuras:
            figura.desenhar(self.canvas)

        if self.figura_nova:
            self.figura_nova.desenhar(
                self.canvas,
                tracejado=(4, 2)
            )

        if self.poligono_em_construcao:

            self.poligono_em_construcao.desenhar(
                self.canvas,
                tracejado=(4, 2)
            )

            if len(self.poligono_em_construcao.pontos) > 0:

                ultimo_x, ultimo_y = \
                    self.poligono_em_construcao.pontos[-1]

                self.canvas.create_line(
                    ultimo_x,
                    ultimo_y,
                    self.mouse_x,
                    self.mouse_y,
                    dash=(4, 2),
                    fill=self.poligono_em_construcao.cor_pincel
                )
    
    def apagar_tudo(self):
        self.canvas.delete("all")
        self.figuras = []


janela = tk.Tk()
app = PaintTkinter(janela)
janela.mainloop()
