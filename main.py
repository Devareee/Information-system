from application import auth
from PyQt5 import QtWidgets
import sys
import pathlib


class Application:
    def __init__(self):
        self.app_path = pathlib.Path(__file__).parent.resolve().joinpath('application') 
        self.ui_path = self.app_path.joinpath('ui')

        self.app = QtWidgets.QApplication(sys.argv)
        self.auth = auth.Auth(self)
        self.app.exec_()


if __name__ == '__main__':
    app = Application()
