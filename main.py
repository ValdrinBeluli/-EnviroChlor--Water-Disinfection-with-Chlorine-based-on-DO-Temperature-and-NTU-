

'''This code represents an engineering tool developed in Python using the Tkinter and Matplotlib libraries to create a graphical interface for monitoring and analyzing chlorine, temperature, dissolved oxygen (DO), and turbidity (NTU) in water. The system simulates measurements and analyzes the necessary chlorine level for disinfecting water, depending on measured values for DO, temperature, and NTU.

Main components of the tool:

Class Sensor: Represents a sensor that reads randomly generated values for the main variables (e.g., chlorine, DO, temperature). This class contains methods for calculating the chlorine level based on:
- DO level,
- temperature,
- and the difference in NTU between inlet and outlet.
The main tool (EngineeringTool): Contains the graphical interface where the user can manually enter values for NTU and temperature. The use of graphs allows for the visualization of the read data, along with predictions and differences between various chlorine levels.

Graphs and analyses: The tool creates graphs that show the relationships between chlorine and DO, temperature, as well as NTU, illustrating the differences and averages of chlorine levels. Predictions of future chlorine levels are based on historical data collected by the sensor.

This tool can be used to simulate and analyze the effectiveness of water disinfection with chlorine, based on important parameters such as temperature and dissolved oxygen. Its functionality offers an experimental approach that can be useful for research laboratories or scientific studies related to water quality and disinfection.'''

import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Sensor:
    def __init__(self, name):
        self.name = name
        self.values = []

    def read_value(self):
        value = np.random.uniform(0, 14)
        self.values.append(value)
        return value

    def determine_chlorine_level_by_do(self, do_level):
        return max(0, 10 - 0.5 * do_level)

    def determine_chlorine_level_by_temp(self, temp_level):
        return max(0, 8 - 0.3 * temp_level)

    def determine_klor_level_by_ntu_temp(self, ntu_inlet, ntu_outlet, temp_level):
        # Llogarit ndryshimin në NTU
        ntu_diff = ntu_outlet - ntu_inlet  # Këtu kemi ndryshuar pozitat për ta pasur rritje pas përpunimit
        # Llogarit nivelin e klorit në bazë të NTU dhe temperaturës
        klor_level = max(0, 5 + 0.2 * ntu_diff - 0.1 * temp_level)
        return klor_level  # Kthe rezultat

    def predict_next(self):
        return np.mean(self.values[-5:]) if len(self.values) >= 5 else self.values[-1]

class EngineeringTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Monitoring Chlorine, Temperature, DO, and NTU")
        self.geometry("1600x800")

        self.chlorine_sensor = Sensor("Chlorine")
        self.do_sensor = Sensor("DO")
        self.temp_sensor = Sensor("Temperature")

        frame_graph = ttk.Frame(self)
        frame_graph.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.fig_chlorine, (self.ax_chlorine, self.ax_do_temp_ntu) = plt.subplots(2, 1, figsize=(10, 8))
        self.canvas_chlorine = FigureCanvasTkAgg(self.fig_chlorine, master=frame_graph)
        self.canvas_chlorine.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        frame_command = ttk.Frame(self)
        frame_command.pack(side=tk.BOTTOM, fill=tk.X)

        self.ntu_inlet_entry = ttk.Entry(frame_command)
        self.ntu_inlet_entry.pack(side=tk.LEFT, padx=10)
        self.ntu_inlet_entry.insert(0, "NTU Inlet")

        self.ntu_outlet_entry = ttk.Entry(frame_command)
        self.ntu_outlet_entry.pack(side=tk.LEFT, padx=10)
        self.ntu_outlet_entry.insert(0, "NTU Outlet")

        self.temp_entry = ttk.Entry(frame_command)
        self.temp_entry.pack(side=tk.LEFT, padx=10)
        self.temp_entry.insert(0, "Temperature")

        self.btn_read = ttk.Button(frame_command, text="Read Values", command=self.read_values)
        self.btn_read.pack(side=tk.LEFT, padx=10, pady=10)

        self.btn_show = ttk.Button(frame_command, text="Show Graphs", command=self.plot_chlorine_do_temp_ntu)
        self.btn_show.pack(side=tk.LEFT, padx=10, pady=10)

    def read_values(self):
        chlorine_value = self.chlorine_sensor.read_value()
        do_value = self.do_sensor.read_value()
        temp_value = float(self.temp_entry.get())
        ntu_inlet = float(self.ntu_inlet_entry.get())
        ntu_outlet = float(self.ntu_outlet_entry.get())
        print(f"Chlorine value: {chlorine_value:.2f} mg/L, DO value: {do_value:.2f} mg/L, Temperature value: {temp_value:.2f} °C")
        print(f"NTU Inlet: {ntu_inlet:.2f}, NTU Outlet: {ntu_outlet:.2f}")

    def plot_values(self, ax, values, title, color, predicted_value=None):
        ax.clear()
        ax.plot(values, color=color, marker='o')
        ax.set_title(title)
        ax.set_xlabel("Number of Measurements")
        ax.set_ylabel("Value (mg/L)")
        if predicted_value is not None:
            ax.axhline(predicted_value, color='orange', linestyle='--', label=f'Prediction: {predicted_value:.2f} mg/L')
        ax.legend()
        ax.grid(True)

    def plot_chlorine_do_temp_ntu(self):
        predicted_chlorine = self.chlorine_sensor.predict_next()

        do_level = self.do_sensor.values[-1] if self.do_sensor.values else 0
        temp_level = float(self.temp_entry.get())
        ntu_inlet = float(self.ntu_inlet_entry.get())
        ntu_outlet = float(self.ntu_outlet_entry.get())

        do_levels = np.linspace(0, 14, 100)
        temp_levels = np.linspace(0, 30, 100)

        chlorine_do = [self.chlorine_sensor.determine_chlorine_level_by_do(do) for do in do_levels]
        chlorine_temp = [self.chlorine_sensor.determine_chlorine_level_by_temp(temp) for temp in temp_levels]
        chlorine_ntu_temp = self.chlorine_sensor.determine_klor_level_by_ntu_temp(ntu_inlet, ntu_outlet, temp_level)

        chlorine_avg = np.mean([
            self.chlorine_sensor.determine_chlorine_level_by_do(do_level),  
            self.chlorine_sensor.determine_chlorine_level_by_temp(temp_level),
            chlorine_ntu_temp
        ])

        chlorine_diff = [abs(c_do - self.chlorine_sensor.determine_chlorine_level_by_temp(do)) for c_do, do in zip(chlorine_do, do_levels)]
        chlorine_diff_percentage = [(diff / c_do * 100 if c_do != 0 else 0) for diff, c_do in zip(chlorine_diff, chlorine_do)]

        self.ax_do_temp_ntu.clear()
        self.ax_do_temp_ntu.plot(do_levels, chlorine_do, label="Chlorine (mg/L) based on DO (mg/L)", color='green')
        self.ax_do_temp_ntu.plot(temp_levels, chlorine_temp[:len(temp_levels)], label="Chlorine (mg/L) based on Temperature (°C)", color='blue')
        self.ax_do_temp_ntu.axhline(chlorine_ntu_temp, color='brown', linestyle='--', label=f'Chlorine based on NTU ({ntu_inlet:.2f} - {ntu_outlet:.2f}) and Temperature ({temp_level:.2f} °C)')
        self.ax_do_temp_ntu.axhline(chlorine_avg, color='magenta', linestyle='--', label=f'Average Chlorine: {chlorine_avg:.2f} mg/L')
        self.ax_do_temp_ntu.plot(do_levels, chlorine_diff, label="Difference (mg/L)", color='red', linestyle='--')
        self.ax_do_temp_ntu.plot(do_levels, chlorine_diff_percentage, label="Difference (%)", color='purple', linestyle='-.')

        self.ax_do_temp_ntu.axvline(do_level, color='orange', linestyle='--', label=f'DO: {do_level:.2f} mg/L')
        self.ax_do_temp_ntu.axvline(temp_level, color='purple', linestyle='--', label=f'Temperature: {temp_level:.2f} °C')
        self.ax_do_temp_ntu.set_title("Water Disinfection with Chlorine based on DO, Temperature, and NTU")
        self.ax_do_temp_ntu.set_xlabel("DO (mg/L) and Temperature (°C)")
        self.ax_do_temp_ntu.set_ylabel("Chlorine (mg/L) and Difference (%)")

        for i in range(len(do_levels)):
            if i % 10 == 0:
                self.ax_do_temp_ntu.text(do_levels[i], chlorine_do[i], f'{chlorine_do[i]:.2f}', color='green', fontsize=8)
                self.ax_do_temp_ntu.text(temp_levels[i], chlorine_temp[i], f'{chlorine_temp[i]:.2f}', color='blue', fontsize=8)
                self.ax_do_temp_ntu.text(do_levels[i], chlorine_diff[i], f'{chlorine_diff[i]:.2f}', color='red', fontsize=8)
                self.ax_do_temp_ntu.text(do_levels[i], chlorine_diff_percentage[i], f'{chlorine_diff_percentage[i]:.2f}%', color='purple', fontsize=8)

        self.ax_do_temp_ntu.legend()
        self.ax_do_temp_ntu.grid(True)

        self.plot_values(self.ax_chlorine, self.chlorine_sensor.values, "Chlorine Level (mg/L)", 'green', predicted_chlorine)
        self.canvas_chlorine.draw()

if __name__ == "__main__":
    app = EngineeringTool()
    app.mainloop()

