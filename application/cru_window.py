from PyQt5 import QtWidgets, uic
from . import qt


class CRUWindow(QtWidgets.QMainWindow):
    def __init__(self, app, update_func, table, mode, args, select_func=None, values_count=None):
        super(CRUWindow, self).__init__()

        self.app = app
        self.update_func = update_func
        self.table = table
        self.mode = mode[0]
        if self.mode == 'edit':
            self.id = mode[1]
        self.args = args
        self.select_func = select_func
        self.values_count = values_count

        uic.loadUi(self.app.ui_path.joinpath('cru_window.ui'), self)
        self.centralwidget.setContentsMargins(9, 9, 9, 9)

        titles = {
            'edit': 'Редактирование',
            'add': 'Добавление',
            'search': 'Поиск'
        }

        button_names = {
            'edit': 'Изменить',
            'add': 'Добавить',
            'search': 'Найти'
        }

        self.setWindowTitle(titles[self.mode])
        self.setFixedSize(400, 0)

        for i, arg in enumerate(self.args):
            if arg[1] == 'line':
                lineEdit = QtWidgets.QLineEdit(self.centralwidget)
                lineEdit.setObjectName(f'l{i+1}')
                lineEdit.setPlaceholderText(arg[0])
                self.verticalLayout.addWidget(lineEdit)
                if self.mode == 'edit':
                    text = str(self.app.pg.get_field_by_id(self.id, arg[2], self.table))
                    lineEdit.setText(text)

            elif arg[1] == 'noeditline':
                lineEdit = QtWidgets.QLineEdit(self.centralwidget)
                lineEdit.setObjectName(f'l{i+1}')
                lineEdit.setPlaceholderText(arg[0])
                self.verticalLayout.addWidget(lineEdit)
                lineEdit.setText(arg[2])
                lineEdit.setReadOnly(True)
                if self.mode == 'edit':
                    text = str(self.app.pg.get_field_by_id(self.id, arg[2], self.table))
                    lineEdit.setText(text)
            
            elif arg[1] == 'combo':
                comboBox = QtWidgets.QComboBox(self.centralwidget)
                comboBox.setObjectName(f'c{i+1}')
                self.fill_combo_box(comboBox, arg[2], arg[3])
                self.verticalLayout.addWidget(comboBox)
                if self.mode == 'edit':
                    for i in range(comboBox.count()):
                        id = comboBox.itemText(i).split(',')[0]
                        if id == str(self.app.pg.get_field_by_id(self.id, arg[4], self.table)):
                            comboBox.setCurrentIndex(i)
                            break

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setText(button_names[self.mode])
        self.pushButton.setFocus()
        self.pushButton.clicked.connect(self.pushButton_clicked)
        self.verticalLayout.addWidget(self.pushButton)
    

    def fill_combo_box(self, combo_box, field, table):
        for row in self.app.pg.get_id_field(field, table):
            combo_box.addItem(f'{row[0]}, {row[1]}')
    

    def pushButton_clicked(self):
        values = []
        for i, arg in enumerate(self.args):
            if arg[1] == 'line':
                lineEdit = self.findChild(QtWidgets.QLineEdit, f'l{i+1}')
                values.append(f"'{lineEdit.text()}'")

            elif arg[1] == 'noeditline':
                lineEdit = self.findChild(QtWidgets.QLineEdit, f'l{i+1}')
                values.append(f"'{arg[3]}'")
            
            elif arg[1] == 'combo':
                comboBox = self.findChild(QtWidgets.QComboBox, f'c{i+1}')
                values.append(f"'{comboBox.currentText().split(',')[0]}'")

        if self.mode == 'edit':
            fields = []
            for i, arg in enumerate(self.args):
                if arg[1] == 'line':
                    fields.append(f'{arg[2]}={values[i]}')
                elif arg[1] == 'combo':
                    fields.append(f'{arg[4]}={values[i]}')
            try:
                self.app.pg.update_values(', '.join(fields), self.id, self.table)
            except:
                self.app.pg.rollback()
                qt.message('Ошибка изменения', 'Введены некорректные данные', 'error')
                return
            self.update_func()
        
        elif self.mode == 'add':
            try:
                self.app.pg.insert_values(', '.join(values), self.table)
            except:
                self.app.pg.rollback()
                qt.message('Ошибка добавления', 'Введены некорректные данные', 'error')
                return
            self.update_func()
        
        elif self.mode == 'search':
            for i in range(len(values)):
                if values[i] == '':
                    values[i] = None
                else:
                    values[i] = values[i].replace('\'', '')

            try:
                rows = self.select_func(*values[0:len(self.args)])
            except:
                self.app.pg.rollback()
                qt.message('Ошибка поиска', 'Введены некорректные данные', 'error')
                return
            self.update_func(rows)
        
        self.close()