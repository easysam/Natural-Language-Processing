import os
import re

newsgroups = os.listdir('./20_newsgroups')
dictionary = dict()
CF = dict()
DF = dict()
tempFileDict = list()
for newsgroup in newsgroups:
    dictionary[newsgroup] = dict()
    dictionary[newsgroup]['#ALL#'] = 0
    for file in os.listdir('./20_newsgroups/' + newsgroup):
        with open('./20_newsgroups/' + newsgroup + '/' + file, 'r', encoding='Windows 1252') as curFile:
            for line in curFile.readlines():
                words = re.split(r'[\s|`|~|!|@|#|$|%|^|&|*|(|)|=|_|+|[|{|}|;|,|.|<|>/|?|:|\-|"|\'|\\|\]]+', line)
                for word in words:
                    if word == '':
                        continue
                    if re.match(r'[\d]+.[\d]+', word):
                        word = '#NUMBER#'
                    if word in dictionary[newsgroup]:
                        dictionary[newsgroup][word] += 1
                    else:
                        dictionary[newsgroup][word] = 1
                        # 统计 Category Frequency
                        if word in CF:
                            CF[word] += 1
                        else:
                            CF[word] = 1
                    if word not in tempFileDict:
                        tempFileDict.append(word)
            # 统计文档中不同特征的总数目 和 Document Frequency
            for word in tempFileDict:
                dictionary[newsgroup]['#ALL#'] += dictionary[newsgroup][word]
                if word in DF:
                    DF[word] += 1
                else:
                    DF[word] = 1
            tempFileDict.clear()

with open('./dictionary.txt', 'w', encoding='utf-8') as curFile:
    for category in dictionary:
        for word in dictionary[category]:
            curFile.write(category + ' ' + word + ' ' + str(dictionary[category][word]) + '\n')

with open('./CF.txt', 'w', encoding='utf-8') as curFile:
    for eachItem in sorted(CF.items(), key=lambda item: item[1]):
        curFile.write(eachItem[0] + ' ' + str(eachItem[1]) + '\n')

with open('./DF.txt', 'w', encoding='utf-8') as curFile:
    for eachItem in sorted(DF.items(), key=lambda item: item[1]):
        curFile.write(eachItem[0] + ' ' + str(eachItem[1]) + '\n')
