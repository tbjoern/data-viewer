import abc
from collections import namedtuple

Algorithm = namedtuple('Algorithm', ['name', 'id', 'arguments'])

class View:
    def display_list(self, list, handler):
        raise NotImplementedError()
    def display_plot(self, plot):
        raise NotImplementedError()
    def loop(self):
        raise NotImplementedError()

class DataProvider:
    def open_path(self, path):
        raise NotImplementedError()
    def get_instances(self):
        raise NotImplementedError()
    def get_algorithms(self):
        raise NotImplementedError()
    def get_plot_data(self, instance, algorithms):
        raise NotImplementedError()

    instances = property(get_instances)
    algorithms = property(get_algorithms)
    

class Plotter:
    def plot(self, plot_data):
        raise NotImplementedError()
