import os

import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pandasModel import PandasModel
from PyQt5 import uic
from MyUtill import MyUtill
from refineData import RefineData
from mergeData import MergeData
from ExceptionHook import ExceptionHook
import sys

ex = ExceptionHook()
mu = MyUtill()
rd = RefineData()
md = MergeData()
formClass = uic.loadUiType("./resources/dataMerge.ui")[0]
class MergeDataGUI(QDialog, QWidget, formClass):
    def __init__(self, parent=None):
        print('[DataMergeMain] __init__****')
        super(MergeDataGUI, self).__init__(parent)

        self.df1 = pd.DataFrame()
        self.df2 = pd.DataFrame()
        self.model1 = None
        self.model2 = None
        self.setupUi(self)
        self.initUI()

    def setDf1(self,df):
        print('[DataMergeMain] setDf1****')
        self.df1 = df

    def getDf1(self):
        print('[DataMergeMain] getDf1****')
        return self.df1

    def setDf2(self,df):
        print('[DataMergeMain] setDf2****')
        self.df2 = df

    def getDf2(self):
        print('[DataMergeMain] getDf2****')
        return self.df2

    def setModel1(self, df):
        print('[DataMergeMain] setModel1****')
        self.model1 = PandasModel(df)

    def getModel1(self):
        print('[DataMergeMain] getModel1****')
        return self.model1

    def setModel2(self, df):
        print('[DataMergeMain] setModel2****')
        self.model2 = PandasModel(df)

    def getModel2(self):
        print('[DataMergeMain] getModel2****')
        return self.model1

    def initUI(self):
        print('[DataMergeMain] initUI*****')
        try:
            self.openFile_table1.clicked.connect(self.setView1)
            self.openFile_table2.clicked.connect(self.setView2)
            self.mergeBtn.clicked.connect(self.openPreviewData)
            self.cancelBtn.clicked.connect(self.mergeDataCancel)
            self.setWindowTitle('Merge Data::::데이터 병합')
            self.setWindowIcon(QIcon('./resources/table2.png'))

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

    def setView1(self):
        print('[DataMergeMain] setView1*****')
        try:
            df, path, fileName = self.openfile()
            if df.empty:
                 print('empty DataFrame!!')
            else:
                self.setDf1(df)
                self.setModel1(df)
                self.setTableView(df, self.tableView1, self.model1)
                self.label_table1.setText(fileName[:-4])

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

    def setView2(self):
        print('[DataMergeMain] setView2*****')
        try:
            df, path, fileName = self.openfile()

            if df.empty:
                print('empty DataFrame!!')

            else:
                self.setDf2(df)
                self.setModel2(df)
                self.setTableView(df, self.tableView2, self.model2)
                self.label_table2.setText(fileName[:-4])
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

    def openfile(self):
        print('[DataMergeMain] openfile*****')
        p = ''
        file_tuple = QFileDialog.getOpenFileName(self, 'Open File_table1', './')
        try:
            if file_tuple != ('', ''):
                p = file_tuple[0]

            else:
                p = ''

            if p != '':
                path, fileName = mu.getPath_FileName(p)

                try:
                    df = pd.read_csv(p, encoding='cp949', engine='python')

                except:
                    df = pd.read_csv(p, encoding='utf-8-sig', engine='python')

                return df, path, fileName

            else:
                print('[DataMergeMain] openfile::::DataFrameLoad Fail!!')
                return pd.DataFrame(), None, None

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

    def setTableView(self, df, tableView, model):
        print('[DataMergeMain] setTableView*****')
        if df.empty:
            print('[DataMergeMain] setTableView: Empty DataFrame')

        else:
            print('[DataMergeMain] setTableView: DataFrame init::::tableView Loading')
            tableView.horizontalHeader().setStretchLastSection(True)
            tableView.setAlternatingRowColors(True)
            tableView.setSelectionBehavior(QTableView.SelectRows)
            tableView.setModel(model)
            tableView.show()

    def getFileName(self):
        print('[DataMergeMain] getFileName****')
        name = self.label_table1.text()
        print(name)
        name = name.replace('change_', '')
        return name

    def getSameCols(self):
        print('[DataMergeMain] getSameCols****')
        cols = []
        for i in self.df1.columns.to_list():
            for j in self.df2.columns.to_list():
                if i == j:
                    cols.append(i)
                    print(i)
                    print(j)
        print(cols)
        return cols

    def openSelectKeys(self):
        print('[DataMergeMain] openSelectKeys****')
        cols = self.getSameCols()
        sk = SelectKeys(cols, self)
        sk.exec_()
        print(sk.checked)
        return sk.checked

    def openPreviewData(self):
        print('[DataMergeMain] openPreviewData****')
        keys = self.openSelectKeys()
        if keys != []:
            mergeDf = md.mergeDf(self.df1, self.df2, keys)
            pv = PreviewData(df=mergeDf, fileName=self.getFileName(), parent=self)
            pv.exec_()

        else:
            print('No selected columns')
            # ex.show_exception_box('Exception Occured::\n\tNo selected columns')

    def mergeDataCancel(self):
        print('[DataMergeMain] mergeDataCancel****')
        self.close()


prevDataUI = uic.loadUiType('./resources/prevData.ui')[0]
class PreviewData(QDialog, QWidget, prevDataUI):
    def __init__(self, df=pd.DataFrame, fileName='temp', parent=None):
        print('[PreviewData] __init__')
        super(PreviewData, self).__init__(parent)
        self.df = df
        self.fileName=fileName
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        print('[PreviewData] initUI')
        self.label.setText(self.fileName)
        self.setTableView(self.df)
        self.saveBtn.clicked.connect(self.previewDataSave)
        self.cancelBtn.clicked.connect(self.previewDataCancel)

        self.setWindowTitle('Preivew::::미리보기')
        self.setWindowIcon(QIcon('./resources/table2.png'))

    def setTableView(self, df):
        print('[PreviewData] setTableView')
        if df.empty:
            print('df.empty')

        else:
            model = PandasModel(df)
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.setAlternatingRowColors(True)
            self.tableView.setSelectionBehavior(QTableView.SelectRows)
            self.tableView.setModel(model)
            self.tableView.show()

    def previewDataSave(self):
        print('[PreviewData] previewDataSave')
        print(self.fileName)
        path, fileType = QFileDialog.getSaveFileName(parent=self, caption='Save File',
                                                     directory=f'./{self.fileName}.csv',
                                                     filter='CSV (*.csv);;Excel (*.xlsx)')
        print(path)
        if fileType == 'CSV (*.csv)':
            self.saveToCsv(path)

        elif fileType == 'Excel (*.xlsx)':
            self.saveToExcel(path)

        else:
            print('file type not found')
            ex.show_exception_box('file type not found')

    def saveToCsv(self, path):
        print('[PreviewData] saveToCsv')
        self.df.to_csv(path, encoding='cp949', index=False)
        os.startfile(path)

    def saveToExcel(self, path):
        print('[PreviewData] saveToExcel')
        self.df.to_excel(path, columns=self.df.columns.to_list(), index=False)
        os.startfile(path)

    def previewDataCancel(self):
        print('[PreviewData] previewDataCancel')
        self.close()


class SelectKeys(QDialog, QWidget):
    def __init__(self, cols, parent=None):
        print('[SelectKeys] __init__')
        super(SelectKeys, self).__init__(parent)
        self.cols = cols
        self.checkBoxes = []
        self.checked = []
        self.initUI()
        self.show()

    def setChecked(self, li):
        print('[SelectKeys] setChecked')
        self.checked = li

    def initUI(self):
        print('[SelectKeys] initUI')
        try:
            self.vbox = QVBoxLayout()
            self.vbox.addWidget(QLabel('key 속성을 선택해 주세요.'))
            self.addCheckBox(self.vbox)

            self.okBtn = QPushButton('확인')
            self.okBtn.clicked.connect(self.selectKeysOK)
            self.cancelBtn = QPushButton('취소')
            self.cancelBtn.clicked.connect(self.selectKeysCancel)

            hbox = QHBoxLayout()
            hbox.addWidget(self.okBtn)
            hbox.addWidget(self.cancelBtn)
            self.vbox.addLayout(hbox)

            self.setLayout(self.vbox)

            self.setWindowTitle('Select Key')
            self.setWindowIcon(QIcon('./resources/clipboard.png'))
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)


    def addCheckBox(self, layout):
        print('[SelectKeys] addCheckBox')
        try:
            gridL = QGridLayout()
            for idx, item in enumerate(self.cols):
                checkBox = QCheckBox(item, self)
                gridL.addWidget(checkBox, idx//2, idx%2)
                self.checkBoxes.append(checkBox)

            layout.addLayout(gridL)

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

        return layout

    def getCheckedBoxList(self):
        print('[SelectKeys] getCheckedBoxList')
        li = []
        try:
            if self.checkBoxes != []:
                for item in self.checkBoxes:
                    if item.isChecked():
                        li.append(item.text())

            else:
                ex.show_exception_box('Exception Occured::: checkBox == None\nAdd column name List to create CheckBoxes')

        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

        return li

    def selectKeysOK(self):
        print('[SelectKeys] selectKeysOK')
        try:
            checked = self.getCheckedBoxList()
            self.setChecked(checked)
            self.close()
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_traceback)

    def selectKeysCancel(self):
        print('[SelectKeys] selectKeysCancel')
        self.close()






if __name__ == "__main__":
    print('*')
    try:
        qApp = QApplication.instance()
        if not qApp:
            qApp = QApplication(sys.argv)
        mdg = MergeDataGUI()
        mdg.show()

        mdg.activateWindow()
        mdg.raise_()
        qApp.exec_()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ex.exception_hook(exc_type, exc_value, exc_traceback)