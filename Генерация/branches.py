import random

n = 2500

f1 = open('street.txt', encoding='utf-8')
street=f1.read().split('\n')
f1.close()

f2 = open('c_name.txt', encoding='utf-8')
names=f2.read().split('\n')
f2.close()

f = open('branches.sql', 'w', encoding='utf-8')
for i in range (n):
	f.write("INSERT INTO branches VALUES (DEFAULT, " + str(random.randint(1, 2500)) + ", '" + names[random.randint(0, 49)] + str(random.randint(1, 5)) + "', " + str(random.randint(1, 10)) + ", '" + street[random.randint(0, 29)] + ", " + str(random.randint(1, 100)) + "', " + "38071" + str(random.randint(1111111, 9999999)) + ", " + str(random.randint(5, 20000)) + ");\n")
f.close()
