from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from . import qt, excel
import math
import psycopg


class QueryWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(QueryWindow, self).__init__()
        self.app = app
        uic.loadUi(self.app.ui_path.joinpath('queries.ui'), self)

        self.executeButton.clicked.connect(self.executeButton_clicked)
        self.excelButton.clicked.connect(self.excelButton_clicked)

        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.table.verticalHeader().setVisible(False)

        self.setFixedSize(self.size())
        self.show()

        self.queries = [
                ('Вывести филиалы в заданном городе', 'query1', '1', 'Город'),
                ('Вывести клиентов с заданным социальным положением', 'query2', '1', 'Социальное положение'),
                ('Вывести клиентов, которые заключили договоры в заданную дату', 'query3', '1', 'Дата'),
                ('Вывести филиалы, которые заключили договоры в заданную дату', 'query4', '1', 'Дата'),
                ('Вывести компании и их филиалы', 'query5', '0'),
                ('Вывести компании и их типы', 'query6', '0'),
                ('Вывести клиентов и их договоры после увеличения суммы страхования в полтора раза', 'query7', '0'),
                ('Вывести компании, у которых нет филиалов', 'query8', '0'),
                ('Вывести филиалы и их сотрудников', 'query9', '0'),
                ('Вывести компании, у которых нет филиалов, получившие лицензию в указанный период', 'query10', '2', 'Год 1', 'Год 2'),
                ('Вывести количество компаний в каждом городе', 'query11', '0'),
                ('Вывести количество компаний указанного типа', 'query12', '1', 'Тип компании'),
                ('Вывести клиентов, сумма страхования всех контрактов которых больше заданной', 'query13', '1', 'Сумма страхования'),
                ('Вывести клиентов, сумма страхования всех контрактов которых больше заданной, рожденных в заданную дату', 'query14', '2', 'Сумма страхования', 'Дата'),
                ('Вывести филиалы и сумму страхования всех контрактов, заключенных в период за указанные даты', 'query15', '2', 'Дата 1', 'Дата 2'),
                ('Вывести филиалы, сумма страхования контрактов которых больше средней суммы страхования контрактов всех филиалов', 'query16', '0'),
                ('Вывести общее и среднее количество работников филиалов', 'query17', '0'),
                ('Вывести количество компаний, получивших лицензию в заданном году, в каждом городе', 'query18', '1', 'Год'),
                ('Вывести количество клинтов, у которых в имени есть заданные буквы', 'query19', '1', 'Буквы'),
                ('Вывести количество компаний указанного типа(по индексу)', 'query20', '1', 'Тип компании'),
                ('Вывести названия компаний и филиалов', 'query21', '0'),
                ('Вывести клиентов с указанными социальными положениями', 'query22', '2', 'Положение 1', 'Положение 2'),
                ('Вывести клиентов с социальными положениями кроме указанных', 'query23', '2', 'Положение 1', 'Положение 2'),
                ('Вывести контракты и ценовую категорию суммы их страхования', 'query24', '0'),
            ]

        self.fill_combo_box()
        self.comboBox.currentIndexChanged.connect(self.comboBox_currentIndexChanged)
        self.comboBox_currentIndexChanged()
        self.total = 1


    def executeButton_clicked(self):
        current_query = self.queries[self.comboBox.currentIndex()]
        sql_query = current_query[1]
        
        if current_query[2] == '1':
            if current_query[1] == 'query20':
                id = str(self.app.pg.get_id('type', self.lineEdit1.text(), 'company_types')).split(',')[0][1::]
                sql_query += f"('{id}')"
            else:
                sql_query += f"('{self.lineEdit1.text()}')"
        elif current_query[2] == '2':
            sql_query += f"('{self.lineEdit1.text()}', '{self.lineEdit2.text()}')"

        self.table.clear()
        self.table.setRowCount(0)
        for i, column in enumerate(self.app.pg.get_column_names(sql_query)):
            self.table.setColumnCount(i+1)
            self.table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(column))
            self.table.resizeColumnsToContents()
        
        self.rows = self.app.pg.get_all(sql_query)
        for row in self.rows:
            qt.add_table_row(self.table, row)
        
        self.table.resizeColumnsToContents()


    def comboBox_currentIndexChanged(self):
        self.current_page = 0
        self.lineEdit1.setPlaceholderText('')
        self.lineEdit2.setPlaceholderText('')
        self.lineEdit1.setText('')
        self.lineEdit2.setText('')
        current_query = self.queries[self.comboBox.currentIndex()]

        if current_query[2] == '1':
            self.lineEdit1.setEnabled(True)
            self.lineEdit2.setEnabled(False)
            self.executeButton.setEnabled(True)
            self.lineEdit1.setPlaceholderText(current_query[3])
        elif current_query[2] == '2':
            self.lineEdit1.setEnabled(True)
            self.lineEdit2.setEnabled(True)
            self.executeButton.setEnabled(True)
            self.lineEdit1.setPlaceholderText(current_query[3])
            self.lineEdit2.setPlaceholderText(current_query[4])
        else:
            self.lineEdit1.setEnabled(False)
            self.lineEdit2.setEnabled(False)
            self.executeButton.setEnabled(False)
            self.executeButton_clicked()


    def fill_combo_box(self):
        for query in self.queries:
            self.comboBox.addItem(query[0])

    def excelButton_clicked(self):
        excel.export(self.rows)
        qt.message('Экспорт в Excel', 'Экспорт произведен', 'info')
