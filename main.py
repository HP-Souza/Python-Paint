from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_pincel_var.get())
    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)], cor_pincel_var.get())
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_pincel_var.get())
    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retângulo", (event.x, event.y, event.x, event.y), cor_pincel_var.get())

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "linha":
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get())
    elif figura_nova[0] == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get())
    elif figura_nova[0] == "retângulo":
        figura_nova = ("retângulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get())
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, cor in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill = cor)
        elif fig == "rabisco":
            canvas.create_line(values, fill = cor)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline = cor)
        elif fig == "retângulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline = cor)

def desenhar_figura_nova():
    fig, values, color = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill = color)
    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill = color)
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline =color)
    elif fig == "retângulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline = color)

def incompleta(figura):
    fig, values, cor = figura
    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "rabisco":
        return len(values) <= 1
    elif fig == "oval":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "retângulo":
        return (values[0], values[1]) == (values[2], values[3])



#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras

root = Tk()
frame = Frame(root)
root.title("Python Paint")

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

# label
label = ttk.Label(frame,  text='Formas:')
label.grid(column=0, row=0, sticky=W, **paddings)

# Menu de formas
tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no Menu de formas
forma_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Rabisco', 'Rabisco', 'Linha', 'Oval', 'Retângulo')
forma_menu.grid(column=1, row=0, sticky=W, **paddings)

# Menu de cores
cor_pincel_var = StringVar(root) # Guarda a cor atual do pincel, que é usada para desenhar as figuras
cor_menu = ttk.OptionMenu(frame, cor_pincel_var,
                             'black', 'black', 'red', 'green', 'blue', 'yellow')
cor_menu.grid(column=2, row=0, sticky=W, **paddings)


canvas = Canvas(frame, bg='white', width=600, height=600)
canvas.grid(column=0, row=1, columnspan=3, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()