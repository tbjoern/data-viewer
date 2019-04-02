from data_viewer.interfaces import DataProvider
import os
import json
import csv
from collections import namedtuple

Algorithm = namedtuple('Algorithm', ['name', 'id', 'arguments'])

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
        for dirpath, _, filenames in os.walk(path):
            self._instances.extend(
                (dirpath, name, extension)
                for name, extension in 
                map(os.path.splitext, filenames) 
                if extension == '.csv'
            )
        self._instances.sort(key=lambda x: x[1])

    def read_algorithms_from_path(self, path):
        json_files = []
        for dirpath, _, filenames in os.walk(path):
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
            arguments = algorithm_config['arguments'] if 'arguments' in config else None
            self._algorithms.append(Algorithm(algorithm_config['name'], algorithm_config['id'], arguments))

    def get_instances(self):
        for _, name, _ in self._instances:
            yield name

    def get_algorithms(self):
        return self._algorithms

    def get_plot_data(self, instance, algorithms):
        
        return self.read_csv_data(instance)

    def get_full_instance_path(self, instance):
        for dirpath, name, extension in self._instances:
            if name == instance:
                return os.path.join(dirpath, name + extension)
        raise IndexError(f'Instance not found: {instance}')

    def build_algorithm_name(self, algorithm):
        name_parts = list()
        name_parts.append(algorithm.name)
        if algorithm.arguments:
            for key,value in algorithm["arguments"].items():
                name_parts.append(f"{key}={value}")
        return " ".join(name_parts)

    def read_csv_data(self, instance):
        csv_path = self.get_full_instance_path(instance)
        plot_data = { 'data': {}, 'labels': {}, 'filename': instance}
        data = plot_data['data']
        labels = plot_data['labels']
        for algorithm in self._algorithms:
            data[algorithm.id] = {}
            labels[algorithm.id] = self.build_algorithm_name(algorithm)
        print(f'reading {csv_path}')
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f, delimiter=',')
            for row in csvreader:
                algo_id = int(row["algorithm"])
                run_nr = int(row["run_number"])
                if not run_nr in data[algo_id]:
                    data[algo_id][run_nr] = { 'iteration':[], 'cut_weight':[] }
                data[algo_id][run_nr]['iteration'].append(int(row['iteration']))
                data[algo_id][run_nr]['cut_weight'].append(int(row['cut_weight']))
        return plot_data

    instances = property(get_instances)
    algorithms = property(get_algorithms)
