from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem


def message(title, text, msg_type):
    msg = QMessageBox()

    if msg_type == 'info':
        msg.setIcon(QMessageBox.Information)
    elif msg_type == 'error':
        msg.setIcon(QMessageBox.Critical)
    elif msg_type == 'warn':
        msg.setIcon(QMessageBox.Warning)
    else:
        msg.setIcon(QMessageBox.Information)
    
    msg.setWindowTitle(title)
    msg.setText(text)
    msg.exec_()


def add_table_row(table, row_data):
    row = table.rowCount()
    table.setRowCount(row + 1)
    col = 0
    for item in row_data:
        cell = QTableWidgetItem(str(item))
        table.setItem(row, col, cell)
        col += 1