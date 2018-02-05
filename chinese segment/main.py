import re

print("Welcome to the chinese segment test!")
print("Training...")
fsource = open("source.txt")
data = fsource.readlines()
lines_of_training = len(data)
# print("lines of source: ", len(data))        # output the length of the file
dictionary = set()
for line in data:
    if len(line) > 20:
        line = line[line.index('/m'):]
        regular = re.compile(r'[a-zA-Z\[\]\s{*}]')
        line, n = re.subn(regular, '', line)
        line = line.split('/')
        for item in line:
            dictionary.add(item)
words_of_source = len(dictionary)
# print("words of source: ", len(dictionary))
max_word_length = 0
for item in dictionary:
    if len(item) > max_word_length:
        max_word_length = len(item)
        # print(item)


precision = 0
recall = 0

fsource = open("tester.txt")
data = fsource.readlines()
# print("lines of tester: ", len(data))        # output the length of the file
lines_amount = 0
for line in data:
    if len(line) > 20:
        lines_amount = lines_amount + 1
        line = line[line.index('/m'):]
        regular = re.compile(r'[a-zA-Z|\[|\]|\s|{*}]')
        line, n = re.subn(regular, '', line)

        temp = line
        temp = set(temp.split('/'))  # The true segment
        temp_result = set()

        regular = re.compile(r'/')
        line, n = re.subn(regular, '', line)
        # print(line)
        line_length = len(line)
        x = 0
        while x < line_length:
            y = min(x + max_word_length, line_length)
            while y > x:
                if line[x:y] in dictionary:
                    # print(line[x:y])
                    temp_result.add(line[x:y])
                    x = y
                    break
                y = y - 1
                if y == x:
                    # print(line[x])
                    temp_result.add(line[x:x])
                    x = x + 1
        # print(len(temp_result & temp) / len(temp_result))
        precision = precision + len(temp_result & temp) / len(temp_result)
        # print(len(temp_result & temp) / len(temp))
        recall = recall + len(temp_result & temp) / len(temp)
recall = recall/lines_amount
precision = precision/lines_amount
print("The final recall is ", recall)
print("The final precision is ", precision)

print("the F is ", 2*recall*precision/(recall + precision))

fsource.close()

print("\n")
print("lines of training set is ", lines_of_training)
print("words of training set is ", words_of_source)

print("The max word length of the training set is ", max_word_length)

temp_dictionary = set()
fsource = open("tester.txt")
data = fsource.readlines()
print("lines of tester: ", len(data))        # output the length of the file
for line in data:
    if len(line) > 20:
        line = line[line.index('/m'):]
        regular = re.compile(r'[a-zA-Z|\[|\]|\s|{*}|/]')
        line, n = re.subn(regular, '', line)
        line = line.split('/')
        for item in line:
            temp_dictionary.add(item)
print("words of tester: ", len(temp_dictionary))

c = 0
while c != 'q' and c != 'Q':
    c = input("Press [I] to input new text\nOr [Q] to quit")
    if c == 'i' or c == 'I':
        c = input("Please input your test:")

        line_length = len(c)
        x = 0
        while x < line_length:
            y = min(x + max_word_length, line_length)
            while y > x:
                if c[x:y] in dictionary:
                    print(c[x:y])
                    temp_result.add(c[x:y])
                    x = y
                    break
                y = y - 1
                if y == x:
                    print(line[x])
                    temp_result.add(c[x:x])
                    x = x + 1

