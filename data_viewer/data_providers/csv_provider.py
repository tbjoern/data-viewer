from data_viewer.interfaces import DataProvider, Algorithm
import os
import json
import csv
from functools import lru_cache
from copy import deepcopy

class InvalidDirFormat(Exception):
    pass

# self._instances = {
#     "name_of_instance": {
#         "algorithm xyz hash": [
#             (0, "path/to/csvfile"),
#             (7, "path/to/different/csvfile"),
#         ].
#         ...
#     },
#     ...
# }
# self._algorithms = {
#     "algorithms xyz hash": {
#         Algorithm(
#             name,
#             arguments: {
#                 key: value
#             }
#         )
#     }
# }
class CSVDataProvider:
    def __init__(self):
        self.path = None
        self._instances = {}
        self._algorithms = {}

    def open_path(self, path):
        self.path = path
        self.add_directory(path)

    def add_directory(self, path):
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
        
        if 'algorithms' in config:
            for algorithm_config in config['algorithms']:
                if 'arguments' in algorithm_config:
                    arguments = algorithm_config['arguments']
                else:
                    arguments = None
                algorithm = Algorithm(algorithm_config['name'], arguments)
                algorithm_hash = self.hash(algorithm)
                if not algorithm_hash in self._algorithms:
                    self._algorithms[algorithm_hash] = algorithm
                run_algorithms.append((algorithm_hash, algorithm_config['id']))
        else:
            for mutation_operator_config in config['mutators']:
                if 'arguments' in mutation_operator_config:
                    arguments = mutation_operator_config['arguments']
                else:
                    arguments = None
                algorithm = Algorithm(mutation_operator_config['type'], arguments)
                algorithm_hash = self.hash(algorithm)
                if not algorithm_hash in self._algorithms:
                    self._algorithms[algorithm_hash] = algorithm
                run_algorithms.append((algorithm_hash, mutation_operator_config['id']))
        
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

    def hash(self, algorithm):
        tokens = [algorithm.name]
        if algorithm.arguments is not None:
            for key, value in algorithm.arguments.items():
                tokens.append(str(key))
                tokens.append(str(value))
        return "-".join(tokens)
        

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

    def get_item_metadata(self, instance):
        metadata = {
            "fieldnames": None
        }
        fieldnames = []
        non_data_fields = ['id', 'run']
        for algorithm_hash, id_path_pairs in self._instances[instance].items():
            for algorithm_id, path in id_path_pairs:
                instance_fieldnames = self.read_csv_header(path)
                for field in instance_fieldnames:
                    if not field in fieldnames and not field in non_data_fields:
                        fieldnames.append(field)
        metadata["fieldnames"] = fieldnames
        return metadata

    def get_plot_data(self, instance, algorithms):
        ret_data = {
            'data': {},
            'labels': {},
            'instance_name': instance
        }
        for algorithm in algorithms:
            algorithm_hash = self.hash(algorithm)
            if not algorithm_hash in ret_data['data']:
                ret_data['data'][algorithm_hash] = []
                ret_data['labels'][algorithm_hash] = self.build_algorithm_name(algorithm)
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
        # print(algorithm)
        name_parts = list()
        name_parts.append(algorithm.name)
        if algorithm.arguments:
            for key,value in algorithm.arguments.items():
                name_parts.append(f"{key}={value}")
        return " ".join(name_parts)

    @lru_cache(maxsize=10)
    def read_csv_header(self, csv_path):
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f, delimiter=',')
            csvreader.fieldnames = [x.strip() for x in csvreader.fieldnames]
            return list(csvreader.fieldnames)

    @lru_cache(maxsize=10)
    def read_csv_data(self, csv_path):
        # data = {
        #     "4": { # algorithm id
        #         "0" : [ # run number
        #             (generation, fitness, ...)
        #         ],
        #         "1" : [
        #             ....
        #         ],
        #         ...
        #     },
        #     ...
        # }
        data = {}
        print(f'reading {csv_path}')
        with open(csv_path, "r") as f:
            csvreader = csv.DictReader(f, delimiter=',')
            csvreader.fieldnames = [x.strip() for x in csvreader.fieldnames]
            datafields = [x for x in csvreader.fieldnames if x not in ['id','run']]
            for row in csvreader:
                algo_id = int(row["id"])
                if algo_id not in data:
                    data[algo_id] = {}
                run_nr = int(row["run"])
                if not run_nr in data[algo_id]:
                    data[algo_id][run_nr] = []
                datapoints = []
                for field in datafields:
                    datapoints.append(int(float(row[field])))
                data[algo_id][run_nr].append(tuple(datapoints))
        return data

    instances = property(get_instances)
    algorithms = property(get_algorithms)
