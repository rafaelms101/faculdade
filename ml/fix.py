file = open('dota_old.txt')
str = file.read()
lines = str.split('\n')
for line in lines:
    ints = line.split()
    if len(ints) != 13:
        print(line)
