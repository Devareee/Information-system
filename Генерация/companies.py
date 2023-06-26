import random

n = 2500

f = open('c_name.txt', encoding='utf-8')
names=f.read().split('\n')
f.close()

f = open('companies.sql', 'w', encoding='utf-8')
for i in range (n):
	f.write("INSERT INTO companies VALUES (DEFAULT, '" + names[random.randint(0, 49)] + "', " + str(random.randint(1, 8)) + ", " + str(random.randint(1970, 2022)) + ", " + str(random.randint(1, 10)) + ", " + "38071" + str(random.randint(1111111, 9999999)) + ");\n")
f.close()
