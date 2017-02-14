from PyQt4 import QtGui
# from mainwindow import Ui_MainWindow

class NotAuthorized(QtGui.QDialog):
    def __init__(self, parent=None):
        super(NotAuthorized, self).__init__(parent)
        self.textName = QtGui.QLabel("Protected dataset, not authorized")
        self.buttonAccept = QtGui.QPushButton('Accept', self)
        self.buttonAccept.clicked.connect(self.handleAccept)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.textName)
        layout.addWidget(self.buttonAccept)
        self.setLayout(layout)
        self.setWindowTitle("Protected")

    def handleAccept(self):
        self.accept()
            
