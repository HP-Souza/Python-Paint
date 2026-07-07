import tkinter as tk
from Views.CanvasView import CanvasView
from Models.Desenhos import Desenhos
from Controllers.CanvasController import CanvasController


janela = tk.Tk()
model = Desenhos()
view = CanvasView(janela, model)
controller = CanvasController(model, view)
view.set_controller(controller)
janela.mainloop()