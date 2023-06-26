from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from . import qt, cru_window, query_window


class ClientWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(ClientWindow, self).__init__()
        self.app = app
        uic.loadUi(self.app.ui_path.joinpath('client.ui'), self)
        self.contractsTable.setColumnWidth(0, 5)
        self.contractsTable.setColumnWidth(1, 229)
        self.contractsTable.setColumnWidth(2, 230)
        self.contractsTable.setColumnWidth(3, 195)
        self.contractsTable.setColumnWidth(4, 191)
        self.companiesTable.setColumnWidth(0, 5)
        self.companiesTable.setColumnWidth(1, 165)
        self.companiesTable.setColumnWidth(2, 208)
        self.companiesTable.setColumnWidth(3, 206)
        self.companiesTable.setColumnWidth(4, 140)
        self.companiesTable.setColumnWidth(5, 135)
        self.branchesTable.setColumnWidth(0, 5)
        self.branchesTable.setColumnWidth(1, 130)
        self.branchesTable.setColumnWidth(2, 130)
        self.branchesTable.setColumnWidth(3, 130)
        self.branchesTable.setColumnWidth(4, 204)
        self.branchesTable.setColumnWidth(5, 130)
        self.branchesTable.setColumnWidth(6, 130)

        self.contractsTable.cellClicked.connect(self.contractsTable_cellClicked)
        self.addcontractButton.clicked.connect(self.addcontract)
        self.deletecontractButton.clicked.connect(self.deletecontract)
        self.searchcontractButton.clicked.connect(self.searchcontract)

        self.searchcompanyButton.clicked.connect(self.searchcompany)
        self.searchbranchButton.clicked.connect(self.searchbranch)

        self.client = self.app.pg.get_all_clients()[0]
        self.label_3.setText('ФИО: ' + self.client[1])
        self.label_4.setText('Дата рождения: ' + str(self.client[2]))
        self.label_5.setText('Социальное положение: ' + self.client[3])
        self.label_6.setText('Телефон: ' + self.client[4])

        self.tabWidget.setCurrentIndex(0)
        self.centralwidget.setContentsMargins(9, 9, 9, 9)
        self.setFixedSize(self.size())
        self.show()
        self.tabWidget.tabBarClicked.connect(self.tab_changed)

    def tab_changed(self, index):
        if index == 0:
            self.update_contracts()
        elif index == 1:
            self.update_companies()
            self.update_branches()

    def update_contracts(self, rows=None):
        self.contractsTable.clearContents()
        self.contractsTable.setRowCount(0)

        if rows==None:
            rows = self.app.pg.get_contracts_by_client_id2(self.client[0])
        for names in rows:
            qt.add_table_row(self.contractsTable, names)

    def update_companies(self, rows=None):
        self.companiesTable.clearContents()
        self.companiesTable.setRowCount(0)

        if rows==None:
            rows = self.app.pg.get_companies()
        for names in rows:
            qt.add_table_row(self.companiesTable, names)

        if len(rows) > 0:
            self.companiesTable.selectRow(0)
            self.companiesTable_cellClicked(0, 0)

    def update_branches(self, rows=None):
        self.branchesTable.clearContents()
        self.branchesTable.setRowCount(0)

        if rows==None:
            rows = self.app.pg.get_branches()
        for names in rows:
            qt.add_table_row(self.branchesTable, names)

        if len(rows) > 0:
            self.branchesTable.selectRow(0)
            self.branchesTable_cellClicked(0, 0)

    def searchcontract(self):
        if self.contractsTable.rowCount() == 0: return
        self.contracts_search_window = cru_window.CRUWindow(
            self.app,
            self.update_contracts,
            'contracts',
            ('search',),
            (('Филиал', 'line'),
            ('Вид страхования', 'line'),
            ('Сумма страхования', 'line'),
            ('Дата заключения договора', 'line')),
            self.app.pg.select_contracts_where2
        )
        self.contracts_search_window.show()

    def addcontract(self):
        self.contracts_add_window = cru_window.CRUWindow(
            self.app,
            self.update_contracts,
            'contracts',
            ('add',),
            (('Филиал', 'combo', 'name', 'branches'),
            ('Клиент', 'noeditline', self.client[1], self.client[0]),
            ('Вид страхования', 'combo', 'type', 'insurance_types'),
            ('Сумма страхования', 'line'),
            ('Дата заключения договора', 'line'))
        )
        self.contracts_add_window.show()

    def deletecontract(self):
        self.app.pg.delete_by_id(self.contractsTable.item(self.contracts_table_row, 0).text(), 'contracts')
        self.update_contracts()

    def searchcompany(self):
        if self.companiesTable.rowCount() == 0: return
        self.companies_search_window = cru_window.CRUWindow(
            self.app,
            self.update_companies,
            'companies',
            ('search',),
            (('Компания', 'line'),
            ('Тип компании', 'line'),
            ('Год получения лицензии', 'line'),
            ('Город', 'line'),
            ('Телефон', 'line')),
            self.app.pg.select_companies_where
        )
        self.companies_search_window.show()

    def searchbranch(self):
        if self.branchesTable.rowCount() == 0: return
        self.branches_search_window = cru_window.CRUWindow(
            self.app,
            self.update_branches,
            'branches',
            ('search',),
            (('Компания', 'line'),
            ('Филиал', 'line'),
            ('Город', 'line'),
            ('Адрес', 'line'),
            ('Телефон', 'line'),
            ('Количество сотрудников', 'line')),
            self.app.pg.select_branches_where
        )
        self.branches_search_window.show()

    def contractsTable_cellClicked(self, row, column):
            self.contracts_table_row = row

    def companiesTable_cellClicked(self, row, column):
            self.companies_table_row = row

    def branchesTable_cellClicked(self, row, column):
            self.branches_table_row = row