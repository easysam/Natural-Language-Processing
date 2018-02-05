import re
import cmath

parameterA = dict()
parameterB = dict()
parameterPI = dict()
with open('./A.txt', 'r', encoding='utf-8') as curFile:
    for line in curFile.readlines():
        parameter = re.split(r'[\s|/]+', line.strip())
        if parameter[1] == '#ALL#':
            parameterA[parameter[0]] = dict()
            parameterA[parameter[0]]['#ALL#'] = int(parameter[2])
        else:
            parameterA[parameter[0]][parameter[1]] = float(parameter[2])/parameterA[parameter[0]]['#ALL#']

with open('./B.txt', 'r', encoding='utf-8') as curFile:
    for line in curFile.readlines():
        parameter = re.split('/', line.strip())
        if parameter[1] == '#ALL#':
            parameterB[parameter[0]] = dict()
            parameterB[parameter[0]][parameter[1]] = int(parameter[2])
        else:
            parameterB[parameter[0]][parameter[1]] = float(parameter[2])/parameterB[parameter[0]]['#ALL#']

with open('./PI.txt', 'r', encoding='utf-8') as curFile:
    parameterPI['#ALL#'] = int(re.split(' ', curFile.readline().strip())[1])
    for line in curFile.readlines():
        parameter = re.split(' ', line.strip())
        parameterPI[parameter[0]] = float(parameter[1])/parameterPI['#ALL#']

for pos in parameterB:
    if pos not in parameterPI:
        parameterPI[pos] = float(0.5) / 1000000

for i in parameterB:
    if i not in parameterA:
        parameterA[i] = dict()
        parameterA[i]['#ALL#'] = len(parameterB)
    for j in parameterB:
        if j not in parameterA[i]:
            parameterA[i][j] = float(0.5)/1000000

for i in parameterA:
    for j in parameterA[i]:
        if j == '#ALL#':
            continue
        parameterA[i][j] = cmath.log(parameterA[i][j], 2).real

for i in parameterB:
    for j in parameterB[i]:
        if j == '#ALL#':
            continue
        parameterB[i][j] = cmath.log(parameterB[i][j], 2).real

for i in parameterPI:
    if i == '#ALL#':
        continue
    parameterPI[i] = cmath.log(parameterPI[i], 2).real


posToNum = dict()
numToPos = dict()
i = 1
for pos in parameterB:
    posToNum[pos] = i
    numToPos[i] = pos
    i += 1

allIn = 0
successRet = 0
with open('./tester.txt', 'r', encoding='utf-8') as curFile:
    lines = curFile.readlines()
    '''每行单独解决，输入观测序列，输出词性序列。正确数和总数累加，最后算正确率'''
    for line in lines:
        if line == '\n':
            continue
        '''用以存储输入序列'''
        sequenceIn = list()
        sequenceOut = list()
        # 用以存储维特比矩阵、回退矩阵
        viterbiMatrix = list()
        viterbiMatrix.append(dict())
        viterbiPath = list()
        viterbiPath.append(dict())
        finalPath = dict()

        words = re.split(r'[\s]+', line[22:].strip())
        allIn += len(words)
        for word in words:
            tempComb = re.split('/', word.strip())
            sequenceIn.append(tempComb)
        sequenceIn.insert(0, (0, 0))
        # 初始化
        viterbiMatrix.append(dict())
        viterbiPath.append(dict())
        for pos in parameterB:
            if sequenceIn[1][0] not in parameterB[pos]:
                parameterB[pos][sequenceIn[1][0]] = cmath.log(float(0.5)/1000000, 2).real
            viterbiMatrix[1][posToNum[pos]] = parameterPI[pos]+parameterB[pos][sequenceIn[1][0]]
            viterbiPath[1][posToNum[pos]] = 0

        # 归纳计算
        for t in range(2, len(sequenceIn)):
            viterbiMatrix.append(dict())
            viterbiPath.append(dict())
            for j in parameterB:
                tempMax = float('-Inf')
                for i in parameterB:
                    tempFloat = viterbiMatrix[t-1][posToNum[i]] + parameterA[i][j]
                    if tempFloat > tempMax:
                        tempMax = viterbiMatrix[t-1][posToNum[i]] + parameterA[i][j]
                        viterbiPath[t][posToNum[j]] = posToNum[i]
                if sequenceIn[t][0] not in parameterB[j]:
                    parameterB[j][sequenceIn[t][0]] = cmath.log(float(0.5) / 1000000, 2).real
                viterbiMatrix[t][posToNum[j]] = tempMax+parameterB[j][sequenceIn[t][0]]

        t = len(sequenceIn)-1
        tempMax = float('-Inf')
        # 终结
        for i in viterbiMatrix[t]:
            if viterbiMatrix[t][i] > tempMax:
                tempMax = viterbiMatrix[t][i]
                finalPath[t] = i

        for i in range(1, t):
            finalPath[t-i] = viterbiPath[t-i+1][finalPath[t-i+1]]
        tempSuccessRate = 0
        print('输入序列：', end='')
        for word in words:
            print(word, end=' ')
        print('\n输出序列：', end='')
        for i in range(1, len(finalPath)+1):
            print(sequenceIn[i][0] + '/' + numToPos[finalPath[i]], end=' ')
            if numToPos[finalPath[i]] == sequenceIn[i][1]:
                successRet += 1
                tempSuccessRate += 1
        print('\n成功率：' + str(round(tempSuccessRate/len(words), 3)))

        viterbiPath.clear()
        viterbiMatrix.clear()
        finalPath.clear()
        sequenceIn.clear()
        sequenceOut.clear()

    print('总成功率：' + str(successRet / allIn))
