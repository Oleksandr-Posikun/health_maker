# === Interface Segregation ===

class CoordinateParserInterface:
    def parse_coordinate(self, coordinate: str) -> list:
        """
        Parses the coordinate string and returns a list of floating-point numbers.

        :param coordinate: A string representing a coordinate.
        :type coordinate: str
        :return: A list of floating-point numbers representing the parsed coordinates.
        :rtype: list
        """
        pass


class RunningWorkoutResultsInterface:
    def get_run_time(self):
        pass

    def get_distance(self):
        pass

    def get_map(self):
        pass

    def get_speed(self):
        pass
