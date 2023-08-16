from aiogram.dispatcher.filters.state import StatesGroup, State


class WorkoutsMenuState(StatesGroup):
    run_workout = State()

    @classmethod
    def get_class_variables(cls):
        return [getattr(cls, attr) for attr in dir(cls) if isinstance(getattr(cls, attr), State)]

