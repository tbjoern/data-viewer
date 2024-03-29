class Controller:
    def __init__(self, data_provider, plotter):
        self.view = None
        self.data_provider = data_provider
        self.plotter = plotter

    def item_metadata(self, item):
        return self.data_provider.get_item_metadata(item)

    def handle_item_selected(self, item):
        algorithms = self.view.get_selected_algorithms()
        data = self.data_provider.get_plot_data(item, algorithms)
        axes = self.view.get_selected_axes()
        axes_names = self.data_provider.get_item_metadata(item)['fieldnames']
        axes_names = tuple(axes_names[i] for i in axes)
        plot = self.plotter.plot(data, self.view.get_iteration_limit(), axes, axes_names)
        self.view.display_plot(plot)

    def open_path(self, path):
        self.data_provider.open_path(path)
        instances = self.data_provider.instances
        instances.sort()
        algorithms = self.data_provider.algorithms
        algorithms = [(self.data_provider.build_algorithm_name(algorithm), algorithm) for algorithm in algorithms]
        self.view.display_instances(instances, None)
        self.view.display_algorithms(algorithms, None)

    def start(self):
        self.view.loop()

    def save_plot(self, plot):
        self.plotter.save_plot(plot)
