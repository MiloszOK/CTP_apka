import tkinter as tk
from PIL import Image, ImageTk
import tkinter.filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style
import numpy as np
import pandas as pd

# ------------ TWORZENIE OKNA ------------- #


window = tk.Tk()
window.iconbitmap('pngimg.ico')
window.title('Najwspanialsza apka CTP w tej galaktyce!')
window.geometry('460x400')

matplotlib.style.use('fivethirtyeight')

fig = plt.figure(constrained_layout=True)
fig.canvas.manager.set_window_title('Wykres')
ax1 = fig.add_subplot(1, 1, 1)
fileread = 0

nazwa_var = tk.StringVar()
typ_var = tk.StringVar()
zakres_dol_var = tk.IntVar()
zakres_gora_var = tk.IntVar()
syg_dol_var = tk.IntVar()
syg_gora_var = tk.IntVar()

bg = tk.PhotoImage(file='koks.png')
bg_label = tk.Label(window, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --------------------- TOTALNE GŁUPOTY NIE RUSZAĆ! --------------------- #

def animationn():
  global current_frame, loop

  image = object11[current_frame]

  cwiczenie_1.configure(image=image)
  current_frame = (current_frame + 1) % frames1  # Reset to 0 using modulo

  loop = window.after(50, animationn)  # Schedule next animation frame

# ------------------ FUNKCJE --------------- #


def plot(i):
    global fileread
    if fileread == 0:
        fileread = tk.filedialog.askopenfile()
    else:
        with open(fileread.name) as file:
            df = pd.read_csv(file, sep='    ', engine='python')
            aa = pd.DataFrame(df)
            if 'exp' in globals():
                bb = aa.transform(lambda x: x * exp + b)
                beta = [bb.at[y, 'U [V]'] for y in range(0, len(bb))]
            else:
                beta = [aa.at[y, 'U [V]'] for y in range(0, len(aa))]
            alpha = [aa.at[i, 't [s]'] for i in range(0, len(aa))]
            ax1.clear()
            plt.plot(alpha, beta)
            if 'exp' in globals():
                plt.ylabel('obr')
                plt.title('Wykres obr/t')
            else:
                plt.ylabel('U [V]')
                plt.title('Wykres U/t')
            plt.xlabel('t [s]')


def show():
    anim = animation.FuncAnimation(fig, func=plot, interval=3000, frames=10, repeat=True)
    plt.show()


def submit():
    nazwa = nazwa_var.get()
    typ = typ_var.get()

    global exp,b
    exp = ((zakres_gora_var.get()-zakres_dol_var.get())/(syg_gora_var.get()-syg_dol_var.get()))
    b = zakres_dol_var.get() - syg_dol_var.get()*exp
    print(exp, b)
    nazwa_var.set('')
    typ_var.set('')
    zakres_dol_var.set('')
    syg_dol_var.set('')
    zakres_gora_var.set('')
    syg_gora_var.set('')

def unsubmit():
    if 'exp' in globals():
        global exp
        del exp


cwiczenie_1 = tk.Label(window, image='')
podpis1 = 'cw1.gif'
cw1 = Image.open(podpis1)
frames1 = cw1.n_frames
object11 = []
for i in range(frames1):
    obj = tk.PhotoImage(file=podpis1, format = f'gif -index {i}')
    object11.append(obj)

nazwa_label = tk.Label(window, text='Nazwa czujnika:', font=('calibre', 10, 'bold'))
nazwa_entry = tk.Entry(window, textvariable=nazwa_var, width=18, font=('calibre', 10, 'normal'))
typ_label = tk.Label(window, text='Typ czujnika:', font=('calibre', 10, 'bold'))
typ_entry = tk.Entry(window, textvariable=typ_var, width=18, font=('calibre', 10, 'normal'))
zakres_dol_label = tk.Label(window, text='Zakres pomiarowy:', font=('calibre', 10, 'bold'))
zakres_dol_entry = tk.Entry(window, textvariable=zakres_dol_var, width=18, font=('calibre', 10, 'normal'))
zakres_pause_label = tk.Label(window, text=' - ', font=('calibre', 10, 'bold'))
zakres_gora_entry = tk.Entry(window, textvariable=zakres_gora_var, width=18, font=('calibre', 10, 'normal'))
syg_dol_label = tk.Label(window, text='Sygnał wyjściowy:', font=('calibre', 10, 'bold'))
syg_dol_entry = tk.Entry(window, textvariable=syg_dol_var, width=18, font=('calibre', 10, 'normal'))
syg_pause_label = tk.Label(window, text=' - ', font=('calibre', 10, 'bold'))
syg_gora_entry = tk.Entry(window, textvariable=syg_gora_var, width=18, font=('calibre', 10, 'normal'))

sub_btn = tk.Button(window, text='Przelicz', command=submit)
unsub_btn = tk.Button(window, text='Usuń przelicznik', command=unsubmit)
chooseFile = tk.Button(command=show, text='Wgraj plik')


# ------------------ Rozłożenie elementów w oknie --------------- #

#zakres_dol_entry.place(x=15, y=60, height=60, width=120)

cwiczenie_1.grid(row=0, column=0, columnspan=4, sticky='w')
nazwa_label.grid(row=1, column=0, sticky='w', padx=5)
nazwa_entry.grid(row=1, column=1, sticky='e')
typ_label.grid(row=2, column=0, sticky='w', padx=5)
typ_entry.grid(row=2, column=1, sticky='e')
zakres_dol_label.grid(row=3, column=0, sticky='w', padx=5)
zakres_dol_entry.grid(row=3, column=1, sticky='e')
zakres_pause_label.grid(row=3, column=2, sticky='w')
zakres_gora_entry.grid(row=3, column=3, sticky='e')
syg_dol_label.grid(row=4, column=0, sticky='w', padx=5)
syg_dol_entry.grid(row=4, column=1, sticky='e')
syg_pause_label.grid(row=4, column=2, sticky='w')
syg_gora_entry.grid(row=4, column=3)
sub_btn.grid(row=5, column=1)
unsub_btn.grid(row=5, column=2)
chooseFile.grid(row=6, column=1)
window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=1)

current_frame = 0
animationn()
window.mainloop()

# Dodać nazwę, typ, zakres pomiarowy i sygnał wyjściowy czujnika (sygnał analogowy U(t)).
# Przeprowadzenie kalibracji - WF(t) = a*x*U(t)+b
# Wygenerowanie wykresu XY w czasie rzeczywistym (chyba U(t)) i po kalibracji