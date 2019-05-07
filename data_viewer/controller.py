class Controller:
    def __init__(self, data_provider, plotter):
        self.view = None
        self.data_provider = data_provider
        self.plotter = plotter

    def handle_item_selected(self, item):
        algorithms = self.view.get_selected_algorithms()
        data = self.data_provider.get_plot_data(item, algorithms)
        plot = self.plotter.plot(data, self.view.get_iteration_limit())
        self.view.display_plot(plot)

    def open_path(self, path):
        self.data_provider.open_path(path)
        instances = self.data_provider.instances
        algorithms = self.data_provider.algorithms
        self.view.display_instances(instances, None)
        self.view.display_algorithms(algorithms, None)

    def start(self):
        self.view.loop()
