from data_viewer.interfaces import DataProvider
from math import floor
import os
import json
import csv
from functools import lru_cache

class ConfigNotFound(Exception):
    pass

class AmbiguousInstanceDir(Exception):
    pass

class ArrayCSVDataProvider(DataProvider):
    def __init__(self):
        self._instances = {}
        self._algorithms = {}
        self.config = {}

    def get_instances(self):
        return list(self._instances.keys())

    def get_algorithms(self):
        return list(self._algorithms.values())

    instances = property(get_instances)
    algorithms = property(get_algorithms)

    def open_path(self, path):
        # read config
        # assuming it has the same name as the directory
        directory = os.path.basename(os.path.abspath(path))
        configfile = directory + ".json"
        configpath = os.path.join(path, configfile)

        if not os.path.isfile(configpath):
            raise ConfigNotFound(f"No config at path {configpath}")

        with open(configpath, 'r') as f:
            self.config = json.load(f)

        _, subdirs, _ = next(os.walk(path))

        if not len(subdirs) == 1:
            raise AmbiguousInstanceDir(f"Found {len(subdirs)} subdirs in {path}, 1 expected")

        instancedir = os.path.join(path, subdirs[0])

        configcount = sum(len(files) for path, dirs, files in os.walk(instancedir))

        runcount = self.config["run_count"]
        algorithmcount = len(self.config["algorithms"])
        algorithm_run_combinations = runcount * algorithmcount
        instancecount = floor(configcount / (algorithm_run_combinations))

        #print(f"{runcount} {algorithmcount} {instancecount} {configcount} {runcount * algorithmcount * instancecount}")

        # index files
        for path, dirs, files in os.walk(path):
            for f in files:
                # naming scheme: name-config_1234.json.out
                filename, extension = os.path.splitext(f)
                if not extension == '.out':
                    continue
                full_filepath = os.path.join(path, f)
                filename = os.path.splitext(filename)[0] # remove .json extension

                instancename, configstring = filename.rsplit('-',1) # name, config_1234
                confignumber = int(configstring.split('_', 1)[1]) # 1234
                algorithm_run_number = confignumber % algorithm_run_combinations
                algorithmid = floor(algorithm_run_number / runcount)
                runnumber = algorithm_run_number % runcount

                #print(f"{confignumber} {algorithm_run_number} {algorithmid} {runnumber}")

                if not instancename in self._instances:
                    self._instances[instancename] = {}

                if not algorithmid in self._instances[instancename]:
                    self._instances[instancename][algorithmid] = []

                self._instances[instancename][algorithmid].append(full_filepath)

        for algorithm_config in self.config["algorithms"]:
            if "arguments" in algorithm_config:
                arguments = algorithm_config["arguments"]
            else:
                arguments = None
            self._algorithms[algorithm_config["id"]] = (algorithm_config["id"], algorithm_config["name"], arguments)


    def get_item_metadata(self, instance):
        metadata = {
            "fieldnames": [
                "generation",
                "fitness",
                "total_time",
                "flips"
            ]
        }
        return metadata

    def build_algorithm_name(self, algorithm):
        tokens = [algorithm[1]]
        if algorithm[2] is not None:
            if "decay_rate" in algorithm[2]:
                tokens.append(algorithm[2]["decay_rate"])
            if "power_law_beta" in algorithm[2]:
                tokens.append(algorithm[2]["power_law_beta"])
        return "_".join((str(x) for x in tokens))

    def get_plot_data(self, instance, algorithms):
        ret_data = {
            'data': {},
            'labels': {},
            'instance_name': instance
        }

        for algorithm in algorithms:
            id = algorithm[0]
            if not id in self._instances[instance]:
                continue

            ret_data['data'][id] = []
            for filename in self._instances[instance][id]:
                run_data = self.read_run_data(filename)
                ret_data['data'][id].append(run_data)
            ret_data['labels'][id] = self.build_algorithm_name(algorithm)
        
        return ret_data

    @lru_cache(maxsize=160)
    def read_run_data(self, filename):
        data = []
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            # skip header
            next(reader)
            
            for row in reader:
                id, run, generation, fitness, total_time, flips = row
                data.append((int(generation), float(fitness), float(total_time), float(flips)))
        return data


