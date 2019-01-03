import os
import sys

import pytesseract
from PIL import Image
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QThread, QDir
from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox
from PyQt5.QtWidgets import QMainWindow

from ocr_ui import Ui_MainWindow


class OcrThread(QThread):
    signal = pyqtSignal(str)  # 括号里填写信号传递的参数

    def __init__(self, path):
        super().__init__()
        self.path = path

    def __del__(self):
        self.wait()

    def run(self):
        print("path===>" + self.path)
        # 进行任务操作
        text = pytesseract.image_to_string(Image.open(self.path), lang='chi_sim')
        print("result:"+text)
        self.signal.emit(text)  # 发射信号


class OcrWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(OcrWindow, self).__init__(parent)
        self.setupUi(self)
        self.init()

    def init(self):
        self.setQcrShortcut()

        self.textEdit_result.setTextColor(QtGui.QColor(0, 0, 0))
        self.lineEdit_image_path.setStyleSheet("color:black");
        self.label_screenshort_image.setText("请先使用QQ、微信、钉钉等工具截屏")

        self.pushButton_choose_picture.clicked.connect(self.openFile)
        self.pushButton_start_recognition.clicked.connect(self.ocr)
        self.pushButton_screenshort_paste.clicked.connect(self.pasteImage)
        self.pushButton_screenshort_recognition.clicked.connect(self.ocrScreenshot)

    def ocr(self):
        imagePath = self.lineEdit_image_path.text()
        if imagePath.strip() == '':
            print('s is null')
            self.dialg("请选择要识别图片")
            return
        self.startOcr(imagePath)

    def ocrScreenshot(self):
        imageFormat = 'png'
        saveScreenshotPath = QDir.currentPath() + "/screenshot." + imageFormat
        if saveScreenshotPath.strip() == '':
            print('s is null')
            self.dialg("请粘贴将要识别图片")
            return
        if self.getattribute("screenshotPixmap") is None:
            self.dialg("请粘贴将要识别图片")
            return
        if self.screenshotPixmap.isNull():
            self.dialg("请重新截图识别")
            return
        self.screenshotPixmap.save(saveScreenshotPath, imageFormat)
        self.startOcr(saveScreenshotPath)

    def startOcr(self, path):
        self.thread = OcrThread(path)
        self.thread.signal.connect(self.callback)
        self.thread.start()  # 启动线程

    def callback(self, text):
        if text.strip() == '':
            self.dialg("识别结果为空！")
            return
        self.textEdit_result.setText(text)
        pass

    def getattribute(self, name):
        try:
            r = object.__getattribute__(self, name)
        except:
            r = None
        return r

    def pasteImage(self):
        clipboard = QApplication.clipboard()
        self.screenshotPixmap = clipboard.pixmap();
        if self.screenshotPixmap.isNull():
            print("没有截屏")
            self.dialg("请先使用QQ、微信、钉钉等工具截屏")
            return
        else:
            print("已经截屏")
        # self.label_screenshort_image.setPixmap(self.screenshotPixmap)
        self.label_screenshort_image.setPixmap(self.screenshotPixmap.scaled(
            QSize(300, 300), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def openFile(self):
        imgPath, filetype = QFileDialog.getOpenFileName(self,
                                                        "选取文件",
                                                        os.getcwd(),
                                                        "All Files (*);;Picture Files (*.png);;Picture Files (*.jpg)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(imgPath, filetype)
        self.lineEdit_image_path.setText(imgPath)

    def dialg(self, text: str):
        QMessageBox.information(self,  # 使用infomation信息框
                                "提示",
                                text,
                                QMessageBox.Yes)

    def setQcrShortcut(self):
        """
        set ctrl-c/ctrl-v, etc...
        """

        # copy_action = qt.QAction(self)
        # copy_action.setObjectName('action_copy')
        # copy_action.triggered.connect(self.slot_copy)
        # copy_action.setShortcut(qt.QKeySequence(qt.QKeySequence.Copy))
        # copy_action.setShortcutContext(qt.Qt.WidgetWithChildrenShortcut)
        # self.addAction(copy_action)

        # paste_action = QAction(self)
        # paste_action.setObjectName('action_paste')
        # paste_action.triggered.connect(self.slot_paste)
        # paste_action.setShortcut(QKeySequence(QKeySequence.Paste))
        # paste_action.setShortcutContext(Qt.WidgetWithChildrenShortcut)
        # self.addAction(paste_action)
    def slot_paste(self):
        self.pasteImage()
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = OcrWindow()
    window.show()

    sys.exit(app.exec_())
