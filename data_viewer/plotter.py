from matplotlib.figure import Figure
import numpy as np
from data_viewer.interfaces import Plotter

class MatplotlibPlotter(Plotter):
    def __init__(self):
        self.colors = ['b','g','r','m','c','y','k','orange']

    def plot(self, plot_data, iteration_limit=None):
        f = Figure()
        plt = f.add_subplot(111)
        data = plot_data['data']
        labels = plot_data['labels']
        plot_name = plot_data['instance_name']
        plot_nr = 0
        for algo_hash, runs in data.items():
            data_array = data[algo_hash]
            min_length = None
            for run_data in data_array:
                if min_length is None or len(run_data) < min_length:
                    min_length = len(run_data)
            if iteration_limit is not None and min_length > iteration_limit:
                min_length = iteration_limit
            for i, run_data in enumerate(data_array):
                data_array[i] = run_data[:min_length]
            nparray = np.array(data_array)
            cut_weight_mean = nparray.mean(axis=0)
            sigma = nparray.std(axis=0)
            color = self.colors[plot_nr%len(self.colors)]
            fmt = '-'
            indices = np.arange(min_length)
            plt.plot(indices, cut_weight_mean, fmt, label=labels[algo_hash], color=color)
            plt.fill_between(indices, cut_weight_mean+sigma, cut_weight_mean-sigma, facecolor=color, alpha=0.5)
            plot_nr += 1
        plt.legend(loc='lower right', prop={'size': 6})
        f.suptitle(plot_name)
        return f
