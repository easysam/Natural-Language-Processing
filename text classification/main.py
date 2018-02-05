import os
import re
import math
import cmath
# Document Frequency
DF = dict()
# 拉普拉斯估计P(ti|Ci)
PTC = dict()
# 词典
dictionary = dict()
newsgroups = os.listdir('./20_newsgroups')
for newsgroup in newsgroups:
    dictionary[newsgroup] = dict()
    PTC[newsgroup] = dict()

with open('./dictionary.txt', 'r', encoding='utf-8') as curFile:
    for line in curFile.readlines():
        parameters = re.split(r'[\s]+', line)
        dictionary[parameters[0]][parameters[1]] = int(parameters[2])

with open('./DF.txt', 'r', encoding='utf-8') as curFile:
    for line in curFile.readlines():
        parameters = re.split(r'[\s]+', line)
        DF[parameters[0]] = int(parameters[1])

for newsgroup in dictionary:
    for other in DF:
        if other in dictionary[newsgroup]:
            PTC[newsgroup][other] = \
                (1 + dictionary[newsgroup][other]) / (len(dictionary[newsgroup]) + dictionary[newsgroup]['#ALL#'])
        else:
            PTC[newsgroup][other] = 1 / (len(dictionary[newsgroup]) + dictionary[newsgroup]['#ALL#'])

successRate = 0
successRates = dict()
testers = os.listdir('./tester')
for tester in testers:
    tempSuccessRate = 0
    testerFiles = os.listdir('./tester/' + tester)
    for testerFile in testerFiles:
        with open('./tester/' + tester + '/' + testerFile, 'r', encoding='Windows 1252') as curFile:
            tempFileStatics = dict()
            tempFileBelong = dict()
            for newsgroup in dictionary:
                tempFileBelong[newsgroup] = 0
            for line in curFile.readlines():
                words = re.split(r'[\s|`|~|!|@|#|$|%|^|&|*|(|)|=|_|+|[|{|}|;|,|.|<|>/|?|:|\-|"|\'|\\|\]]+', line)
                for word in words:
                    if word == '':
                        continue
                    if re.match(r'[\d]+.[\d]+', word) or (word not in DF):
                        word = '#NUMBER#'
                    if word in tempFileStatics:
                        tempFileStatics[word] += 1
                    else:
                        tempFileStatics[word] = 1
            for newsgroup in tempFileBelong:
                son = 1
                parent = 0
                for word in tempFileStatics:
                    son += cmath.log(math.pow(PTC[newsgroup][word], tempFileStatics[word]), 2)
                for tempNewsgroup in PTC:
                    temp = 1
                    for word in tempFileStatics:
                        temp += cmath.log(math.pow(PTC[tempNewsgroup][word], tempFileStatics[word]), 2)
                    parent += temp
                tempFileBelong[newsgroup] = son.real - parent.real
            for eachItem in sorted(tempFileBelong.items(), key=lambda item: item[1], reverse=True):
                print(tester + ':' + eachItem[0] + ':' + str(tempFileBelong[eachItem[0]]))
                if eachItem[0] == tester:
                    tempSuccessRate += 1
                    successRate += 1
                    break
                if tester == 'talk.religion.misc' and eachItem[0] == 'alt.atheism':
                    tempSuccessRate += 1
                    successRate += 1
                    break
                if tester == 'alt.atheism' and eachItem[0] == 'talk.religion.misc':
                    tempSuccessRate += 1
                    successRate += 1
                    break
                if math.isnan(tempFileBelong[eachItem[0]]):
                    continue
                break
            tempFileBelong.clear()
            tempFileStatics.clear()
    tempSuccessRate /= 200
    successRates[tester] = tempSuccessRate
    print(str(tempSuccessRate))

successRate /= 4000
print('\nSuccess Rate：' + str(successRate))
for eachSuccessRate in successRates:
    print(eachSuccessRate + ':' + str(successRates[eachSuccessRate]))
#        print('\n')
