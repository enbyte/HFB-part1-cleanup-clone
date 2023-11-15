from random import shuffle
import os

names = ['peena lop', 'tall', 'gavin', 'nayla', 'zadie', 'Lord of all Goodness, Sunny Crowder-Sklar', 'jo a quin']

shuffled = shuffle(names)
same = True

while same:
    for i in range(len(names)):
        if names[i] == shuffled[i]:
            continue

for i in range(len(names)):
    os.system('clear')
    input("hello %s ur person is %s next is %s" % (names[i], shuffled[i], names[i+1]))


    