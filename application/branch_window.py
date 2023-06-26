from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from . import qt, cru_window


class BranchWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(BranchWindow, self).__init__()
        self.app = app
        uic.loadUi(self.app.ui_path.joinpath('branch_employee.ui'), self)
        self.contractsTable.setColumnWidth(0, 5)
        self.contractsTable.setColumnWidth(1, 320)
        self.contractsTable.setColumnWidth(2, 245)
        self.contractsTable.setColumnWidth(3, 240)
        self.contractsTable.setColumnWidth(4, 223)
        self.clientsTable.setColumnWidth(0, 5)
        self.clientsTable.setColumnWidth(1, 288)
        self.contractsTable_2.setColumnWidth(0, 5)
        self.contractsTable_2.setColumnWidth(1, 230)
        self.contractsTable_2.setColumnWidth(2, 229)
        self.contractsTable_2.setColumnWidth(3, 229)

        self.addcontractButton.clicked.connect(self.addcontract)
        self.addclientButton.clicked.connect(self.addclient)
        self.addclientcontractButton.clicked.connect(self.addclientcontract)
        self.deletecontractButton.clicked.connect(self.deletecontract)
        self.deleteclientButton.clicked.connect(self.deleteclient)
        self.deleteclientcontractButton.clicked.connect(self.deletecontract)
        self.searchcontractButton.clicked.connect(self.searchcontract)
        self.searchclientButton.clicked.connect(self.searchclient)
        self.contractsTable.cellClicked.connect(self.contractsTable_cellClicked)
        self.clientsTable.cellClicked.connect(self.clientsTable_cellClicked)

        self.branch = self.app.pg.get_branch()
        self.label_3.setText('Компания: ' + self.branch[0])
        self.label_4.setText('Название: ' + self.branch[1])
        self.label_5.setText('Город: ' + self.branch[2])
        self.label_6.setText('Адрес: ' + self.branch[3])
        self.label_7.setText('Телефон: ' + self.branch[4])
        self.label_8.setText('Количество сотрудников: ' + str(self.branch[5]))

        self.centralwidget.setContentsMargins(9, 9, 9, 9)
        self.setFixedSize(self.size())
        self.show()

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBarClicked.connect(self.tab_changed)

    def tab_changed(self, index):
        if index == 0:
            self.update_contracts()
        elif index == 1:
            self.update_clients()
    
    def update_contracts(self, rows=None):
        self.contractsTable.clearContents()
        self.contractsTable.setRowCount(0)
        if rows==None:
            rows = self.app.pg.get_contracts()
        for names in rows:
            qt.add_table_row(self.contractsTable, names)
        
        if len(rows) > 0:
            self.contractsTable.selectRow(0)

    def update_clients(self, rows=None):
        self.clientsTable.clearContents()
        self.clientsTable.setRowCount(0)
        self.contractsTable_2.clearContents()
        self.contractsTable_2.setRowCount(0)
        if rows==None:
            rows = self.app.pg.get_all_clients()
        for names in rows:
            qt.add_table_row(self.clientsTable, names)
        
        if len(rows) > 0:
            self.clientsTable.selectRow(0)
            self.clientsTable_cellClicked(0, 0)

    def clientsTable_cellClicked(self, row, column):
        self.clients_table_row = row
        self.contractsTable_2.clearContents()
        self.contractsTable_2.setRowCount(0)
        self.client_id = self.clientsTable.item(row, 0).text()
        client = self.app.pg.get_client_by_id(self.client_id)
        self.label_11.setText('Дата рождения: ' + str(client[1]))
        self.label_12.setText('Социальное положение: ' + client[2])
        self.label_13.setText('Телефон: ' + client[3])
        for contract in self.app.pg.get_contracts_by_client_id(self.client_id):
            qt.add_table_row(self.contractsTable_2, contract)

    def contractsTable_cellClicked(self, row, column):
        self.contracts_table_row = row

    def addcontract(self):
        self.contracts_add_window = cru_window.CRUWindow(
            self.app,
            self.update_contracts,
            'contracts',
            ('add',),
            (('Филиал', 'noeditline', self.branch[1], self.app.pg.get_branches()[0][0]),
            ('Клиент', 'combo', 'name', 'clients'),
            ('Вид страхования', 'combo', 'type', 'insurance_types'),
            ('Сумма страхования', 'line'),
            ('Дата заключения договора', 'line'))
        )
        self.contracts_add_window.show()

    def addclient(self):
        self.clients_add_window = cru_window.CRUWindow(
            self.app,
            self.update_clients,
            'clients',
            ('add',),
            (('ФИО', 'line'),
            ('Дата рождения', 'line'),
            ('Социальное положение', 'combo', 'status', 'social_statuses'),
            ('Телефон', 'line'))
        )
        self.clients_add_window.show()

    def addclientcontract(self):
        self.contracts_add_window = cru_window.CRUWindow(
            self.app,
            self.update_contracts,
            'contracts',
            ('add',),
            (('Филиал', 'noeditline', self.branch[1], self.app.pg.get_branches()[0][0]),
            ('Клиент', 'noeditline', self.clientsTable.item(self.clients_table_row, 1).text(), self.client_id),
            ('Вид страхования', 'combo', 'type', 'insurance_types'),
            ('Сумма страхования', 'line'),
            ('Дата заключения договора', 'line'))
        )
        self.contracts_add_window.show()

    def deletecontract(self):
        self.app.pg.delete_by_id(self.contractsTable.item(self.contracts_table_row, 0).text(), 'contracts')
        self.update_contracts()

    def deleteclient(self):
        self.app.pg.delete_by_id(self.clientsTable.item(self.clients_table_row, 0).text(), 'clients')
        self.update_clients()

    def searchcontract(self):
        if self.contractsTable.rowCount() == 0: return
        self.contracts_search_window = cru_window.CRUWindow(
            self.app,
            self.update_contracts,
            'contracts',
            ('search',),
            (('Клиент', 'line'),
            ('Вид страхования', 'line'),
            ('Сумма страхования', 'line'),
            ('Дата заключения договора', 'line')),
            self.app.pg.select_contracts_where3
        )
        self.contracts_search_window.show()

    def searchclient(self):
        if self.clientsTable.rowCount() == 0: return
        self.clients_search_window = cru_window.CRUWindow(
            self.app,
            self.update_clients,
            'clients',
            ('search',),
            (('ФИО', 'line'),
            ('Дата рождения', 'line'),
            ('Социальное положение', 'line'),
            ('Телефон', 'line')),
            self.app.pg.select_clients_where
        )
        self.clients_search_window.show()
