from datetime import date
import random

n = 2500

start_date = date(day=1, month=1, year=2010).toordinal()
end_date = date(day=1, month=1, year=2022).toordinal()

def get_rand_date():
    return date.fromordinal(random.randint(start_date, end_date)).strftime("%d.%m.%Y")

f = open('contracts.sql', 'w', encoding='utf-8')
for i in range (n):
	f.write("INSERT INTO contracts VALUES (DEFAULT, " + str(random.randint(1, 2500)) + ", " + str(random.randint(1, 2500)) + ", " + str(random.randint(1, 9)) + ", " + str(random.randint(1, 99)) + str(10**random.randint(1, 4)) + ", '" + get_rand_date() + "');\n")
f.close()
