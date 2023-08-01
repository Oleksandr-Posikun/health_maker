class DataSaver:
    def __init__(self, model):
        """
        Constructor of the DataSaver class.

        :param model: Data model for saving.
        :type model: class
        """
        self.model = model

    def save_data_in_model(self, **kwargs):
        """
        Saves data into the model.

        :param kwargs: Pairs of "field name - value" for saving into the model.
        :type kwargs: dict
        """
        new_instance = self.model(**kwargs)
        new_instance.save()

    def overwrite_data(self, row_id: int, **kwargs):
        """
        Overwrites data in the model for a specific row.

        :param row_id: Identifier of the row to overwrite data.
        :type row_id: int
        :param kwargs: Pairs of "field name - value" for overwriting in the model.
        :type kwargs: dict
        """
        instance = self.model.objects.get(id=row_id)

        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()

    def update_data_in_model(self, row_id: int, row_name: str, **kwargs):
        """
        Updates data in the model.

        :param row_id: Identifier of the row to update data.
        :type row_id: int
        :param row_name: Name of the field containing route coordinates.
        :type row_name: str
        :param kwargs: Pairs of "field name - value" for updating in the model.
        :type kwargs: list
        """
        instance = self.model.objects.get(id=row_id)

        route_coordinates = kwargs.get(row_name, [])
        existing_coordinates = getattr(instance, row_name, [])
        updated_coordinates = existing_coordinates + route_coordinates
        kwargs[row_name] = updated_coordinates

        for key, value in kwargs.items():
            setattr(instance, key, value)

        instance.save()
