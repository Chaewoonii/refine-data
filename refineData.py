import pandas as pd
import numpy as np
import os
import re

class RefineData:
    def __init__(self):
        self.dong = {'용계동': '진잠동',
                     '대정동': '진잠동',
                     '성북동': '진잠동',
                     '교촌동': '진잠동',
                     '원내동': '진잠동',
                     '세동': '진잠동',
                     '송정동': '진잠동',
                     '방동': '진잠동',
                     '학하동': '학하동',
                     '계산동': '학하동',
                     '덕명동': '학하동',
                     '원신흥동': '원신흥동',
                     '상대동': '상대동',
                     '구암동': '온천1동',
                     '구성동': '온천1동',
                     '어은동': '온천2동',
                     '궁동': '온천2동',
                     '장대동': '온천2동',
                     '갑동': '노은1동',
                     '노은동': '노은1동',
                     '외삼동': '노은2동',
                     '안산동': '노은2동',
                     '수남동': '노은2동',
                     '하기동': '노은2동',
                     '덕진동': '신성동',
                     '추목동': '신성동',
                     '방현동': '신성동',
                     '화암동': '신성동',
                     '신봉동': '신성동',
                     '자운동': '신성동',
                     '장동': '신성동',
                     '도룡동': '신성동',
                     '가정동': '신성동',
                     '신성동': '신성동',
                     '전민동': '전민동',
                     '문지동': '전민동',
                     '원촌동': '전민동',
                     '금탄동': '구즉동',
                     '대동': '구즉동',
                     '신동': '구즉동',
                     '금고동': '구즉동',
                     '둔곡동': '구즉동',
                     '봉산동': '구즉동',
                     '구룡동': '구즉동',
                     '송강동': '구즉동',
                     '관평동': '관평동',
                     '용산동': '관평동',
                     '탑립동': '관평동'
                     }

    def printLi(self, li):
        for idx, c in enumerate(li):
            print(f'{idx+1}. {c}')

    def checkCol(self, df):
        col = df.columns.to_list()
        col.sort(reverse=True)

        print('속성을 선택해주세요.\n')
        self.printLi(col)
        choice = int(input('')) - 1

        if choice == -1:
            print('trace back: checkCol')
            return 0, 0

        return col, choice

    def checkKeys(self, li):
        print('기준 속성 선택(숫자 입력)\n(예: 1,2,3)')
        self.printLi(li)
        check = input('')

        check = check.split(',')
        keys = []
        for k in check:
            idx = int(k)-1
            keys.append(li[idx])

        return keys

    def setColName(self, df, target, colName):
        df = df.rename(columns={target:colName})
        return df

    def getAddLi(self, li):
        li = self.delSpecial(li)
        for idx, add in enumerate(li):
            add = str(add).strip()
            if add != 'nan':

                if add.startswith('대전광역시 유성구'):
                    pass

                elif add.startswith('대전 유성 '):
                    add = add.replace('대전 유성', '대전광역시 유성구 ')

                elif add.startswith('대전 '):
                    add = add.replace('대전 ', '대전광역시 ')

                elif '대전시' in add:
                    add = add.replace('대전시', '대전광역시')

                elif '대전유성' in add:
                    add = add.replace('대전유성', '대전광역시 유성구 ')

                elif '대전 유성' in add:
                    add = add.replace('대전 유성', '대전광역시 유성구')

                elif add.startswith('유성구'):
                    add = '대전광역시 ' + add

                elif add.startswith('대전광역시 유성대로'):
                    add = add.replace('유성대로', '유성구 유성대로')

                else:
                    add = '대전광역시 유성구 '+add

                add = add.strip()
                if '번지' in add: add = add.replace('번지', '')
                if '동' in add and '로' in add: add = re.sub('\S{1,3}동[^로]', '', add)
                if add.endswith('대전광역시 유성구'): add = add.replace('대전광역시 유성구','')
                if add.endswith('일원'): add = add.replace('일원', '')
                if '  ' in add: add = re.sub('  ', ' ', add)

                add = add.strip()
                li[idx] = add

        return li

    # 괄호 삭제, ㅇㅇ동 삭제, 상세주소 남기기
    def setAddress_detail(self, li):
        detail = []
        li = self.getAddLi(li)
        for idx, add in enumerate(li):
            add = str(add)
            if add == 'nan' or add == 'NaN' or add == 'None':
                detail.append('')
            else:
                if '로' in add and '길' in add:
                    i = re.search('\w*번?길\D*\d+-?\d*', add)

                else:
                    try:
                        i = re.search('\w*[동,리,로,길,산]\D*\d+-?\d*', add)
                    except:
                        i = re.search('\w*[구]\D*\d+-?\d*', add)

                if i != None:
                    i = i.end()
                else:
                    try:
                        i = re.search(',', add).start()
                    except:
                        i = len(add)

                add_detail = add[i:].replace('(', ' ').replace(')', ' ')
                add_detail = re.sub('\s\D{1,3}동', '', add_detail)

                add_detail = add_detail.strip()

                if ',,' in add_detail: add_detail = add_detail.replace(',,', '')
                if add_detail.startswith('.') or add_detail.startswith(','): add_detail = re.sub('^[,|.]', '',
                                                                                                     add_detail)
                if add_detail.endswith('.') or add_detail.endswith(','): add_detail = re.sub('[,|.]$', '',
                                                                                                 add_detail)

                add_detail = add_detail.strip()
                detail.append(add_detail)

                li[idx] = add[:i]

        return li, detail

    def setZipCode(self, li):
        zc_li = []
        for idx, add in enumerate(li):
            if add != 'nan':
                print(add)
                add = str(add).strip()
                zc = re.findall('34\d{3}', add)
                if zc != []:
                    zc = zc[0]
                    add = add.replace(zc, '')
                    if '()' in add: add = add.replace('()', '')
                    add = add.strip()
                    zc_li.append(zc)
                    li[idx] = add
                    print(f'{zc}: {add}')

                else:
                    zc_li.append('')
                    print('우편번호 없음')


        print(zc_li)
        return zc_li, li


    # 특수문자 제거
    def delSpecial(self,li):
        for idx, add in enumerate(li):
            if add != 'nan':
                add = str(add).strip()
                add = re.sub('["\'+=!#%&<>;:?<>`]','',add)

                if '㈜' in add: add = add.replace('㈜', '(주)')
                if '(주)' not in add and '주)' in add: add = add.replace('주)', '(주)')
                if '?' in add: add = add.replace('?','')

                if '\n' in add: add = add.replace('\n', ', ')
                if '/' in add: add = add.replace('/',',')

                if '＠ ' in add: add = add.replace('＠', '아파트')
                elif '＠' in add: add = add.replace('＠', '아파트 ')

                if '@ ' in add: add = add.replace('@', '아파트')
                elif '@' in add: add = add.replace('@', '아파트 ')

                if '.' in add:
                    if '. ' in add:
                        add = add.replace('.', ',')
                    else:
                        add = add.replace('.', ', ')

                add = add.strip()
                if add.startswith('.') or add.startswith(','): add = re.sub('^[,|.]','',add)
                if add.endswith('.') or add.endswith(','): add = re.sub('[,|.]$','',add)
                add = add.strip()
                li[idx] = add

        return li

    #괄호 이후로 모두 삭제
    def delAfterBracket(self, li):
        for idx, add in enumerate(li):
            if '(' in add:
                i = add.find('(')
                li[idx] = add[:i].strip()

        return li

    # 괄호삭제
    def delBracket(self,li):
        for idx, item in enumerate(li):
            item = str(item)
            b = re.findall("\([^)]*\)", item)
            print(b)

            if '(주)' in item:
                if len(b) > 0:
                    i = item.find('(주)')
                    item = item.replace('(주)', '')
                    if len(b) > 1:
                        for item in b:
                            item = item.replace(item, '')
                    elif len(b) == 1:
                        item = item.replace(b[0], '')

                    item = f'{item[:i]}(주){item[i:]}'
                else:
                    print('괄호없음')



            else:
                if len(b) > 0:
                    if len(b) > 1:
                        for item in b:
                            item = item.replace(item, '')
                    elif len(b) == 1:
                        item = item.replace(b[0], '')

                else:
                    print('괄호없음')

            item = item.strip()
            li[idx] = item

        return li

    #엔터 삭제
    def delEnter(self, li):
        for idx, add in enumerate(li):
            add = str(add)
            add = add.split('\n')
            add = ', '.join(add)
            add = re.sub('  ', ' ', add)
            add = re.sub(',,', ',', add)
            li[idx] = add

        return li

    #/삭제
    def delSlash(self, li):
        for idx, add in enumerate(li):
            add = str(add)
            if '\n' in add:
                add = add.replace('\n', '')
            add = add.split('/')
            add = ', '.join(add)
            add = re.sub('  ', ' ', add)


            li[idx] = add

        return li

    # 날짜 정제
    def getDateLi(self, li):
        for idx, data in enumerate(li):
            data = str(data)
            data = data.replace(' ', '')
            print(data)
            if '.' in data:
                print('init')
                data = data.split('.')

                if '-' not in data[0]:
                    print('1')
                    year = int(data[0])
                    if 0 <= year <= 22: data[0] = '20' + str(year)
                    elif 22 < year < 100: data[0] = '19' + str(year)
                    else: pass

                    if len(data[1]) == 1:
                        print('2')
                        data[1] = '0' + data[1]

                elif '-' in data[0]:
                    data = '-'.join(data)


                if type(data) == list and len(data) >= 3:
                    if len(data[2]) == 1: data[2] = '0'+data[2]
                    data = '-'.join(data).strip()

                elif type(data) == list and len(data) == 2:
                    print('3')
                    if len(data[1]) == 1: data[1] = '0'+data[1]
                    data = f'{"-".join(data)}-01'

                elif type(data) == list and len(data) == 1:
                    print('4')
                    pass

            elif '-' in data and len(data) != 10:
                data = data.split('-')

                if '-' not in data[0]:
                    year = int(data[0])
                    if 0 <= year <= 22: data[0] = '20' + str(year)
                    elif 22 < year < 100: data[0] = '19' + str(year)

                    if len(data[1]) == 1: data[1] = '0' + data[1]

                elif '-' in data[0]:
                    data = '-'.join(data)

                if type(data) == list and len(data) > 3:
                    if len(data[1]) == 1: data[1] = '0' + data[1]
                    elif len(data[1]) == 0:data[2] = '01'
                    if len(data[2]) == 1: data[2] = '0' + data[2]
                    elif len(data[2]) == 0: data[2] = '01'
                    data = '-'.join(data[:3])

                elif type(data) == list and len(data) == 3:
                    if len(data[1]) == 1: data[1] = '0' + data[1]
                    elif len(data[1]) == 0: data[2] = '01'
                    if len(data[2]) == 1: data[2] = '0' + data[2]
                    elif len(data[2]) == 0: data[2] = '01'
                    data = '-'.join(data)

                elif type(data) == list and len(data) == 2:
                    if len(data[1]) == 1: data[1] = '0' + data[1]
                    elif len(data[1]) == 0: data[1] = '01'
                    data = f'{"-".join(data)}-01'


                elif type(data) == list and len(data) == 1:
                    pass

            elif type(data) == str and len(data) == 5:
                if data.startswith('20') or data.startswith('19'):
                    data = f'{data[:4]}-0{data[4]}-01'
                else:
                    pass

            elif type(data) == str and len(data) == 6:
                print('5')
                data = f'{data[:4]}-{data[4:]}-01'

            elif type(data) == str and len(data) == 8:
                data = f'{data[:4]}-{data[4:6]}-{data[6:]}'

            else:
                print('6')
                pass

            if data.endswith('-'): data = data[:-1]
            li[idx] = data
        return li

    #YEAR, MONTH
    def getYMLi(self, li):
        year = []
        month = []
        for idx, data in enumerate(li):
            data = str(data)
            data = data.split('-')
            if len(data) == 1:
                print('trace back: getYMLi')
                return 0, 0
            year.append(data[0])
            month.append(data[1])

        return year, month

    # 전화번호 정제
    def getPNumLi(self, li):
        print('[RefineData] getPNumli init@@@@')
        for idx, num in enumerate(li):
            num = str(num)
            num = re.sub(' ', '', num)
            if num.startswith('042'):
                if len(num) == 10:
                    num = f'{num[:3]}-{num[3:6]}-{num[6:]}'
                else:
                    pass
            elif num.startswith('00420'):
                print('@@')
                num = f'042-{num[5:8]}-{num[8:]}'

            elif num.startswith('010'):
                if len(num) == 11:
                    num = f'{num[:3]}-{num[3:7]}-{num[7:]}'
                else:
                    pass

            elif len(num) == 7:
                num = f'042-{num[:3]}-{num[3:]}'

            elif len(num) == 8:
                if '-' in num:
                    num = f'042-{num}'
                else:
                    num = f'{num[:4]}-{num[4:]}'
            else:
                pass

            if '--' in num : num = num.replace('--', '-')
            li[idx] = num.strip()
        return li

    #전화번호 정제
    def getPNum(self, num):
        num = str(num)
        num = re.sub(' ', '', num)
        if num.startswith('042'):
            if len(num) == 10:
                num = f'{num[:3]}-{num[3:6]}-{num[6:]}'
            else:
                pass
        elif num.startswith('00420'):
            print('@@')
            num = f'042-{num[5:8]}-{num[8:]}'

        elif num.startswith('010'):
            if len(num) == 11:
                num = f'{num[:3]}-{num[3:7]}-{num[7:]}'
            else:
                pass

        elif len(num) == 7:
            num = f'042-{num[:3]}-{num[3:]}'

        elif len(num) == 8:
            if '-' in num:
                num = f'042-{num}'
            else:
                num = f'{num[:4]}-{num[4:]}'
        else:
            pass

        if '--' in num : num = num.replace('--', '-')
        num = num.strip()
        return num
#004208541234
    # 여러 전화번호
    def getPNumLi_multi(self, li):
        for idx, num in enumerate(li):
            num1 = str(num)
            numLi = re.findall('\d*-?\d{3,4}-\d{4}', num1)
            if numLi != []:
                numLi = self.getPNumLi(numLi)
                num1 = ', '.join(numLi)

            else:
                num1 = self.getPNum(num1)

            if num1 != '':
                li[idx] = num1

        print(li)
        return li

    # 단위 변환
    def changeUnit(self, li, option=0):
        # m->cm변환
        if option == 0:
            for idx, d in enumerate(li):
                d = float(d) * 100
                li[idx] = d

        # cm->m변환
        elif option == 1:
            for idx, d in enumerate(li):
                d = float(d) * 0.01
                li[idx] = d

        else:
            print('[RefineData] changeUnit Fail!!')

        return li

    #비식별화
    def getNameLi(self,li):
        for idx, n in enumerate(li):
            n = str(n).strip()
            if n == 'nan' or n == 'NaN' or n == 'None':
                pass
            else:
                print(n)
                if '외' in n:
                    n = f'{n[0]}○{n[2:]}'
                    li[idx] = n

                elif '(주)' in n or '㈜' in n or '구청' in n or '법인' in n or '목욕탕' in n:
                    pass

                elif len(n) == 2:
                    n = f'{n[0]}○'
                    li[idx] = n

                elif len(n) == 3:
                    n = f'{n[0]}{"○" * (len(n) - 2)}{n[-1]}'
                    li[idx] = n
                elif len(n) > 3:

                    if '.' in n:
                        print(',,,,')
                        n = n.replace(' ', '')
                        nLi = n.split('.')
                        for idx2, n2 in enumerate(nLi):
                            if len(n2) == 1:
                                n2 = f'{n2[0]}{"○" * (len(n2) - 2)}{n2[-1]}'
                            elif len(n2) == 2:
                                n2 = f'{n2[0]}○'
                            else:
                                n2 = f'{n2[0]}{"○" * (len(n2) - 2)}{n2[-1]}'
                            nLi[idx2] = n2
                        n = ', '.join(nLi)
                        li[idx] = n

                    elif ',' in n:
                        nLi = n.split(',')
                        for idx2, n2 in enumerate(nLi):
                            if len(n2) == 1:
                                n2 =f'{"○" * (len(n2) - 2)}'.join([nLi[idx2], nLi[idx2+1][-1]])
                            elif len(n2) == 2:
                                n2 = f'{n2[0]}○'
                            else:
                                n2 = f'{n2[0]}{"○" * (len(n2) - 2)}{n2[-1]}'
                            nLi[idx2] = n2
                        n = ', '.join(nLi)
                        li[idx] = n

                    elif ' ' in n and '.' not in n:
                        nLi = n.split(' ')
                        for idx2, n2 in enumerate(nLi):
                            n2 = n2.strip()
                            if len(n2) == 1:
                                n2 = f'{"○" * (len(n2) - 2)}'.join([nLi[idx2], nLi[idx2 + 1][-1]])
                            elif len(n2) == 2:
                                n2 = f'{n2[0]}○'
                            else:
                                print(n2)
                                n2 = f'{n2[0]}{"○" * (len(n2) - 2)}{n2[-1]}'

                            nLi[idx2] = n2
                        n = ', '.join(nLi)
                        li[idx] = n

                    else:
                        n = f'{n[0]}{"○" * (len(n) - 2)}{n[-1]}'
                        li[idx] = n

            # n = f'{n[0]}{"○" * (len(n) - 2)}{n[-1]}'

        return li

    #데이터 붙이기
    def addCharLi(self, li, char):
        for idx, data in enumerate(li):
            data = str(data)
            if char not in data:
                li[idx] = data+char

        return li

    #데이터 자르기
    def delCharLi(self, li, char):
        for idx, data in enumerate(li):
            data = str(data)
            if char in data:
                li[idx] = data.replace(char, '')
        return li

    #공백 삭제
    def delBlank(self, li):
        for idx, data in enumerate(li):
            data = str(data)
            li[idx] = data.replace(' ', '')
        return li

    #대소문자 변경
    def getUL_li(self, li, flag=True):
        if flag == True:
            for idx, data in enumerate(li):
                li[idx] = data.upper()

        elif flag == False:
            for idx, data in enumerate(li):
                li[idx] = data.lower()

        else:
            print('[RefineData] getUL_li Fail!!')

        return li

    def getCondiDf(self, df, col, condiD, condiS):
        if condiS == '같음':
            df = df[df[col] == condiD]
        elif condiS == '이상':
            df = df[df[col] >= condiD]
        elif condiS == '이하':
            df = df[df[col] <= condiD]
        elif condiS == '초과':
            df = df[df[col] > condiD]
        elif condiS == '미만':
            df = df[df[col] < condiD]

        print(df)
        return df

