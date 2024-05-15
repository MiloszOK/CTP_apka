import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style
import numpy as np
import pandas as pd


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

wsp_var = tk.StringVar()

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
                bb = aa.transform(lambda x: x*float(exp))
                beta = [bb.at[y, 'U [V]'] for y in range(0, len(bb))]
            else:
                beta = [aa.at[y, 'U [V]'] for y in range(0, len(aa))]
            alpha = [aa.at[i, 't [s]'] for i in range(0, len(aa))]
            ax1.clear()
            plt.plot(alpha, beta)
            plt.ylabel('obr')
            plt.xlabel('t [s]')
            plt.title('Wykres obr/t')


def show():
    anim = animation.FuncAnimation(fig, func=plot, interval=1000, frames=10, repeat=False)
    plt.show()


def submit():
    wsp = wsp_var.get()

    wsp_var.set("")
    global exp
    exp = float(wsp)

# współczynnik V/obr
wsp_label = tk.Label(window, text = 'Współczynnik V/obr', font=('calibre',10, 'bold'))
wsp_label2 = tk.Label(window, text = '(domyślnie 1)', font=('calibre',10, 'bold'))
wsp_entry = tk.Entry(window, textvariable = wsp_var, font=('calibre', 10, 'normal'))
sub_btn=tk.Button(window,text = 'Submit', command = submit)
chooseFile = tk.Button(command=show, text='Wgraj plik, którego wykres chcesz wygenerować')

# ------------------ Rozłożenie elementów w oknie --------------- #

wsp_label.grid(row=0,column=0)
wsp_label2.grid(row=1,column=0)
wsp_entry.grid(row=0,column=1)
sub_btn.grid(row=1,column=1)
chooseFile.grid(row=3, column=1)

window.mainloop()


# Dodać nazwę, typ, zakres pomiarowy i sygnał wyjściowy czujnika (sygnał analogowy U(t)).
# Przeprowadzenie kalibracji - WF(t) = a*x*U(t)+b
# Wygenerowanie wykresu XY w czasie rzeczywistym (chyba U(t)) i po kalibracji
