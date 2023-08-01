import folium
from geopy.distance import geodesic

from Telegram_bot_backend.interface import RunningWorkoutResultsInterface


class RunningWorkoutTimeResults:
    def __init__(self, start_time, finish_time):
        self.start_time = start_time
        self.finish_time = finish_time

    def get_interval_time(self):
        """
        Calculates the interval time between start_time and finish_time.

        :return: The interval time.
        :rtype: timedelta
        """
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
        """
        Calculates the average speed based on time and distance.

        :return: The average speed.
        :rtype: float
        """
        speed = self.distance / self.time
        return speed

    def speed_kilometer_hour(self):
        """
        Converts the average speed to kilometers per hour.

        :return: The average speed in kilometers per hour.
        :rtype: float
        """
        speed = self.average_speed()
        result = speed * 18 / 5
        return result


class RunningWorkoutGeoResults:
    def __init__(self, coordinate: list):
        self.coordinate = coordinate

    def sums_steps(self, a: int, b: int):
        """
        Calculates the geodesic distance between two points (a and b) in the coordinate list.

        :param a: The index of the first point in the coordinate list.
        :type a: int
        :param b: The index of the second point in the coordinate list.
        :type b: int
        :return: The geodesic distance between the two points.
        :rtype: float
        """
        lat1, lon1 = self.coordinate[a]
        lat2, lon2 = self.coordinate[b]
        point1 = (lat1, lon1)
        point2 = (lat2, lon2)
        distance = geodesic(point1, point2).meters
        return float(distance)

    def sums_distance(self):
        """
        Calculates the total distance covered in the coordinate list.

        :return: The total distance covered.
        :rtype: float
        """
        all_distance = 0
        for i in range(len(self.coordinate) - 1):
            all_distance += self.sums_steps(i, i + 1)
        return all_distance

    def create_map(self):
        """
        Creates a folium map based on the given coordinates.

        :return: The HTML representation of the folium map.
        :rtype: str
        """
        run_map = folium.Map(location=[self.coordinate[0][1], self.coordinate[0][0]], zoom_start=15)
        folium.PolyLine(
            locations=[[coord[1], coord[0]] for coord in self.coordinate],
            color='blue',
            weight=5
        ).add_to(run_map)

        map_html = run_map.get_root().render()
        return map_html


class RunningWorkoutResults(RunningWorkoutResultsInterface):
    def __init__(self, start_time, finish_time, coordinate: list):
        self.time_processing = RunningWorkoutTimeResults(start_time, finish_time)
        self.workout_processing = RunningWorkoutGeoResults(coordinate)

    def get_run_time(self):
        """
        Retrieves the interval time of the running workout.

        :return: The interval time.
        :rtype: timedelta
        """
        result = self.time_processing.get_interval_time()
        return result

    def get_distance(self):
        """
        Retrieves the total distance covered during the running workout.

        :return: The total distance covered.
        :rtype: float
        """
        return self.workout_processing.sums_distance()

    def get_map(self):
        """
        Retrieves the folium map of the running workout route.

        :return: The HTML representation of the folium map.
        :rtype: str
        """
        return self.workout_processing.create_map()

    def get_speed(self):
        """
        Retrieves the running workout speed results.

        :return: The running workout speed results.
        :rtype: dict
        """
        distance = self.workout_processing.sums_distance()
        time = self.time_processing.get_interval_time()

        result = RunningWorkoutSpeedResults(time, distance)

        return result
