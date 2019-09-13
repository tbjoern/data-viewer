from matplotlib.figure import Figure
import numpy as np
from data_viewer.interfaces import Plotter

class Plot:
    def __init__(self, figure, name):
        self.figure = figure
        self.name = name

def get_axis_data(axis, algo_data):
    data_array = [list(list(zip(*l))[axis]) for l in algo_data]
    for i,array in enumerate(data_array):
        np_array = np.array(array)
        # np_array = np.maximum.accumulate(np_array)
        data_array[i] = np_array
    min_length = None
    for run_data in data_array:
        if min_length is None or len(run_data) < min_length:
            min_length = len(run_data)
    if axis==3:
        for run_data in data_array:
            run_data[0] = 0
    for i, run_data in enumerate(data_array):
        data_array[i] = run_data[:min_length]
    return data_array

class MatplotlibPlotter(Plotter):
    def __init__(self):
        self.colors = list(reversed(['red', 'orange', 'yellow', 'greenyellow','turquoise','cornflowerblue','mediumpurple','mediumorchid','hotpink']))

    def plot(self, plot_data, iteration_limit=None, axes=(0,1)):
        f = Figure()
        plt = f.add_subplot(111)
        data = plot_data['data']
        labels = plot_data['labels']
        plot_name = plot_data['instance_name']
        plot_nr = 0
        xaxis, yaxis = axes
        for algo_hash, runs in data.items():
            indices = get_axis_data(xaxis, data[algo_hash])
            
            data_array = get_axis_data(yaxis, data[algo_hash])

            if iteration_limit is not None:
                for i,(run_index, run_data) in enumerate(zip(indices, data_array)):
                    for j, value in enumerate(run_index): 
                        if value > iteration_limit:
                            limit_index = j 
                            indices[i] = run_index[:limit_index]
                            data_array[i] = run_data[:limit_index]
                            break

            color = self.colors[plot_nr%len(self.colors)]
            fmt = '.--'

            for x, y in zip(indices, data_array):
                line, = plt.plot(x, y, fmt, color=color)
            line.set_label(labels[algo_hash])

            plot_nr += 1
        # plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3,
        #    ncol=1, mode="expand", borderaxespad=0., prop={'size': 6})
        # Shrink current axis's height by 10% on the bottom
        box = plt.get_position()
        plt.set_position([box.x0, box.y0 + box.height * 0.2,
                        box.width, box.height * 0.8])

        # Put a legend below current axis
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
                fancybox=True, shadow=True, ncol=2)
        f.suptitle(plot_name)
        return Plot(f, plot_name)

    def save_plot(self, plot):
        plot.figure.savefig(plot.name + '.png')

