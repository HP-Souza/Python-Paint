import os
import tkinter as tk
from tkinter import filedialog
from Models.Desenhos import Desenhos
from States.EstadosDesenho2Pontos import EstadoDesenho2Pontos
from States.EstadosPoligonoReto import EstadoPoligonoReto
from States.EstadosSelecao import EstadoSelecao


class CanvasController:

    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.mouse_x = 0
        self.mouse_y = 0
        self.area_transferencia = None

        self.estado = EstadoDesenho2Pontos(self)
        self.view.tipo_figura_var.trace_add('write', self.alternar_estado)
        self.view.cor_pincel_var.trace_add("write", self.mudar_cor)
        self.view.cor_preenchimento_var.trace_add("write", self.mudar_cor)

    def alternar_estado(self, *args):
        if self.view.tipo_figura_var.get() == 'Poligono Reto':
            self.estado = EstadoPoligonoReto(self)
        elif self.view.tipo_figura_var.get() == 'Seleção':
            self.estado = EstadoSelecao(self)
        else:
            self.estado = EstadoDesenho2Pontos(self)

    def salvar_arquivo(self):
        if self.model.caminho_arquivo:
            self.model.salvar(self.model.caminho_arquivo)
        else:
            self.salvar_como()
        self.view.atualizar()

    def salvar_como(self):
        caminho = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON Files', '*.json'), ('All Files', '*.*')],
            title='Salvar desenho como'
        )
        if caminho:
            self.model.salvar(caminho)
            self.view.atualizar()

    def abrir_arquivo(self):
        caminho = filedialog.askopenfilename(
            defaultextension='.json',
            filetypes=[('JSON Files', '*.json'), ('All Files', '*.*')],
            title='Abrir desenho'
        )
        if caminho:
            self.model.carregar(caminho)
            self.view.atualizar()

    def vincular_eventos(self):

        self.view.canvas.bind('<ButtonPress-1>',self.clique_esquerdo)
        self.view.canvas.bind('<B1-Motion>',self.atualizar_figura_nova)
        self.view.canvas.bind('<ButtonRelease-1>',self.incluir_figura_nova)
        self.view.canvas.bind('<Button-3>',self.finalizar_poligono)
        self.view.canvas.bind('<Motion>',self.atualizar_mouse)
        self.view.janela.bind("<Delete>", self.deletar_figura)
        self.view.janela.bind("<Control-c>", self.copiar)
        self.view.janela.bind("<Control-v>", self.colar)
        self.view.janela.bind("<Control-g>", self.agrupar_figuras)
        self.view.janela.bind("<Up>", self.mover_frente_1)
        self.view.janela.bind("<Down>", self.mover_tras_1)
        self.view.janela.bind("<Right>", self.mover_frente_todos)
        self.view.janela.bind("<Left>", self.mover_tras_todos)
        self.view.botao_limpar.config(command=self.apagar_tudo)
        self.view.botao_salvar.config(command=self.salvar_arquivo)
        self.view.botao_salvar_como.config(command=self.salvar_como)
        self.view.botao_abrir.config(command=self.abrir_arquivo)

    def finalizar_poligono(self, event=None):
        self.estado.finalizar_poligono(event)
        self.view.atualizar()

    def iniciar_figura_nova(self, event):
        self.estado.iniciar_figura_nova(event)

    def atualizar_figura_nova(self, event):
        self.estado.atualizar_figura_nova(event)
        self.view.atualizar()

    def apagar_tudo(self):
        self.model.limpar()
        self.view.atualizar()

    def clique_esquerdo(self, event):
        self.estado.clique_esquerdo(event)
        self.view.atualizar()

    def atualizar_mouse(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        self.estado.atualizar_mouse(event)
        self.view.atualizar()

    def incluir_figura_nova(self, event):
        self.estado.incluir_figura_nova(event)
        self.view.atualizar()
    
    def selecionar_figura(self, event):
        self.estado.clique_esquerdo(event)
        self.view.atualizar()

    def deletar_figura(self, event=None):
        self.model.remover_figura()
        self.view.atualizar()

    def copiar(self, event=None):
        self.estado.copiar(event)
        self.view.atualizar()

    def colar(self, event=None):
        self.estado.colar(event)
        self.view.atualizar()

    def mover_frente_1(self, event=None):
        self.estado.mover_frente_1()
        self.view.atualizar()

    def mover_tras_1(self, event=None):
        self.estado.mover_tras_1()
        self.view.atualizar()

    def mover_frente_todos(self, event=None):
        self.estado.mover_frente_todos()
        self.view.atualizar()

    def mover_tras_todos(self, event=None):
        self.estado.mover_tras_todos()
        self.view.atualizar()

    def agrupar_figuras(self, event=None):
        self.estado.agrupar_figuras(event)
        self.view.atualizar()

    def mudar_cor(self, *args, event=None):
        self.estado.mudar_cor(event)
        self.view.atualizar()
