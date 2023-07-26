import re


class LocationProcessing:
    def __init__(self, model):
        self.model = model

    def create_coordinate(self, coordinate):
        data = coordinate
        pattern = r'\d+\.\d+'
        matches = re.findall(pattern, data)

        numbers = [float(match) for match in matches]

        return numbers

    def save_data_in_model(self, **kwargs):
        new = self.model()
        for key, value in kwargs.items():
            setattr(new, key, value)

        new.save()

    def update_data_in_model(self, row_id, **kwargs):
        instance = self.model.objects.get(id=row_id)
        route_coordinates = kwargs.get('route_coordinates', [])
        existing_coordinates = instance.route_coordinates if hasattr(instance, 'route_coordinates') else []
        updated_coordinates = existing_coordinates + route_coordinates
        kwargs['route_coordinates'] = updated_coordinates

        for key, value in kwargs.items():
            setattr(instance, key, value)
        instance.save()
