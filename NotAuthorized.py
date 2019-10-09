from PyQt5.uic.Compiler.qtproxies import QtWidgets
# from mainwindow import Ui_MainWindow

class NotAuthorized(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(NotAuthorized, self).__init__(parent)
        self.textName = QtWidgets.QLabel("Protected dataset, not authorized")
        self.buttonAccept = QtWidgets.QPushButton('Accept', self)
        self.buttonAccept.clicked.connect(self.handleAccept)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.textName)
        layout.addWidget(self.buttonAccept)
        self.setLayout(layout)
        self.setWindowTitle("Protected")

    def handleAccept(self):
        self.accept()
            
