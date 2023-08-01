import re
import folium
from geopy.distance import geodesic
from Health_maker_project.interaction_with_model import DataSaver


class CoordinateParser:
    def parse_coordinate(self, coordinate: str) -> list:
        """
        Parses a string with coordinates and returns numeric values.

        :param coordinate: String with coordinates in the format "x.y".
        :type coordinate: str
        :return: List of numeric coordinate values.
        :rtype: list
        """
        pattern = r'\d+\.\d+'
        matches = re.findall(pattern, coordinate)
        numbers = [float(match) for match in matches]
        return numbers


class LocationProcessing:
    def __init__(self, model):
        """
        Constructor of the LocationProcessing class.

        :param model: Data model for saving, updating, and overwriting.
        :type model: class
        """
        self.coordinate_parser = CoordinateParser()
        self.data_saver = DataSaver(model)

    def process_coordinate(self, coordinate: str) -> list:
        """
        Processes a string with coordinates and returns numeric coordinate values.

        :param coordinate: String with coordinates in the format "x.y".
        :type coordinate: str
        :return: List of numeric coordinate values.
        :rtype: list
        """
        return self.coordinate_parser.parse_coordinate(coordinate)

    def save_data(self, **kwargs):
        """
        Saves data into the model.

        :param kwargs: Pairs of "field name - value" for saving into the model.
        :type kwargs: any
        """
        self.data_saver.save_data_in_model(**kwargs)

    def update_data(self, row_id: int, row_name: str, **kwargs):
        """
        Updates data in the model.

        :param row_id: Identifier of the row to update data.
        :type row_id: int
        :param row_name: Name of the field containing route coordinates.
        :type row_name: str
        :param kwargs: Pairs of "field name - value" for updating in the model.
        :type kwargs: list
        """
        self.data_saver.update_data_in_model(row_id, row_name, **kwargs)

    def overwrite_data(self, row_id: int, **kwargs):
        """
        Overwrites data in the model for a specific row.

        :param row_id: Identifier of the row to overwrite data.
        :type row_id: int
        :param kwargs: Pairs of "field name - value" for overwriting in the model.
        :type kwargs: any
        """
        self.data_saver.overwrite_data(row_id, **kwargs)


class RunningWorkoutTimeResults:
    def __init__(self, start_time, finish_time):
        self.start_time = start_time
        self.finish_time = finish_time

    def get_interval_time(self):
        running_time = self.finish_time - self.start_time
        return running_time


class RunningWorkoutSpeedResults:
    def __new__(cls, time, distance):
        instance = super(RunningWorkoutSpeedResults, cls).__new__(cls)
        instance.time = float(time.total_seconds())
        instance.distance = distance

        result_dict = {
            'converted speed': instance.speed_kilometer_hour(),
            'speed': instance.average_speed()
        }

        return result_dict

    def average_speed(self):
        speed = self.distance / self.time

        return speed

    def speed_kilometer_hour(self):
        speed = self.average_speed()
        result = speed * 18 / 5

        return result


class RunningWorkoutGeoResults:
    def __init__(self, coordinate: list):
        self.coordinate = coordinate

    def sums_steps(self, a: int, b: int):
        lat1, lon1 = self.coordinate[a]
        lat2, lon2 = self.coordinate[b]

        point1 = (lat1, lon1)
        point2 = (lat2, lon2)

        distance = geodesic(point1, point2).meters
        return float(distance)

    def sums_distance(self):
        all_distance = 0
        for i in range(len(self.coordinate) - 1):
            all_distance += self.sums_steps(i, i + 1)
        return all_distance

    def create_map(self):
        run_map = folium.Map(location=[self.coordinate[0][1], self.coordinate[0][0]], zoom_start=15)
        folium.PolyLine(
            locations=[[coord[1], coord[0]] for coord in self.coordinate],
            color='blue',
            weight=5
        ).add_to(run_map)

        map_html = run_map.get_root().render()

        return map_html


class RunningWorkoutResults:
    def __init__(self, start_time, finish_time, coordinate: list):
        self.time_processing = RunningWorkoutTimeResults(start_time, finish_time)
        self.workout_processing = RunningWorkoutGeoResults(coordinate)

    def get_run_time(self):
        result = self.time_processing.get_interval_time()
        return result

    def get_distance(self):
        return self.workout_processing.sums_distance()

    def get_map(self):
        return self.workout_processing.create_map()

    def get_speed(self):
        distance = self.workout_processing.sums_distance()
        time = self.time_processing.get_interval_time()

        result = RunningWorkoutSpeedResults(time, distance)
        return result
