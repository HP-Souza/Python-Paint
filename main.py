import tkinter as tk
from Views.CanvasView import CanvasView
from Models.Desenhos import Desenhos
from Controllers.CanvasController import CanvasController

janela = tk.Tk()
model = Desenhos()
model.carregar()

view = CanvasView(janela, model)
controller = CanvasController(model, view)
view.set_controller(controller)

def on_close():
    model.salvar()
    janela.destroy()

janela.protocol("WM_DELETE_WINDOW", on_close)
janela.mainloop()