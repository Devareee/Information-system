from datetime import date
import random

n = 100000

sc = ["Государственный служащий", "Работник торговой сферы", "Работник бюджетной сферы", "Безработный", "Предприниматель", "Пенсионер", "Рабочий", "Студент"]
ct = ['ООО', 'ОАО', 'ЗАО', 'Государственное предприятие', 'Полное товарищество', 'Коммандитное товарищество', 'Хозяйственное общество', 'Производственный кооператив']
c = ['Донецк', 'Макеевка', 'Ясиноватая', 'Горловка', 'Харцызск', 'Енакиево', 'Торез', 'Шахтерск', 'Новоазовск', 'Старобешево']
ins = ['Медицинское', 'Социальное', 'Пенсионное', 'ОСАГО', 'Банковский вклад', 'Пассажирское', 'Ответственность', 'Личное', 'Имущественное']

bd1 = date(day=1, month=1, year=1940).toordinal()
bd2 = date(day=1, month=1, year=2006).toordinal()

start_date = date(day=1, month=1, year=2010).toordinal()
end_date = date(day=1, month=1, year=2022).toordinal()

def get_rand_bd():
    return date.fromordinal(random.randint(bd1, bd2)).strftime("%d.%m.%Y")

def get_rand_date():
    return date.fromordinal(random.randint(start_date, end_date)).strftime("%d.%m.%Y")

fem_name=fem_sur=fem_sec=male_name=male_sur=male_sec=[]
f1 = open('fem_sur.txt', encoding='utf-8')
fem_sur=f1.read().split('\n')
f1.close()
f2 = open('fem_name.txt', encoding='utf-8')
fem_name=f2.read().split('\n')
f2.close()
f3 = open('fem_sec.txt', encoding='utf-8')
fem_sec=f3.read().split('\n')
f3.close()
f4 = open('male_sur.txt', encoding='utf-8')
male_sur=f4.read().split('\n')
f4.close()
f5 = open('male_name.txt', encoding='utf-8')
male_name=f5.read().split('\n')
f5.close()
f6 = open('male_sec.txt', encoding='utf-8')
male_sec=f6.read().split('\n')
f6.close()

f7 = open('street.txt', encoding='utf-8')
street=f7.read().split('\n')
f7.close()

def get_rand_name():
    if random.randint(0, 1):
        return str(fem_sur[random.randint(0, 254)]+" "+fem_name[random.randint(0, 185)]+" "+fem_sec[random.randint(0, 56)])
    else:
        return str(male_sur[random.randint(0, 249)]+" "+male_name[random.randint(0, 209)]+" "+male_sec[random.randint(0, 64)])

f = open('c_name.txt', encoding='utf-8')
names=f.read().split('\n')
f.close()

f = open('json_date.sql', 'w', encoding='utf-8')
for i in range (n):
	f.write('INSERT INTO json_table (data) VALUES (\'{"name": "' + get_rand_name() + '", "bd": "' + get_rand_bd() + '", "social_status": "' + sc[random.randint(0, 7)] 
    + '", "phone": "' + "38071" + str(random.randint(1111111, 9999999)) + '", "contract": [{"branch": {"company": {"title" : "' + names[random.randint(0, 49)] 
    + '","type" : "' + ct[random.randint(0, 7)] + '","city" : "' + c[random.randint(0, 9)] + '","year": ' + str(random.randint(1970, 2022)) + '}, "title2": "' 
    + names[random.randint(0, 49)] + str(random.randint(1, 5)) + '", "address": "' + street[random.randint(0, 29)] + ", " + str(random.randint(1, 100)) + '", "workers": ' 
    + str(random.randint(5, 20000)) + '}, "insurance": "' + ins[random.randint(0, 8)] + '", "sum" : ' + str(random.randint(1, 99) * 10**random.randint(1, 4)) 
    + ', "date": "' + get_rand_date() + '"}, {"branch": {"company": {"title" : "' + names[random.randint(0, 49)] 
    + '","type" : "' + ct[random.randint(0, 7)] + '","city" : "' + c[random.randint(0, 9)] + '","year": ' + str(random.randint(1970, 2022)) + '}, "title2": "' 
    + names[random.randint(0, 49)] + str(random.randint(1, 5)) + '", "address": "' + street[random.randint(0, 29)] + ", " + str(random.randint(1, 100)) + '", "workers": ' 
    + str(random.randint(5, 20000)) + '}, "insurance": "' + ins[random.randint(0, 8)] + '", "sum" : ' + str(random.randint(1, 99) * 10**random.randint(1, 4)) 
    + ', "date": "' + get_rand_date() + '"}]}\');\n');
f.close()
