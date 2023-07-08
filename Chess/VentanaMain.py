import tkinter as tk
from tkinter import messagebox
import subprocess

#acomodar esto por favor azcarate no entendí que pedo con esto T - T
def iniciar_partida():
    subprocess.Popen(["python", "ChessMain.py"])
    # messagebox.showinfo("Todo bien","Ejecutando partida...")
    ventana.destroy()

def mostrar_enunciado():
    enunciado = """Ajedrez loco

Si mantenemos las piezas del juego pero alteramos la mecánica del ajedrez y sus reglas nos encontramos con un buen montón de variantes entre las que una curiosa (en realidad todas lo son) es el ajedrez loco, del que una vez más hay otras variantes con ligeras modificaciones.

En esta variante lo más importante es que si capturamos una pieza rival la convertimos en nuestra (cambia de color) para colocarla donde queramos en nuestro tumo. Los peones y los caballos ganan relevancia en esta variante, y si uno captura una dama debe ser especialmente cuidadoso a la hora de recolocarla para que no se la capturen a él."""

    messagebox.showinfo("Enunciado del Proyecto", enunciado)


def acerca_de():
    info = "Proyecto realizado por:\n\n- Juan Camilo Azcarate Cardenas \n- Estefany Castro Agudelo \n- Valentina Hurtado García\n- Daniel Goméz suares \n\n Universidad del Valle \n Introducción a la inteligencia artificial \n 2023-1"
    messagebox.showinfo("Acerca de", info)




def create_gradient(canvas, x, y, width, height, color1, color2):
    # Calcular los incrementos de color para cada componente RGB
    r1, g1, b1 = canvas.winfo_rgb(color1)
    r2, g2, b2 = canvas.winfo_rgb(color2)
    r_increment = (r2 - r1) / height
    g_increment = (g2 - g1) / height
    b_increment = (b2 - b1) / height

    # Crear el degradado
    for i in range(height):
        # Calcular el color en la posición actual del degradado
        r = int(r1 + (r_increment * i))
        g = int(g1 + (g_increment * i))
        b = int(b1 + (b_increment * i))
        color = f"#{r:02x}{g:02x}{b:02x}"

        # Dibujar la línea en la posición actual del degradado
        canvas.create_line(x, y + i, x + width, y + i, fill=color)


# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Proyecto de Inteligencia Artificial")
ventana.geometry("500x500")

# Crear el lienzo para el degradado
canvas = tk.Canvas(ventana, width=500, height=500)
canvas.pack(fill=tk.BOTH, expand=True)

# Crear el degradado en el lienzo
create_gradient(canvas, 0, 250, 500, 500, "#263238", "#78909C")

# Frame para contener los botones y centrarlos
frame_botones = tk.Frame(ventana, bg="#B0BEC5")
frame_botones.pack(expand=True)

# Fuente para los botones
fuente = ("Times New Roman", 18, "bold")

# Función para abrir una nueva ventana de simulación
boton_simulacion = tk.Button(frame_botones, text="Empezar partida de ajedrez",
                             font=fuente, bg="#ECEFF1", command=iniciar_partida)
boton_simulacion.pack(pady=10)

# Función para mostrar el enunciado del proyecto
boton_enunciado = tk.Button(frame_botones, text="Mostrar Enunciado",
                            font=fuente, bg="#ECEFF1", command=mostrar_enunciado)
boton_enunciado.pack(pady=10)

# Función para mostrar Los integrantes del grupo
boton_acerca_de = tk.Button(
    frame_botones, text="Integrantes", font=fuente, bg="#ECEFF1", command=acerca_de)
boton_acerca_de.pack(pady=10)

# Centrar el frame de los botones en la ventana
frame_botones.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Ejecutar la aplicación
ventana.mainloop()


