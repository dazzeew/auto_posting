from aiogram.dispatcher.filters.state import State, StatesGroup

class steps(StatesGroup):
	take_post = State()
	update_statement = State()
	check_switch = State()
	take_time = State()
	awaiting_post = State()
	update_data = State()
	update_post = State()
	delete_post = State()

