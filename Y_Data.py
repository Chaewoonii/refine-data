from PyQt5.QtCore import Qt
from RefineDataGUI import *
from MergeDataGUI import *

mainUI = uic.loadUiType('./resources/mainUI.ui')[0]
class RefineDataMainWindow(QDialog, QWidget,mainUI):
    def __init__(self, parent=None):
        super(RefineDataMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.initUi()

    def initUi(self):
        self.openRefineDataBtn.clicked.connect(self.openRefineData)
        self.openMergeDataBtn.clicked.connect(self.openMergeData)
        self.verticalLayout.setAlignment(Qt.AlignCenter)
        self.setWindowTitle('Y-Data')
        self.setWindowIcon(QIcon('./resources/clipboard.png'))

    def openRefineData(self):
        refine = DataModule()
        refine.exec_()

    def openMergeData(self):
        merge = MergeDataGUI()
        merge.exec_()


if __name__== "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)

    main = RefineDataMainWindow()
    main.show()
    main.activateWindow()
    main.raise_()
    app.exec_()