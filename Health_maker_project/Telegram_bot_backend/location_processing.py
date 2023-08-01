import re

from Telegram_bot_backend.interface import CoordinateParserInterface


class LocationProcessor(CoordinateParserInterface):
    def __init__(self, model):
        self.model = model

    def parse_coordinate(self, coordinate: str) -> list:
        """
        Parses the coordinate string and returns a list of floating-point numbers.

        :param coordinate: A string representing a coordinate.
        :type coordinate: str
        :return: A list of floating-point numbers representing the parsed coordinates.
        :rtype: list
        """
        pattern = r'\d+\.\d+'
        matches = re.findall(pattern, coordinate)
        numbers = [float(match) for match in matches]

        return numbers
