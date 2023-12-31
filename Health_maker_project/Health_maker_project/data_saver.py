from Health_maker_project.interface import DataSaverInterface


class DataSaver(DataSaverInterface):
    def __init__(self, model):
        self.model = model

    def save_data_in_model(self, **kwargs):
        """
        Saves data into the specified model.

        :param kwargs: Keyword arguments representing data fields and values to be saved.
        :type kwargs: any
        """
        new_instance = self.model(**kwargs)
        new_instance.save()

    def overwrite_data(self, row_id: int, **kwargs):
        """
        Overwrites data in the specified model row.

        :param row_id: The ID of the row to be updated.
        :type row_id: int
        :param kwargs: Keyword arguments representing data fields and values to be updated.
        :type kwargs: any
        """
        instance = self.model.objects.get(id=row_id)

        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()

    def update_data_in_model(self, row_id: int, row_name: str, **kwargs):
        """
        Updates data in the specified model row.

        :param row_id: The ID of the row to be updated.
        :type row_id: int
        :param row_name: The name of the row to be updated.
        :type row_name: str
        :param kwargs: Keyword arguments representing data fields and values to be updated.
        :type kwargs: any
        """
        instance = self.model.objects.get(id=row_id)
        route_coordinates = kwargs.get(row_name, [])
        existing_coordinates = getattr(instance, row_name, [])
        updated_coordinates = existing_coordinates + route_coordinates
        kwargs[row_name] = updated_coordinates

        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()