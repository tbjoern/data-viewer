from data_viewer.interfaces import DataProvider, Plotter

class DataProviderMock(DataProvider):
    def open_path(self, path):
        pass
    
    def get_instances(self):
        return ['Alice', 'Bob', 'Charlie']

    def get_algorithms(self):
        return ['unif']

    def get_plot_data(self, instance, algorithms):
        return [1,2,3,4,5]

class PlotterMock(Plotter):
    def plot(self, plot_data):
        return {}
