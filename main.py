from tkinter import *
from tkinter import ttk

# Quando mouse é pressionado
def iniciar_figura_nova(event): 
    global figura_nova
    if tipo_figura_var.get() == 'Linha':
        figura_nova = ("linha", (event.x, event.y, event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif tipo_figura_var.get() == 'Rabisco':
        figura_nova = ("rabisco", [(event.x, event.y)], cor_pincel_var.get(), cor_preenche_var.get())
    elif tipo_figura_var.get() == 'Oval':
        figura_nova = ("oval", (event.x, event.y, event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif tipo_figura_var.get() == 'Retângulo':
        figura_nova = ("retângulo", (event.x, event.y, event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif tipo_figura_var.get() == 'Círculo':
        figura_nova = ("círculo", (event.x, event.y, event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())

# Quando mouse é movido com o botão pressionado
def atualizar_figura_nova(event):
    global figura_nova
    if figura_nova[0] == "rabisco":
        figura_nova[1].append((event.x, event.y))
    elif figura_nova[0] == "linha":
        figura_nova = ("linha", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif figura_nova[0] == "oval":
        figura_nova = ("oval", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif figura_nova[0] == "retângulo":
        figura_nova = ("retângulo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y), cor_pincel_var.get(), cor_preenche_var.get())
    elif figura_nova[0] == "círculo":
        raio = ((figura_nova[1][0] - figura_nova[1][2])**2 + (figura_nova[1][1] - figura_nova[1][3])**2)**0.5
        figura_nova = ("círculo", (figura_nova[1][0], figura_nova[1][1], event.x, event.y, raio), cor_pincel_var.get(), cor_preenche_var.get())
    desenhar_figuras()
    desenhar_figura_nova()

# Quando mouse é solto
def incluir_figura_nova(event): 
    if not incompleta(figura_nova): # para evitar incluir figuras incompletas, como uma linha sem comprimento ou um rabisco com um único ponto
        figuras.append(figura_nova) 
    desenhar_figuras()

def desenhar_figuras():
    canvas.delete("all")
    for fig, values, color, preenche in figuras:
        if fig == "linha":
            canvas.create_line(values[0], values[1], values[2], values[3], fill = color)
        elif fig == "rabisco":
            canvas.create_line(values, fill = color)
        elif fig == "oval":
            canvas.create_oval(values[0], values[1], values[2], values[3], outline = color, fill = preenche)
        elif fig == "retângulo":
            canvas.create_rectangle(values[0], values[1], values[2], values[3], outline = color, fill = preenche)
        elif fig == "círculo":
            canvas.create_oval(values[0]-values[4], values[1]-values[4], values[2]+values[4], values[3]+values[4], outline = color, fill = preenche)

def desenhar_figura_nova():
    fig, values, color, preenche = figura_nova
    if fig == "linha":
        canvas.create_line(values[0], values[1], values[2], values[3], dash=(4, 2), fill = color)
    elif fig == "rabisco":
        canvas.create_line(values, dash=(4, 2), fill = color)
    elif fig == "oval":
        canvas.create_oval(values[0], values[1], values[2], values[3], dash=(4, 2), outline = color, fill = preenche)
    elif fig == "retângulo":
        canvas.create_rectangle(values[0], values[1], values[2], values[3], dash=(4, 2), outline = color, fill = preenche)
    elif fig == "círculo":
            canvas.create_oval(values[0]-values[4], values[1]-values[4], values[2]+values[4], values[3]+values[4], outline = color, fill = preenche)

def incompleta(figura):
    fig, values, cor, preenche = figura
    if fig == "linha":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "rabisco":
        return len(values) <= 1
    elif fig == "oval":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "retângulo":
        return (values[0], values[1]) == (values[2], values[3])
    elif fig == "círculo":
        return (values[0], values[1]) == (values[2], values[3])



#******* MAIN *******#

figuras = []       # Todas as figuras desenhadas
figura_nova = None # Figura que está sendo desenhada, mas ainda não foi incluída em figuras
raio = None

root = Tk()
frame = Frame(root)
root.title("Python Paint")

# Widgets arranjados com Layout grid dentro de frame
paddings = {'padx': 5, 'pady': 5} 

#Menu de Formas
label = ttk.Label(frame,  text='Formas:')
label.grid(column=0, row=0, sticky=W, **paddings)

tipo_figura_var = StringVar(root) # Guarda o tipo de figura selecionado no Menu de formas
forma_menu = ttk.OptionMenu(frame, tipo_figura_var,
                             'Rabisco', 'Rabisco', 'Linha', 'Retângulo', 'Oval', 'Círculo' )
forma_menu.grid(column=1, row=0, sticky=W, **paddings)

# Menu de cores
label = ttk.Label(frame,  text='Cores:')
label.grid(column=2, row=0, sticky=W, **paddings)

cor_pincel_var = StringVar(root) # Guarda a cor atual do pincel, que é usada para desenhar as figuras
cor_menu = ttk.OptionMenu(frame, cor_pincel_var,
                             'black', 'black', 'red', 'green', 'blue', 'yellow')
cor_menu.grid(column=3, row=0, sticky=W, **paddings)

#Menu de Preenchimentos
label = ttk.Label(frame,  text='Preenchimento:')
label.grid(column=4, row=0, sticky=W, **paddings)

cor_preenche_var = StringVar(root) # Guarda a cor atual do pincel, que é usada para desenhar as figuras

preenche_menu = ttk.OptionMenu(frame, cor_preenche_var,
                             None, None, 'black', 'red', 'green', 'blue', 'yellow')
preenche_menu.grid(column=6, row=0, sticky=W, **paddings)


canvas = Canvas(frame, bg='white', width=1200, height=1200)
canvas.grid(column=0, row=1, columnspan=8, sticky=W, **paddings)

frame.pack()

# Eventos de mouse associados ao canvas - com seus callbacks
canvas.bind('<ButtonPress-1>', iniciar_figura_nova)
canvas.bind('<B1-Motion>', atualizar_figura_nova)
canvas.bind('<ButtonRelease-1>', incluir_figura_nova)

root.mainloop()