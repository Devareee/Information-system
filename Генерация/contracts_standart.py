from datetime import date
import random

n = 500000

start_date = date(day=1, month=1, year=2010).toordinal()
end_date = date(day=1, month=1, year=2022).toordinal()

types=['Личное','Имущественное','Медицинское','ОСАГО']

f7 = open('c_name.txt', encoding='utf-8')
names=f7.read().split('\n')
f7.close()

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

def get_rand_name():
    if random.randint(0, 1):
        return str(fem_sur[random.randint(0, 254)]+" "+fem_name[random.randint(0, 185)]+" "+fem_sec[random.randint(0, 56)])
    else:
        return str(male_sur[random.randint(0, 249)]+" "+male_name[random.randint(0, 209)]+" "+male_sec[random.randint(0, 64)])

def get_rand_date():
    return date.fromordinal(random.randint(start_date, end_date)).strftime("%d.%m.%Y")

f = open('contracts_standart.sql', 'w', encoding='utf-8')
f.write("INSERT INTO contracts_standart VALUES")
for i in range (n-1):
	f.write(" (DEFAULT, '" + names[random.randint(0, 49)] + str(random.randint(1, 5)) + "', '" + get_rand_name() + "', '"
         + types[random.randint(0, 3)] + "', " + str(random.randint(1, 99) * 10**random.randint(1, 4)) + ", '" + get_rand_date() + "'),")
f.write(" (DEFAULT, '" + names[random.randint(0, 49)] + str(random.randint(1, 5)) + "', '" + get_rand_name() + "', '"
         + names[random.randint(0, 3)] + "', " + str(random.randint(1, 99) * 10**random.randint(1, 4)) + ", '" + get_rand_date() + "')")
f.write(";")
f.close()
