from matplotlib.figure import Figure
import numpy as np
from data_viewer.interfaces import Plotter

class MatplotlibPlotter(Plotter):
    def __init__(self):
        self.colors = ['b','g','r','m','c','y','k','orange']

    def plot(self, plot_data):
        f = Figure()
        plt = f.add_subplot(111)
        data = plot_data['data']
        labels = plot_data['labels']
        filename = plot_data['filename']
        for algo_id, runs in data.items():
            data_array = []
            for run_nr, run_data in runs.items():
                data_array.append(run_data['cut_weight'])
            min_length = None
            for run_data in data_array:
                if min_length is None or len(run_data) < min_length:
                    min_length = len(run_data)
            for i, run_data in enumerate(data_array):
                data_array[i] = run_data[:min_length]
            nparray = np.array(data_array)
            cut_weight_mean = nparray.mean(axis=0)
            sigma = nparray.std(axis=0)
            color = self.colors[algo_id%len(self.colors)]
            fmt = '-'
            indices = np.arange(min_length)
            plt.plot(indices, cut_weight_mean, fmt, label=labels[algo_id], color=color)
            plt.fill_between(indices, cut_weight_mean+sigma, cut_weight_mean-sigma, facecolor=color, alpha=0.5)
        plt.legend(loc='lower right', prop={'size': 6})
        f.suptitle(filename)
        return f
