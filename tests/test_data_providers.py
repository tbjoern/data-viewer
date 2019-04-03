import pytest
from data_viewer.data_providers.csv_provider import CSVDataProvider

@pytest.fixture
def csv_provider(shared_datadir):
    provider = CSVDataProvider()
    provider.open_path(shared_datadir)
    return provider

class TestCsvProvider:
    def test_open_path(self, csv_provider, shared_datadir):
        assert len(list(csv_provider.algorithms)) == 2
        assert len(list(csv_provider.instances)) == 2

    def test_get_plot_data(self, csv_provider):
        instance = next(csv_provider.instances)
        algorithm = next(csv_provider.algorithms)

        data = csv_provider.get_plot_data(instance, [algorithm])

        expected_data = {
            'data': {
                0: {
                    0: {
                        'iteration': [0, 1, 2],
                        'cut_weight': [0, 30, 40]
                    },
                    1: {
                        'iteration': [0, 1, 2],
                        'cut_weight': [1, 31, 41]
                    }
                }
            },
            'labels': {
                0: 'test_one'
            },
            'filename': 'first'
        }

        assert data == expected_data


