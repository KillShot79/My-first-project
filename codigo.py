import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pan
from tkinter import filedialog

#funcion para leer archivos csv
def cargar_csv():
    try:
        archivo=filedialog.askopenfilename(filetypes=[('CSV files','*.csv')],title='Selecciona un archivo CSV')
        if not archivo:
            return
        si=pan.read_csv(archivo)
        if 'Distancia' not in si.columns or 'Modulo' not in si.columns or 'Angulo' not in si.columns:
            resultado.config(text='El csv no tiene los datos necesarios.')
            return
        for widget in inputs.winfo_children():
            widget.destroy()
        entradas.clear()
        for i, row in si.iterrows():
            tk.Label(inputs, text=f'Fuerza {i+1}').grid(row=i, column=0, padx=0,pady=10)
            tk.Label(inputs, text='Distancia al punto de aplicacion de la fuerza(m)').grid(row=i, column=1)
            entry_d=tk.Entry(inputs, width=10)
            entry_d.grid(row=i, column=2)
            entry_d.insert(0, row['Distancia'])

            tk.Label(inputs, text='Modulo(N)').grid(row=i, column=3)
            entry_modulo=tk.Entry(inputs, width=10)
            entry_modulo.grid(row=i, column=4)
            entry_modulo.insert(0,row['Modulo'])

            tk.Label(inputs, text='Angulo').grid(row=i, column=5)
            entry_angle=tk.Entry(inputs,width=10)
            entry_angle.grid(row=i, column=6)
            entry_angle.insert(0, row['Angulo'])
            entradas.append((entry_d,entry_modulo,entry_angle))
        boton_calcular.pack(pady=10)
        resultado.config(text='Los datos del CSV han sido extraidos')
    except Exception as e:
        resultado.config(text=f'Error al extraer los datos: {e}')
#Creamos la ventana donde se ejecutara el programa mediante la libreria tkinter
ventana=tk.Tk()
ventana.title("Analisis de cuerpos en equilibrio")
ventana.geometry("1000x500")
etiqueta1=tk.Label(ventana, text="Antes de continuar fije un sistema coordenado para ingresar las fuerzas y utilice las medidas del " 
"sistema internacional")
etiqueta1.pack()

#Se pide la cantidad de fuerzas al usuario
tk.Label(ventana,text='¿Cuantas fuerzas actuan en el cuerpo?', pady=10).pack()
entry_n=tk.Entry(ventana)
entry_n.pack()

#creamos frames para organizar las entradas del usuario
inputs=tk.Frame(ventana)
inputs.pack()
entradas=[]
#funcion para crear los campos donde introducir los datos
def crear_campos():
    for widget in inputs.winfo_children():
        widget.destroy()
    entradas.clear()
    try:
        n=int(entry_n.get())
        if n<=0:
            resultado.config(text='Debe haber al menos una fuerza.')
            return
    except ValueError:
        resultado.config(text='Ingrese un numero valido de fuerzas')
        return
    for i in range(n):
        tk.Label(inputs, text=f'Fuerza {i+1}').grid(row=i,column=0, padx=5,pady=10)
        tk.Label(inputs, text=f'Distancia del punto de aplicacion de la fuerza al centro de masa(m): ').grid(row=i, column=1)
        entry_d=tk.Entry(inputs, width=10)
        entry_d.grid(row=i,column=2)

        tk.Label(inputs, text='Modulo (N):').grid(row=i,column=3)
        entry_modulo=(tk.Entry(inputs, width=10))
        entry_modulo.grid(row=i, column=4)

        tk.Label(inputs, text='Angulo(°)').grid(row=i, column=5)
        entry_angle=tk.Entry(inputs, width=10)
        entry_angle.grid(row=i,column=6)
        entradas.append((entry_d,entry_modulo,entry_angle))
    boton_calcular.pack(pady=10)

#funcion determinar el equilibrio y crear el grafico de los modulos de las fuerzas
def analisis_equilibrio():
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    sumx=0
    sumy=0
    sumtorque=0
    fuerzas=[]
    nro_fuerza=[]
    try:
        for i, (d,m,a) in enumerate(entradas):
            dpm=float(d.get()) #dcm es la distancia del centro de masa al punto de accion
            modulo=float(m.get())
            angulo=float(a.get())
            angulo_rad=np.radians(angulo)
            fuerzas.append(modulo)
            nro_fuerza.append(i+1)
            sumy+=modulo*np.sin(angulo_rad)
            sumx+=modulo*np.cos(angulo_rad)
            sumtorque+=modulo*np.sin(angulo_rad)*dpm

        if round(sumx,5)==0 and round(sumy,5)==0 and round(sumtorque,5)==0:
            resultado.config(text='El cuerpo se encuentra en equilibrio.')
        if round(sumx,5)==0 and round(sumy,5)==0 and round(sumtorque,5)!=0:
            resultado.config(text=f'Es necesaria un torque de {round(sumtorque,2)}Nm para que el cuerpo este en equilibrio.')
        if round(sumx,5)==0 and round(sumy,5)!=0 and round(sumtorque)==0:
            resultado.config(text=f'Es necesaria una fuerza en el eje y de {round(sumy,2)}N para que el cuerpo este en equilibrio.')
        if round(sumx,5)!=0 and round(sumy,5)==0 and round(sumtorque,5)==0:
            resultado.config(text=f'Es necesaria una fuerza de {round(sumx,2)}N en el eje x para que el cuerpo este en equilibrio.')
        if round(sumx,5)!=0 and round(sumy,5)!=0 and round(sumtorque,5)==0:
            resultado.config(text=f'Es necesaria una fuerza de ({round(sumx,2)},{round(sumy,2)})N para que el cuerpo este en equilibrio.')
        if round(sumx,5)!=0 and round(sumy,5)==0 and round(sumtorque,5)!=0:
            resultado.config(text=f'Son necesarios una fuerza de {round(sumx,2)}N en el eje x y un torque de {round(sumtorque,2)}Nm para que el cuerpo este en equilibrio.')
        if round(sumx,5)==0 and round(sumy,5)!=0 and round(sumtorque,5)!=0:
            resultado.config(text=f'Son necesarios una fuerza de {round(sumy,2)}N en el eje y y un torque de {round(sumtorque,2)}Nm para que el cuerpo este en equilibrio.')
        if round(sumx,5)!=0 and round(sumy,5)!=0 and round(sumtorque,5)!=0:
            resultado.config(text=f'Son necesarios una fuerza de ({round(sumx,2)},{round(sumy,2)})N y un torque de {round(sumtorque,2)}Nm para que el cuerpo este en equilibrio.')
    except ValueError:
        resultado.config(text='Ingrese los valores nuevamente')

    grafico=tk.Toplevel(ventana)
    grafico.title('Grafico de modulo de las fuerzas')
    fig,ax=plt.subplots()
    ax.bar(nro_fuerza,fuerzas, color='green')
    ax.set_title('Modulo de fuerzas')
    ax.set_xlabel('Fuerzas')
    ax.set_ylabel('Newtons (N)')
    grafico=FigureCanvasTkAgg(fig, master=grafico)
    grafico.draw()
    grafico.get_tk_widget().pack()

boton1=tk.Button(ventana, text='Comencemos', command=crear_campos)
boton1.pack(pady=10)
boton_calcular=tk.Button(ventana, text="Calcular el equilibrio", command=analisis_equilibrio)

resultado=tk.Label(ventana, text='')
resultado.pack(pady=10)

boton_csv=tk.Button(ventana, text='Cargar archivo CSV', command=cargar_csv)
boton_csv.pack(pady=5)
ventana.mainloop() 