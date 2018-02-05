import re

parameterA = dict()
parameterB = dict()
parameterPI = dict()
parameterPI['#ALL#'] = 0

def addToB(temp):
    if temp[1] in parameterB:
        if temp[0] in parameterB[temp[1]]:
            parameterB[temp[1]][temp[0]] += 1
        else:
            parameterB[temp[1]][temp[0]] = 1
    else:
        parameterB[temp[1]] = dict()
        parameterB[temp[1]]['#ALL#'] = 0
        parameterB[temp[1]][temp[0]] = 1
    parameterB[temp[1]]['#ALL#'] += 1
    return


with open('./source.txt', 'r', encoding='utf-8') as sourceFile:
    for line in sourceFile.readlines():
        if line == '\n':
            continue
        words = re.split(r'[\s]+', line[22:].strip())
        # 统计参数PI
        temp = re.split(r'[/]', words[0])
        if temp[1] in parameterPI:
            parameterPI[temp[1]] += 1
        else:
            parameterPI[temp[1]] = 1
        parameterPI['#ALL#'] += 1
        # 统计参数A、B
        for i in range(0, len(words) - 1):
            a = re.split(r'[/]', words[i])
            b = re.split(r'[/]', words[i+1])
            # 记录参数A
            tempString = a[1]+'/'+b[1]
            if tempString in parameterA:
                parameterA[tempString] += 1
            else:
                if a[1]+'/#ALL#' not in parameterA:
                    parameterA[a[1] + '/#ALL#'] = 0
                parameterA[tempString] = 1
            parameterA[a[1] + '/#ALL#'] += 1
            # 记录参数B
            addToB(a)
            addToB(b)

with open('./A.txt', 'w', encoding='utf-8') as curFile:
    items = sorted(parameterA.items())
    for item, value in items:
        curFile.write(item + ' ' + str(value)+'\n')

with open('./B.txt', 'w', encoding='utf-8') as curFile:
    for pos in parameterB:
        for word in parameterB[pos]:
            curFile.write(pos+'/'+word+'/'+str(parameterB[pos][word])+'\n')

with open('./PI.txt', 'w', encoding='utf-8') as curFile:
    for item in parameterPI:
        curFile.write(item + ' ' + str(parameterPI[item])+'\n')
