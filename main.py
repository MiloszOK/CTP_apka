import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
import zad3
# ------------ TWORZENIE OKNA ------------- #


window = tk.Tk()
window.title('Najwspanialsza apka CTP w tej galaktyce!')
window.geometry('500x600')
window.config(pady=20, padx=20)

matplotlib.style.use('fivethirtyeight')

fig = plt.figure(constrained_layout=True)
fig.canvas.manager.set_window_title('Wykres')
ax1 = fig.add_subplot(1, 1, 1)
fileread = 0

nazwa_var = tk.StringVar()
typ_var = tk.StringVar()
zakres_dol_var = tk.IntVar()
zakres_gora_var = tk.IntVar()
zakres_gora_var.set(10)
syg_dol_var = tk.IntVar()
syg_gora_var = tk.IntVar()
syg_gora_var.set(10)
przedzial_czas_dol = tk.IntVar()
przedzial_czas_dol.set(1)
przedzial_czas_gora = tk.IntVar()
przedzial_czas_gora.set(2)

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
            pts = oblicz_maksima(beta)
            p = ile_maksimow_w_przedziale(pts, alpha)
            ax1.clear()
            plt.plot(alpha, beta)
            plt.plot([alpha[i] for i in pts], [beta[i] for i in pts], "x", label='Maksima lokalne')
            plt.ylabel('obr')
            plt.xlabel('t [s]')
            plt.title('Wykres obr/t')

def oblicz_maksima(a):
    peaks, _ = find_peaks(a)
    return peaks

def ile_maksimow_w_przedziale(peaks, alpha, start=przedzial_czas_dol, end=przedzial_czas_gora):
    start = start.get()
    end = end.get()
    count = 0
    for peak in peaks:
        if start <= alpha[peak] <= end:
            count += 1
    counter_label = tk.Label(window, text=str(count))
    counter_label.grid(row=7, column=1)
    return count
def show():
    anim = animation.FuncAnimation(fig, func=plot, interval=1000, frames=10, repeat=True)
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

nazwa_label = tk.Label(window, text='Nazwa czujnika:', font=('calibre', 10, 'bold'))
nazwa_entry = tk.Entry(window, textvariable=nazwa_var, font=('calibre', 10, 'normal'))
typ_label = tk.Label(window, text='Typ czujnika:', font=('calibre', 10, 'bold'))
typ_entry = tk.Entry(window, textvariable=typ_var, font=('calibre', 10, 'normal'))
zakres_dol_label = tk.Label(window, text='Zakres pomiarowy:', font=('calibre', 10, 'bold'))
zakres_dol_entry = tk.Entry(window, textvariable=zakres_dol_var, font=('calibre', 10, 'normal'))
zakres_pause_label = tk.Label(window, text=' - ', font=('calibre', 10, 'bold'))
zakres_gora_entry = tk.Entry(window, textvariable=zakres_gora_var, font=('calibre', 10, 'normal'))
syg_dol_label = tk.Label(window, text='Sygnał wyjściowy:', font=('calibre', 10, 'bold'))
syg_dol_entry = tk.Entry(window, textvariable=syg_dol_var, font=('calibre', 10, 'normal'))
syg_pause_label = tk.Label(window, text=' - ', font=('calibre', 10, 'bold'))
syg_gora_entry = tk.Entry(window, textvariable=syg_gora_var, font=('calibre', 10, 'normal'))

maksima_label = tk.Label(window, text='Przedzial t:', font=('calibre', 10, 'bold'))
czas_dol_entry = tk.Entry(window, textvariable=przedzial_czas_dol, font=('calibre', 10, 'normal'))
czas_gora_entry = tk.Entry(window, textvariable=przedzial_czas_gora, font=('calibre', 10, 'normal'))
impulsy_result = tk.Label(window, text='Impulsy:', font=('calibre', 10, 'normal'))

flowplot = tk.Button(command=zad3.main, text="Wykres predkosci obrotowej")
sub_btn = tk.Button(window, text='Submit', command=submit)
chooseFile = tk.Button(command=show, text='Wgraj plik')
maxplot = tk.Button(command=zad3.plot1s, text="Zlicz impulsy")

# ------------------ Rozłożenie elementów w oknie --------------- #

#zakres_dol_entry.place(x=15, y=60, height=60, width=120)

nazwa_label.grid(row=0, column=0)
nazwa_entry.grid(row=0, column=1)
typ_label.grid(row=1, column=0)
typ_entry.grid(row=1, column=1)
zakres_dol_label.grid(row=2, column=0)
zakres_dol_entry.grid(row=2, column=1)
zakres_pause_label.grid(row=2, column=2)
zakres_gora_entry.grid(row=2, column=3)
syg_dol_label.grid(row=3, column=0)
syg_dol_entry.grid(row=3, column=1)
syg_pause_label.grid(row=3, column=2)
syg_gora_entry.grid(row=3, column=3)
sub_btn.grid(row=4, column=1)
chooseFile.grid(row=5, column=1)


maksima_label.grid(row=6, column=0)
czas_dol_entry.grid(row=6, column=1)
zakres_pause_label.grid(row=6, column=2)
czas_gora_entry.grid(row=6, column=3)
impulsy_result.grid(row=7, column=0)
flowplot.grid(row=8, column=0)
maxplot.grid(row=9, column=0)
window.mainloop()

# Dodać nazwę, typ, zakres pomiarowy i sygnał wyjściowy czujnika (sygnał analogowy U(t)).
# Przeprowadzenie kalibracji - WF(t) = a*x*U(t)+b
# Wygenerowanie wykresu XY w czasie rzeczywistym (chyba U(t)) i po kalibracji
