# read test.txt
with open("test.txt") as file:
    for line in file:
        print(line[0])
