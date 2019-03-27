class Controller:
    def __init__(self, data_provider, plotter):
        self.view = None
        self.data_provider = data_provider
        self.plotter = plotter

    def handle_item_selected(self, item):
        algorithms = list(self.data_provider.algorithms)
        data = self.data_provider.get_plot_data(item, algorithms)
        plot = self.plotter.plot(data)
        self.view.display_plot(plot)

    def open_path(self, path):
        self.data_provider.open_path(path)
        instances = self.data_provider.instances
        self.view.display_list(instances)

    def start(self):
        self.view.loop()
