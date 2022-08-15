from django.core.management.base import BaseCommand
from django.conf import settings 
from .airtablemodule import AirtableCustom as AT
from accounts.models import Account, MyAccountManager
#from pathlib import Path

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types.message import ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from asgiref.sync import sync_to_async

from asgiref.sync import sync_to_async

import os

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"




class FSM(StatesGroup):
	name = State()
	password1=State()
	password2=State()
	passwordcorrect=State()


class Command(BaseCommand):
	


	help="TelegramBot"


	def handle(self, *args, **options):
		storage = MemoryStorage()
		bot = Bot(token = settings.TELEGRAM_TOKEN)
		print(settings.TELEGRAM_TOKEN)
		dp = Dispatcher(bot, storage=storage)

		@dp.message_handler(commands=['start'], state = None)
		async def process_start_command(message: types.Message):
			data1 = [message.from_user.id, message.from_user.first_name, message.from_user.username]
			await FSM.password1.set()
			await message.reply(f"Hi, {message.from_user.first_name}, create password:")
			print(data1)

		@dp.message_handler(state=FSM.password1)
		async def save_password(message: types.Message, state:FSMContext):
			pw1=message.text
			print(pw1)
			async with state.proxy() as data:
				data['password1']=pw1
				data['name']=message.from_user.first_name
				data['tg_id']=message.from_user.id
				data['telegram_name']=message.from_user.username

			await FSM.password2.set()
			await message.reply('Repeat password:')

		@dp.message_handler(state = FSM.password2)
		async def password_check(message: types.Message, state=FSMContext):
			pw2 = message.text
			async with state.proxy() as data:
				data['password2']=pw2
			if data['password1']==data['password2']:
				await message.reply('Password is correct')
				await FSM.passwordcorrect.set()
				async with state.proxy() as data:
					print(data)
				#печать данных в базу данных

				#AT.set_connection()
				AT.new_record(
					tgId=str(data['tg_id']), 
					name = data['name'], 
					telegram_name=data['telegram_name'], 
					password=data['password1']
					)
				Account.objects.create_user(
				tgname=data['telegram_name'], 
				password=data['password1'],
				tgid=data['tg_id'],
				username=data['name'])
				await message.reply(f'''Registration is finished. 
				https://herokuteb.herokuapp.com/accounts/login/ 
				Auth with your telegram_name: {data['telegram_name']} 
				and password''')
				print('registration finished')
				await state.finish()

			elif data['password1']!=data['password2']:
				await message.reply('Password is not correct, try again')
				await FSM.password1.set()

		


			     
			




		executor.start_polling(dispatcher=dp, skip_updates = True)









#_____bot____








		
	
