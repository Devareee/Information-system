from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
from . import qt, cru_window, cu_users_window


class AdminWindow(QtWidgets.QMainWindow):
    def __init__(self, app):
        super(AdminWindow, self).__init__()
        self.app = app
        uic.loadUi(self.app.ui_path.joinpath('admin.ui'), self)

        self.socialstatusesTable.setColumnWidth(0, 5)
        self.socialstatusesTable.setColumnWidth(1, 334)
        self.citiesTable.setColumnWidth(0, 5)
        self.citiesTable.setColumnWidth(1, 334)
        self.insurancetypesTable.setColumnWidth(0, 5)
        self.insurancetypesTable.setColumnWidth(1, 334)
        self.companytypesTable.setColumnWidth(0, 5)
        self.companytypesTable.setColumnWidth(1, 334)
        self.usersTable.setColumnWidth(0, 270)
        self.usersTable.setColumnWidth(1, 269)
        self.usersTable.setColumnWidth(2, 270)

        self.adduserButton.clicked.connect(self.adduser)
        self.addsocialstatusButton.clicked.connect(self.addsocialstatus)
        self.addcityButton.clicked.connect(self.addcity)
        self.addinsurancetypeButton.clicked.connect(self.addinsurancetype)
        self.addcompanytypeButton.clicked.connect(self.addcompanytype)

        self.deleteuserButton.clicked.connect(self.deleteuser)
        self.deletesocialstatusButton.clicked.connect(self.deletesocialstatus)
        self.deletecityButton.clicked.connect(self.deletecity)
        self.deleteinsurancetypeButton.clicked.connect(self.deleteinsurancetype)
        self.deletecompanytypeButton.clicked.connect(self.deletecompanytype)

        self.editsocialstatusButton.clicked.connect(self.editsocialstatus)
        self.editcityButton.clicked.connect(self.editcity)
        self.editinsurancetypeButton.clicked.connect(self.editinsurancetype)
        self.editcompanytypeButton.clicked.connect(self.editcompanytype)

        self.usersTable.cellClicked.connect(self.usersTable_cellClicked)
        self.socialstatusesTable.cellClicked.connect(self.socialstatusesTable_cellClicked)
        self.citiesTable.cellClicked.connect(self.citiesTable_cellClicked)
        self.insurancetypesTable.cellClicked.connect(self.insurancetypesTable_cellClicked)
        self.companytypesTable.cellClicked.connect(self.companytypesTable_cellClicked)

        self.centralwidget.setContentsMargins(9, 9, 9, 9)
        self.setFixedSize(self.size())
        self.show()

        self.tabWidget.setCurrentIndex(0)
        self.tabWidget.tabBarClicked.connect(self.tab_changed)

    def tab_changed(self, index):
        if index == 0:
            self.update_socialstatuses()
            self.update_cities()
            self.update_insurancetypes()
            self.update_companytypes()
        elif index == 1:
            self.update_users()
    
    def update_socialstatuses(self):
        self.socialstatusesTable.clearContents()
        self.socialstatusesTable.setRowCount(0)

        rows = self.app.pg.get_socialstatuses()
        for names in rows:
            qt.add_table_row(self.socialstatusesTable, names)

    def update_cities(self):
        self.citiesTable.clearContents()
        self.citiesTable.setRowCount(0)

        rows = self.app.pg.get_cities()
        for names in rows:
            qt.add_table_row(self.citiesTable, names)

    def update_insurancetypes(self):
        self.insurancetypesTable.clearContents()
        self.insurancetypesTable.setRowCount(0)

        rows = self.app.pg.get_insurancetypes()
        for names in rows:
            qt.add_table_row(self.insurancetypesTable, names)

    def update_companytypes(self):
        self.companytypesTable.clearContents()
        self.companytypesTable.setRowCount(0)

        rows = self.app.pg.get_companytypes()
        for names in rows:
            qt.add_table_row(self.companytypesTable, names)

    def update_users(self):
        self.usersTable.clearContents()
        self.usersTable.setRowCount(0)

        rows = self.app.pg.get_users()
        for names in rows:
            qt.add_table_row(self.usersTable, names)

        if len(rows) > 0:
            self.usersTable.selectRow(0)
            self.usersTable_cellClicked(0, 0)

    def adduser(self):
        self.users_add_window = cu_users_window.CUUsersWindow(
            self.app,
            self.update_users
        )
        self.users_add_window.show()
    
    def addsocialstatus(self):
        self.socialstatuses_add_window = cru_window.CRUWindow(
            self.app,
            self.update_socialstatuses,
            'social_statuseses',
            ('add',),
            (('Социальное положение', 'line'),)
        )
        self.socialstatuses_add_window.show()

    def addcity(self):
        self.cities_add_window = cru_window.CRUWindow(
            self.app,
            self.update_cities,
            'cities',
            ('add',),
            (('Город', 'line'),)
        )
        self.cities_add_window.show()

    def addinsurancetype(self):
        self.insurancetypes_add_window = cru_window.CRUWindow(
            self.app,
            self.update_insurancetypes,
            'insurance_types',
            ('add',),
            (('Вид страхования', 'line'),)
        )
        self.insurancetypes_add_window.show()

    def addcompanytype(self):
        self.companytypes_add_window = cru_window.CRUWindow(
            self.app,
            self.update_companytypes,
            'company_types',
            ('add',),
            (('Тип компании', 'line'),)
        )
        self.companytypes_add_window.show()

    def deleteuser(self):
        self.app.pg.drop_user(self.usersTable.item(self.users_table_row, 0).text())
        self.update_users()
    
    def deletesocialstatus(self):
        self.app.pg.delete_by_id(self.socialstatusesTable.item(self.socialstatuses_table_row, 0).text(), 'social_statuses')
        self.update_socialstatuses()

    def deletecity(self):
        self.app.pg.delete_by_id(self.citiesTable.item(self.cities_table_row, 0).text(), 'cities')
        self.update_cities()

    def deleteinsurancetype(self):
        self.app.pg.delete_by_id(self.insurancetypesTable.item(self.insurancetypes_table_row, 0).text(), 'insurance_types')
        self.update_insurancetypes()

    def deletecompanytype(self):
        self.app.pg.delete_by_id(self.companytypesTable.item(self.companytypes_table_row, 0).text(), 'company_types')
        self.update_companytypes()

    def editcity(self):
        if self.citiesTable.rowCount() == 0: return
        self.cities_edit_window = cru_window.CRUWindow(
            self.app,
            self.update_cities,
            'cities',
            ('edit', self.citiesTable.item(self.cities_table_row, 0).text()),
            (('Сумма страхования', 'line', 'city'),)
        )
        self.cities_edit_window.show()

    def editsocialstatus(self):
        if self.socialstatusesTable.rowCount() == 0: return
        self.socialstatuses_edit_window = cru_window.CRUWindow(
            self.app,
            self.update_socialstatuses,
            'social_statuseses',
            ('edit', self.socialstatusesTable.item(self.socialstatuses_table_row, 0).text()),
            (('Социальное положение', 'line', 'status'),)
        )
        self.socialstatuses_edit_window.show()

    def editinsurancetype(self):
        if self.insurancetypesTable.rowCount() == 0: return
        self.insurancetypes_edit_window = cru_window.CRUWindow(
            self.app,
            self.update_insurancetypes,
            'insurance_types',
            ('edit', self.insurancetypesTable.item(self.insurancetypes_table_row, 0).text()),
            (('Вид страхования', 'line', 'type'),)
        )
        self.insurancetypes_edit_window.show()

    def editcompanytype(self):
        if self.companytypesTable.rowCount() == 0: return
        self.companytypes_edit_window = cru_window.CRUWindow(
            self.app,
            self.update_companytypes,
            'company_types',
            ('edit', self.companytypesTable.item(self.companytypes_table_row, 0).text()),
            (('Тип компании', 'line', 'type'),)
        )
        self.companytypes_edit_window.show()

    def usersTable_cellClicked(self, row, column):
            self.users_table_row = row

    def socialstatusesTable_cellClicked(self, row, column):
            self.socialstatuses_table_row = row

    def citiesTable_cellClicked(self, row, column):
            self.cities_table_row = row

    def insurancetypesTable_cellClicked(self, row, column):
            self.insurancetypes_table_row = row

    def companytypesTable_cellClicked(self, row, column):
            self.companytypes_table_row = row
