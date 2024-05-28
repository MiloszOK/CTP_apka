import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from scipy.signal import find_peaks
import tkinter as tk

file_path = './L6 13K2_3.lvm'
num_values = 100
start_index = 0

def retrieve_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()


    end_of_header_idx = lines.index('***End_of_Header***\t\t\t\t\t\n')

    data = pd.read_csv(file_path, sep='\t', skiprows=end_of_header_idx+2, header=None, decimal=',')
    x = data[0]
    v0 = data[1]
    v1 = data[2]
    v2 = data[3]
    v3 = data[4]

    return x, v0, v1, v2, v3

x, v0, v1, v2, v3 = retrieve_data(file_path)


def update(frame):
    global start_index
    if start_index + num_values < total_values:
        start_index += 5
        ax.clear()
        ax.plot(x[start_index:start_index+num_values], v0[start_index:start_index+num_values], label='v0')
        ax.plot(x[start_index:start_index+num_values], v1[start_index:start_index+num_values], label='v1')
        ax.plot(x[start_index:start_index+num_values], v2[start_index:start_index+num_values], label='v2')
        ax.plot(x[start_index:start_index+num_values], v3[start_index:start_index+num_values], label='v3')
        ax.set_xlabel('x')
        ax.set_ylabel('Value')
        ax.set_title(f'Voltage_0 (Values {start_index+1} to {start_index+num_values})')
        ax.legend()
        pkt = oblicz_maksima(v0[start_index:start_index+num_values])
        ax.grid(True)

def oblicz_maksima(a):
    peaks, _ = find_peaks(a)
    return peaks

def ile_maksimow_w_przedziale(peaks, alpha, start=1, end=2):
    start = start.get()
    end = end.get()
    count = 0
    for peak in peaks:
        if start <= alpha[peak] <= end:
            count += 1
    #counter_label = tk.Label(window, text=str(count))
    #counter_label.grid(row=7, column=1)
    return count

def main():
    global fig, ax, total_values
    x, v0, v1, v2, v3 = retrieve_data(file_path)
    total_values = len(x)

    # Set up the figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Update the plot every second
    ani = FuncAnimation(fig, update, frames=np.arange(0, total_values, num_values), interval=1000)

    # Set x-axis ticks to show every 50th value
    x_ticks = np.arange(0, total_values, 5000)
    ax.set_xticks(x_ticks)

    plt.show()
