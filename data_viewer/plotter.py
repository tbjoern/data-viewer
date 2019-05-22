from matplotlib.figure import Figure
import numpy as np
from data_viewer.interfaces import Plotter

class Plot:
    def __init__(self, figure, name):
        self.figure = figure
        self.name = name

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
            data_array = [list(list(zip(*l))[1]) for l in data[algo_hash]]
            indices = list(list(zip(*data[algo_hash][0]))[0])
            min_length = None
            for run_data in data_array:
                if min_length is None or len(run_data) < min_length:
                    min_length = len(run_data)
            iteration_limit_index = None
            if iteration_limit is not None:
                for i, iteration in enumerate(indices):
                    if iteration >= iteration_limit:
                        iteration_limit_index = i
                        break
            if iteration_limit_index is not None:
                if min_length > iteration_limit_index:
                    min_length = iteration_limit_index
            print(min_length)
            print(iteration_limit)
            print(iteration_limit_index)
            for i, run_data in enumerate(data_array):
                data_array[i] = run_data[:min_length]
            nparray = np.array(data_array)
            cut_weight_mean = nparray.mean(axis=0)
            sigma = nparray.std(axis=0)
            color = self.colors[plot_nr%len(self.colors)]
            fmt = '-'
            indices = indices[:min_length]
            plt.plot(indices, cut_weight_mean, fmt, label=labels[algo_hash], color=color)
            plt.fill_between(indices, cut_weight_mean+sigma, cut_weight_mean-sigma, facecolor=color, alpha=0.5)
            plot_nr += 1
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
           ncol=2, mode="expand", borderaxespad=0., prop={'size': 6})
        f.suptitle(plot_name)
        return Plot(f, plot_name)

    def save_plot(self, plot):
        plot.figure.savefig(plot.name + '.png')

