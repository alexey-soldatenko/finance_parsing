from lxml import html
import requests
from datetime import date
import csv

''' Собираем данные о курсах доллара, евро и рубля по отношению к гривне'''

headers = {'User-Agent': 'Mozilla/5.0'}
#запрашиваем страницу и записываем её в файл
request = requests.get('https://finance.i.ua/', headers=headers)
with open('parse_finance.html', 'w') as file:
	file.write(request.text)

#парсим файл, ищем нужную таблицу, все её строки
document = html.parse('parse_finance.html')
table = document.xpath('//table[@class="table table-data -important"]')[2]
tr = table.findall('.//tr')

#находим значение курса валют в отдельных строках
usd = tr[1].find('.//span/span').text
eur = tr[2].find('.//span/span').text
rub = tr[4].find('.//span/span').text

#заполняем словарь значениями курсов и текущей даты
date_now = date.today()
curses = {}
curses["usd"] = usd
curses["eur"] = eur
curses["rub"] = rub
curses["date"] = date_now

field_names = ['usd', 'eur', 'rub', 'date']
header = False

try:
	with open('currencies.csv', 'r') as file:
		#проверяем наличие заголовка в файле
		if file.readline() == 'usd,eur,rub,date\n':
			header = True

except FileNotFoundError:
	pass

#записываем значение словаря в файл csv
with open('currencies.csv', 'a') as file:
	csv_writer = csv.DictWriter(file, fieldnames=field_names)
	if not header:
		csv_writer.writeheader()
	csv_writer.writerow(curses) 
