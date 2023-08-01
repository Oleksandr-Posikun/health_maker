class DataSaverInterface:
    def save_data_in_model(self, **kwargs):
        pass

    def overwrite_data(self, row_id: int, **kwargs):
        pass

    def update_data_in_model(self, row_id: int, row_name: str, **kwargs):
        pass

