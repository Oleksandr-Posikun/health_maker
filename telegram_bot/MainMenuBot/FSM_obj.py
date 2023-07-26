from aiogram.dispatcher.filters.state import StatesGroup, State


class MainMenuState(StatesGroup):
    main_menu = State()
    main_menu2 = State()
    main_menu3 = State()

    @classmethod
    def get_class_variables(cls):
        return [getattr(cls, attr) for attr in dir(cls) if isinstance(getattr(cls, attr), State)]

