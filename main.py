import tkinter as tk
from PIL import Image, ImageTk
from fpdf import FPDF
import tkinter.filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style
import numpy as np
import datetime
import pandas as pd
from scipy.signal import find_peaks
import zad3

# ------------ TWORZENIE OKNA ------------- #

window = tk.Tk()
window.iconbitmap('pngimg.ico')
window.title('Apka CTP v0.0.1')
window.geometry('460x400')

matplotlib.style.use('fivethirtyeight')

fig, axs = plt.subplots(2, 1, constrained_layout=True)
fig.canvas.manager.set_window_title('Wykresy')
ax1, ax2 = axs
fileread = 0

nazwa_var = tk.StringVar()
typ_var = tk.StringVar()
zakres_dol_var = tk.IntVar()
zakres_gora_var = tk.IntVar()
zakres_gora_var.set(10)
syg_dol_var = tk.IntVar()
syg_gora_var = tk.IntVar()
syg_gora_var.set(10)
company_var = tk.StringVar()
client_var = tk.StringVar()
przedzial_czas_dol = tk.IntVar()
przedzial_czas_dol.set(1)
przedzial_czas_gora = tk.IntVar()
przedzial_czas_gora.set(2)

now = datetime.datetime.now()


bg = tk.PhotoImage(file='koks.png')
bg_label = tk.Label(window, image=bg)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# --------------------- ANIMACJA --------------------- #

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
            pts = oblicz_maksima(beta)
            p = ile_maksimow_w_przedziale(pts, alpha)
            ax1.clear()
            ax2.clear()
            ax1.plot(alpha, beta)
            plt.plot([alpha[i] for i in pts], [beta[i] for i in pts], "x", label='Maksima lokalne')
            plt.ylabel('obr')
            plt.xlabel('t [s]')
            plt.title('Wykres obr/t')
            if 'exp' in globals():
                ax1.set_ylabel('obr')
                ax1.set_title('Wykres obr/t')
            else:
                ax1.set_ylabel('U [V]')
                ax1.set_title('Wykres U/t')
            ax1.set_xlabel('t [s]')
            if 'exp' in globals():
                ax2.plot(alpha, bb)
                ax2.set_ylabel('WF(t)')
                ax2.set_title('Wykres WF(t)/t')
            ax2.set_xlabel('t [s]')

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
    counter_label.grid(row=11, column=2)
    return count

def show():
    anim = animation.FuncAnimation(fig, func=plot, interval=3000, frames=10, repeat=True)
    plt.show()

def submit():
    nazwa = nazwa_var.get()
    typ = typ_var.get()
    company = company_var.get()
    client = client_var.get()

    global exp, b
    exp = ((zakres_gora_var.get() - zakres_dol_var.get()) / (syg_gora_var.get() - syg_dol_var.get()))
    b = zakres_dol_var.get() - syg_dol_var.get() * exp
    print(exp, b, nazwa, typ, company, client)

    # nazwa_var.set('')
    # typ_var.set('')
    # zakres_dol_var.set('')
    # syg_dol_var.set('')
    # zakres_gora_var.set('')
    # syg_gora_var.set('')
    # company_var.set('')
    # client_var.set('')

def unsubmit():
    if 'exp' in globals():
        global exp
        del exp

def export():
    plt.savefig('line_plot.pdf')
    plt.savefig('line_plot.png')
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(40, 10, f"Klient: {client_var.get()}")
    pdf.ln(10)
    pdf.cell(60, 10, f"Firma: {company_var.get()}")
    pdf.ln(10)
    pdf.cell(60, 10, f"Urzadzenie pomiarowe: {nazwa_var.get()}")
    pdf.ln(10)
    pdf.cell(60, 10, f"Typ urzadzenia: {typ_var.get()}")
    pdf.ln(10)
    pdf.cell(60, 10, f"Data: {now}")

    pdf.ln(20)
    pdf.image('line_plot.png', h=100)
    pdf.output("Raport.pdf")


cwiczenie_1 = tk.Label(window, image='')
podpis1 = 'cw1.gif'
cw1 = Image.open(podpis1)
frames1 = cw1.n_frames
object11 = [tk.PhotoImage(file=podpis1, format=f'gif -index {i}') for i in range(frames1)]

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
zakresior_pause_label = tk.Label(window, text=' - ', font=('calibre', 10, 'bold'))
syg_gora_entry = tk.Entry(window, textvariable=syg_gora_var, width=18, font=('calibre', 10, 'normal'))
company_label = tk.Label(window, text='Nazwa firmy:', font=('calibre', 10, 'bold'))
company_entry = tk.Entry(window, textvariable=company_var, width=18, font=('calibre', 10, 'normal'))
client_label = tk.Label(window, text='Nazwa klienta:', font=('calibre', 10, 'bold'))
client_entry = tk.Entry(window, textvariable=client_var, width=18, font=('calibre', 10, 'normal'))

maksima_label = tk.Label(window, text='Przedzial t:', font=('calibre', 10, 'bold'))
czas_dol_entry = tk.Entry(window, textvariable=przedzial_czas_dol, width=18, font=('calibre', 10, 'normal'))
czas_gora_entry = tk.Entry(window, textvariable=przedzial_czas_gora, width=18, font=('calibre', 10, 'normal'))
impulsy_result = tk.Label(window, text='Impulsy:', font=('calibre', 10, 'normal'))

flowplot = tk.Button(command=zad3.main, text="Wykres predkosci obrotowej")
maxplot = tk.Button(command=zad3.plot1s, text="Zlicz impulsy")

sub_btn = tk.Button(window, text='Przelicz', command=submit)
unsub_btn = tk.Button(window, text='Usuń przelicznik', command=unsubmit)
chooseFile = tk.Button(command=show, text='Wgraj plik')
zapis = tk.Button(command=export, text="Wyeksportuj")

# ------------------ Rozłożenie elementów w oknie --------------- #

cwiczenie_1.grid(row=0, column=0, columnspan=4, sticky='w')
nazwa_label.grid(row=1, column=0, sticky='w', padx=5)
nazwa_entry.grid(row=1, column=1, sticky='e')
typ_label.grid(row=2, column=0, sticky='w', padx=5)
typ_entry.grid(row=2, column=1, sticky='e')
zakres_dol_label.grid(row=3, column=0, sticky='w', padx=5)
zakres_dol_entry.grid(row=3, column=1, sticky='e')
zakres_pause_label.grid(row=3, column=2, sticky='w')
zakres_gora_entry.grid(row=3, column=3)
syg_dol_label.grid(row=4, column=0, sticky='w', padx=5)
syg_dol_entry.grid(row=4, column=1, sticky='e')
syg_pause_label.grid(row=4, column=2, sticky='w')
syg_gora_entry.grid(row=4, column=3)
company_label.grid(row=5, column=0, sticky='w', padx=5)
company_entry.grid(row=5, column=1, sticky='e')
client_label.grid(row=6, column=0, sticky='w', padx=5)
client_entry.grid(row=6, column=1, sticky='e')
sub_btn.grid(row=7, column=1)
unsub_btn.grid(row=7, column=3)
chooseFile.grid(row=8, column=1)
zapis.grid(row=8, column=3)
zakres_pause_label.grid(row=3, column=2, sticky='w')

maksima_label.grid(row=10, column=0, sticky='w')
czas_dol_entry.grid(row=10, column=1, sticky='e')
zakresior_pause_label.grid(row=10, column=2, sticky='w')
czas_gora_entry.grid(row=10, column=3, sticky='e')
impulsy_result.grid(row=11, column=0, sticky='w')
flowplot.grid(row=12, column=1)
maxplot.grid(row=13, column=1)

window.grid_columnconfigure(0, weight=2)
window.grid_columnconfigure(1, weight=1)

current_frame = 0
animationn()
window.mainloop()
