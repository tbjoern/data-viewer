from data_viewer.interfaces import DataProvider, Algorithm
import os
import json
import csv
from functools import lru_cache
from copy import deepcopy

class InvalidDirFormat(Exception):
    pass

class CSVDataProvider:
    def __init__(self):
        self.path = None
        self._instances = {}
        self._algorithms = {}

    def open_path(self, path):
        self.path = path
        self.add_run(path)

    def add_run(self, path):
        """
        adds data from a directory
        the directory should contain exactly one json file (config)
        and arbitrary many .csv files (can also be in subdirs)
        """
        # read config, add algorithms to list, assign hashes
        json_files = list(self.get_json_files_in_path(path))
        if len(json_files) is not 1:
            raise InvalidDirFormat(f"Path does not contain exactly one json file: {path}. Found {len(json_files)} files.")
        
        with open(json_files[0], 'r') as f:
            config = json.load(f)

        run_algorithms = []
        
        for algorithm_config in config['algorithms']:
            arguments = algorithm_config['arguments'] if 'arguments' in config else None
            algorithm = Algorithm(algorithm_config['name'], arguments)
            algorithm_hash = hash(algorithm)
            if not algorithm_hash in self._algorithms:
                self._algorithms[algorithm_hash] = algorithm
            run_algorithms.append((algorithm_hash, algorithm_config['id']))
        
        # for every instance, add metainfo on which algorithms (as hashes) are contained within
        # maintain a hash-id mapping seperate for every instance
        # also store the file path for every instance-algorithm pair

        for dirpath, name, extension in self.read_instances_from_path(path):
            if name not in self._instances:
                self._instances[name] = { }
            instance_path = os.path.join(dirpath, name + extension)
            for algorithm_hash, algorithm_id in run_algorithms:
                if algorithm_hash not in self._instances[name]:
                    self._instances[name][algorithm_hash] = []
                self._instances[name][algorithm_hash].append(
                    (algorithm_id, instance_path)
                )
        

    def read_instances_from_path(self, path):
        for dirpath, _, filenames in os.walk(path):
            for instance in (
                (dirpath, name, extension)
                for name, extension in 
                map(os.path.splitext, filenames) 
                if extension == '.csv'
            ):
                yield instance

    def get_json_files_in_path(self, path):
        for dirpath, _, filenames in os.walk(path):
            for json_file in (
                os.path.join(dirpath, name + extension)
                for name, extension in 
                map(os.path.splitext, filenames) 
                if extension == '.json'
            ):
                yield json_file

    def get_instances(self):
        return self._instances.keys()

    def get_algorithms(self):
        for algorithm in self._algorithms.values():
            yield algorithm

    def get_plot_data(self, instance, algorithms):
        ret_data = {
            'data': {},
            'labels': {},
            'instance_name': instance
        }
        for algorithm in algorithms:
            algorithm_hash = hash(algorithm)
            if not algorithm_hash in ret_data['data']:
                ret_data['data'][algorithm_hash] = []
                ret_data['labels'][algorithm_hash] = self.build_algorithm_name(self._algorithms[algorithm_hash])
            for algorithm_id, instance_path in self._instances[instance][algorithm_hash]:
                plot_data = self.read_csv_data(instance_path)
                algorithm_data = plot_data[algorithm_id]
                for run_nr, run_data in algorithm_data.items():
                    ret_data['data'][algorithm_hash].append(
                        list(run_data)
                    )
        return ret_data

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

    @lru_cache(maxsize=10)
    def read_csv_data(self, csv_path):
        data = {}
        print(f'reading {csv_path}')
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f, delimiter=',')
            for row in csvreader:
                algo_id = int(row["algorithm"])
                if algo_id not in data:
                    data[algo_id] = {}
                run_nr = int(row["run_number"])
                if not run_nr in data[algo_id]:
                    data[algo_id][run_nr] = []
                data[algo_id][run_nr].append(int(row['cut_weight']))
        return data

    instances = property(get_instances)
    algorithms = property(get_algorithms)
