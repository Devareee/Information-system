from PyQt5 import QtWidgets, uic
from . import postgres, branch_window, admin_window, client_window, qt, query_window
import psycopg


class Auth(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(Auth, self).__init__()
        self.app = app
        uic.loadUi(self.app.ui_path.joinpath('auth.ui'), self)
        self.gridLayout.setContentsMargins(9, 9, 9, 9)
        self.setFixedSize(self.size())
        self.show()

        self.main_window = None
        self.pushButton.clicked.connect(self.pushButton_clicked)


    def pushButton_clicked(self):
        self.app.pg = postgres.Postgres()

        try:
            self.app.pg.connect(self.loginEdit.text(), self.passwordEdit.text())
            role = self.app.pg.check_role()
            self.app.pg.reset_role()
        except:
            qt.message('Ошибка входа', 'Неверный логин или пароль', 'error')
            return
        
        if role == 'branch_employees':
            self.main_window = branch_window.BranchWindow(self.app)
        elif role == 'clients_role':
            self.main_window = client_window.ClientWindow(self.app)
        elif role == 'admins':
            self.main_window = admin_window.AdminWindow(self.app)
        elif role == 'queries_role':
            self.main_window = query_window.QueryWindow(self.app)
        
        self.hide()
