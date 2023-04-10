import pandas as pd
import numpy as np

class MergeData:
    def __init__(self):
        print('[MergeData] __init__')

    #연도 상관 없이 중복 삭제
    def mergeDf(self, df1, df2, key):
        df1 = self.floatToObj(df1)
        df2 = self.floatToObj(df2)
        mergeDf = pd.merge(df1, df2, on=key, how='outer')

        #전체 중복 삭제. 년도가 달라도 삭제됨
        mergeDf = mergeDf.drop_duplicates(key, keep='first')
        mergeDf = self.fillNA(mergeDf)
        newDf = self.newData(mergeDf)
        newDf = self.delXY(newDf)
        return newDf

    #df:null:: float64
    def floatToObj(self, df):
        print(df.dtypes)
        for col in df.columns.to_list():
            if df[col].dtype == 'float64':
                print('*')
                df[col] = df[col].astype('object')
        print(df.dtypes)
        return df

    '''    #연도로 Stack-up
    def stackUpDf(self, df1, df2, key):
        mergeDf = pd.merge(df1, df2, on=key.append('YEAR'), how='outer')

        #같은 년도 내 중복 삭제. 불필요할 시 삭제해도 됨.
        # mergeDf = mergeDf.drop_duplicates(key2, keep='first')
        mergeDf = self.fillNA(mergeDf)
        newDf = self.newData(mergeDf)
        return newDf'''

    def fillNA(self, df):
        cols = df.columns.to_list()
        # np.where(a,b,c): a의 조건을 만족하면 b, 아니면 c로 설정.
        for c in cols:
            if c.endswith('_y'):
                df[c] = np.where(pd.isna(df[c]), df[c.replace('_y', '_x')], df[c])

            elif c.endswith('_x'):
                df[c] = np.where(pd.isna(df[c]), df[c.replace('_y', '_x')], df[c])

        return df

    def delXY(self, df):
        cols = df.columns.to_list()
        for c in cols:
            if c.endswith('_x') or c.endswith('_y'):
                print(c, c[:-2])
                df = df.rename(columns = {c:c[:-2]})
        print(df.columns)
        return df

    def newData(self, df):
        cols = df.columns.to_list()
        nCol = []
        for idx, c in enumerate(cols):
            if c.endswith('_y') == False and c.endswith('_x') == False:
                nCol.append(c)

            elif c.endswith('_y'):
                nCol.append(c)

        nDf = df[nCol]
        return nDf










