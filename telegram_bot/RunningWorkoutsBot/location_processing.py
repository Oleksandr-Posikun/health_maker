import folium

from geopy.distance import geodesic
from datetime import datetime


class LocationProcessing:
    def __init__(self):
        self.steps_list = []
        self.all_steps_list = []
        self.time_list = []
        self.whole_route_list = []

    async def get_coordinates(self, message):
        longitude = message.location.longitude
        latitude = message.location.latitude

        return [latitude, longitude]


    async def sums_steps(self):
        lat1, lon1 = self.steps_list[0]
        lat2, lon2 = self.steps_list[1]

        point1 = (lat1, lon1)
        point2 = (lat2, lon2)

        distance = geodesic(point1, point2).meters

        self.whole_route_list.append(distance)

    async def get_interval_time(self):
        current_time = self.time_list[-1] - self.time_list[0]
        total_seconds = int(current_time.total_seconds())
        time = {'hours': total_seconds // 3600, 'minutes': (total_seconds % 3600) // 60, 'seconds': total_seconds % 60}

        return time

    async def create_map(self):
        m = folium.Map(location=[self.all_steps_list[0][1], self.all_steps_list[0][0]], zoom_start=15)
        folium.PolyLine(
            locations=[[coord[1], coord[0]] for coord in self.all_steps_list],
            color='blue',
            weight=5
        ).add_to(m)

        m.save('route_map.html')
