import numpy as np
import pandas as pd
import math
import random
import matplotlib
import matplotlib.pyplot as plt
import torch

df = pd.read_csv('TEP_FaultFree_Training.csv')

df = df.rename(columns=rename_map)

cols = [
    "reactor_pressure",
    "reactor_level",
    "reactor_temperature",
#     "separator_pressure",
#     "separator_level",
#     "separator_temperature",
#     "stripper_pressure",
#     "stripper_level",
#     "stripper_temperature",
#     "compressor_work",
    "reactor_cooling_water_valve",
#     "condenser_cooling_water_valve",
]


def smooth_signal(signal, group, window_size):
    df[f'{signal}_smooth'] = df.groupby(group)[signal].rolling(window_size).mean().reset_index(level=0, drop=True)


def enter(signal):
    df[f'enter_{signal}'] = df[signal].astype(int).diff() == 1


def exit(signal):
    df[f'enter_{signal}'] = df[signal].astype(int).diff() == -1


def state_num(signal):
    df[f'{signal}_num'] = df[f'enter_{signal}'].cumsum()


def measure(signal, group, measure, label):
    df[f'{signal}_{label}'] = df.groupby(group).transform(measure)[signal]


smooth_signal('reactor_pressure', 'simulation_run', 20)
df['reactor_pressure_rising'] = df['reactor_pressure_smooth'].diff(10) > 0
df['reactor_pressure_falling'] = df['reactor_pressure_smooth'].diff(10) < 0
enter('reactor_pressure_rising')
state_num('reactor_pressure_rising')
measure('reactor_pressure_rising', 'reactor_pressure_rising_num', 'max', 'peak')
measure('reactor_pressure_rising', 'reactor_pressure_rising_num', 'min', 'trough')
# df['reactor_pressure_amplitude'] = (df['reactor_pressure_rising_peak'] - df['reactor_pressure_rising_trough']) / 2