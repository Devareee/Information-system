from PyQt5 import QtWidgets, uic
from . import qt
import psycopg


class CUUsersWindow(QtWidgets.QMainWindow):
    def __init__(self, app, update_func):
        super(CUUsersWindow, self).__init__()
        self.app = app
        self.update_func = update_func
        uic.loadUi(self.app.ui_path.joinpath('cru_window.ui'), self)
        self.centralwidget.setContentsMargins(9, 9, 9, 9)
        self.setWindowTitle('Добавление')
        self.setFixedSize(400, 0)

        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setPlaceholderText('Логин')
        self.verticalLayout.addWidget(self.lineEdit)
        
        self.lineEdit2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit2.setPlaceholderText('Пароль')
        self.verticalLayout.addWidget(self.lineEdit2)

        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.addItem('Сотрудник филиала')
        self.comboBox.addItem('Клиент')
        self.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
        self.verticalLayout.addWidget(self.comboBox)

        self.comboBox2 = QtWidgets.QComboBox(self.centralwidget)
        for row in self.app.pg.get_id_field('name', 'branches'):
            self.comboBox2.addItem(f'{row[1]}, {row[0]}')
        self.verticalLayout.addWidget(self.comboBox2)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText('Добавить')
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.verticalLayout.addWidget(self.pushButton)


    def comboBox_currentIndexChanged(self):
        self.comboBox2.clear()
        if self.comboBox.currentIndex() == 0:
            for row in self.app.pg.get_id_field('name', 'branches'):
                self.comboBox2.addItem(f'{row[1]}, {row[0]}')
        else:
            for row in self.app.pg.get_id_field('name', 'clients'):
                self.comboBox2.addItem(f'{row[1]}, {row[0]}')


    def pushButton_clicked(self):
        branch_id = self.comboBox2.currentText().split(',')[1]
        role = self.comboBox.currentText()

        try:
            login = self.lineEdit.text()
            password = self.lineEdit2.text()
            if '' in (login, password):
                raise Exception()
            self.app.pg.create_user(login, password, role, branch_id)
        except:
            self.app.pg.rollback()
            qt.message('Ошибка добавления', 'Некорректные данные либо пользователь уже существует', 'error')
            return

        self.update_func()
        self.close()
