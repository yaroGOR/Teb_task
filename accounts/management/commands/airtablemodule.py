import os
from pyairtable import Table, Api
from django.conf import settings 

#api_key = Api('keyLHrirqC2QXV8fe')
from django.core.management.base import BaseCommand

tableName='Table 1'
api = settings.AIRTABLE_API
baseId=settings.AIRTABLE_BASEID
class Command(BaseCommand):
	def handle(self, *args, **options):


		table = Table(api, baseId, table)
		print(table)
		print(type(table.all()))
		for i in table.all():
			print(i)
		print(table.all()[2]['fields'])

		table.create({'ID':'1','Name':'Pupkin','Telegram name':'@pupkin','password':'123'})
class AirtableCustom():
	def set_connection(table='Table 1'):
		table = Table(api, baseId, table)
		print('pumpum')
		print(table.all())
	def new_record(tgId, name, telegram_name, password):
		table = Table(api, baseId, 'Table 1')
		table.create({'ID':tgId,'Name':name,'Telegram name':'@'+telegram_name,'password':password})

