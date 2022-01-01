from config import TOKEN,id_admin,id_chat,defolt_time_wait
from functions import list_write_list,write_in_txt

from datetime import datetime, date, time, timedelta

from aiogram import Bot, Dispatcher, types, executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import aiogram
import asyncio
import aiohttp

import os
import sys

import time

from states import steps

from keyboards import create_keyboard,post_data_keyboard, main_keyboard

# from res import restart

#-1001352261993
bot = Bot(TOKEN, parse_mode = 'HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


async def main(): 
    loop = asyncio.get_event_loop()
    url = "https://api.telegram.org/"

    async with aiohttp.ClientSession(loop=loop, trust_env=True) as session:
        async with session.get(url, timeout=30) as resp:
            return resp.status

# @dp.message_handler(commands = 'restart', state = '*',chat_id = id_admin) #Перезапуск бота
# async def wasup(message):
# 	await bot.send_message(message.chat.id, text = "Перезапуск бота...",reply_markup = None)
# 	os.execv(sys.executable, [sys.executable] + sys.argv)


@dp.message_handler(commands = 'start', state = '*',chat_id = id_admin) #Начало
async def wasup(message):
	await bot.send_message(message.chat.id, text = "Привет, вова , потом допишу вступление, в клавиатуре возможные кнопки, жмякай,тестируй",reply_markup = main_keyboard())


@dp.message_handler(lambda message: message.text and 'Список постов' in message.text, state = '*',chat_id = id_admin) #Вывод постов в файле
async def spisok(message):
	try:
		l = list_write_list()
		if len(l) == 0:
			await bot.send_message(message.chat.id,text = 'Посты отсутствуют',reply_markup = main_keyboard())
		else:
			stroka = ""
			j = 1
			for i in range(0,int(len(l)),2):
				if l[i+1][-1] == "m":
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1].replace("m",""),"%Y/%m/%d/%H/%M")) + "\n"
				else:
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1],"%Y/%m/%d/%H/%M")) + "\n"
				j += 1
			await bot.send_message(message.chat.id,text = stroka,reply_markup = main_keyboard())
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так...',reply_markup = main_keyboard())

@dp.message_handler(lambda message: message.text and 'Удалить пост' in message.text, state = '*',chat_id = id_admin) #Начальный хендлер для удаления поста
async def delete(message):
	try:
		l = list_write_list()
		if len(l) == 0:
			await bot.send_message(message.chat.id,text = 'Посты отсутствуют')
		else:
			stroka = ""
			j = 1
			for i in range(0,int(len(l)),2):
				if l[i+1][-1] == "m":
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1].replace("m",""),"%Y/%m/%d/%H/%M")) + "\n"
				else:
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1],"%Y/%m/%d/%H/%M")) + "\n"
				j += 1
			stroka += "Выберите пост который хотите удалить отправив номер поста"
			await bot.send_message(message.chat.id,text = stroka,reply_markup = create_keyboard())
			await steps.delete_post.set()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так...',reply_markup = main_keyboard())

@dp.message_handler(content_types = ['text'], state = steps.delete_post,chat_id = id_admin) #Хендлер для удаления поста
async def delete_from(message, state: FSMContext):
	try:
		l = list_write_list()
		if message.text == 'Отмена':
			await bot.send_message(message.chat.id, text = 'Главное меню..',reply_markup = main_keyboard())
			await state.finish() 
		elif (message.text.isdigit()) == False:
			await bot.send_message(message.chat.id, text = 'Неккоректный ввод, повторите ввод или нажмите Отмена',reply_markup = create_keyboard())
			return
		elif (int(message.text))*2 > len(l) or int(message.text) < 1:
			await bot.send_message(message.chat.id, text = 'Такого поста не существует, повторите попытку или нажмите Отмена',reply_markup = create_keyboard())
			return	
		else:
			del(l[int(message.text)*2 - 1])
			del(l[int(message.text)*2 - 2])
			write_in_txt(l)
			await bot.send_message(message.chat.id, text = 'Пост удалён!', reply_markup = main_keyboard())
			os.execv(sys.executable, [sys.executable] + sys.argv)
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()


		

@dp.message_handler(lambda message: message.text and 'Создать пост' in message.text, state = '*',chat_id = id_admin) #Начало для добавления поста
async def create_post(message):
	await bot.send_message(message.chat.id,text = "Ссылка на пост",reply_markup = create_keyboard())
	await steps.take_post.set()


@dp.message_handler(content_types = ['text'], state = steps.take_post,chat_id = id_admin) #Хендлер для записи поста
async def main_change(message, state: FSMContext):
	try:
		if (message.text).find("\n") != -1 or len(message.text) > 250:
			await bot.send_message(message.chat.id, text = 'Объём поста не должен превышать 250 символов и 1 строку, повторите попытку или нажмите Отмена')
			return
		elif message.text == 'Отмена':
			await bot.send_message(message.chat.id, text = 'Главное меню..',reply_markup = main_keyboard())
			await state.finish()
		else:
			await state.update_data(post = message.text)
			await bot.send_message(message.chat.id,text = "Дату подскажи в формате Год/Месяц/День/Час/Минута 2021/11/13/15/24",reply_markup = create_keyboard())
			await steps.take_time.set()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()


@dp.message_handler(content_types = ['text'], state = steps.take_time,chat_id = id_admin) #Хендлер для записи даты
async def main_change(message, state: FSMContext):
	try:
		if message.text == 'Отмена':
			await bot.send_message(message.chat.id, text = 'Главное меню..', reply_markup = main_keyboard())
			await state.finish()
		else:
			l = list_write_list()
			try:
				datetime.strptime(message.text,"%Y/%m/%d/%H/%M")
			except:
				await bot.send_message(message.chat.id, text = 'Неккоректная дата, попытайтесь снова',reply_markup = create_keyboard())
				return
			if (datetime.strptime(message.text,"%Y/%m/%d/%H/%M")  <= datetime.now()):
				await bot.send_message(message.chat.id, text = 'Введённая дата идёт раньше сегодняшней даты',reply_markup = create_keyboard())
				return
			if len(l) != 0:
				count = -1 
				print(l[0][-1])
				for i in range(0,int(len(l)),2):
					if l[i + 1][-1] == "m":
						count = i
				await state.update_data(count_min = count)
				user_data = await state.get_data()
				if count != -1:
					if (datetime.strptime(message.text,"%Y/%m/%d/%H/%M")  < datetime.strptime(l[int(user_data['count_min']) + 1].replace("m",""),"%Y/%m/%d/%H/%M")) and datetime.strptime(message.text,"%Y/%m/%d/%H/%M") > datetime.now():
						l = list_write_list()
						f = open('text.txt','a')
						if len(l) == 0:
							f.write(user_data['post'] + "\n" + message.text)
						else:
							f.write("\n" + user_data['post'] + "\n" + message.text)
						f.close()
						await bot.send_message(message.chat.id,text = "Понял принял, пну этот пост ровно по времени", reply_markup = main_keyboard())
						os.execv(sys.executable, [sys.executable] + sys.argv)
					else:
						l = list_write_list()
						f = open('text.txt','a')
						if len(l) == 0:
							f.write(user_data['post'] + "\n" + message.text)
						else:
							f.write("\n" + user_data['post'] + "\n" + message.text)
						f.close()
						await bot.send_message(message.chat.id,text = "Понял принял, пну этот пост ровно по времени", reply_markup = main_keyboard())
						await state.finish()
				else:
					user_data = await state.get_data()
					l = list_write_list()
					f = open('text.txt','a')
					if len(l) == 0:
						f.write(user_data['post'] + "\n" + message.text)
					else:
						f.write("\n" + user_data['post'] + "\n" + message.text)
					f.close()
					await bot.send_message(message.chat.id,text = "Понял принял, пну этот пост ровно по времени", reply_markup = main_keyboard())
					await state.finish()
			else:
				user_data = await state.get_data()
				l = list_write_list()
				f = open('text.txt','a')
				if len(l) == 0:
					f.write(user_data['post'] + "\n" + message.text)
				else:
					f.write("\n" + user_data['post'] + "\n" + message.text)
				f.close()
				await bot.send_message(message.chat.id,text = "Понял принял, пну этот пост ровно по времени", reply_markup = main_keyboard())
				os.execv(sys.executable, [sys.executable] + sys.argv)
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()



@dp.message_handler(lambda message: message.text and 'Редактировать пост' in message.text, state = '*',chat_id = id_admin) #Начало для изменения параметра поста
async def updt(message):
	try:
		if message.text == "Отмена":
			await bot.send_message(message.chat.id, text = 'Главное меню..', reply_markup = main_keyboard())
			await state.finish()
		l = list_write_list()
		if len(l) == 0:
			await bot.send_message(message.chat.id,text = 'Посты отсутствуют',reply_markup = main_keyboard())
		else:
			stroka = ""
			j = 1
			for i in range(0,int(len(l)),2):
				if l[i+1][-1] == "m":
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1].replace("m",""),"%Y/%m/%d/%H/%M")) + "\n"
				else:
					stroka += str(j) + ". Пост: " + l[i] + "\n Время отправки: " + str(datetime.strptime(l[i + 1],"%Y/%m/%d/%H/%M")) + "\n"
				j += 1
			stroka += "Отправьте номер поста"
			await bot.send_message(message.chat.id,text = stroka,reply_markup = create_keyboard())
			await steps.update_statement.set()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так',reply_markup = main_keyboard())



@dp.message_handler(content_types = ['text'], state = steps.update_statement,chat_id = id_admin) #Хендлер промежуточный для выбора постов
async def upd_stat(message, state: FSMContext):
	try:
		l = list_write_list()
		if message.text == 'Отмена': 
			await bot.send_message(message.chat.id, text = 'Главное меню..',reply_markup = main_keyboard())
			await state.finish()
		elif (message.text.isdigit()) == False:
			await bot.send_message(message.chat.id, text = 'Неккоректный ввод, повторите ввод или нажмите Отмена',reply_markup = create_keyboard())
			return
		elif (int(message.text))*2 > len(l) or int(message.text) < 1:
			await bot.send_message(message.chat.id, text = 'Такого поста не существует, повторите попытку или нажмите Отмена',reply_markup = create_keyboard())
			return
		else:
			await state.update_data(count = message.text)
			await bot.send_message(message.chat.id,text = "Выберите что хотите изменить",reply_markup = post_data_keyboard())
			await steps.check_switch.set()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()
	
@dp.message_handler(content_types = ['text'], state = steps.check_switch,chat_id = id_admin) #Хендлер для выбора поста/времени
async def chk_switch(message, state: FSMContext):
	try:
		if (message.text == "Дата"):
			await bot.send_message(message.chat.id,text = "Введите дату в формате Год/Месяц/День/Час/Минута 2021/11/13/15/24",reply_markup = create_keyboard())
			await steps.update_data.set()
		elif (message.text == "Пост"):
			await bot.send_message(message.chat.id,text = "Введите пост:",reply_markup = create_keyboard())
			await steps.update_post.set()
		elif (message.text == "Отмена"): 
			await bot.send_message(message.chat.id,text = "Начальное меню..",reply_markup = main_keyboard())
			await state.finish()
		else:
			await bot.send_message(message.chat.id,text = "Ты ошибся, выбери то что нужно",reply_markup = post_data_keyboard())
			return
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()

@dp.message_handler(content_types = ['text'], state = steps.update_data,chat_id = id_admin) #Хендлер для изменения даты
async def upd_data(message, state: FSMContext):
	try:	
		if message.text == 'Отмена':
			await bot.send_message(message.chat.id, text = 'Главное меню..', reply_markup = main_keyboard())
			await state.finish()
		else:
			try:
				datetime.strptime(message.text,"%Y/%m/%d/%H/%M")
			except:
				await bot.send_message(message.chat.id, text = 'Неккоректная дата, попытайтесь снова',reply_markup = create_keyboard())
				return
		if (datetime.strptime(message.text,"%Y/%m/%d/%H/%M")  <= datetime.now()):
			await bot.send_message(message.chat.id, text = 'Введённая дата идёт раньше сегодняшней даты',reply_markup = create_keyboard())
			return
		l = list_write_list()
		count = -1 
		for i in range(0,int(len(l)),2):
			if l[i + 1][-1] == "m":
				count = i
		await state.update_data(count_min = count)
		user_data = await state.get_data()
		if user_data['count_min'] != -1:
			if (datetime.strptime(message.text,"%Y/%m/%d/%H/%M")  < datetime.strptime(l[int(user_data['count_min']) + 1].replace("m",""),"%Y/%m/%d/%H/%M")) or (datetime.strptime(message.text,"%Y/%m/%d/%H/%M")  > datetime.strptime(l[int(user_data['count_min']) + 1].replace("m",""),"%Y/%m/%d/%H/%M")):
				l[int(user_data['count'])*2 - 1] = message.text
				write_in_txt(l)
				await bot.send_message(message.chat.id, text = "Запись изменена!", reply_markup = main_keyboard())
				os.execv(sys.executable, [sys.executable] + sys.argv)
			else:
				l[int(user_data['count'])*2 - 1] = message.text
				write_in_txt(l)
				await bot.send_message(message.chat.id, text = "Запись изменена!", reply_markup = main_keyboard())
				await state.finish()
		else:
			l[int(user_data['count'])*2 - 1] = message.text
			write_in_txt(l)
			await bot.send_message(message.chat.id, text = "Запись изменена!", reply_markup = main_keyboard())
			await state.finish()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()

@dp.message_handler(content_types = ['text'], state = steps.update_post,chat_id = id_admin) #Хендлер для изменения поста
async def upd_post(message, state: FSMContext):	
	try:
		if message.text == 'Отмена':
			await bot.send_message(message.chat.id, text = 'Главное меню..', reply_markup = main_keyboard())
			await state.finish()
		elif (message.text).find("\n") != -1 or len(message.text) > 250:
			await bot.send_message(message.chat.id, text = 'Объём поста не должен превышать 250 символов и 1 строку, повторите попытку или нажмите Отмена',reply_markup = None)
			return
		else:
			l = list_write_list()
			user_data = await state.get_data()
			if int(user_data['count']) == 1:
				l[0] = message.text
			else: 
				l[int(user_data['count'])*2 - 2] = message.text
			write_in_txt(l)
			await bot.send_message(message.chat.id, text = "Запись изменена!",reply_markup = main_keyboard())
			await state.finish()
	except:
		await bot.send_message(message.chat.id,text = 'Что-то пошло не так,возвращение в начальное меню...',reply_markup = main_keyboard())
		await state.finish()


async def on_startup(x): #Функция на старт бота 
	try:
		await main()
		asyncio.create_task(wait_post())
	except:
		os.execv(sys.executable, [sys.executable] + sys.argv)


async def wait_post(): #Функция для просмотра минимального поста и остановке функции
	global timeout 
	try:
		l = list_write_list()
		if len(l) == 0:
			timeout = 0
			await bot.send_message(id_admin,text = "Список записей пуст, цикл отправки постов остановлен")
			timeout = datetime.now()
			await asyncio.sleep(defolt_time_wait)
			return await wait_post()
		for i in range(0,int(len(l)),2):
			if l[i + 1][-1] == "m":
				l[i + 1] = l[i + 1].replace("m","") 
		minimum = datetime.strptime(l[1],"%Y/%m/%d/%H/%M")
		count = 1
		for i in range(len(l)):
			if i % 2 == 1:
				if minimum > datetime.strptime(l[i],"%Y/%m/%d/%H/%M"):
					minimum = datetime.strptime(l[i],"%Y/%m/%d/%H/%M")
					count = i
		print(minimum - datetime.now())
		l[count] += "m"
		write_in_txt(l)
		await bot.send_message(id_admin,text = "Бот работает, цикл ждёт времени записи")
		timeout = datetime.now()
		await asyncio.sleep((minimum - datetime.now()).total_seconds())
		l = list_write_list()
		await bot.send_message(id_chat,text = l[count - 1])
		l = list_write_list()
		del(l[count])
		del(l[count - 1])
		write_in_txt(l)
		return await wait_post()
	except:
		await bot.send_message(id_admin,text = 'Что-то пошло не так...',reply_markup = main_keyboard())



if __name__ == '__main__':
	executor.start_polling(dp, skip_updates = True, on_startup = on_startup)


