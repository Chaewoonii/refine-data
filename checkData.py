import pandas as pd
import numpy as np
import os
from MyUtill import MyUtill
import re
import copy





class CheckData:
    def __init__(self, p):
        self.path = p
        self.dong = {'용계동':'진잠동',
        '대정동':'진잠동',
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
        '도룡동':'신성동',
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

    '''
    데이터 로딩
    시트 내 중복체크
    파일 간 중복체크
    sql 이용
   '''

    def setPath(self,p):
        self.path = p

    def getPath(self):
        return self.path

    # 파일 1개 내 중복체크
    '''def getColNames(self, dataFrame):
        df = pd.DataFrame()
        cols = []

        if dataFrame.endswith('.csv'):
            df = pd.read_csv(f'{self.path}/{dataFrame}', encoding='cp949', engine='python')
        else:
            df = pd.read_csv(f'{self.path}/{dataFrame}.csv', encoding='cp949', engine='python')

        cols = df.columns
    
        return cols'''


    # 모든 컬럼을 적용해서 검사
    def checkDu(self, df):
        s = df.duplicated()
        s = pd.Series(s, name='duplicated')
        df1 = pd.concat([df, s], axis=1)

        print(df1.head())

        condi = df1['duplicated'] == True
        print(df1[condi])

        return df1[condi]


    # 일부 컬럼을 선택하여 검사
    def checkDuCols(self, df, cols):
        s = df.duplicated(subset=cols)
        s = pd.Series(s, name='duplicated')
        df1 = pd.concat([df, s], axis=1)

        print(df1.head())

        condi = df1['duplicated'] == True
        print(df1[condi])

        return df1[condi]

    #해당 디렉토리 내 파일 중복검사
    def checkAllDir(self, li, co):
        if not os.path.isdir(f'{self.path}/checkData'):
            os.mkdir(f'{self.path}/checkData')

        for idx, dir in enumerate(li):
            for f in co[idx]:
                if not f.startswith('check'):
                    print(f'{self.path}/{dir}/{f}')
                    try:
                        df = pd.read_csv(f'{self.path}/{dir}/{f}', encoding='cp949', engine='python')

                    except:
                        df = pd.read_csv(f'{self.path}/{dir}/{f}', encoding='utf-8-sig', engine='python')


                    checkData = self.checkDu(df)
                    checkData = checkData.dropna(how='all', axis=0)

                    if checkData.empty == False:
                        checkData.to_csv(f'{self.path}/checkData/check_{f}', encoding='utf-8-sig', index=False)


    #checkData일괄삭제
    def delAllCheckData(self):
        li = os.listdir(f'{self.path}/checkData')
        for f in li:
            os.remove(f'{self.path}/checkData/{f}')


    #빈 df만 삭제
    def delCheckData(self):
        li = os.listdir(f'{self.path}/checkData')
        for f in li:
            try:
                df = pd.read_csv(f'{self.path}/checkData/{f}', encoding='cp949', engine='python')
            except:
                df = pd.read_csv(f'{self.path}/checkData/{f}', encoding='utf-8-sig', engine='python')

            df = df.dropna(how='all', axis=0)
            if df.empty == True:
                os.remove(f'{self.path}/checkData/{f}')

    #컬럼 프린트
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

    #키 선택
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


    def setColByEx(self, df1, df2):
        col1 = df1.columns.to_list()
        col2 = df2.columns.to_list()
        col1.sort(reverse=True)
        col2.sort(reverse=True)
        print(col1)
        print(col2)


        print('변경할 컬럼 이름 선택\n')
        self.printLi(col1)
        choice = int(input('')) - 1
        n_col = col1[choice]

        print('어떤 이름으로 변경하시겠습니까?\n')
        self.printLi(col2)
        choice2 = int(input('')) - 1
        o_col = col2[choice2]

        df1 = df1.rename(columns={n_col:o_col})

        print(df1.columns)
        print(df2.columns)


        return df1

    def setCols(self, df):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setCols')
            return df

        o_col = col[choice]

        n_col = input(f'변경할 이름을 입력해주세요.\n{o_col}→\t')

        df1 = df.rename(columns={o_col: n_col})

        print(df1.columns)

        return df1

    '''def setCols(self, df1, df2):
        col1 = df1.columns.to_list()
        col2 = df2.columns.to_list()'''




    '''def addCol(self, df1, df2):
        col1 = df1.columns.to_list()
        col2 = df2.columns.to_list()
        col1.sort(reverse=True)
        col2.sort(reverse=True)
        print(col1)
        print(col2)

        print('추가할 속성을 선택해주세요.\n')
        self.printLi(col1)
        choice = int(input('')) - 1
        colName = col1[choice]

        df2[f'{colName}'] = None

        print(df2.head())
        return df2'''

    def addCol(self, df1):
        col1 = df1.columns.to_list()
        col1.sort(reverse=True)
        print(col1)

        colName = input('추가할 속성명을 입력해주세요.\n')

        df1[f'{colName}'] = None

        print(df1.head())
        return df1

    def addColData(self, df1, colName, data):
        col1 = df1.columns.to_list()
        col1.sort(reverse=True)
        print(col1)

        df1[f'{colName}'] = data

        print(df1.head())
        return df1

    def dropCol(self,df):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: dropCol')
            return df

        o_col = col[choice]
        df = df.drop(o_col, axis=1)
        return df

    def mergeDf(self, df1, df2):
        col1 = df1.columns.to_list()
        col2 = df2.columns.to_list()
        print(col1)
        print(col2)

        # key = self.checkKeys(col2)
        key = []
        for c1 in col1:
            if c1 in col2:
                key.append(c1)
        key = self.checkKeys(key)

        mergeDf = pd.merge(df1,df2, on=key, how='outer')
        mergeDf = mergeDf.drop_duplicates(key, keep='first')

        col3 = mergeDf.columns.to_list()
        print(col3)
        for c in col3:
            if c.endswith('_y'):
                mergeDf[c] = np.where(pd.notna(mergeDf[c])==False, mergeDf[c.replace('_y','_x')], mergeDf[c])

            if c.endswith('_x'):
                mergeDf[c] = np.where(pd.notna(mergeDf[c])==False, mergeDf[c.replace('_x','_y')], mergeDf[c])

        print('*'*30)
        print(mergeDf.head())


        return key, mergeDf

    def mergeDf_2(self, df1, df2, key):

        print(df1.info(verbose=True))
        print(df2.info(verbose=True))

        key2 = key.copy()
        key2.append('YEAR')

        mergeDf = pd.merge(df1,df2, on=key2, how='outer')
        mergeDf = mergeDf.drop_duplicates(key2, keep='first')

        col3 = mergeDf.columns.to_list()
        print(col3)
        for c in col3:
            if c.endswith('_y'):
                mergeDf[c] = np.where(pd.notna(mergeDf[c]) == False, mergeDf[c.replace('_y', '_x')], mergeDf[c])

        print('*'*30)
        print(mergeDf.head())


        return key2, mergeDf

    '''def fillNa(self, df):
        cols = df.columns.to_list()
        for c in cols:
            if c.endswith('_y'):
                for idx, d in enumerate(df[c]):
                    if d.isna() == True:
                        df.iloc[idx,c] = df.iloc[idx,f'c[:-2]_x']

        return df'''

    def saveDf_mkdir(self,df,path,folderName,fileName):
        if os.path.isdir(f'{path}/{folderName}') == False:
            os.mkdir(f'{path}/{folderName}')

        df.to_csv(f'{path}/{folderName}/{fileName}', encoding='utf-8-sig', index=False)
        os.startfile(f'{path}/{folderName}')

    def saveDf(self,df,path,fileName):
        if fileName.startswith('change'):
            df.to_csv(f'{path}/{fileName}', encoding='utf-8-sig', index=False)
        else:
            df.to_csv(f'{path}/change_{fileName}', encoding='utf-8-sig', index=False)
        os.startfile(f'{path}')

    # 주소 정제
    def setAddress(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setAddress')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.getAddLi(addLi)
        print(addLi)
        if flag == True: df['Address'] = addLi
        else: df[o_col] = addLi

        return df

    #주소정제_리스트 반환
    def getAddLi(self, data):
        data = self.delSpecial(data)
        for idx, add in enumerate(data):
            add = str(add).strip()
            if add != 'nan':

                if add.startswith('대전광역시 유성구'):
                    pass

                elif add.startswith('대전 유성 '):
                    add = add.replace('대전 유성', '대전광역시 유성구 ')

                elif add.startswith('대전 '):
                    add = add.replace('대전 ', '대전광역시 ')

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
                data[idx] = add

        return data

    def setSpecial(self,df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setSpecial')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.delSpecial(addLi)
        print(addLi)
        if flag == True:
            df['Refinement'] = addLi
        else:
            df[o_col] = addLi

        return df

    #특수문자
    def delSpecial(self,li):
        for idx, add in enumerate(li):
            if add != 'nan':
                add = str(add).strip()
                add = re.sub('["\'+=!#%&<>;:]','',add)
                r_li = re.findall('[\D]\d+', add)

                if add.startswith('34'):
                    add = add[5:]

                for a in r_li:
                    if ' ' not in a and '-' not in a:
                        add = add.replace(f'{a}', f'{a[0]} {a[1:]}')


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


    '''def delAfterBracket(self, li):
        for idx, add in enumerate(li):
            add = re.sub('\(.*\)','',add)
            li[idx] = add
    
        return li'''

    #괄호삭제
    def delBracket(self,li):

        for idx, add in enumerate(li):
            add = str(add)

            if '(주)' in add:
                i = add.find('(주)')
                add = add.replace('(주)', '')
                add = re.sub("\(.*\)|\s-\s.*", '', add)
                add = f'{add[:i]}(주){add[i:]}'

            else:
                add = re.sub("\(.*\)|\s-\s.*", '', add)

            li[idx] = add

        return li

    def setBracket(self,df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setBracket')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.delBracket(addLi)
        print(addLi)
        if flag == True:
            df[f'delBr_{o_col}'] = addLi
        else:
            df[o_col] = addLi

        return df

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

    def setEnter(self,df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setEnter')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.delEnter(addLi)
        print(addLi)
        if flag == True:
            df[f'delEn_{o_col}'] = addLi
        else:
            df[o_col] = addLi

        return df

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

    def setSlash(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setSlash')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.delSlash(addLi)
        print(addLi)
        if flag == True:
            df[f'delSl_{o_col}'] = addLi
        else:
            df[o_col] = addLi

        return df

    #괄호 삭제, ㅇㅇ동 삭제, 상세주소 남기기
    def delBracket_add(self,li):
        detail = []
        for idx, add in enumerate(li):
            add = str(add)
            if add == 'nan' or add == 'NaN' or add == 'None':
                detail.append('nan')
            else:
                if '로' in add and '길' in add:
                    i = re.search('\w*번?길\s*\w*\d+-?\d*', add)

                else:
                    try:
                        i = re.search('\w*[동,리,로,길,산]\s*\w*\d+-?\d*', add)
                    except:
                        i = re.search('\w*[구]\w*\d*-?\d*', add)

                if i != None:
                    i = i.end()
                else:
                    try:
                        i = re.search(',', add).start()
                    except:
                        i = len(add)

                add_detail = add[i:].replace('(', ' ').replace(')', ' ')
                add_detail = re.sub('\s\D{1,3}동','', add_detail)

                add_detail = add_detail.strip()

                if ',,' in add_detail: add_detail = add_detail.replace(',,', '')
                if add_detail.startswith('.') or add_detail.startswith(','): add_detail = re.sub('^[,|.]','',add_detail)
                if add_detail.endswith('.') or add_detail.endswith(','): add_detail = re.sub('[,|.]$','',add_detail)

                add_detail = add_detail.strip()
                detail.append(add_detail)

                li[idx] = add[:i]

        return li, detail

    def setAddr_detail(self,df,flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setAddr_detail')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.getAddLi(addLi)
        addLi = self.delSpecial(addLi)
        addLi, detail = self.delBracket_add(addLi)

        print(addLi)
        if flag == True:
            df['Address'] = addLi
            if '상세주소' in col: df['Address_detail'] = detail
            else: df['상세주소'] = detail
        else:
            df[o_col] = addLi
            df['상세주소'] = detail

        return df

    def setAdd_B(self,df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setAdd_B')
            return df

        o_col = col[choice]

        addLi = df[o_col].to_list()
        addLi = self.getAddLi(addLi)
        addLi = self.delAfterBracket(addLi)
        print(addLi)

        if flag == True: df['Address'] = addLi
        else: df[o_col] = addLi

        return df

    #merge 후 데이터 선택
    def newData(self, df):
        cols = df.columns.to_list()
        nCol = []
        for idx, c in enumerate(cols):
            if (c.startswith('기준년도') or c.startswith('YEAR') or  c.startswith('year')
                    or c.startswith('데이터기준일자') or c.startswith('month') or c.startswith('MONTH'))\
                    and (c.endswith('_y')):
                nCol.append(c)
            elif c.endswith('_y'):
                nCol.append(c)
            elif c.endswith('_y') == False and c.endswith('_x') == False:
                nCol.append(c)

        print(nCol)
        # nCol.sort(reverse=True)
        nDf = df[nCol]
        return nDf

    #key컬럼 표시.
    def saveKey(self, path, key, year, department, fileName):
        import csv
        f = open(f'{path}/merge_keys.csv', 'a')
        wr = csv.writer(f)
        key = ', '.join(key)
        key = [year, department, fileName, key]
        wr.writerow(key)

        f.close()



    #날짜정제_리스트 반환
    '''def getDateLi(self, li):
        for idx, data in enumerate(li):
            data = str(data)
            data = data.replace(' ','')
            
            if '.' in data: 
                data = data.split('.')
                year = int(data[0])
                
                if 0 <= year <= 22: data[0] = '20' + str(year)
                elif 22 < year < 100: data[0] = '19' + str(year)

                if len(data[1]) == 1: data[1] = f'0{data[1]}'

                if len(data[2]) == 1: data[2] = f'0{data[2]}'

            elif '-' in data and len(data) != 10:
                data = data.split('-')
            

            
            data = f'{data[0]}-{data[1]}-{data[2]}'

            if len(data) == 4 and '-' not in data:
                pass

            elif len(data) == 6 and '-' not in data:
                data = f'{data[:4]}-{data[4:]}-01'

            elif len(data) > 6 and '-' not in data:
                data = f'{data[:4]}-{data[4:6]}-{data[6:]}'
            li[idx] =data
        return li'''

    def getDateLi(self, li):
        for idx, data in enumerate(li):
            if type(data) == float and pd.isna(data) == False:
                data = int(data)
            data = str(data)
            data = data.replace(' ', '')

            if '.' in data:
                data = data.split('.')

                if '-' not in data[0]:
                    year = int(data[0])
                    if 0 <= year <= 22: data[0] = '20' + str(year)
                    elif 22 < year < 100: data[0] = '19' + str(year)

                    if len(data[1]) == 1: data[1] = '0' + data[1]

                elif '-' in data[0]:
                    data = '-'.join(data)


                if type(data) == list and len(data) >= 3:
                    if len(data[2]) == 1: data[2] = '0'+data[2]
                    data = '-'.join(data).strip()

                elif type(data) == list and len(data) == 2:
                    data = f'{"-".join(data)}-01'

                elif type(data) == list and len(data) == 1:
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
                    if len(data[2]) == 1: data[2] = '0' + data[2]
                    elif len(data[2]) == 0: data[2] = '01'
                    data = '-'.join(data[:3])

                elif type(data) == list and len(data) == 3:
                    if len(data[2]) == 1: data[2] = '0' + data[2]
                    elif len(data[2]) == 0: data[2] = '01'
                    data = '-'.join(data)

                elif type(data) == list and len(data) == 2:
                    data = f'{"-".join(data)}-01'


                elif type(data) == list and len(data) == 1:
                    pass

            elif type(data) == str and len(data) == 5:
                data = f'{data[:4]}-0{data[4]}-01'

            elif type(data) == str and len(data) == 6:
                data = f'{data[:4]}-{data[4:]}-01'

            elif type(data) == str and len(data) == 8:
                data = f'{data[:4]}-{data[4:6]}-{data[6:]}'

            if data.endswith('-'): data = data[:-1]
            li[idx] = data
        return li

    def setDate(self, df):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setDate')
            return df

        o_col = col[choice]

        li = df[o_col].to_list()
        li = self.getDateLi(li)

        df[o_col] = li

        return df


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

    def setYM(self, df):
        col, choice = self.checkCol(df)

        if choice == -1:
            print('trace back: setYM')
            return df

        o_col = col[choice]

        li = df[o_col].to_list()
        li = self.getDateLi(li)
        year, month = self.getYMLi(li)
        if year == 0 and month == 0:
            print('trace back: setYM')
            return df



        df[o_col] = li
        df['YEAR'] = year
        df['MONTH'] = month

        return df


    #전화번호 정제
    def getPnumLi(self,li):
        for idx, num in enumerate(li):
            num = str(num)
            num = num.replace(' ','')
            if num.startswith('0') == False:
                if len(num) == 8:
                    num = '042-'+num

            if '--' in num: num = num.replace('--','-')
            if num.startswith('-'):
                num = num.replace('-','')
            li[idx] = num
        return li

    def getPNumLi(self, li):
        for idx, num in enumerate(li):
            num = str(num)
            num = num.replace(' ','')
            if num.startswith('042'):
                if '-' in num:
                    if '--' in num:
                        num = num.replace('--','-')
                elif len(num) == 10:
                    num = f'{num[:3]}-{num[3:6]}-{num[6:]}'
                else:
                    pass

            elif num.startswith('010'):
                if '-' in num:
                    if '--' in num:
                        num = num.replace('--', '-')
                elif len(num) == 11:
                    num = f'{num[:3]}-{num[3:7]}-{num[7:]}'
                else:
                    pass

            elif len(num) == 7:
                num = f'042-{num[:3]}-{num[3:]}'

            elif len(num) == 8:
                if '-' in num:
                    num = f'042-{num}'
                    if '--' in num:
                        num = num.replace('--', '-')
                else:
                    num = f'{num[:4]}-{num[4:]}'

            else:
                pass

            li[idx] = num.strip()
            return li


    #여러 전화번호
    def getPNumLi_multi(self, li):
        for idx, num in enumerate(li):
            num = str(num)
            numLi = re.findall('\d*-?\d{3,4}-\d{4}', num)
            numLi = self.getPnumLi(numLi)
            num = ', '.join(numLi)
            li[idx] = num
        print(li)
        return li


    def setPnum(self,df):
        col1 = df.columns.to_list()
        col1.sort(reverse=True)

        print('전화번호에 해당하는 속성을 선택해주세요.\n')
        self.printLi(col1)
        choice = int(input('')) - 1
        o_col = col1[choice]

        li = df[o_col].to_list()
        li = self.getPNumLi_multi(li)

        df[o_col] = li

        return df


    #m->cm 변환
    def mToCm(self,li,flag=True):

        #cm->m변환
        if flag==False:
            for idx, d in enumerate(li):
                d = int(float(d) * 0.01)
                li[idx] = d

        else:
            for idx, d in enumerate(li):
                d = int(float(d) * 100)
                li[idx] = d

        return li

    def setUnit(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setUnit')
            return df

        o_col = col[choice]

        li = df[o_col].to_list()
        if flag == True: li = self.mToCm(li)
        else: li = self.mToCm(li,False)

        df[o_col] = li

        return df

    #비식별화
    def setName(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setName')
            return df

        o_col = col[choice]

        li = df[o_col].to_list()
        li = self.getNameLi(li)
        if flag == True:
            df[o_col] = li
        else:
            df['Name'] = li
        return df

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

#     데이터 붙이기
    def addData(self, df, str):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: addData')
            return df

        o_col = col[choice]

        li = df[o_col].to_list()
        li = self.getDataLi(li, str)
        print(li)
        df[o_col] = li

        return df


    def getDataLi(self, li, str):
        for idx, data in enumerate(li):
            if str not in data:
                li[idx] = data+str

        return li

    # 데이터 출력
    def printData(self,df):
        col, choice = self.checkCol(df)
        if choice == -1:
            print('back')
            return df

        o_col = col[choice]
        print(df[o_col].head())

    # 공백 삭제
    def setBlank(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setBlank')
            return df

        o_col = col[choice]
        dataLi = df[o_col].to_list()
        dataLi = self.delBlank(dataLi)
        if flag == True:
            df[f'del_{o_col}'] = dataLi
        else:
            df[o_col] = dataLi

        return df

    def delBlank(self, li):
        for idx, data in enumerate(li):
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
            print('trace back: getUL_li')
            return li
        return li

    def setUpperLower(self, df, flag_col=True, flag_UL=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setLower')
            return df

        o_col = col[choice]
        dataLi = df[o_col].to_list()
        dataLi = self.getUL_li(dataLi, flag_UL)
        if flag_col == True:
            df[f'lower_{o_col}'] = dataLi
        else:
            df[o_col] = dataLi

        return df

    #법정동->행정동 변경
    def changeDong(self, li):
        temp = []
        for idx, dong in enumerate(li):
            try:
                temp.append(self.dong[dong])
            except:
                temp.append('')
        return temp

    def setDong(self, df, flag=True):
        col, choice = self.checkCol(df)

        if col == 0 and choice == 0:
            print('trace back: setBlank')
            return df

        o_col = col[choice]
        dataLi = df[o_col].to_list()
        dataLi = self.changeDong(dataLi)
        print(dataLi)
        if flag == True:
            df[f'{o_col}_행정동'] = dataLi
        else:
            df[o_col] = dataLi

        return df

if __name__ == '__main__':
    path = 'C:/Users/USER/Desktop/까마귀/'
    df = pd.read_csv(path+'merge2_청소행정과_불법투기과태료부과현황.csv', encoding='cp949', engine='python')
    cd = CheckData(path)
    h_dong = cd.changeDong(df['법정동'])
    df['행정동_2'] = h_dong
    df.to_csv(path+'temp.csv', encoding='utf-8-sig', index=False)
