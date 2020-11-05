import times
import pytest
import yaml


def get_test_data(file_path):
    test_array = []
    # Load the fixtures for testing
    with open(file_path) as file:
        loaded_tests = yaml.load(file, Loader=yaml.SafeLoader)
        for test in loaded_tests:
            # Get test parameters
            test_parameters = list(test.values())[0]
            # Convert expected arrays into tuples
            expected_values = []
            for expected in test_parameters['expected']:
                expected_values.append((expected[0], expected[1]))
            # Make the current test tuple
            current_test = (times.time_range(
                                test_parameters['time_range_1']['start'],
                                test_parameters['time_range_1']['end'],
                                test_parameters['time_range_1'].get('num_intervals', 1),
                                test_parameters['time_range_1'].get('time_between_intervals', 0)),
                            times.time_range(
                                test_parameters['time_range_2']['start'],
                                test_parameters['time_range_2']['end'],
                                test_parameters['time_range_2'].get('num_intervals', 1),
                                test_parameters['time_range_2'].get('time_between_intervals', 0)),
                            expected_values)
            # Add it to the array
            test_array.append(current_test)
    return test_array

@pytest.mark.parametrize("time_range_1, time_range_2, expected", get_test_data("./week05-testing/fixture.yaml"))
def test_fixture_input(time_range_1, time_range_2, expected):
    result = times.compute_overlap_time(time_range_1, time_range_2)
    assert result == expected

def test_negative_time_interval():
    """Tests a time range which goes backwards"""
    with pytest.raises(ValueError):
        times.time_range("2010-01-12 15:00:00", "2010-01-12 12:00:00")
