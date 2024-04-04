import tkinter as tk
import tkinter.filedialog
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.style
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


# ------------------ FUNKCJE --------------- #


def plot(i):
    global fileread
    if fileread == 0:
        fileread = tk.filedialog.askopenfile()
    else:
        with open(fileread.name) as file:
            df = pd.read_csv(file, sep='    ', engine='python')
            aa = pd.DataFrame(df)
            alpha = [aa.at[i, 't [s]'] for i in range(0, len(aa))]
            beta = [aa.at[y, 'U [V]'] for y in range(0, len(aa))]
            ax1.clear()
            plt.plot(alpha, beta)
            plt.ylabel('U [V]')
            plt.xlabel('t [s]')
            plt.title('Wykres U/t')



def show():
    anim = animation.FuncAnimation(fig, func=plot, interval=1000, frames=10, repeat=False)
    plt.show()


chooseFile = tk.Button(command=show, text='Wgraj plik, którego wykres chcesz wygenerować')
chooseFile.grid(column=0, row=0)


window.mainloop()
