import abc

class View:
    def display_list(self, list, handler):
        raise NotImplementedError()
    def display_plot(self, plot):
        raise NotImplementedError()
    def loop(self):
        raise NotImplementedError()
    
class Controller:
    def handle_item_selected(self, item):
        raise NotImplementedError()
    def open_archive(self, path):
        raise NotImplementedError()

class DataProvider:
    def list_instances(self):
        raise NotImplementedError()
    def list_algorithms(self):
        raise NotImplementedError()
    def get_plot_data(self, instance, algorithms):
        raise NotImplementedError()

class Plotter:
    def plot(self, instance, algorithms):
        raise NotImplementedError()
