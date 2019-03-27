from data_viewer.interfaces import DataProvider
import os
import json

class CSVDataProvider:
    def __init__(self):
        self.path = None
        self._instances = []
        self._algorithms = []

    def open_path(self, path):
        self.path = path
        self._instances = []
        self._algorithms = []

        self.read_algorithms_from_path(path)
        self.read_instances_from_path(path)

    def read_instances_from_path(self, path):
        for dirpath, dirname, filenames in os.walk(path):
            self._instances.extend(
                (dirpath, name, extension)
                for name, extension in 
                map(os.path.splitext, filenames) 
                if extension == '.csv'
            )
        self._instances.sort(key=lambda x: x[1])

    def read_algorithms_from_path(self, path):
        json_files = []
        for dirpath, dirname, filenames in os.walk(path):
            json_files.extend(
                os.path.join(dirpath, name + extension)
                for name, extension in 
                map(os.path.splitext, filenames) 
                if extension == '.json'
            )
        for json_file in json_files:
            print(json_file)
            with open(json_file) as f:
                config = json.load(f)
            self.parse_json_config(config)
        
    def parse_json_config(self, config):
        for algorithm_config in config['algorithms']:
            self._algorithms.append(algorithm_config['name'])

    def get_instances(self):
        for _, name, _ in self._instances:
            yield name

    def get_algorithms(self):
        return self._algorithms

    def get_plot_data(self, instance, algorithms):
        raise NotImplementedError()

    instances = property(get_instances)
    algorithms = property(get_algorithms)
