from bs4 import BeautifulSoup
import re
programsFile = None

try:
    programsFile = open('programs.html', 'r', encoding='utf-8')
except IOError:
    print('Error with programs file')

def squeeze(char,s):
    while char*2 in s:
        s=s.replace(char*2,char)
    return s

programsText = programsFile.read()
soup = BeautifulSoup(programsText, 'lxml')

finalResult = []
resultStrings = [[],[], [], [], [], [], []]
codesList = []
cards1 = soup.findAll('div', class_='education__card education__color-1')
default_string = 'education__card education__color-'

for i in range(8):
    current_string = 'education__card education__color-' + str(i+1)
    cards1 = soup.findAll('div', class_=current_string)
    branch = []
    for it in cards1:
        res = it.findAllNext('div', class_='row')
        program = []
        for it2 in res:
            tmp = it2.getText()
            tmp = tmp.replace('\n', ' ')
            tmp = tmp.replace(' ', ' ')
            program.append(squeeze(' ', tmp))
        branch.append(program)
    finalResult.append(branch)

for i in range(len(finalResult)):
    for j in range(len(finalResult[i])):
        for k in range(0, len(finalResult[i][j])-3, 5):
            resString = ''
            str0 = finalResult[i][j][k+3]
            resString = resString + str0[len('Факультет')+1:] + ';'
            str1 = finalResult[i][j][k]
            iterator = None
            flag = False
            index = str1.find(' ')
            test = finalResult[i][j][k + 1]

            if test in codesList:
                flag = True
            else:
                codesList.append(test)
                flag = False

            if flag:
                continue

            for z in range(len(str1)-1, 0, -1):
                if str1[z] == ' ':
                    iterator = z
                    break

            resString = resString + str1[:iterator] + ';'

            resString = resString + finalResult[i][j][k + 1] + ';'

            str2 = finalResult[i][j][k+2]
            index = 0
            index = str2.find('Бакалавриат')
            if index > -1:
                resString = resString + str2[:index+len('Бакалавриат')]
                year = str2[index+len('Бакалавриат')]
                if year == '4':
                    resString += ' 4 года;'
                else:
                    resString = resString + ' ' + year + ' лет;'
            else:
                index = str2.find('Специалитет')
                resString = resString + 'Специалитет'
                year = str2[index+len('Специалитет')]
                if year == '5':
                    resString += ' 5 лет;'
                else:
                    resString += ' 6 лет;'
            str3 = finalResult[i][j][k+4]
            resString = resString + 'Параметры поступления: '
            index = str3.find('ЕГЭ: ')
            lastIndex = str3.find('Вступительные')
            resString = resString + str3[len('ЕГЭ: ') + index:lastIndex - 1] + ';'
            resultStrings[i].append(resString)

x = 2

dictOtr = {0: 'Транспорт', 1: 'Строительство', 2: 'Промышленность', 3: 'Логистика', 4: 'Информационные технологии', 5: 'Экономика и менеджмент', 6: 'Психология'}

f = open('spec.txt', 'w', encoding='utf-8')
for i in range(len(resultStrings)):
    for j in range(len(resultStrings[i])):
        f.write(resultStrings[i][j] + '\n')


