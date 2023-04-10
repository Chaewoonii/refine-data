import sys
import os
import pandas as pd
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from pandasModel import PandasModel
from PyQt5 import uic
from MyUtill import MyUtill
from refineData import RefineData
from ExceptionHook import ExceptionHook

#예외처리 안함...ㅎㅎ....ㅜ
ex = ExceptionHook()
formClass = uic.loadUiType("./resources/dataModuleUI.ui")[0]
class DataModule(QDialog, QWidget, formClass):
    def __init__(self):
        print('[DataModule] __init__****')
        super().__init__()
        self.mu = MyUtill()
        self.rd = RefineData()
        self.path = ''
        self.fileName = ''
        self.df = pd.DataFrame()
        self.model = PandasModel(self.df)
        self.cols = []
        self.setupUi(self)
        self.initUi()


    def initUi(self):
        print('[DataModule] initUi****')
        self.openFileBtn.clicked.connect(self.setTableView)
        self.setColNameBtn.clicked.connect(self.setColName)
        self.addColBtn.clicked.connect(self.addCol)
        self.delColBtn.clicked.connect(self.delCol)
        self.setAddressBtn.clicked.connect(self.setAddress)
        self.setNameBtn.clicked.connect(self.setName)
        self.setPhoneNumBtn.clicked.connect(self.setPhoneNum)
        self.setDateBtn.clicked.connect(self.setDate)
        self.changeUnitBtn.clicked.connect(self.changeUnit)
        self.addCharBtn.clicked.connect(self.addChar)
        self.delCharBtn.clicked.connect(self.delChar)
        self.delSpCharBtn.clicked.connect(self.delSpecial)
        self.extractDataBtn.clicked.connect(self.extractData)

        self.saveBtn.clicked.connect(self.dataModuleSave)
        self.cancelBtn.clicked.connect(self.dataModuleClose)
        self.setWindowTitle('Refine Data::::데이터 정제')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def setPath(self, path):
        print('[DataModule] setPath****')
        self.path = path

    def getPath(self):
        print('[DataModule] getPath****')
        return self.path

    def setDF(self, df):
        print('[DataModule] setDF****')
        self.df = df


    def getDF(self):
        print('[DataModule] getDF****')
        return self.df

    def setCols(self, li):
        print('[DataModule] setCols****')
        self.cols = li

    def getCols(self):
        print('[DataModule] getCols****')
        return self.cols

    def setModel(self, df):
        print('[DataModule] setModel****')
        self.model = PandasModel(df)

    def getModel(self):
        print('[DataModule] getModel****')
        return self.model

    def openFile(self):
        print('[DataModule] openFile****')
        p = ''

        file_tuple = QFileDialog.getOpenFileName(self, 'Open file', './')
        try:
            if file_tuple != ('', ''):
                p = file_tuple[0]
            else:
                print('else')
        except:
            print('except')

        else:
            print('except else')

        if p != '':
            print(p)
            self.path, self.fileName = self.mu.getPath_FileName(p)
            try:
                df = pd.read_csv(p, encoding='cp949', engine='python')

            except:
                df = pd.read_csv(p, encoding='utf-8-sig', engine='python')

            self.setDF(df)
            self.setCols(df.columns.to_list())
            self.setModel(df)
            self.fileNameLabel.setText(self.fileName.replace('.csv',''))
            return df

        else:
            print('DataFrameLoad Fail!!')
            return pd.DataFrame()


    def setTableWidget(self):
        print('[DataModule] setTableWidget****')
        df = self.openFile()
        self.tableWidget.setRowCount(len(df.index))
        self.tableWidget.setColumnCount(len(df.columns))
        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                self.tableWidget.setItem(i,j,QTableWidgetItem(str(df.iloc[i,j])))

        for idx, name in enumerate(df.columns.to_list()):
            self.tableWidget.setHorizontalHeaderItem(idx, QTableWidgetItem(str(name)))

    def setTableView(self):
        print('[DataModule] setTableView****')
        df = self.openFile()
        print('[DataModule] setTableViewDebug****')
        print(df)
        if df.empty:
            print('[DataModule] setTableView: Empty DataFrame')

        else:
            print('[DataModule] setTableView: DataFrame init::::::tableView Loading')
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.setAlternatingRowColors(True)
            self.tableView.setSelectionBehavior(QTableView.SelectRows)
            self.tableView.setModel(self.model)
            self.tableView.show()

        print('stv debug end')

    def setTableView2(self, df):
        print('[DataModule] setTableView2****')
        if df.empty:
            print('[DataModule] setTableView2: Empty DataFrame')

        else:
            print('[DataModule] setTableView2: DataFrame init::::::tableView Loading')
            self.setModel(df)
            self.tableView.horizontalHeader().setStretchLastSection(True)
            self.tableView.setAlternatingRowColors(True)
            self.tableView.setSelectionBehavior(QTableView.SelectRows)
            self.tableView.setModel(self.model)
            self.tableView.show()

    def setColName(self):
        print('[DataModule] setColName****')
        sct = SelectCol_Text(self, self.cols)
        sct.exec_()

        target = sct.getTarget()
        colName = sct.getText()

        if target != '' and colName != '':
            self.df = self.df.rename(columns={target : colName})
        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)

    def addCol(self):
        print('[DataModule] addCol****')
        adc = AddColWindow(self)
        adc.exec_()

        colName = adc.getInputCol()
        data = adc.getInputData()

        if colName != '' and data != '':
            self.df[colName] = data
        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)

    def delCol(self):
        print('[DataModule] delCol****')

        sc = SelectCol(self, self.cols)
        sc.exec_()

        target = sc.getTarget()
        if target != '':
            self.df = self.df.drop(target, axis=1)
        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)

    def setAddress(self):
        print('[DataModule] setAddress****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()

        if target != '':
            so = SelectOption(self, ['일반', '괄호삭제', '상세주소 분리', '우편번호 분리'])
            so.exec_()
            option = so.getSelectedNum()
            if option != -1:
                if option == 0:
                    self.df[target] = self.rd.getAddLi(self.df[target].to_list())

                elif option == 1:
                    self.df[target] = self.rd.delAfterBracket(self.df[target].to_list())

                elif option == 2:
                    self.df[target], self.df['상세주소'] = self.rd.setAddress_detail(self.df[target].to_list())

                elif option == 3:
                    self.df['우편번호'], self.df[target] = self.rd.setZipCode(self.df[target].to_list())

        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)

    def setName(self):
        print('[DataModule] setName****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()

        if target != '':
            self.df[target] = self.rd.getNameLi(self.df[target].to_list())
        self.setTableView2(self.df)

    def setPhoneNum(self):
        print('[DataModule] setPhoneNum****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()

        if target != '':
            self.df[target] = self.rd.getPNumLi_multi(self.df[target].to_list())
        self.setTableView2(self.df)

    def setDate(self):
        print('[DataModule] setDate****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()
        if target != '':
            so = SelectOption(self, ['YYYY-MM-DD', 'YEAR, MONTH 분리'])
            so.exec_()
            option = so.getSelectedNum()
            if option != -1:
                if option == 0:
                    self.df[target] = self.rd.getDateLi(self.df[target].to_list())
                else:
                    self.df[target] = self.rd.getDateLi(self.df[target].to_list())
                    self.df['YEAR'], self.df['MONTH'] = self.rd.getYMLi(self.df[target].to_list())

        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)

    def changeUnit(self):
        print('[DataModule] setDate****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()

        if target != '':
            so = SelectOption(self, ['m->cm', 'cm->m'])
            so.exec_()
            option = so.getSelectedNum()
            if option != -1:
                self.df[target] = self.rd.changeUnit(self.df[target].to_list(), option)
        self.setTableView2(self.df)

    def addChar(self):
        print('[DataModule] setDate****')
        sct = SelectCol_Text(self, self.cols)
        sct.exec_()
        target = sct.getTarget()
        text = sct.getText()
        if target != '' and text != '':
            self.df[target] = self.rd.addCharLi(self.df[target].to_list(), text)
        self.setTableView2(self.df)

    def delChar(self):
        print('[DataModule] setDate****')
        sct = SelectCol_Text(self, self.cols)
        sct.exec_()
        target = sct.getTarget()
        text = sct.getText()
        if target != '' and text != '':
            self.df[target] = self.rd.delCharLi(self.df[target].to_list(), text)
        self.setTableView2(self.df)

    def delSpecial(self):
        print('[DataModule] delSpecial****')
        sc = SelectCol(self, self.cols)
        sc.exec_()
        target = sc.getTarget()

        if target != '':
            so = SelectOption(self, ['일반', '엔터삭제', '/삭제', '공백 삭제', '대소문자 변경', '괄호삭제'])
            so.exec_()
            option = so.getSelectedNum()
            if option != -1:
                if option == 0:
                    self.df[target]  = self.rd.delSpecial(self.df[target].to_list())

                elif option == 1:
                    self.df[target] = self.rd.delEnter(self.df[target].to_list())

                elif  option == 2:
                    self.df[target] = self.rd.delSlash(self.df[target].to_list())

                elif option == 3:
                    self.df[target] = self.rd.delBlank(self.df[target].to_list())

                elif option == 4:
                    if option != -1:
                        so2 = SelectOption(self, ['소문자->대문자', '대문자->소문자'])
                        so2.exec_()
                        option2 = so2.getSelectedNum()
                        if option2 == 1: self.df[target] = self.rd.getUL_li(self.df[target].to_list(), False)
                        else: self.df[target] = self.rd.getUL_li(self.df[target].to_list())

                elif option == 5:
                    self.df[target] = self.rd.delBracket(self.df[target].to_list())

        self.setCols(self.df.columns.to_list())
        self.setTableView2(self.df)
    '''
    def extractData(self):
        print('[DataModule] extractData****')
        sct = SelectCol_Text(self, self.cols)
        sct.exec_()

        target = sct.getTarget()
        text = sct.getText()

        if target != '' and text != '':
            self.df = self.df[self.df[target] == text]
        self.setTableView2(self.df)
    '''
    def extractData(self):
        print('[DataModule] extractData****')
        sc = SelectCol(parent=self, cols=['문자\t\t\t\t', '숫자\t\t'])
        sc.exec_()

        target = sc.getTarget()
        if target == '문자\t\t\t\t':
            self.extractData_Str()
        elif target == '숫자\t\t':
            self.extractData_Int()

    def extractData_Str(self):
        print('[DataModule] extractData_Str****')
        sct = SelectCol_Text(self, self.cols)
        sct.exec_()

        target = sct.getTarget()
        text = sct.getText()

        if target != '' and text != '':
            self.df = self.df[self.df[target] == text]
        self.setTableView2(self.df)

    def extractData_Int(self):
        print('[DataModule] extractData_Int****')
        try:
            ed = ExtractData(self, self.df.columns.to_list())
            ed.exec_()

            df = self.rd.getCondiDf(self.df, ed.selectedCol, ed.condiD, ed.condiS)
            print(df)
            self.setDF(df)


        except:
            exc_type, exc_value, exc_target = sys.exc_info()
            ex.exception_hook(exc_type, exc_value, exc_target)


    def dataModuleSave(self):
        print('[DataModule] dataModuleSave****')
        path, fileType = QFileDialog.getSaveFileName(parent=self, caption='Save File',
                                                     directory=f'./{self.fileName}',
                                                     filter='CSV (*.csv);;Excel (*.xlsx)')
        if fileType == 'CSV (*.csv)':
            self.df.to_csv(path, encoding='cp949', index=False)
            os.startfile(path)

        elif fileType == 'Excel (*.xlsx)':
            self.df.to_excel(path, columns=self.df.columns.to_list(), index=False)
            os.startfile(path)

        else:
            print('file type not found')

    def dataModuleClose(self):
        print('[DataModule] dataModuleClose****')
        self.close()

class SelectCol_Text(QDialog, QWidget):
    def __init__(self, parent, colNames):
        print('[SelectCol_Text] __init__----')
        super(SelectCol_Text, self).__init__(parent)
        self.col_li = colNames
        self.target = ''
        self.text = ''
        self.cnt = len(colNames)
        self.initUI()

        self.show()

    def initUI(self):
        print('[SelectCol_Text] initUI----')
        print(self.col_li)
        self.box1 = QGridLayout()
        for i in range(self.cnt):
            globals()[f'rbtn{i}'] = QRadioButton(f'rbtn{i}', self)
            globals()[f'rbtn{i}'].setText(self.col_li[i])
            self.box1.addWidget(globals()[f'rbtn{i}'], i // 2, i % 2)

        self.textBox = QLineEdit()
        self.textBox.returnPressed.connect(self.selectCol_TextConfirm)

        self.SelectCol_TextCommit = QPushButton('확인', self)
        self.SelectCol_TextCommit.clicked.connect(self.selectCol_TextConfirm)
        self.SelectCol_TextCancel = QPushButton('취소', self)
        self.SelectCol_TextCancel.clicked.connect(self.selectCol_TextClose)

        self.box2 = QHBoxLayout()
        self.box2.addWidget(self.SelectCol_TextCommit)
        self.box2.addWidget(self.SelectCol_TextCancel)

        self.box3 = QVBoxLayout()
        self.box3.addLayout(self.box1)
        self.box3.addWidget(self.textBox)
        self.box3.addLayout(self.box2)

        self.setLayout(self.box3)
        self.setWindowTitle('속성 선택')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def setTarget(self, target):
        print('[SelectCol_Text] setTarget----')
        self.target = target
        print(self.target)

    def getTarget(self):
        print('[SelectCol_Text] getTarget----')
        return self.target

    def setText(self):
        print('[SelectCol_Text] setText----')
        self.text = self.textBox.text()
        print(self.text)

    def getText(self):
        print('[SelectCol_Text] getText----')
        return self.text

    def selectCol_TextConfirm(self):
        print('[SelectCol_Text] selectCol_TextConfirm----')
        for i in range(self.cnt):
            if globals()[f'rbtn{i}'].isChecked():
                self.setTarget(self.col_li[i])
        self.setText()
        self.close()

    def selectCol_TextClose(self):
        print('[SelectCol_Text] selectCol_TextClose----')
        self.close()

class SelectCol(QDialog, QWidget):
    def __init__(self, parent, cols):
        print('[SelectCol] __init__----')
        super(SelectCol, self).__init__(parent)
        self.cols = cols
        self.target = ''
        self.cnt = len(cols)
        self.initUI()
        self.show()

    def initUI(self):
        print('[SelectCol] initUI----')
        self.gbox = QGridLayout()

        for i in range(self.cnt):
            globals()[f'rbtn{i}'] = QRadioButton(f'rbtn{i}', self)
            globals()[f'rbtn{i}'].setText(self.cols[i])
            self.gbox.addWidget(globals()[f'rbtn{i}'], i//2, i%2)


        self.SelectColCommit = QPushButton('확인', self)
        self.SelectColCommit.clicked.connect(self.selectColConfirm)
        self.SelectColCancel = QPushButton('취소', self)
        self.SelectColCancel.clicked.connect(self.selectColClose)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.SelectColCommit)
        self.hbox.addWidget(self.SelectColCancel)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.gbox)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle('속성 선택')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def selectColConfirm(self):
        print('[SelectCol] selectColConfirm----')
        for i in range(self.cnt):
            if globals()[f'rbtn{i}'].isChecked():
                self.setTarget(self.cols[i])
        self.close()

    def setTarget(self, target):
        print('[SelectCol] setTarget----')
        self.target = target

    def getTarget(self):
        print('[SelectCol] getTarget----')
        return self.target

    def selectColClose(self):
        print('[SelectCol] selectColClose----')
        self.close()

class AddColWindow(QDialog, QWidget):
    def __init__(self, parent):
        print('[AddColWindow] __init__----')
        super(AddColWindow, self).__init__(parent)
        self.inputCol = ''
        self.inputData = ''
        self.initUI()

        self.show()

    def initUI(self):
        print('[AddColWindow] initUI----')
        self.gbox = QGridLayout()
        self.label1 = QLabel('속성명 입력: ',self)
        self.label2 = QLabel('데이터 입력: ', self)
        self.lineEd_col = QLineEdit()
        self.lineEd_data = QLineEdit()

        self.gbox.addWidget(self.label1, 0, 0)
        self.gbox.addWidget(self.lineEd_col, 0, 1)
        self.gbox.addWidget(self.label2, 1, 0)
        self.gbox.addWidget(self.lineEd_data, 1, 1)

        self.AddColWindowCommit = QPushButton('확인', self)
        self.AddColWindowCommit.clicked.connect(self.addColWindowConfirm)

        self.AddColWindowCancel = QPushButton('취소', self)
        self.AddColWindowCancel.clicked.connect(self.addColWindowClose)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.AddColWindowCommit)
        self.hbox.addWidget(self.AddColWindowCancel)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.gbox)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle('속성 추가')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def setInputCol(self):
        print('[AddColWindow] setInputCol----')
        self.inputCol = self.lineEd_col.text()

    def getInputCol(self):
        print('[AddColWindow] getInputCol----')
        return self.inputCol

    def setInputData(self):
        print('[AddColWindow] setInputData----')
        self.inputData = self.lineEd_data.text()

    def getInputData(self):
        print('[AddColWindow] getInputData----')
        return self.inputData

    def addColWindowConfirm(self):
        print('[AddColWindow] addColWindowConfirm----')
        self.setInputCol()
        self.setInputData()
        self.close()

    def addColWindowClose(self):
        print('[AddColWindow] addColWindowClose----')
        self.close()

class SelectOption(QDialog, QWidget):
    def __init__(self, parent, options):
        super(SelectOption, self).__init__(parent)
        self.options = options
        self.cnt = len(self.options)
        self.selectedNum = -1
        self.initUI()

    def initUI(self):
        print('[SelectCol] initUI----')
        self.gbox = QGridLayout()

        for i in range(self.cnt):
            globals()[f'rbtn{i}'] = QRadioButton(f'rbtn{i}',self)
            globals()[f'rbtn{i}'].setText(self.options[i])
            self.gbox.addWidget(globals()[f'rbtn{i}'], i // 2, i % 2)

        self.SelectOptionCommit = QPushButton('확인', self)
        self.SelectOptionCommit.clicked.connect(self.selectOptionConfirm)

        self.SelectOptionCancel = QPushButton('취소', self)
        self.SelectOptionCancel.clicked.connect(self.selectOptionClose)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.SelectOptionCommit)
        self.hbox.addWidget(self.SelectOptionCancel)

        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.gbox)
        self.vbox.addLayout(self.hbox)

        self.setLayout(self.vbox)
        self.setWindowTitle('옵션 선택')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def setSelectedNum(self, option):
        self.selectedNum = option

    def getSelectedNum(self):
        return self.selectedNum

    def selectOptionConfirm(self):
        for i in range(self.cnt):
            if globals()[f'rbtn{i}'].isChecked():
                self.setSelectedNum(i)
        self.close()

    def selectOptionClose(self):
        self.close()


extractDataUI = uic.loadUiType('./resources/extractData.ui')[0]
class ExtractData(QDialog, QWidget, extractDataUI):
    def __init__(self, parent=None, cols=None):
        super(ExtractData, self).__init__(parent)
        self.cols = cols
        self.rbtnLi = []
        self.selectedCol = None
        self.condiD = 0.0
        self.condiS = ''
        self.setupUi(self)
        self.initUI()
        self.show()

    def initUI(self):
        self.setCols(self.cols, self.gridLayout)
        self.okBtn.clicked.connect(self.extractDataOk)
        self.cancelBtn.clicked.connect(self.extractDataCancel)

    def setCols(self, cols, layout):
        li = self.getRbtnLi(cols)
        self.setRbtnLi(li)
        self.addToLayout(li, layout)

    def getRbtnLi(self, cols):
        li = []
        for i, item in enumerate(cols):
            rbtn = QRadioButton(item, self)
            li.append(rbtn)
        return li

    def addToLayout(self, li, layout):
        for i, item in enumerate(li):
            layout.addWidget(item, i // 2, i % 2)
        return layout

    def extractDataOk(self):
        self.setCondies()
        self.close()

    def extractDataCancel(self):
        self.close()

    def setCondiD(self, double):
        self.condiD = double

    def setCondiS(self, string):
        self.condiS = string

    def setRbtnLi(self, li):
        self.rbtnLi = li

    def setSelectedCol(self, selected):
        self.selectedCol = selected

    def setCondies(self):
        selected = self.getSelected()
        self.setSelectedCol(selected)
        self.setCondiD(self.doubleSpinBox.value())
        self.setCondiS(self.comboBox.currentText())

    def getSelected(self):
        selected = ''
        for item in self.rbtnLi:
            if item.isChecked():
                selected = item.text()
        return selected



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        dm = DataModule()
        dm.show()
        app.exec_()

    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        ex.show_exception_box(exc_type, exc_value, exc_traceback)